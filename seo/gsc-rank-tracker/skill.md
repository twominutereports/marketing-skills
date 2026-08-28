---
name: tmr-gsc-rank-tracker
description: Use this skill when the user wants to track how they rank for their target keywords over time in Google Search Console — e.g. "track my rankings", "rank tracker", "keyword position history", "how am I ranking", "show my ranking trend", "am I climbing or slipping on Google". It ASKS the user which keywords to check, which country, and the lookback period (1, 3, or 6 months); pulls average position from GSC (filtered by exact query + country + date), sampled twice a month (1st & 15th); and produces an inline insights summary plus a large color-coded rank-grid dashboard artifact. No page URL is required.
version: 1.2.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with the Google Search Console (gsc) connector"
---

# GSC Rank Tracker

> **MCP version note.** This skill targets the current TMR MCP. Its data flow is: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`, `generate_query`, and `get_data_insights` no longer exist. Connector ID: **`gsc`** (Search Console). Field IDs are raw. The query template is stored in `queries.json` and mirrored at the bottom of this file. Date ranges and snapshot anchors are computed fresh at runtime — nothing is hardcoded.

## Purpose

A keyword rank tracker built on Google Search Console. The user supplies the exact keywords they want to track — no page URLs required, since each keyword is tracked site-wide. The skill shows how each keyword has ranked over a chosen lookback window (1, 3, or 6 months), sampled twice a month, filtered to a single country. Output is a large color-coded grid (green = winning, yellow = watch, orange/red = slipping, grey = not ranked) plus a short written read of the biggest movers. It replaces a paid rank-tracker subscription with the user's own Search Console data.

Trigger phrases: "track my rankings", "rank tracker", "keyword position history", "how am I ranking", "show me my ranking trend", "am I climbing or slipping on Google".

## Connectors required

This skill uses the following TMR connector(s):
- Google Search Console (`gsc`)

The runtime procedure verifies this is available before doing any analytical work. Do not proceed with partial connector availability.

---

## Runtime procedure

Follow these steps in order. Do not skip steps. Do not rearrange. **This skill collects its inputs by ASKING the user — never assume the keywords, country, or period.**

### 1. Check that TMR's tools are available

Inspect your available tools. The current Two Minute Reports MCP exposes: `verify_team_details`, `list_connectors`, `get_connector_accounts`, `get_connector_query_schema`, `validate_query`, `run_query`. The prefix may vary (e.g. "Two Minute Reports", "TMR"); match by tool function and the TMR MCP server (`https://mcp.twominutereports.com/mcp`), not by exact prefix.

**If none of these tools are present**, tell the user:

> *"This skill needs Two Minute Reports connected to your Claude account, but I don't see it in your tools. TMR lets you query your marketing data (including Search Console) from inside Claude. Connect it once here — https://twominutereports.com/help/mcp/claude — then run this skill again."*

If a `suggest_connectors` capability exists, surface a one-tap connect option. Then stop.

If the tools ARE present, hold the resolved prefix and continue.

### 2. Verify team and plan status

Call `verify_team_details`.

- **Multiple teams** → present them and ask which to use; note any `cancelled` team. Store the chosen `teamId` for every later call.
- **One team** → use its `teamId` and say which is active.
- **Plan status:** `active`, `in_trial`, `non_renewing` are fine. If `cancelled`, stop: *"Your Two Minute Reports plan is cancelled, so I can't pull data. Reactivate at hub.twominutereports.com/billing, then run this skill again."*
- **Auth/session error, or no teams** → *"Two Minute Reports is connected, but I couldn't verify your team — your session may have expired. Reconnect TMR with the account that holds your team, then run this skill again. Reference: https://twominutereports.com/help/mcp/claude"* (trigger `suggest_connectors` if available), then stop.
- **Other failure** → *"Couldn't reach Two Minute Reports right now — please try again in a moment."* and stop.

### 3. Verify the GSC connector is provisioned

Call `get_connector_accounts(teamId, connectorId:"gsc", status:"enabled")`.

- **At least one enabled property** → continue. If only one property, use it automatically. If several, present them and ask which property to track.
- **No accounts** → *"This skill needs Google Search Console set up inside Two Minute Reports with an enabled property, but I don't see one. Open TMR, add Search Console (and enable a property), then run this skill again."* Stop.
- **Call fails entirely** → treat as a step-2 session failure and use the reconnect message.

### 4. Locate skill folder, load config, and COLLECT INPUTS (ask, don't assume)

