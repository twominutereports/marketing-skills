#!/usr/bin/env python3
"""
Build the AI Traffic Audit dashboard from a Two Minute Reports run_query result.

Usage:
  python3 build_dashboard.py --input run_query_result.json --out dashboard.html \
      --account "<property label>" --window "YYYY-MM-DD to YYYY-MM-DD" \
      --compare "YYYY-MM-DD to YYYY-MM-DD" [--run-time "YYYY-MM-DD HH:MM"] [--summary summary.json]

The input is the raw JSON returned by run_query (shape: {connectorResults:[{results:[{title,data:{headers,rows}}]}]}).
Query titles must match queries.json. Logos are read from ./logos (next to this script) and embedded as data URIs,
so the output HTML is fully self-contained.
Prints a compact JSON summary to stdout (and to --summary if given) for writing the insights.
"""
import argparse, base64, json, os, sys
from collections import defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(HERE, "logos")
TEMPLATE = os.path.join(HERE, "dashboard_template.html")

# Order matters: first match wins. Keys are matched as case-insensitive substrings of GA4 "Session source".
PLATFORMS = [
    {"id": "chatgpt",    "name": "ChatGPT",    "keys": ["chatgpt", "openai"],          "logo": "chatgpt.png", "color": "#10a37f"},
    {"id": "gemini",     "name": "Gemini",     "keys": ["gemini", "bard"],             "logo": "gemini.png",  "color": "#6f6cf6"},
    {"id": "claude",     "name": "Claude",     "keys": ["claude.ai", "anthropic"],     "logo": "claude.png",  "color": "#d97757"},
    {"id": "perplexity", "name": "Perplexity", "keys": ["perplexity"],                 "logo": "perplexity.png", "color": "#1fb8cd"},
    {"id": "copilot",    "name": "Copilot",    "keys": ["copilot"],                    "logo": "copilot.png", "color": "#0a78d1"},
    {"id": "meta-ai",    "name": "Meta AI",    "keys": ["meta.ai"],                    "logo": "meta-ai.png", "color": "#1877f2"},
    {"id": "grok",       "name": "Grok",       "keys": ["grok", "x.ai"],               "logo": "grok.png",    "color": "#52525b"},
    {"id": "deepseek",   "name": "DeepSeek",   "keys": ["deepseek"],                   "logo": "deepseek.png", "color": "#5786fe"},
    {"id": "mistral",    "name": "Mistral",    "keys": ["mistral"],                    "logo": "mistral.png", "color": "#fa520f"},
    {"id": "poe",        "name": "Poe",        "keys": ["poe.com"],                    "logo": "poe.png", "color": "#5d5cde"},
    {"id": "you",        "name": "You.com",    "keys": ["you.com"],                    "logo": None, "letter": "Y", "color": "#9333ea"},
]

TITLES = {
    "pages": "AI Referral Source x Landing Page",
    "trend": "AI Referral Daily Trend",
    "total": "Site Total",
    "prev":  "AI Referral Sources Previous Period",
}


def classify(source):
    s = (source or "").lower()
    for p in PLATFORMS:
        if any(k in s for k in p["keys"]):
            return p["id"]
    return None


def logo_uri(fname):
    if not fname:
        return None
    path = os.path.join(LOGO_DIR, fname)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def load_results(path):
    with open(path) as f:
        d = json.load(f)
    out = {}
    for c in d.get("connectorResults", []):
        for r in c.get("results", []):
            data = r.get("data") or {}
            out[r.get("title")] = data.get("rows") or []
    return out


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def fmt_date(v):
    s = str(v)
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
    return s[:10]