Locate this skill's install folder to read/write `config.json` and read `queries.json`:
1. `/mnt/skills/user/tmr-gsc-rank-tracker/`
2. else `find /mnt/skills -name "tmr-gsc-rank-tracker" -type d 2>/dev/null` → first result
3. else "no install folder": use the query template at the bottom of this file, skip config read/write, skip the save prompt in step 7.

Hold the path as `<install-path>`. Read `<install-path>/config.json`.

**If `saved: true`:** tell the user *"Using your saved setup: `<N>` keywords, country `<code>`, last `<months>` month(s). Say 'change config' to update."* Use stored values. If they say "change config", treat as `saved:false` and run the collection flow, then re-ask in step 7.

**If `saved:false`, missing, or unreadable — ASK these three things, in this order.** Ask them clearly (a short numbered prompt or one question at a time is fine), and wait for answers before proceeding:

1. **Which keywords to check rank?** Ask the user to paste their keywords, **one per line — just the keywords, no URLs needed.** Example:
   ```
   facebook ads reporting tool
   google ads reporting tool
   marketing reporting software
   ```
   Each keyword is tracked **site-wide** — GSC returns the property's average position for that exact query, so a page URL is not required and should NOT be asked for. Parse each line into `{ keyword }`.

   **Optional page pinning (only if the user volunteers it):** if a line contains a pipe (`keyword | https://full/url`), treat the URL as a page to pin for that keyword only, and store it as `{ keyword, page }`. Never ask for or require this — it is a power-user extra. If a pinned URL is malformed, show it back and ask them to fix just that line (or drop the pin).

2. **Which country?** Ask which country's rankings to show. Convert the answer to an **ISO-3166 alpha-3** code for `reportParams.countries` (India → `ind`, United States → `usa`, United Kingdom → `gbr`, Canada → `can`, Australia → `aus`, etc.). If unsure, confirm the code with the user.

3. **How far back?** Ask the user to choose the lookback period: **last 1 month, last 3 months, or last 6 months.** (These are the only allowed values.) The sampling cadence is fixed regardless of choice: **twice a month** (a snapshot on the 1st and the 15th of each month). So 1 month ≈ 2 snapshots, 3 months ≈ 6, 6 months ≈ 12.

If config read failed unexpectedly, don't crash — run the collection flow and say *"Couldn't read your saved settings — let's set them again."*

### 5. Build, validate, and run one query per target

Load the query template from `<install-path>/queries.json` (fallback: the template at the bottom of this file): `connectorId:"gsc"`, `metrics:["position","clicks","impressions"]`, `dimensions:["date"]`, `date_spec` = last N months (N from the user), `snapshot_spec` = twice a month. **Dates are not stored — compute them now.**

a. **Resolve the window.** `endDate` = today − 3 days (GSC lag). `startDate` = endDate − N calendar months, where N ∈ {1, 3, 6} from step 4. Format `YYYY-MM-DD`.