def build(args):
    R = load_results(args.input)
    missing = [t for t in TITLES.values() if t not in R]
    if missing:
        print(f"WARNING: missing query results: {missing}", file=sys.stderr)

    # --- per platform x page ---
    plat = defaultdict(lambda: {"sessions": 0, "users": 0, "engaged": 0, "key_events": 0, "eng_sec": 0, "sources": set()})
    pages = defaultdict(lambda: {"total": 0, "key_events": 0, "engaged": 0, "by": defaultdict(int)})
    for row in R.get(TITLES["pages"], []):
        src, page = row[0], row[1] or "(not set)"
        pid = classify(src)
        if not pid:
            continue
        s, u, e, k, sec = (num(x) for x in row[2:7])
        P = plat[pid]
        P["sessions"] += s; P["users"] += u; P["engaged"] += e; P["key_events"] += k; P["eng_sec"] += sec
        P["sources"].add(src)
        pg = pages[page]
        pg["total"] += s; pg["key_events"] += k; pg["engaged"] += e; pg["by"][pid] += s

    # --- previous period ---
    prev = defaultdict(float)
    for row in R.get(TITLES["prev"], []):
        pid = classify(row[0])
        if pid:
            prev[pid] += num(row[1])

    # --- trend ---
    trend = defaultdict(lambda: defaultdict(float))
    for row in R.get(TITLES["trend"], []):
        pid = classify(row[1])
        if pid:
            trend[fmt_date(row[0])][pid] += num(row[2])

    total_rows = R.get(TITLES["total"], [])
    site_sessions = num(total_rows[0][0]) if total_rows else 0
    site_users = num(total_rows[0][1]) if total_rows and len(total_rows[0]) > 1 else 0

    ai_sessions = sum(p["sessions"] for p in plat.values())
    ai_prev = sum(prev.values())
    meta = {p["id"]: p for p in PLATFORMS}
    active_ids = sorted(set(plat) | set(prev), key=lambda i: -plat[i]["sessions"] if i in plat else 0)

    platforms_out = []
    for pid in active_ids:
        P = plat.get(pid) or {"sessions": 0, "users": 0, "engaged": 0, "key_events": 0, "eng_sec": 0, "sources": set()}
        m = meta[pid]
        top_pages = sorted(((pg, v["by"][pid]) for pg, v in pages.items() if v["by"].get(pid)), key=lambda x: -x[1])[:5]
        platforms_out.append({
            "id": pid, "name": m["name"], "color": m["color"], "logo": logo_uri(m.get("logo")), "letter": m.get("letter"),
            "sessions": P["sessions"], "users": P["users"], "key_events": P["key_events"],
            "engagement_rate": (P["engaged"] / P["sessions"]) if P["sessions"] else 0,
            "avg_eng_sec": (P["eng_sec"] / P["users"]) if P["users"] else 0,
            "share": (P["sessions"] / ai_sessions) if ai_sessions else 0,
            "prev_sessions": prev.get(pid, 0),
            "sources": sorted(P["sources"]),
            "top_pages": [{"page": a, "sessions": b} for a, b in top_pages],
        })

    pages_out = sorted(
        ({"page": pg, "total": v["total"], "key_events": v["key_events"],
          "engagement_rate": (v["engaged"] / v["total"]) if v["total"] else 0,
          "by": dict(v["by"])} for pg, v in pages.items()),
        key=lambda x: -x["total"])

    dates = sorted(trend)
    trend_out = [{"date": d, "by": dict(trend[d])} for d in dates]

    data = {
        "meta": {
            "title": "AI Traffic Audit",
            "account": args.account,
            "window": args.window,
            "compare": args.compare,
            "demo": bool(args.demo),
            "run_time": args.run_time or datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ga4_logo": logo_uri("ga4.png"),
        },
        "kpis": {
            "ai_sessions": ai_sessions, "ai_prev_sessions": ai_prev,
            "ai_users": sum(p["users"] for p in plat.values()),
            "ai_key_events": sum(p["key_events"] for p in plat.values()),
            "ai_engagement_rate": (sum(p["engaged"] for p in plat.values()) / ai_sessions) if ai_sessions else 0,
            "site_sessions": site_sessions, "site_users": site_users,
            "ai_share": (ai_sessions / site_sessions) if site_sessions else 0,
            "platform_count": len([p for p in platforms_out if p["sessions"] > 0]),
            "page_count": len(pages_out),
        },
        "platforms": platforms_out,
        "pages": pages_out,
        "trend": trend_out,
    }

    with open(TEMPLATE) as f:
        html = f.read()
    blob = json.dumps(data).replace("</", "<\\/")
    html = html.replace("/*__DATA__*/null", blob)
    html = html.replace("{{PAGE_TITLE}}", f"AI Traffic Audit — {data['meta']['run_time']} — {args.account}")
    with open(args.out, "w") as f:
        f.write(html)

    summary = {
        "kpis": data["kpis"],
        "platforms": [{k: p[k] for k in ("name", "sessions", "prev_sessions", "share", "engagement_rate", "key_events", "avg_eng_sec", "sources", "top_pages")} for p in platforms_out],
        "top_pages": [{"page": p["page"], "total": p["total"], "key_events": p["key_events"], "by": {meta[k]["name"]: v for k, v in p["by"].items()}} for p in pages_out[:15]],
    }
    s = json.dumps(summary, indent=1)
    if args.summary:
        with open(args.summary, "w") as f:
            f.write(s)
    print(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--account", required=True)
    ap.add_argument("--window", required=True)
    ap.add_argument("--compare", default="")
    ap.add_argument("--run-time", default="")
    ap.add_argument("--summary", default="")
    ap.add_argument("--demo", action="store_true", help="label the dashboard as demo/mock data")
    build(ap.parse_args())