b. **Build snapshot anchors (twice a month).** Collect every **1st and 15th** of each calendar month that falls within `[startDate, endDate]`, ascending. Each anchor defines a snapshot window running from that anchor up to the day before the next anchor (the final anchor's window ends at `endDate`). Label each column by its anchor date (e.g. `1 Jul`, `15 Jun`). This yields ~2 columns per month.

c. **Assemble one query per keyword.** For each keyword:
   - `metrics`: `["position","clicks","impressions"]`
   - `dimensions`: `["date"]`
   - `filters`: **always** `[{filterField:"query", operator:"equals", expression:<keyword>}]`. **Only if the user pinned a page** for this keyword, add `{filterField:"page", operator:"equals", expression:<page>}`. Do not add a page filter otherwise.
   - `reportParams`: `{ gscReportType:"analytics", searchTypes:["web"], countries:[<country code>] }`
   - `sort`: `[{sortField:"date", direction:"asc"}]`
   - `dateRange`: resolved `startDate`/`endDate`
   Put all keyword queries into one connectors entry: `{ connectorId:"gsc", accountIds:[<property>], queries:[…] }`, each with a distinct `title` like `Rank – <keyword>`.

d. **Validate.** Call `validate_query(teamId, userQuery, connectors:[…])`. If any query errors, don't run — explain briefly and stop (usually a bad alpha-3 country code or a malformed page URL).

e. **Confirm.** If `auto_confirm_query` is `true`, skip. Otherwise summarize in plain English (property, country, N keywords, period, twice-monthly snapshots) and ask for a yes. Wait.

f. **Run.** Call `run_query(teamId, connectors:[…], limit:1000)`. Each query returns rows of `[date, position, clicks, impressions]` for days with impressions in the country (empty days are absent).
   - **Large results:** if a result is a stored file path, read/parse it with code execution — pull `connectorResults[].results[].data.headers`/`.rows`.

g. **Bucket into snapshots.** For each target and each snapshot window, compute the **impression-weighted average position** (`Σ(position×impressions)/Σ(impressions)`), rounded to 1 decimal. Empty window → **N/R**. Build a matrix: rows = targets, columns = anchor dates (newest → oldest), values = position or N/R.

h. **Summary column.** For each target: `latest` = most recent non-N/R value; `previous` = the non-N/R value immediately before it; `change = previous − latest` (positive = improved, since lower position is better), rounded to 1 decimal.

### 6. Produce the dual output

#### Insights (inline chat)

Write 150–300 words. Match the tone/structure of this sanitized template — fill `[brackets]` with real data:

> **Rank movement, last [period] ([country]), [N] tracked pages.**
> [X pages] rank on page one, [Y pages] sit in positions [range], and [Z pages] aren't ranking in [country] right now.
> Strongest: **[keyword]** has held position [value] — your anchor page. Biggest gainer: **[keyword]** improved [delta] spots to [new].
> Watch list: **[keyword]** slipped from [old] to [new]; **[keyword]** is volatile — [describe]; **[keyword]** shows almost no impressions.
> One move: [the single highest-leverage recommendation grounded in the data.]

Lead with how many pages win vs. slip, name the biggest gainer and biggest concern, end with one concrete recommendation. Never invent movement the data doesn't show; if a page has too few points to judge, say so.

#### Dashboard (artifact)

Produce a NEW artifact each run — never overwrite a prior one. Save as an HTML file to the outputs location and present it. Title:

`GSC Rank Tracker — <YYYY-MM-DD HH:MM> — <property label>`

Build a full standalone HTML document using the design below. Keep the structure, CSS, and sizing; only fill data. It must be **large and screenshot-ready** (max-width ~1600px), with:
- A header row: title with a status dot, a subtitle line (`Property · Country · Period · Sampled twice a month` + a note that values are impression-weighted average position, lower is better, plus generated timestamp), and a row of **KPI tiles**: Keywords tracked, Ranking on page one (pos ≤ 10), Improving vs. last snapshot (change > 0), Not ranking now (most-recent window is N/R).
- A card containing a horizontally scrollable table. **Sticky** first two columns: "Keyword" (keyword bold; beneath it in monospace grey show the pinned page path if one was pinned, otherwise the muted label `site-wide`) and "Rank" (latest value as a large pill + a ▲/▼ change indicator beneath). Then one column per snapshot anchor, newest → oldest.
- Each position renders as a rounded **pill**. Color by band: `pos ≤ 10` green (`#c9f7d5`/text `#12683a`), `11–20` yellow (`#fdf0be`/`#7a5610`), `21–50` orange (`#ffdcb8`/`#9a3412`), `>50` red (`#ffd1d1`/`#a01919`), N/R grey (`#f4f7fb`/`#c3ccd8`).
- Change indicator: `change>0` → `▲ {change}` green (`#16a34a`); `change<0` → `▼ {|change|}` red (`#dc2626`); else `—` grey.
- A legend of the four bands + N/R, and a footnote explaining columns run newest→oldest on the 1st & 15th and that N/R means zero impressions for that exact keyword in that country/window.
- Styling notes: Inter/system font, soft radial page background, cards with `border-radius:22px` and a soft shadow, generous padding, `font-variant-numeric:tabular-nums` on pills, subtle row hover. Base pill font ~15px, rank pill ~18px, H1 ~30px.

Reference scaffold (fill `{{...}}`, generate one `<th>` per anchor and one row per target; each data cell is `<td><span class="pill p-<band>">{{VALUE}}</span></td>`):

```html
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GSC Rank Tracker</title>
<style>
 *{box-sizing:border-box;margin:0;padding:0}
 body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:radial-gradient(1200px 600px at 20% -10%,#eef4ff 0%,#f1f5f9 55%);color:#0f172a;padding:40px 32px;-webkit-font-smoothing:antialiased}
 .wrap{max-width:1600px;margin:0 auto}
 .head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;flex-wrap:wrap;margin-bottom:22px}
 h1{font-size:30px;font-weight:800;letter-spacing:-.02em;display:flex;align-items:center;gap:12px}
 h1 .dot{width:12px;height:12px;border-radius:50%;background:#16a34a;box-shadow:0 0 0 5px rgba(22,163,74,.15)}
 .sub{font-size:15px;color:#64748b;margin-top:8px;line-height:1.5}.sub b{color:#334155}
 .kpis{display:flex;gap:14px;flex-wrap:wrap}
 .kpi{background:#fff;border:1px solid #e6ebf2;border-radius:16px;padding:16px 22px;min-width:150px;box-shadow:0 2px 8px rgba(15,23,42,.04)}
 .kpi-n{font-size:32px;font-weight:800;letter-spacing:-.02em;line-height:1}.kpi-l{font-size:12.5px;color:#64748b;margin-top:8px;font-weight:500}
 .card{background:#fff;border:1px solid #e6ebf2;border-radius:22px;box-shadow:0 12px 40px rgba(15,23,42,.08);overflow:hidden}
 .scroll{overflow-x:auto}
 table{border-collapse:separate;border-spacing:0;width:100%;font-size:15px;white-space:nowrap}
 thead th{background:#fbfcfe;color:#64748b;font-weight:600;font-size:13px;letter-spacing:.02em;text-transform:uppercase;padding:18px 16px;text-align:center;border-bottom:1px solid #eef2f7}
 thead th:first-child{text-align:left;position:sticky;left:0;background:#fbfcfe;z-index:3;min-width:300px}
 thead th:nth-child(2){position:sticky;left:300px;background:#fbfcfe;z-index:3}
 tbody td{padding:14px 16px;text-align:center;border-bottom:1px solid #f1f5f9}
 tbody tr:last-child td{border-bottom:none}tbody tr:hover td{background:#fafcff}
 td.kw{text-align:left;position:sticky;left:0;background:#fff;z-index:2}tbody tr:hover td.kw{background:#fafcff}
 .kw-t{font-weight:700;font-size:16px}.kw-p{font-size:12.5px;color:#94a3b8;margin-top:3px;font-family:ui-monospace,Menlo,monospace}
 td.rank{position:sticky;left:300px;background:#fff;z-index:2;border-right:2px solid #eef2f7}tbody tr:hover td.rank{background:#fafcff}
 .rank-c{font-size:13px;font-weight:700;margin-top:6px}.c-up{color:#16a34a}.c-down{color:#dc2626}.c-flat{color:#cbd5e1}
 .pill{display:inline-block;min-width:44px;padding:9px 12px;border-radius:11px;font-weight:700;font-size:15px;font-variant-numeric:tabular-nums}
 .rankpill{font-size:18px;min-width:50px}
 .p-green{background:#c9f7d5;color:#12683a}.p-yellow{background:#fdf0be;color:#7a5610}.p-orange{background:#ffdcb8;color:#9a3412}.p-red{background:#ffd1d1;color:#a01919}.p-na{background:#f4f7fb;color:#c3ccd8;font-weight:600}
 .legend{display:flex;gap:22px;flex-wrap:wrap;margin-top:20px;font-size:13.5px;color:#475569;align-items:center}
 .legend .sw{display:inline-block;width:16px;height:16px;border-radius:5px;vertical-align:middle;margin-right:7px}
 .foot{margin-top:16px;font-size:12.5px;color:#94a3b8}
</style></head><body><div class="wrap">
  <div class="head">
    <div><h1><span class="dot"></span>GSC Rank Tracker</h1>
      <div class="sub">Property <b>{{PROPERTY}}</b> · Country <b>{{COUNTRY}}</b> · Period <b>Last {{MONTHS}} month(s)</b> · Sampled <b>twice a month</b><br>Impression-weighted average position from Google Search Console · lower is better · generated {{RUN_TIME}}</div>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="kpi-n">{{KPI_TRACKED}}</div><div class="kpi-l">Keywords tracked</div></div>
      <div class="kpi"><div class="kpi-n" style="color:#16a34a">{{KPI_PAGE1}}</div><div class="kpi-l">Ranking on page one</div></div>
      <div class="kpi"><div class="kpi-n" style="color:#0284c7">{{KPI_IMPROVING}}</div><div class="kpi-l">Improving vs. last snapshot</div></div>
      <div class="kpi"><div class="kpi-n" style="color:#dc2626">{{KPI_NOTRANK}}</div><div class="kpi-l">Not ranking now</div></div>
    </div>
  </div>
  <div class="card"><div class="scroll"><table>
    <thead><tr><th>Keyword &amp; Landing Page</th><th>Rank</th>{{DATE_HEADERS}}</tr></thead>
    <tbody>{{ROWS}}</tbody>
  </table></div></div>
  <div class="legend"><b>Position band:</b>
    <span><span class="sw" style="background:#c9f7d5"></span>Top 10</span>
    <span><span class="sw" style="background:#fdf0be"></span>11–20</span>
    <span><span class="sw" style="background:#ffdcb8"></span>21–50</span>
    <span><span class="sw" style="background:#ffd1d1"></span>50+</span>
    <span><span class="sw" style="background:#f4f7fb;border:1px solid #e6ebf2"></span>N/R</span>
  </div>
  <div class="foot">Columns run newest → oldest, on the 1st &amp; 15th of each month. N/R = a snapshot window with zero impressions for that exact keyword in {{COUNTRY}}.</div>
</div></body></html>
```

Row template:
```html
<tr>
  <td class="kw"><div class="kw-t">{{KEYWORD}}</div><div class="kw-p">{{PAGE_PATH}}</div></td>
  <td class="rank"><span class="pill p-{{LATEST_BAND}} rankpill">{{LATEST}}</span><div class="rank-c">{{CHANGE_INDICATOR}}</div></td>
  {{CELLS}}
</tr>
```

### 7. Save configuration (first run only, if none existed)

After producing both outputs, ask:

> "Want me to remember this setup — your keywords, country, and lookback period — for next time? (yes / no) And auto-confirm the query on future runs? (yes / no)"

If yes to either, write `<install-path>/config.json`:

```json
{
  "version": "1.2.0",
  "saved": true,
  "accounts": { "gsc": [{ "label": "<property>", "value": "<property>" }] },
  "country": "<alpha-3 code>",
  "months": 6,
  "keywords": [{ "keyword": "<kw>" }, { "keyword": "<kw>", "page": "<optional pinned url>" }],
  "auto_confirm_query": false,
  "saved_at": "<ISO 8601 timestamp>"
}
```

Wrap the write in error handling. On failure: *"Couldn't save your settings to disk — they'll be remembered for this conversation only."* and continue. If they say no, leave the default `saved:false`.

## Notes for end users

- The skill asks three things first: **which keywords** (just keywords, no URLs), **which country**, and **how far back (1 / 3 / 6 months)**. Sampling is fixed at twice a month (1st & 15th).
- Rankings come from **Google Search Console's average position** — Google's own logged data, filtered to your **exact keyword + chosen country + date**. This is the average across all impressions in the window, not a fixed-location live SERP check. GSC data lags 2–3 days, so the newest snapshot ends a few days before today.
- A cell is **N/R** when there were no impressions for that exact keyword in that country during that window.
- Match the **exact keyword** as it appears in Search Console (casing aside). Each keyword is tracked **site-wide** by default. If you want to lock a keyword to one specific page, add ` | https://full/url` after it — optional, never required.
- Say "change config" mid-run to change keywords, country, or period. Every run makes a fresh dashboard artifact.
- Requires the Two Minute Reports MCP connected. If it isn't, the skill points you to https://twominutereports.com/help/mcp/claude.

## Query templates

(Fallback copy of `queries.json` in case the install folder can't be located at runtime.)

```json
{
  "queries": [
    {
      "title": "Rank history (per target)",
      "connectorId": "gsc",
      "metrics": ["position", "clicks", "impressions"],
      "dimensions": ["date"],
      "filters": [
        { "filterField": "query", "operator": "equals", "expression": "{{TARGET_KEYWORD}}" }
      ],
      "optional_filters": [
        { "when": "user pinned a page", "filterField": "page", "operator": "equals", "expression": "{{OPTIONAL_TARGET_PAGE_URL}}" }
      ],
      "reportParams": { "gscReportType": "analytics", "searchTypes": ["web"], "countries": ["{{COUNTRY_CODE}}"] },
      "sort": [{ "sortField": "date", "direction": "asc" }],
      "date_spec": { "type": "last_n_months", "n": "{{MONTHS}}", "allowed_n": [1, 3, 6], "lag_days": 3 },
      "snapshot_spec": { "per_month": 2, "anchors": ["1st", "15th"], "aggregation": "impression_weighted_avg_position" }
    }
  ]
}
```
