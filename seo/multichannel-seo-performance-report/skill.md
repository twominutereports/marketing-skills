---
name: tmr-multichannel-seo-performance-report
description: Use this skill when the user asks for an SEO performance report, a monthly/28-day SEO report, or Google Search Console + GA4 + AI traffic (ChatGPT, Gemini, Perplexity, Claude, Copilot) + PageSpeed Insights / Core Web Vitals + Google Business Profile (GMB) performance together. Covers clicks, impressions, CTR, position, top queries, striking-distance keywords, sessions, engagement, key events, organic landing pages, AI referrals, LCP/INP/CLS, Lighthouse scores, profile views, calls, directions and reviews, last 28 days vs prior 28. Produces an inline insights summary plus a 5-tab HTML dashboard.
version: 1.0.0
---

# SEO Performance Report

## Purpose

One SEO performance report that covers search visibility, site traffic, AI assistant traffic, page speed and local presence, built from four Two Minute Reports connectors: Google Search Console, Google Analytics 4, PageSpeed Insights and Google Business Profile (GMB). It compares the last 28 days with the 28 days before that. The output is a short insights summary in chat plus a 5-tab dashboard with each platform's logo:

1. **Overview**: key takeaways, a summary card per platform, the AI-assistant strip and daily trends
2. **Search Console**: clicks, impressions, CTR, position · daily trends · top queries · striking-distance keywords (position 4–20) · CTR opportunities · top pages · device split
3. **Analytics & AI Traffic**: sessions, users, new users, engagement rate, session duration, key events · channel mix · organic landing pages · **AI Traffic** section with AI platform logos (ChatGPT, Gemini, Perplexity, Claude, Copilot, Meta AI, Grok, DeepSeek, Mistral, Poe, You.com): AI sessions, share of traffic, platform cards, stacked daily trend and the landing pages AI assistants send visitors to
4. **Page Speed**: real-user Core Web Vitals from CrUX (LCP, INP, CLS, FCP, TTFB) with pass/fail, for mobile and desktop · Lighthouse scores (Performance, SEO, Accessibility, Best Practices) · lab timings
5. **Business Profile**: views on Search and Maps, website clicks, calls, directions · daily trend · search terms · rating, review count, star distribution and recent reviews (reply status)

Typical requests: "SEO performance report", "monthly SEO report for my site", "how is our organic search doing", "SEO + GA4 + page speed report", "report on Search Console, Analytics and Business Profile", "how much traffic do we get from ChatGPT and other AI tools, plus our SEO numbers".

## Connectors required

This skill uses these TMR connectors:
- Google Search Console (`gsc`): required
- Google Analytics 4 (`ga4`): required
- Page Speed Insights (`psi`): required. **The URL to test must come from the user on every run (or from their saved config). Never guess, infer or derive it from another connector.**
- Google My Business / Business Profile (`gmb`): **optional**. If the user has no enabled GMB account, run the other four tabs; the Business Profile tab then shows a "connect Google Business Profile" note.

Pass `skillId: "tmr-multichannel-seo-performance-report"` on every `validate_query` and `run_query` call.

## How this skill is packaged

Everything lives in this one file, which ships alongside `queries.json` and `readme.md`.

- **Query templates** (near the end): the 25 locked queries, holding field IDs and relative date specs but no dates or accounts. `queries.json` holds the same templates.
- **Dashboard renderer** (at the end): `seo_report.py`, one self-contained Python script with the dashboard HTML template, the GSC/GA4/PSI/GBP logos and the AI platform logos embedded.
  - `plan` resolves the dates and writes the ready-to-send `connectors` arrays.
  - `build` turns the `run_query` results into the dashboard and prints a JSON summary for the insights.

Settings are saved to `~/.tmr-skills/tmr-multichannel-seo-performance-report/config.json`. The renderer is written to `~/.tmr-skills/tmr-multichannel-seo-performance-report/seo_report.py`. Call that folder `<work>`.

## Runtime procedure

Follow these steps in order. Do not skip or rearrange them.

### 1. Check that TMR's tools are available

Look at your available tools. The Two Minute Reports MCP (server URL `https://mcp.twominutereports.com/mcp`) exposes `verify_team_details`, `list_connectors`, `get_connector_accounts`, `get_connector_query_schema`, `validate_query` and `run_query`. The prefix varies because users name the connection differently ("Two Minute Reports", "TMR", a custom name). Match on tool function, not prefix.

**If none of these tools are present**, tell the user:

> *"This skill needs Two Minute Reports to be connected to your Claude account, but I don't see it in your available tools.*
>
> *Two Minute Reports is an analytics platform that lets you query your marketing data (ads, analytics, SEO, e-commerce and more) from inside Claude. You connect it once, and then this skill and any other TMR skill will work.*
>
> *Here's the setup guide: https://twominutereports.com/help/mcp/claude*
>
> *Once it's connected, run this skill again."*

If a `suggest_connectors` capability exists, use it to offer a one-tap connect. Then stop.

### 2. Verify team and plan status

Call `verify_team_details`.

- **Multiple teams:** list them and ask which to use. Mark any team whose `planStatus` is `cancelled`. Store the chosen `teamId`.
- **One team:** use it and tell the user which team is active.
- **Plan status:** `active`, `in_trial` and `non_renewing` are fine. If it is `cancelled`, stop and tell the user: *"Your Two Minute Reports plan is cancelled, so I can't pull data. Reactivate it at hub.twominutereports.com/billing, then run this skill again."* Never call `validate_query` or `run_query` for a cancelled team.
- **Auth, permission or session error, or no teams returned:** tell the user: *"Two Minute Reports is connected, but I couldn't verify your team details. Your session may have expired, or the connection may need re-authenticating. Please reconnect Two Minute Reports with the account that holds your TMR team, then run this skill again. Setup reference: https://twominutereports.com/help/mcp/claude"* Offer `suggest_connectors` if available. Then stop.
- **Any other failure:** tell the user *"Couldn't reach Two Minute Reports right now. Please try again in a moment."* and stop.

### 3. Verify required connectors in TMR

Call `get_connector_accounts(teamId, connectorId, status:"enabled")` for `gsc`, `ga4`, `psi` and `gmb`. These calls are independent, so run them in parallel.

- If `gsc`, `ga4` or `psi` returns no accounts, tell the user: *"This skill needs <missing connectors> set up inside Two Minute Reports, but <it isn't / they aren't> connected with an enabled account yet. Please open Two Minute Reports, add <missing connectors> and enable an account, then run this skill again."* Stop. Do not run a partial report.
- If only `gmb` returns no accounts, continue without it and say once: *"No Google Business Profile is connected, so the Business Profile tab will show a setup note. Everything else runs as normal."*
- If a call fails outright rather than returning empty, treat it as the step 2 session failure.

### 4. Prepare the renderer and load configuration

**Write the renderer.** Create `<work>` if needed, then write the code block from the **Dashboard renderer** section to `<work>/seo_report.py`, byte for byte. Extract it from this file rather than retyping it. It is long and embeds base64 logos:

```bash
W=~/.tmr-skills/tmr-multichannel-seo-performance-report; mkdir -p "$W"
F=$(find / -type f \( -iname "skill.md" \) -path "*tmr-multichannel-seo-performance-report*" -not -path "/proc/*" 2>/dev/null | head -1)
python3 - "$F" "$W/seo_report.py" <<'PY'
import sys,re
src=open(sys.argv[1],encoding="utf-8").read()
m=re.search(r"<!-- seo_report\.py:start -->\s*```python\n(.*?)\n```\s*<!-- seo_report\.py:end -->",src,re.S)
open(sys.argv[2],"w",encoding="utf-8").write(m.group(1)+"\n"); print("renderer ready")
PY
python3 "$W/seo_report.py" -h >/dev/null && echo ok
```

If the file can't be found (empty `$F`), write the code block to `<work>/seo_report.py` exactly as shown. Then check it with `python3 <work>/seo_report.py -h`.

**Load the configuration.** Read `<work>/config.json` if it exists.

**If `config.json` has `saved: true`:** tell the user *"Using your saved configuration: Search Console <label>, GA4 <label>, PageSpeed URL <url>, Business Profile <label or 'not connected'>. Say 'change config' to update these."* Use the stored accounts, `psi_urls` and `auto_confirm_query`. If the user says "change config" at any point, run the collection flow below and ask the save question again in step 7.

**Otherwise (no file, `saved: false`, or unreadable JSON):** if the read failed, say *"Couldn't read your saved settings, so let's set them again."* Then collect the inputs, reusing the step 3 responses:

- **Search Console:** one site property, the site being reported on. If there are several, list them and ask.
- **GA4:** the property for the same site. If there are several, list them and ask.
- **PageSpeed Insights account:** any one enabled `psi` account works. If there are several, pick the first and say so; it only provides API access.
- **PageSpeed URL:** ask *"Which page should PageSpeed test? Paste the full URL (usually your homepage, e.g. https://www.example.com/)."* Use exactly what the user gives. Never take it from the GSC property or the GA4 property name.
- **Business Profile:** if GMB accounts exist, list the locations and let the user pick one or more (or "none").

This report has no monetary metrics, so don't ask for a currency.

### 5. Build, validate and run the queries

a. **Plan.** Resolve every template's date spec against today's real date and write the connector arrays. Pass the user's account IDs exactly as `get_connector_accounts` returned them:

```bash
python3 <work>/seo_report.py plan --today <YYYY-MM-DD> \
  --gsc "<gsc account id>" --ga4 "<ga4 property id>" \
  --psi-account "<psi account id>" --psi-url "<url from the user>" \
  [--gbp "<gmb account id>" ...] --out-dir ./seo_run
```

This writes `./seo_run/core_connectors.json` (GSC, GA4 core, PSI, GBP), `./seo_run/ai_connectors.json` (the four GA4 AI-traffic queries) and `./seo_run/windows.json`. Windows: GA4, GBP and CrUX cover the last 28 days ending yesterday, compared with the 28 days before. GSC covers 28 days ending 3 days ago, because Search Console data lags. Lighthouse runs a fresh audit today. Omit `--gbp` when no GBP location was chosen.

b. **Validate.** Call `validate_query(teamId, userQuery:<the user's request>, skillId, connectors: <contents of core_connectors.json>)`, then the same with `ai_connectors.json`. If anything fails, do not run. Give a short, friendly explanation (it usually means a connector's schema changed) and suggest re-running later or contacting the skill author. Then stop.

c. **Confirm.** Skip this if `auto_confirm_query` is `true`. Otherwise show a plain-English summary: site and accounts, the PageSpeed URL, the date windows from `windows.json`, and what each tab pulls. Ask for a yes.

d. **Run.** `run_query(teamId, skillId, connectors: <core_connectors.json>, limit: 250)` and `run_query(teamId, skillId, connectors: <ai_connectors.json>, limit: 5000)`. These are independent, so run them in parallel.

e. **Save the results to disk unchanged.** If a result comes back as a stored file path (large results do), copy that file to `./seo_run/core.json` or `./seo_run/ai.json`. If it comes back inline, write the exact JSON object (the one containing `connectorResults`) to those files. Do not hand-edit or summarise rows.

f. **Write meta.** Create `./seo_run/meta.json` with labels only, no IDs:

```json
{"site": "<GSC property label>", "run_at": "<YYYY-MM-DD HH:MM> <tz>", "gsc_label": "<GSC property label>",
 "ga4_label": "<GA4 property name>", "gbp_label": "<location name(s) or empty>", "psi_url": "<url tested>"}
```

### 6. Produce the dual output

a. **Build the data and read the summary:**

```bash
python3 <work>/seo_report.py build --results ./seo_run/core.json ./seo_run/ai.json \
  --windows ./seo_run/windows.json --meta ./seo_run/meta.json --out ./seo_run/report.html
```

It prints a JSON summary: KPIs with current, previous and delta per platform, top queries, striking-distance and low-CTR queries, channels, AI platforms, Core Web Vitals, Lighthouse scores, GBP actions and reviews, plus `missing_queries`. Use only these numbers. Never invent values for an empty section; call it "no data this period".

b. **Write the takeaways.** Write 4–6 key takeaways to `./seo_run/highlights.json` as `[{"tone":"good|bad|warn|info","src":"gsc|ga4|ai|psi|gbp","text":"…"}]`, one short sentence each, at least one an action. Then rebuild with `--highlights ./seo_run/highlights.json` so the Overview tab shows them.

c. **Insights (inline chat, 150–300 words).** Structure: headline finding → 2–3 supporting numbers → biggest period-over-period changes (search, traffic, AI, local) → page-speed status → one or two concrete actions. Match the tone and rhythm of this template and fill the brackets with the user's real numbers. Drop a paragraph whose connector isn't connected.

> Organic search is [growing/slipping]. **Clicks [rose/fell] [X%] to [N]** and impressions [rose/fell] [Y%] to [N], while average position moved from [P1] to **[P2]**. GA4 [agrees/differs]: organic search drove **[N sessions] ([X%] of all traffic)** and key events [rose/fell] [Y%] to [N].
>
> **AI assistants [are the fastest-growing source / remain small].** They sent **[N sessions] ([X%] of traffic, [up/down] [Y%])**. [Top platform] accounts for [Z%] of that, followed by [platform 2] and [platform 3]. AI visitors engage at [X%], against a site average of [Y%], and land mostly on [top AI landing pages].
>
> **Page speed [passes/fails].** Mobile Core Web Vitals [pass/fail] for real users (LCP [X s], INP [Y ms], CLS [Z]). The mobile Lighthouse Performance score is [N]; [weakest lab metric] is the main thing holding it back.
>
> **Local is [up/down].** Business Profile actions [rose/fell] [X%], driven by [action type] ([±Y%]). The rating is [R]★ from [N] reviews[, but [N] new reviews have no reply].
>
> **Do this first:** "[striking-distance query]" ranks [P] with [N] impressions. Strengthening [page] for that term is the biggest quick win. Also rewrite the title and meta for "[low-CTR query]": it ranks [P] but only [X%] of searchers click.

d. **Dashboard (artifact).** Publish `./seo_run/report.html` as a **new** artifact for this run. Never update or replace an earlier one. If you can publish artifacts (e.g. an Artifact tool), publish the file; otherwise present or attach the HTML file. Title: `SEO Performance Report — <YYYY-MM-DD HH:MM> — <site>`. The file is self-contained, with logos embedded and no external requests. Its header shows the site, both periods, the GSC window and the run time; the footer lists the accounts and data notes. Do not modify the template, CSS or logos; only the script fills in data.

### 7. Save configuration (first run only, and only if no saved config existed)

After both outputs, ask:

> "Want to save your settings for future runs? This skill can remember your sites, accounts and PageSpeed URL, so you don't have to pick them every time. That helps if you re-run this report regularly or use it in a workflow.
>
> - Save sites, accounts and PageSpeed URL? (yes / no)
> - Auto-confirm the query on future runs? (yes / no; saves a step, but you won't see the query before it runs)"

On yes, write `<work>/config.json` (create the folder if needed):

```json
{
  "version": "1.0.0",
  "saved": true,
  "accounts": {
    "gsc": [{"label": "...", "value": "..."}],
    "ga4": [{"label": "...", "value": "..."}],
    "psi": [{"label": "...", "value": "..."}],
    "gmb": [{"label": "...", "value": "..."}]
  },
  "psi_urls": ["<url the user gave>"],
  "currency": null,
  "auto_confirm_query": false,
  "saved_at": "<ISO 8601 timestamp>"
}
```

Use `"gmb": []` when no Business Profile is used. Wrap the write in error handling. If it fails, don't crash or show a stack trace; say *"Couldn't save your settings to disk, so they'll be remembered for this conversation only. You'll be asked again next time you run this skill."* On success, confirm: *"Saved. Future runs of this skill will use these settings automatically. Say 'change config' inside the skill to update them."* If no answer is yes, leave `config.json` untouched.

## How the numbers are defined

- **Deltas** compare the current window with the previous window of equal length. Percentages show relative change; rates (CTR, engagement, AI share) show change in percentage points (pp). Average position is "lower is better", so a drop shows green.
- **Striking distance**: queries ranking 4–20, sorted by impressions. **CTR opportunities**: positions ≤ 5 with ≥ 100 impressions and CTR under 2%.
- **AI traffic**: GA4 session source matched to known AI assistants (chatgpt/openai, gemini, perplexity, claude.ai/anthropic, copilot, meta.ai, grok/x.ai, deepseek, mistral, poe.com, you.com), any non-paid medium (`ai-assistant`, `referral`, `(not set)`…). Paid mediums (cpc/ppc/paid/display) are excluded. AI share = AI sessions ÷ all GA4 sessions. Assistants that strip the referrer arrive as Direct and can't be counted.
- **Core Web Vitals** (CrUX, 75th percentile, rolling 28 days): LCP ≤ 2.5 s good / > 4 s poor · INP ≤ 200 ms / > 500 ms · CLS ≤ 0.1 / > 0.25 · FCP ≤ 1.8 s / > 3 s · TTFB ≤ 0.8 s / > 1.8 s. "Passed" requires LCP, INP and CLS all good. Sites with too little Chrome traffic have no CrUX data; the tab says so.
- **Lighthouse** scores: 90–100 good, 50–89 needs improvement, 0–49 poor.

## Notes for end users

- The skill shows you the query before it runs, unless you turn on auto-confirm. That lets you catch a wrong site or URL before data is pulled.
- Want a different time range, other metrics or other accounts long-term? Say "change config", or ask for a different skill (skills are kept specific so they're predictable).
- Every run produces an inline insights summary and a new dashboard artifact from the same data.
- PageSpeed always tests the URL you give it; it never guesses.
- This skill needs the Two Minute Reports MCP connected to your Claude account. If it isn't, the skill points you to https://twominutereports.com/help/mcp/claude.

## Query templates

The locked templates, one per line, identical to `queries.json` and to the copy embedded in the renderer. Dates are resolved at runtime from `date_spec` (`lag_days` = days back from today where the window ends; `previous_n_days.offset_days` = shift for the comparison window). `{{PSI_URL}}` is replaced by the user's URL and `{{PSI_ORIGIN}}` by its origin. `batch` says which `run_query` call a template belongs to (`core` limit 250, `ai` limit 5000).

```json
{"version":"1.0.0","batches":{"core":{"limit":250},"ai":{"limit":5000}},"queries":[
{"title":"GSC KPIs - Current","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC KPIs - Previous","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":3}},
{"title":"GSC Daily Trend","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Top Queries","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["query"],"filters":[],"sort":[{"sortField":"impressions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Top Pages","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["page"],"filters":[],"sort":[{"sortField":"clicks","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Device Split","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["device"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GA4 KPIs - Current","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","new_users","engaged_sessions","engagement_rate","average_session_duration","key_events","bounce_rate"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 KPIs - Previous","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","new_users","engaged_sessions","engagement_rate","average_session_duration","key_events","bounce_rate"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GA4 Daily Trend","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","key_events"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 Channel Mix","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","engagement_rate","key_events"],"dimensions":["session_default_channel_grouping"],"filters":[],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 Organic Landing Pages","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["landing_page"],"filters":[{"filterField":"session_default_channel_grouping","operator":"equals","expression":"Organic Search"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Sources - Current","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","total_users","engaged_sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Sources - Previous","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","total_users","engaged_sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GA4 AI Landing Pages","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","engaged_sessions","key_events"],"dimensions":["session_source","session_medium","landing_page"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Daily Trend","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions"],"dimensions":["date","session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"CrUX Field Data - Mobile","tab":"psi","batch":"core","connectorId":"psi","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","first_contentful_paint","experimental_time_to_first_byte"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"crux","urls":"{{PSI_ORIGIN}}","urlType":"origin","psiConnectionType":"origin","psiFormFactor":"mobile"},"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"CrUX Field Data - Desktop","tab":"psi","batch":"core","connectorId":"psi","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","first_contentful_paint","experimental_time_to_first_byte"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"crux","urls":"{{PSI_ORIGIN}}","urlType":"origin","psiConnectionType":"origin","psiFormFactor":"desktop"},"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"Lighthouse Audit - Mobile","tab":"psi","batch":"core","connectorId":"psi","metrics":["performance","seo","accessibility","best_practices","largest_contentful_paint","cumulative_layout_shift","total_blocking_time","first_contentful_paint","speed_index","server_response_time"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"psi","urls":"{{PSI_URL}}","strategy":"mobile","psiFormFactor":"mobile","urlType":"url","psiConnectionType":"url"},"date_spec":{"type":"last_n_days","n":1,"lag_days":0}},
{"title":"Lighthouse Audit - Desktop","tab":"psi","batch":"core","connectorId":"psi","metrics":["performance","seo","accessibility","best_practices","largest_contentful_paint","cumulative_layout_shift","total_blocking_time","first_contentful_paint","speed_index","server_response_time"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"psi","urls":"{{PSI_URL}}","strategy":"desktop","psiFormFactor":"desktop","urlType":"url","psiConnectionType":"url"},"date_spec":{"type":"last_n_days","n":1,"lag_days":0}},
{"title":"GBP KPIs - Current","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_total","views_search","views_maps","actions_website","actions_phone","actions_driving_directions","actions_total"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP KPIs - Previous","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_total","views_search","views_maps","actions_website","actions_phone","actions_driving_directions","actions_total"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GBP Daily Trend","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_search","views_maps","actions_total"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Search Keywords","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["monthly_search_impressions"],"dimensions":["search_terms"],"filters":[],"sort":[{"sortField":"monthly_search_impressions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Reviews Summary","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["total_review_count","total_review_star_rating"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Recent Reviews","tab":"gbp","batch":"core","connectorId":"gmb","metrics":[],"dimensions":["review_star_rating","review_create_date","review_comment","review_reply_comment"],"filters":[],"sort":[{"sortField":"review_create_date","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}}
]}
```

## Dashboard renderer

Write this to `<work>/seo_report.py` (step 4 extracts it automatically). It resolves date windows, parses `run_query` results, classifies AI sources, computes every KPI and delta, and writes the self-contained 5-tab HTML dashboard with all logos embedded. It prints a JSON summary for the insights. Do not modify it at runtime.

<!-- seo_report.py:start -->
```python
#!/usr/bin/env python3
"""SEO Performance Report helper for the tmr-multichannel-seo-performance-report skill.

Two subcommands:

  plan   Resolve every query's relative date_spec against today's date and write the
         ready-to-send `connectors` arrays for validate_query / run_query.

         python3 seo_report.py plan --today YYYY-MM-DD \
             --gsc "sc-domain:example.com" --ga4 123456789 \
             --psi-account "<psi account id>" --psi-url https://example.com/ \
             --gbp "<gbp account id>" [--gbp ...] --out-dir ./run

         Writes run/core_connectors.json, run/ai_connectors.json, run/windows.json

  build  Turn the run_query results into the dashboard HTML and print a JSON summary
         (the numbers Claude uses to write the inline insights).

         python3 seo_report.py build --results run/core.json run/ai.json \
             --windows run/windows.json --meta run/meta.json --out report.html \
             [--highlights run/highlights.json]

The query templates, the dashboard HTML template and all platform / AI logos are
embedded at the bottom of this file, so it is fully self-contained. Do not edit them per run.
"""
import argparse
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from urllib.parse import urlparse


# ---------------------------------------------------------------- AI platforms
# Order is fixed: it sets each platform's chart colour (colour follows the entity).
AI_PLATFORMS = [
    {"id": "chatgpt", "name": "ChatGPT", "keys": ["chatgpt", "openai"]},
    {"id": "gemini", "name": "Gemini", "keys": ["gemini", "bard.google"]},
    {"id": "perplexity", "name": "Perplexity", "keys": ["perplexity"]},
    {"id": "claude", "name": "Claude", "keys": ["claude.ai", "anthropic"]},
    {"id": "copilot", "name": "Copilot", "keys": ["copilot"]},
    {"id": "meta-ai", "name": "Meta AI", "keys": ["meta.ai"]},
    {"id": "grok", "name": "Grok", "keys": ["grok", "x.ai"]},
    {"id": "deepseek", "name": "DeepSeek", "keys": ["deepseek"]},
    {"id": "mistral", "name": "Mistral", "keys": ["mistral"]},
    {"id": "poe", "name": "Poe", "keys": ["poe.com"]},
    {"id": "you", "name": "You.com", "keys": ["you.com"]},
]
PAID_MEDIUM_KEYS = ("cpc", "ppc", "paid", "display", "cpm", "banner")


def classify_ai(source, medium):
    s = (source or "").lower()
    m = (medium or "").lower()
    if any(k in m for k in PAID_MEDIUM_KEYS):
        return None  # paid placements inside AI apps are not organic AI referrals
    for p in AI_PLATFORMS:
        if any(k in s for k in p["keys"]):
            return p["id"]
    return None


# ---------------------------------------------------------------- dates
def resolve(spec, today):
    lag = int(spec.get("lag_days", 0))
    t = spec["type"]
    if t == "last_n_days":
        end = today - dt.timedelta(days=lag)
        start = end - dt.timedelta(days=spec["n"] - 1)
    elif t == "previous_n_days":
        end = today - dt.timedelta(days=lag + spec["offset_days"])
        start = end - dt.timedelta(days=spec["n"] - 1)
    elif t == "month_to_date":
        start, end = today.replace(day=1), today
    elif t == "last_n_months":
        first = today.replace(day=1)
        end = first - dt.timedelta(days=1)
        start = first
        for _ in range(spec["n"]):
            start = (start - dt.timedelta(days=1)).replace(day=1)
    elif t == "fixed":
        return spec["startDate"], spec["endDate"]
    else:
        raise ValueError(f"unknown date_spec {t}")
    return start.isoformat(), end.isoformat()


def load_queries(path=None):
    if path:
        with open(path) as f:
            return json.load(f)
    return json.loads(QUERIES_JSON)


def origin_of(url):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}/" if p.scheme and p.netloc else url


def cmd_plan(a):
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    Q = load_queries(a.queries)
    accounts = {"gsc": a.gsc, "ga4": a.ga4, "psi": a.psi_account, "gmb": a.gbp}
    for k in ("gsc", "ga4", "psi"):
        if not accounts[k]:
            sys.exit(f"missing accounts for {k}")
    connected = [k for k, v in accounts.items() if v]  # gmb is optional
    psi_urls = a.psi_url or []
    if not psi_urls:
        sys.exit("--psi-url is required and must come from the user (never infer it)")
    batches = defaultdict(lambda: defaultdict(list))
    windows = {}
    for q in Q["queries"]:
        if q["connectorId"] not in connected:
            continue
        s, e = resolve(q["date_spec"], today)
        windows[q["title"]] = {"startDate": s, "endDate": e}
        query = {"metrics": q["metrics"], "dimensions": q["dimensions"],
                 "dateRange": {"startDate": s, "endDate": e}}
        if q.get("filters"):
            query["filters"] = q["filters"]
        if q.get("sort"):
            query["sort"] = q["sort"]
        rp = q.get("reportParams")
        if rp:
            rp = dict(rp)
            if rp.get("urls") == "{{PSI_URL}}":
                rp["urls"] = psi_urls
            elif rp.get("urls") == "{{PSI_ORIGIN}}":
                rp["urls"] = sorted({origin_of(u) for u in psi_urls})
            query["reportParams"] = rp
        batches[q["batch"]][q["connectorId"]].append({"title": q["title"], "query": query})
    os.makedirs(a.out_dir, exist_ok=True)
    for b, conns in batches.items():
        arr = [{"connectorId": cid, "accountIds": accounts[cid], "queries": qs} for cid, qs in conns.items()]
        with open(os.path.join(a.out_dir, f"{b}_connectors.json"), "w") as f:
            json.dump(arr, f, indent=1)
    meta_w = {
        "today": today.isoformat(),
        "current": windows["GA4 KPIs - Current"], "previous": windows["GA4 KPIs - Previous"],
        "gsc_current": windows["GSC KPIs - Current"], "gsc_previous": windows["GSC KPIs - Previous"],
        "limits": {b: Q["batches"][b]["limit"] for b in Q["batches"]},
        "queries": windows,
        "connectors": connected,
    }
    with open(os.path.join(a.out_dir, "windows.json"), "w") as f:
        json.dump(meta_w, f, indent=1)
    print(json.dumps({"written": sorted(os.listdir(a.out_dir)), "limits": meta_w["limits"],
                      "current": meta_w["current"], "gsc_current": meta_w["gsc_current"]}, indent=1))


# ---------------------------------------------------------------- results
def num(v):
    try:
        if v is None or v == "":
            return 0.0
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def fmt_date(v):
    s = str(v)
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
    return s[:10]


def load_results(paths, qdefs):
    """Return {title: [ {dims..., metrics..., _lead:[...]} ]} using query definitions for column order."""
    out = {}
    for p in paths:
        with open(p) as f:
            d = json.load(f)
        if isinstance(d, list):  # tolerate a bare connectorResults list
            d = {"connectorResults": d}
        for c in d.get("connectorResults", []):
            for r in c.get("results", []):
                t = r.get("title")
                q = qdefs.get(t)
                rows = (r.get("data") or {}).get("rows") or []
                if not q:
                    continue
                D, M = q["dimensions"], q["metrics"]
                recs = out.setdefault(t, [])
                for row in rows:
                    lead = len(row) - len(D) - len(M)
                    lead = max(lead, 0)
                    rec = {"_lead": row[:lead]}
                    for i, k in enumerate(D):
                        rec[k] = row[lead + i] if lead + i < len(row) else None
                    for i, k in enumerate(M):
                        j = lead + len(D) + i
                        rec[k] = row[j] if j < len(row) else None
                    recs.append(rec)
    return out


def pct(v):
    """Rates may arrive as 0–1 fractions or 0–100 percents; normalise to fraction."""
    v = num(v)
    return v / 100.0 if v > 1.0001 else v


def kv(cur, prev):
    return {"cur": cur, "prev": prev}


def gsc_totals(rows):
    c = sum(num(r.get("clicks")) for r in rows)
    i = sum(num(r.get("impressions")) for r in rows)
    if len(rows) == 1:
        ctr, pos = pct(rows[0].get("ctr")), num(rows[0].get("position"))
    else:
        ctr = c / i if i else 0
        pos = (sum(num(r.get("position")) * num(r.get("impressions")) for r in rows) / i) if i else 0
    return {"clicks": c, "impressions": i, "ctr": ctr, "position": pos}


def ga_totals(rows):
    s = sum(num(r.get("sessions")) for r in rows)
    out = {k: sum(num(r.get(k)) for r in rows) for k in ("sessions", "total_users", "new_users", "engaged_sessions", "key_events")}
    if len(rows) == 1:
        out["engagement_rate"] = pct(rows[0].get("engagement_rate"))
        out["average_session_duration"] = num(rows[0].get("average_session_duration"))
        out["bounce_rate"] = pct(rows[0].get("bounce_rate"))
    else:
        out["engagement_rate"] = out["engaged_sessions"] / s if s else 0
        out["average_session_duration"] = (sum(num(r.get("average_session_duration")) * num(r.get("sessions")) for r in rows) / s) if s else 0
        out["bounce_rate"] = 1 - out["engagement_rate"] if s else 0
    return out


def gsc_rows(rows, key, n):
    agg = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0, "pw": 0.0})
    for r in rows:
        k = r.get(key) or "(not set)"
        a = agg[k]
        a["clicks"] += num(r.get("clicks")); a["impressions"] += num(r.get("impressions"))
        a["pw"] += num(r.get("position")) * num(r.get("impressions"))
    out = []
    for k, a in agg.items():
        i = a["impressions"]
        out.append({"key": k, "clicks": a["clicks"], "impressions": i,
                    "ctr": a["clicks"] / i if i else 0, "position": a["pw"] / i if i else 0})
    out.sort(key=lambda x: (-x["clicks"], -x["impressions"]))
    return out[:n] if n else out


def build_data(R, W, meta):
    data = {"meta": meta, "windows": {k: W[k] for k in ("current", "previous", "gsc_current", "gsc_previous", "today")}}

    # ---------------- GSC
    gc, gp = gsc_totals(R.get("GSC KPIs - Current", [])), gsc_totals(R.get("GSC KPIs - Previous", []))
    trend = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0, "pw": 0.0})
    for r in R.get("GSC Daily Trend", []):
        t = trend[fmt_date(r.get("date"))]
        t["clicks"] += num(r.get("clicks")); t["impressions"] += num(r.get("impressions"))
        t["pw"] += num(r.get("position")) * num(r.get("impressions"))
    gtrend = [{"d": d, "clicks": v["clicks"], "impressions": v["impressions"],
               "ctr": v["clicks"] / v["impressions"] if v["impressions"] else 0,
               "position": v["pw"] / v["impressions"] if v["impressions"] else 0} for d, v in sorted(trend.items())]
    allq = gsc_rows(R.get("GSC Top Queries", []), "query", 0)
    striking = sorted([q for q in allq if 4 <= q["position"] <= 20 and q["impressions"] > 0],
                      key=lambda x: -x["impressions"])[:12]
    low_ctr = sorted([q for q in allq if q["position"] <= 5 and q["impressions"] >= 100 and q["ctr"] < 0.02],
                     key=lambda x: -x["impressions"])[:8]
    data["gsc"] = {
        "kpis": {k: kv(gc[k], gp[k]) for k in gc},
        "trend": gtrend,
        "queries": allq[:20],
        "striking": striking,
        "low_ctr": low_ctr,
        "query_count": len(allq),
        "pages": gsc_rows(R.get("GSC Top Pages", []), "page", 20),
        "devices": gsc_rows(R.get("GSC Device Split", []), "device", 0),
    }

    # ---------------- GA4
    ac, ap = ga_totals(R.get("GA4 KPIs - Current", [])), ga_totals(R.get("GA4 KPIs - Previous", []))
    t2 = defaultdict(lambda: {"sessions": 0.0, "users": 0.0, "key_events": 0.0})
    for r in R.get("GA4 Daily Trend", []):
        t = t2[fmt_date(r.get("date"))]
        t["sessions"] += num(r.get("sessions")); t["users"] += num(r.get("total_users")); t["key_events"] += num(r.get("key_events"))
    ch = defaultdict(lambda: {"sessions": 0.0, "users": 0.0, "eng": 0.0, "key_events": 0.0})
    for r in R.get("GA4 Channel Mix", []):
        c = ch[r.get("session_default_channel_grouping") or "Unassigned"]
        s = num(r.get("sessions"))
        c["sessions"] += s; c["users"] += num(r.get("total_users")); c["key_events"] += num(r.get("key_events"))
        c["eng"] += pct(r.get("engagement_rate")) * s
    channels = sorted([{"name": k, "sessions": v["sessions"], "users": v["users"], "key_events": v["key_events"],
                        "engagement_rate": v["eng"] / v["sessions"] if v["sessions"] else 0} for k, v in ch.items()],
                      key=lambda x: -x["sessions"])
    lp = defaultdict(lambda: {"sessions": 0.0, "eng": 0.0, "key_events": 0.0, "dur": 0.0})
    for r in R.get("GA4 Organic Landing Pages", []):
        p = lp[r.get("landing_page") or "(not set)"]
        s = num(r.get("sessions"))
        p["sessions"] += s; p["key_events"] += num(r.get("key_events"))
        p["eng"] += pct(r.get("engagement_rate")) * s; p["dur"] += num(r.get("average_session_duration")) * s
    pages = sorted([{"page": k, "sessions": v["sessions"], "key_events": v["key_events"],
                     "engagement_rate": v["eng"] / v["sessions"] if v["sessions"] else 0,
                     "duration": v["dur"] / v["sessions"] if v["sessions"] else 0} for k, v in lp.items()],
                   key=lambda x: -x["sessions"])[:20]
    organic = next((c for c in channels if c["name"].lower() == "organic search"), None)
    data["ga4"] = {
        "kpis": {k: kv(ac[k], ap[k]) for k in ac},
        "trend": [{"d": d, **v} for d, v in sorted(t2.items())],
        "channels": channels,
        "organic_pages": pages,
        "organic_sessions": organic["sessions"] if organic else 0,
    }

    # ---------------- AI traffic
    def ai_agg(rows):
        P = defaultdict(lambda: {"sessions": 0.0, "users": 0.0, "engaged": 0.0, "key_events": 0.0, "dur": 0.0, "sources": set()})
        for r in rows:
            pid = classify_ai(r.get("session_source"), r.get("session_medium"))
            if not pid:
                continue
            s = num(r.get("sessions"))
            x = P[pid]
            x["sessions"] += s; x["users"] += num(r.get("total_users")); x["engaged"] += num(r.get("engaged_sessions"))
            x["key_events"] += num(r.get("key_events")); x["dur"] += num(r.get("average_session_duration")) * s
            x["sources"].add(f'{r.get("session_source")} / {r.get("session_medium")}')
        return P
    cur, prev = ai_agg(R.get("GA4 AI Sources - Current", [])), ai_agg(R.get("GA4 AI Sources - Previous", []))
    pg = defaultdict(lambda: {"sessions": 0.0, "engaged": 0.0, "key_events": 0.0, "by": defaultdict(float)})
    top_page = defaultdict(lambda: defaultdict(float))
    for r in R.get("GA4 AI Landing Pages", []):
        pid = classify_ai(r.get("session_source"), r.get("session_medium"))
        if not pid:
            continue
        page = r.get("landing_page") or "(not set)"
        s = num(r.get("sessions"))
        x = pg[page]
        x["sessions"] += s; x["engaged"] += num(r.get("engaged_sessions")); x["key_events"] += num(r.get("key_events"))
        x["by"][pid] += s
        top_page[pid][page] += s
    tr = defaultdict(lambda: defaultdict(float))
    for r in R.get("GA4 AI Daily Trend", []):
        pid = classify_ai(r.get("session_source"), r.get("session_medium"))
        if pid:
            tr[fmt_date(r.get("date"))][pid] += num(r.get("sessions"))
    tot_cur = sum(v["sessions"] for v in cur.values())
    tot_prev = sum(v["sessions"] for v in prev.values())
    plats = []
    for i, p in enumerate(AI_PLATFORMS):
        c = cur.get(p["id"])
        pv = prev.get(p["id"], {}).get("sessions", 0.0)
        if not c and not pv:
            continue
        c = c or {"sessions": 0, "users": 0, "engaged": 0, "key_events": 0, "dur": 0, "sources": set()}
        tp = sorted(top_page[p["id"]].items(), key=lambda x: -x[1])[:3]
        plats.append({"id": p["id"], "name": p["name"], "order": i, "sessions": c["sessions"], "prev": pv,
                      "users": c["users"], "key_events": c["key_events"],
                      "engagement_rate": c["engaged"] / c["sessions"] if c["sessions"] else 0,
                      "duration": c["dur"] / c["sessions"] if c["sessions"] else 0,
                      "share": c["sessions"] / tot_cur if tot_cur else 0,
                      "sources": sorted(c["sources"])[:4], "top_pages": [{"page": a, "sessions": b} for a, b in tp]})
    plats.sort(key=lambda x: -x["sessions"])
    eng_cur = sum(v["engaged"] for v in cur.values())
    eng_prev = sum(v["engaged"] for v in prev.values())
    ke_cur = sum(v["key_events"] for v in cur.values())
    ke_prev = sum(v["key_events"] for v in prev.values())
    site_cur, site_prev = ac["sessions"], ap["sessions"]
    data["ai"] = {
        "kpis": {
            "sessions": kv(tot_cur, tot_prev),
            "share": kv(tot_cur / site_cur if site_cur else 0, tot_prev / site_prev if site_prev else 0),
            "users": kv(sum(v["users"] for v in cur.values()), sum(v["users"] for v in prev.values())),
            "key_events": kv(ke_cur, ke_prev),
            "engagement_rate": kv(eng_cur / tot_cur if tot_cur else 0, eng_prev / tot_prev if tot_prev else 0),
        },
        "platforms": plats,
        "trend": [{"d": d, "by": dict(v)} for d, v in sorted(tr.items())],
        "pages": sorted([{"page": k, "sessions": v["sessions"], "key_events": v["key_events"],
                          "engagement_rate": v["engaged"] / v["sessions"] if v["sessions"] else 0,
                          "by": dict(v["by"])} for k, v in pg.items()], key=lambda x: -x["sessions"])[:20],
    }

    # ---------------- PSI
    def first(title):
        rows = R.get(title, [])
        return rows[0] if rows else None
    def crux(title):
        r = first(title)
        if not r:
            return None
        return {"lcp": num(r.get("largest_contentful_paint")), "inp": num(r.get("interaction_to_next_paint")),
                "cls": num(r.get("cumulative_layout_shift")), "fcp": num(r.get("first_contentful_paint")),
                "ttfb": num(r.get("experimental_time_to_first_byte")),
                "origin": (r.get("_lead") or [None, None])[-1]}
    def secs(v):
        v = num(v)
        return v / 1000.0 if v > 60 else v  # lab timings may arrive in ms or s
    def score(v):
        v = num(v)
        return v * 100 if 0 < v <= 1 else v
    def labr(title):
        r = first(title)
        if not r:
            return None
        return {"performance": score(r.get("performance")), "seo": score(r.get("seo")),
                "accessibility": score(r.get("accessibility")), "best_practices": score(r.get("best_practices")),
                "lcp": secs(r.get("largest_contentful_paint")), "cls": num(r.get("cumulative_layout_shift")),
                "tbt": num(r.get("total_blocking_time")) if num(r.get("total_blocking_time")) > 5 else num(r.get("total_blocking_time")) * 1000,
                "fcp": secs(r.get("first_contentful_paint")), "si": secs(r.get("speed_index")),
                "ttfb": num(r.get("server_response_time")) / 1000.0 if num(r.get("server_response_time")) > 5 else num(r.get("server_response_time")),
                "url": (r.get("_lead") or [None, None])[-1]}
    data["psi"] = {"crux": {"mobile": crux("CrUX Field Data - Mobile"), "desktop": crux("CrUX Field Data - Desktop")},
                   "lab": {"mobile": labr("Lighthouse Audit - Mobile"), "desktop": labr("Lighthouse Audit - Desktop")}}

    # ---------------- GBP
    keys = ["views_total", "views_search", "views_maps", "actions_website", "actions_phone", "actions_driving_directions", "actions_total"]
    def gb(rows):
        return {k: sum(num(r.get(k)) for r in rows) for k in keys}
    bc, bp = gb(R.get("GBP KPIs - Current", [])), gb(R.get("GBP KPIs - Previous", []))
    prev_loc = {r.get("location_name"): r for r in R.get("GBP KPIs - Previous", [])}
    locs = []
    for r in R.get("GBP KPIs - Current", []):
        n = r.get("location_name") or "(location)"
        locs.append({"name": n, **{k: num(r.get(k)) for k in keys},
                     "prev_views": num((prev_loc.get(n) or {}).get("views_total")),
                     "prev_actions": num((prev_loc.get(n) or {}).get("actions_total"))})
    bt = defaultdict(lambda: {"search": 0.0, "maps": 0.0, "actions": 0.0})
    for r in R.get("GBP Daily Trend", []):
        t = bt[fmt_date(r.get("date"))]
        t["search"] += num(r.get("views_search")); t["maps"] += num(r.get("views_maps")); t["actions"] += num(r.get("actions_total"))
    kw = defaultdict(float)
    for r in R.get("GBP Search Keywords", []):
        kw[r.get("search_terms") or "(other)"] += num(r.get("monthly_search_impressions"))
    rs = R.get("GBP Reviews Summary", [])
    cnt = sum(num(r.get("total_review_count")) for r in rs)
    rating = (sum(num(r.get("total_review_star_rating")) * num(r.get("total_review_count")) for r in rs) / cnt) if cnt else (num(rs[0].get("total_review_star_rating")) if rs else 0)
    star_map = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}
    dist = {str(i): 0 for i in range(1, 6)}
    recent = []
    for r in R.get("GBP Recent Reviews", []):
        sv = r.get("review_star_rating")
        st = star_map.get(str(sv).upper(), None) or int(num(sv) or 0)
        if 1 <= st <= 5:
            dist[str(st)] += 1
        if len(recent) < 6:
            recent.append({"stars": st, "date": fmt_date(r.get("review_create_date")),
                           "comment": (r.get("review_comment") or "")[:280], "replied": bool(r.get("review_reply_comment"))})
    replied = sum(1 for r in R.get("GBP Recent Reviews", []) if r.get("review_reply_comment"))
    nrev = len(R.get("GBP Recent Reviews", []))
    data["gbp"] = {
        "kpis": {k: kv(bc[k], bp[k]) for k in keys},
        "locations": sorted(locs, key=lambda x: -x["views_total"]),
        "trend": [{"d": d, **v} for d, v in sorted(bt.items())],
        "keywords": [{"term": k, "impressions": v} for k, v in sorted(kw.items(), key=lambda x: -x[1])[:15]],
        "reviews": {"count": cnt, "rating": rating, "dist": dist, "recent": recent,
                    "new_in_period": nrev, "reply_rate": replied / nrev if nrev else None},
    }
    return data


def delta(c, p):
    return None if not p else (c - p) / p


def auto_highlights(D):
    """A few deterministic call-outs. Claude may replace them with its own via --highlights."""
    H = []
    g = D["gsc"]["kpis"]
    d = delta(g["clicks"]["cur"], g["clicks"]["prev"])
    if d is not None:
        H.append({"tone": "good" if d >= 0 else "bad", "src": "gsc",
                  "text": f"Organic clicks {'up' if d >= 0 else 'down'} {abs(d)*100:.1f}% vs the previous 28 days."})
    if D["gsc"]["striking"]:
        q = D["gsc"]["striking"][0]
        H.append({"tone": "info", "src": "gsc",
                  "text": f"Quick win: “{q['key']}” sits at position {q['position']:.1f} with {int(q['impressions']):,} impressions."})
    a = D["ai"]["kpis"]
    if a["sessions"]["cur"]:
        top = D["ai"]["platforms"][0]["name"] if D["ai"]["platforms"] else "AI assistants"
        H.append({"tone": "info", "src": "ai",
                  "text": f"AI assistants sent {int(a['sessions']['cur']):,} sessions ({a['share']['cur']*100:.2f}% of all traffic); {top} leads."})
    m = D["psi"]["crux"].get("mobile")
    if m:
        ok = m["lcp"] <= 2.5 and m["inp"] <= 0.2 and m["cls"] <= 0.1
        H.append({"tone": "good" if ok else "bad", "src": "psi",
                  "text": "Mobile Core Web Vitals pass for real users." if ok else "Mobile Core Web Vitals fail for real users — see Page Speed."})
    b = D["gbp"]["kpis"]
    d = None if "gmb" not in D.get("connected", ["gmb"]) else delta(b["actions_total"]["cur"], b["actions_total"]["prev"])
    if d is not None:
        H.append({"tone": "good" if d >= 0 else "bad", "src": "gbp",
                  "text": f"Business Profile actions {'up' if d >= 0 else 'down'} {abs(d)*100:.1f}% (calls, website clicks, directions)."})
    return H


def summary(D):
    def kd(block):
        return {k: {"cur": v["cur"], "prev": v["prev"], "delta": delta(v["cur"], v["prev"])} for k, v in block.items()}
    return {
        "gsc": kd(D["gsc"]["kpis"]), "gsc_top_queries": D["gsc"]["queries"][:5], "gsc_striking": D["gsc"]["striking"][:5],
        "gsc_low_ctr": D["gsc"]["low_ctr"][:3], "gsc_top_pages": D["gsc"]["pages"][:5],
        "ga4": kd(D["ga4"]["kpis"]), "ga4_channels": D["ga4"]["channels"][:6], "ga4_organic_pages": D["ga4"]["organic_pages"][:5],
        "ai": kd(D["ai"]["kpis"]), "ai_platforms": [{k: p[k] for k in ("name", "sessions", "prev", "share", "key_events", "engagement_rate")} for p in D["ai"]["platforms"]],
        "ai_top_pages": D["ai"]["pages"][:5],
        "psi": D["psi"], "gbp": kd(D["gbp"]["kpis"]), "gbp_reviews": {k: v for k, v in D["gbp"]["reviews"].items() if k != "recent"},
        "gbp_keywords": D["gbp"]["keywords"][:5], "highlights": D["highlights"],
    }


def cmd_build(a):
    Q = load_queries(a.queries)
    qdefs = {q["title"]: q for q in Q["queries"]}
    R = load_results(a.results, qdefs)
    missing = [t for t in qdefs if t not in R]
    with open(a.windows) as f:
        W = json.load(f)
    with open(a.meta) as f:
        meta = json.load(f)
    D = build_data(R, W, meta)
    D["connected"] = W.get("connectors", ["gsc", "ga4", "psi", "gmb"])
    D["missing"] = [t for t in missing if qdefs[t]["connectorId"] in D["connected"]]
    if a.highlights and os.path.exists(a.highlights):
        with open(a.highlights) as f:
            D["highlights"] = json.load(f)
    else:
        D["highlights"] = auto_highlights(D)
    tpl = TEMPLATE
    logos = json.dumps(LOGOS)
    blob = json.dumps(D, default=list).replace("</", "<\\/")
    title = f"SEO Performance Report — {meta.get('run_at', '')} — {meta.get('site', '')}"
    html = (tpl.replace("{{REPORT_DATA_JSON}}", blob)
               .replace("{{LOGOS_JSON}}", logos.replace("</", "<\\/"))
               .replace("{{TITLE}}", title.replace("<", "&lt;")))
    with open(a.out, "w") as f:
        f.write(html)
    s = summary(D)
    s["missing_queries"] = missing
    s["out"] = a.out
    print(json.dumps(s, indent=1, default=list))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("plan")
    p.add_argument("--today")
    p.add_argument("--gsc", nargs="+", required=True)
    p.add_argument("--ga4", nargs="+", required=True)
    p.add_argument("--psi-account", nargs="+", required=True)
    p.add_argument("--psi-url", nargs="+", required=True)
    p.add_argument("--gbp", nargs="+", default=None, help="optional: omit when the user has no Google Business Profile in TMR")
    p.add_argument("--out-dir", default="seo_run")
    p.add_argument("--queries", help="optional path to queries.json (defaults to the embedded copy)")
    b = sp.add_parser("build")
    b.add_argument("--results", nargs="+", required=True)
    b.add_argument("--windows", required=True)
    b.add_argument("--meta", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--highlights")
    b.add_argument("--queries", help="optional path to queries.json (defaults to the embedded copy)")
    a = ap.parse_args()
    cmd_plan(a) if a.cmd == "plan" else cmd_build(a)


# ================================================================ embedded data
QUERIES_JSON = r'''{"version":"1.0.0","batches":{"core":{"limit":250},"ai":{"limit":5000}},"queries":[
{"title":"GSC KPIs - Current","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC KPIs - Previous","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":3}},
{"title":"GSC Daily Trend","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Top Queries","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["query"],"filters":[],"sort":[{"sortField":"impressions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Top Pages","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["page"],"filters":[],"sort":[{"sortField":"clicks","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GSC Device Split","tab":"gsc","batch":"core","connectorId":"gsc","metrics":["clicks","impressions","ctr","position"],"dimensions":["device"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":3}},
{"title":"GA4 KPIs - Current","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","new_users","engaged_sessions","engagement_rate","average_session_duration","key_events","bounce_rate"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 KPIs - Previous","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","new_users","engaged_sessions","engagement_rate","average_session_duration","key_events","bounce_rate"],"dimensions":[],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GA4 Daily Trend","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","key_events"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 Channel Mix","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","total_users","engagement_rate","key_events"],"dimensions":["session_default_channel_grouping"],"filters":[],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 Organic Landing Pages","tab":"ga4","batch":"core","connectorId":"ga4","metrics":["sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["landing_page"],"filters":[{"filterField":"session_default_channel_grouping","operator":"equals","expression":"Organic Search"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Sources - Current","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","total_users","engaged_sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Sources - Previous","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","total_users","engaged_sessions","engagement_rate","key_events","average_session_duration"],"dimensions":["session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GA4 AI Landing Pages","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions","engaged_sessions","key_events"],"dimensions":["session_source","session_medium","landing_page"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"sessions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GA4 AI Daily Trend","tab":"ai","batch":"ai","connectorId":"ga4","metrics":["sessions"],"dimensions":["date","session_source","session_medium"],"filters":[{"filterField":"session_source","operator":"notEquals","expression":"google"},{"filterField":"session_source","operator":"notEquals","expression":"(direct)"}],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"CrUX Field Data - Mobile","tab":"psi","batch":"core","connectorId":"psi","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","first_contentful_paint","experimental_time_to_first_byte"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"crux","urls":"{{PSI_ORIGIN}}","urlType":"origin","psiConnectionType":"origin","psiFormFactor":"mobile"},"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"CrUX Field Data - Desktop","tab":"psi","batch":"core","connectorId":"psi","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","first_contentful_paint","experimental_time_to_first_byte"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"crux","urls":"{{PSI_ORIGIN}}","urlType":"origin","psiConnectionType":"origin","psiFormFactor":"desktop"},"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"Lighthouse Audit - Mobile","tab":"psi","batch":"core","connectorId":"psi","metrics":["performance","seo","accessibility","best_practices","largest_contentful_paint","cumulative_layout_shift","total_blocking_time","first_contentful_paint","speed_index","server_response_time"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"psi","urls":"{{PSI_URL}}","strategy":"mobile","psiFormFactor":"mobile","urlType":"url","psiConnectionType":"url"},"date_spec":{"type":"last_n_days","n":1,"lag_days":0}},
{"title":"Lighthouse Audit - Desktop","tab":"psi","batch":"core","connectorId":"psi","metrics":["performance","seo","accessibility","best_practices","largest_contentful_paint","cumulative_layout_shift","total_blocking_time","first_contentful_paint","speed_index","server_response_time"],"dimensions":[],"filters":[],"sort":[],"reportParams":{"psiApiMethod":"psi","urls":"{{PSI_URL}}","strategy":"desktop","psiFormFactor":"desktop","urlType":"url","psiConnectionType":"url"},"date_spec":{"type":"last_n_days","n":1,"lag_days":0}},
{"title":"GBP KPIs - Current","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_total","views_search","views_maps","actions_website","actions_phone","actions_driving_directions","actions_total"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP KPIs - Previous","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_total","views_search","views_maps","actions_website","actions_phone","actions_driving_directions","actions_total"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"previous_n_days","n":28,"offset_days":28,"lag_days":1}},
{"title":"GBP Daily Trend","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["views_search","views_maps","actions_total"],"dimensions":["date"],"filters":[],"sort":[{"sortField":"date","direction":"asc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Search Keywords","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["monthly_search_impressions"],"dimensions":["search_terms"],"filters":[],"sort":[{"sortField":"monthly_search_impressions","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Reviews Summary","tab":"gbp","batch":"core","connectorId":"gmb","metrics":["total_review_count","total_review_star_rating"],"dimensions":["location_name"],"filters":[],"sort":[],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}},
{"title":"GBP Recent Reviews","tab":"gbp","batch":"core","connectorId":"gmb","metrics":[],"dimensions":["review_star_rating","review_create_date","review_comment","review_reply_comment"],"filters":[],"sort":[{"sortField":"review_create_date","direction":"desc"}],"date_spec":{"type":"last_n_days","n":28,"lag_days":1}}
]}'''

LOGOS = {
    "platforms": {
        "ga4": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTYgMjg0Ij48cGF0aCBmaWxsPSIjZjlhYjAwIiBkPSJNMjU2LjAwMyAyNDcuOTMzYTM1LjIyNCAzNS4yMjQgMCAwIDEtMzkuMzc2IDM1LjE2MWMtMTguMDQ0LTIuNjctMzEuMjY2LTE4LjM3MS0zMC44MjYtMzYuNjA2VjM2Ljg0NUMxODUuMzY1IDE4LjU5MSAxOTguNjIgMi44ODEgMjE2LjY4Ny4yNGEzNS4yMiAzNS4yMiAwIDAgMSAzOS4zMTYgMzUuMTZ6Ii8+PHBhdGggZmlsbD0iI2UzNzQwMCIgZD0iTTM1LjEwMSAyMTMuMTkzYzE5LjM4NiAwIDM1LjEwMSAxNS43MTYgMzUuMTAxIDM1LjEwMWMwIDE5LjM4Ni0xNS43MTUgMzUuMTAxLTM1LjEwMSAzNS4xMDFTMCAyNjcuNjggMCAyNDguMjk1czE1LjcxNS0zNS4xMDIgMzUuMTAxLTM1LjEwMm05Mi4zNTgtMTA2LjM4N2MtMTkuNDc3IDEuMDY4LTM0LjU5IDE3LjQwNi0zNC4xMzcgMzYuOTA4djk0LjI4NWMwIDI1LjU4OCAxMS4yNTkgNDEuMTIyIDI3Ljc1NSA0NC40MzNhMzUuMTYgMzUuMTYgMCAwIDAgNDIuMTQ2LTM0LjU2VjE0Mi4wODlhMzUuMjIgMzUuMjIgMCAwIDAtMzUuNzY0LTM1LjI4MiIvPjwvc3ZnPg==",
        "gsc": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTYgMjI4Ij48ZGVmcz48cmFkaWFsR3JhZGllbnQgaWQ9IlNWR3VHVEIyZFVJIiBjeD0iMjEuNjYlIiBjeT0iMjguNzA4JSIgcj0iODIuODclIiBmeD0iMjEuNjYlIiBmeT0iMjguNzA4JSIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCguNTk1MDMgLjU5NDg2IC0uNDQwMzQgLjgwMzgzIC4yMTQgLS4wNzMpIj48c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjZjFmMmYyIi8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjZTZlN2U4Ii8+PC9yYWRpYWxHcmFkaWVudD48L2RlZnM+PHBhdGggZmlsbD0iIzczNzM3MyIgZD0iTTE2NS45NzkgMEg5MC4wMjFMNzEuMDk3IDE5LjA1NXYxOC45MjRoMTguOTI0VjE5LjA1NWg3NS45NTh2MTguOTI0aDE4LjkyNFYxOS4wNTV6Ii8+PHBhdGggZmlsbD0iI2JmYmZiZiIgZD0iTTkwLjAyMSAwdjE5LjA1NWg3NS45NThWMHoiLz48cGF0aCBmaWxsPSJ1cmwoI1NWR3VHVEIyZFVJKSIgZD0iTTM2LjQwMiAzNy45OEwwIDc0LjM4MXYxMzQuMTc3YzAgMTAuNTEzIDguNTQyIDE4LjkyNCAxOC45MjQgMTguOTI0aDIxOC4xNTJjMTAuNTEzIDAgMTguOTI0LTguNTQzIDE4LjkyNC0xOC45MjRWNzQuNTEzTDIxOS40NjYgMzcuOTh6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTI4LjUxNyAxMDkuMDc2aDE5OS4wOTd2MTE4LjUzOEgyOC41MTd6Ii8+PHBhdGggZmlsbD0iI2UwZTBlMCIgZD0iTTM2LjQwMiAzNy45NzlMMCA3NC4zODJ2MzQuNjk0aDI1NlY3NC41MTNsLTM2LjUzNC0zNi41MzR6Ii8+PHBhdGggZmlsbD0iI2QxZDFkMSIgZD0iTTQyLjcxIDIxMy4yOUgxMjh2MTQuMTkzSDQyLjcxeiIvPjxwYXRoIGZpbGw9IiM0Mjg1ZjQiIGQ9Ik0yOC41MTcgODYuOTk4YTE0LjY5NSAxNC42OTUgMCAwIDEgMTQuNzItMTQuNzE5aDE2OS41MjdhMTQuNjk1IDE0LjY5NSAwIDAgMSAxNC43MTkgMTQuNzE5djIyLjA3OEgyOC41MTd6Ii8+PHBhdGggZmlsbD0iI2U2ZTZlNiIgZD0iTTU2LjkwMyA5MC4xNTJhNy4wNjcgNy4wNjcgMCAwIDEtNy4wOTYgNy4wOTZhNy4wNjcgNy4wNjcgMCAwIDEtNy4wOTctNy4wOTZhNy4wNjcgNy4wNjcgMCAwIDEgNy4wOTctNy4wOTdhNy4wNjcgNy4wNjcgMCAwIDEgNy4wOTYgNy4wOTdtMjMuNjU2IDBhNy4wNjcgNy4wNjcgMCAwIDEtNy4wOTcgNy4wOTZhNy4wNjcgNy4wNjcgMCAwIDEtNy4wOTYtNy4wOTZhNy4wNjcgNy4wNjcgMCAwIDEgNy4wOTYtNy4wOTdhNy4wNjcgNy4wNjcgMCAwIDEgNy4wOTcgNy4wOTciLz48cGF0aCBmaWxsPSIjYmFiYWJhIiBkPSJtMjI3LjQ4MyAxNjUuMTkxbC0yOS44MzItMjkuODMybC05Ljk4OCAzMC44ODNsLTQwLjczOS00MC42MDhsLTEuMTgzIDYyLjY4NmwxNS4xMTMgMjMuNjU1YzIuMjM0LS4zOTQtMTEuMzAyIDE1LjUwOC0xMS4zMDIgMTUuNTA4aDc3LjkzeiIvPjxwYXRoIGZpbGw9IiM0ZDRkNGQiIGQ9Ik0yMDguODIxIDE2NC4wMDhjMC0xNi44MjEtOS44NTYtMzEuMjc3LTIzLjkxOC0zOC4yNDJ2MzkuOTVsLTE4Ljc5MiAxMC4xMmwtMTkuMDU2LTEwLjEydi00MC4wODJjLTE0LjA2MSA2Ljk2Ni0yMy42NTUgMjEuNTUzLTIzLjY1NSAzOC4yNDNjMCAxNi44MjEgOS43MjUgMzEuMjc3IDIzLjc4NyAzOC4yNDJ2MjUuMzY0aDM3Ljg0OHYtMjUuMzY0YzEzLjkzLTYuODM0IDIzLjc4Ni0yMS40MiAyMy43ODYtMzguMTEiLz48cGF0aCBmaWxsPSIjZDFkMWQxIiBkPSJNNDIuNzEgMTIzLjI2OWg2Ni4zNjZ2NzUuODI4SDQyLjcxeiIvPjwvc3ZnPg==",
        "psi": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjNDI4NUY0IiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+UGFnZVNwZWVkIEluc2lnaHRzPC90aXRsZT48cGF0aCBkPSJNMjIuMzYzIDEuNjM2SDEuNjM1Qy43MzIgMS42MzYgMCAyLjM3LjAwMSAzLjI3M0wwIDIwLjcyN3YuMDAzYzAgLjkwMy43MzMgMS42MzQgMS42MzUgMS42MzRoMjAuNzNjLjkwNCAwIDEuNjM1LS43MzQgMS42MzUtMS42MzdWMy4yNzNjLjAxNi0uODktLjc2LTEuNjQtMS42MzctMS42Mzd6TTMuOTc5IDIuODg2Yy40OTItLjUwNyAxLjI3OS4yOC43Ny43NzItLjQ5MS41MDgtMS4yNzgtLjI3OS0uNzctLjc3MXpNMS44IDIuODljLjUwNy0uNTA5IDEuMjguMjY1Ljc3Mi43NzEtLjQ5My41MDItMS4yNzQtLjI4LS43NzItLjc3MXptMjEuNyAxNy44MzhjLjAxMi42MTEtLjUyNCAxLjE0OC0xLjEzNyAxLjEzNkgxLjYzNUExLjEzNyAxLjEzNyAwIDAgMSAuNSAyMC43MjdMLjUwMSA0LjkxSDIzLjV2MTUuODE5ek0xMSAxNi4xNTlsNS45NDYtNC41NzdjLjIzNS0uMi41NzYuMTI5LjM4OS4zNzJsLS4wMDItLjAwMi0zLjkzNiA2LjM1YTEuNjM4IDEuNjM4IDAgMCAxLTIuNDQ4LjQwNWMtLjc4NS0uNjY4LS44MTEtMS44MzUuMDUtMi41NDh6bTQuNzYzLS43NWMuMDktLjE2OCAyLjAwMi0zLjE4MSAyLjA2LTMuMzUgMi4wNTYgMS44MTMgMy4wMjkgNC4zODIgMi44OTggNy4wMjZoLTMuODE5Yy4wNzMtMS4zOS0uMjktMi42NzgtMS4xMzktMy42NzZ6bS04LjY3OSAzLjY4MkgzLjI3OGMtLjM1Ny03LjAyMiA3LjE0OC0xMS43MzUgMTMuMzktNy45MmwtMy40NjEgMi42MThjLTMuMy0uNzYyLTYuMzY0IDEuNzEtNi4xMjMgNS4zMDJ6Ii8+PC9zdmc+",
        "gbp": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjNDI4NUY0IiByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+R29vZ2xlIE15IEJ1c2luZXNzPC90aXRsZT48cGF0aCBkPSJNMy4yNzMgMS42MzZjLS43MzYgMC0xLjM2My40OTItMS41NjggMS4xNkwwIDkuMjcyYzAgMS42NjQgMS4zMzYgMyAzIDNhMyAzIDAgMDAzLTNjMCAxLjY2NCAxLjMzNiAzIDMgM2EzIDMgMCAwMDMtM2MwIDEuNjUgMS4zNSAzIDMgMyAxLjY2NCAwIDMtMS4zMzYgMy0zIDAgMS42NjQgMS4zMzYgMyAzIDNzMy0xLjMzNiAzLTNsLTEuNzA1LTYuNDc2YTEuNjQ2IDEuNjQ2IDAgMDAtMS41NjgtMS4xNnptOC43MjkgOS4zMjZjLS42MDQgMS4wNjMtMS43MDMgMS44MS0zLjAwMiAxLjgxLTEuMzA0IDAtMi4zOTgtLjc0Ny0zLTEuODA2LS42MDQgMS4wNi0xLjcwMiAxLjgwNi0zIDEuODA2LS40ODQgMC0uOTQ0LS4xLTEuMzYzLS4yNzd2OC4yMzJjMCAuOS43MzYgMS42MzcgMS42MzYgMS42MzdoMTcuNDU0Yy45IDAgMS42MzYtLjczNyAxLjYzNi0xLjYzN3YtOC4yMzJhMy40OCAzLjQ4IDAgMDEtMS4zNjMuMjc3Yy0xLjMwNCAwLTIuMzk4LS43NDYtMy0xLjgwNC0uNjAyIDEuMDU4LTEuNjk2IDEuODA0LTMgMS44MDQtMS4yOTkgMC0yLjM5NC0uNzUtMi45OTgtMS44MXptNS43MjUgMy43NjVjLjgwOCAwIDEuNDg4LjI5OCAyLjAwNy43ODJsLS44NTkuODU5YTEuNjIzIDEuNjIzIDAgMDAtMS4xNDgtLjQ0N2MtLjk4IDAtMS43NzIuODI3LTEuNzcyIDEuODA2IDAgLjk4Ljc5MiAxLjgwNyAxLjc3MiAxLjgwNy44ODIgMCAxLjQ4NS0uNTAxIDEuNjE1LTEuMTkxaC0xLjYxNXYtMS4xNmgyLjgyNmMuMDM1LjE5Ni4wNTQuNC4wNTQuNjEzIDAgMS43MTQtMS4xNDcgMi45MzEtMi44OCAyLjkzMWEzIDMgMCAwMTAtNnoiLz48L3N2Zz4=",
    },
    "ai": {
        "chatgpt": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEVUVFSnp6dOTk5DQ0OUlJQtLS0ZGRkhISEgICDV1dVTU1MAAAACAgL+/v4XFxcnJydVVVV+fn4kJCQ3NzdDQ0M2NjZXV1c7OztISEhoaGgrKysXFxc6OjoTExNJSUmGhoaXl5d3d3eoqKgXFxdlZWUoKChXV1eGhoa3t7c5OTl4eHjIyMhaWlrExMTY2Njl5eUv2SzNAAAAMHRSTlMiF1bGU1QvlN0hpwD9BvXQAwLrsLfKbgSPULzVcXFzMytNKYhtBodJI5IvFVMmFxMn42FtAAADw0lEQVR42nVWh3aqQBBd20vyxi0sRRADyDO2aPL/f/emoZiy5yiwzN1pd2YwMF4JgC3SGF2MaWH5+esy44eA4nE5rLrAHYQk9jdAgHO+HK+01zerHwEJGEdivtwsNqeabuO8XSwOk980dCTvL2KBvXh8co5+6+YTN74B7JqsoP0QyIb9yDi/GyJg7qqmJM/2EmjrRdQN/lhBjDSgRPxEz2m1qbizqYyp9oydWT7IDOGvTrhZ4PmI+CxFXN3BYDvWHhSA4d9xPN2EsTvORaTMvb0FFuuf+TgBBOg0/J52DoItj4O9doigF5MSONfq2BPuVGxNfhDvC8IFui/UYjzkhXyKU/z/hye8ahBFmVvGvXDK1hJzBKTk0BXWN0Bp+dQ+k5D6ismxQDs/CFBJkO0NgJ684Yl7dD3mhHFphy8wTa6HxJCgu8JqBHjHCxHD/T3arYZgAn/wivYYg9cGNY4AFs7EkvwqOeAgu6bFPwI0eO3QqxHgemLj3aln494ljYhzRzQp1fjeAY5eNQ3xlHKH0e1SLSk01uTK0DsABbOepBCSbyXAFdMppcTh3RM8AtaHu5TLWglaSQcdILCGGyBRpylTlCwO6l7ScnHMZoMkrYm4BHhFGQIErfFQLykRREOEEzk2YCgfWyIsqqrPgwZZk3rZdJTv/Ew6UCJac3RsUwIHsri0XwAbZFTUSrygisrAiVWQURRv75f+U/tXkiAA7zMtt3d8fzLM9DgXunFhRss1YJmhqMEiIOPIow2ZCezMkCKOd9qCFjZ5yRoyjgve5EaqX1K00vp0JfJ4woy4A4ALYYaAD6G9yzq262NPNu6ayC1mDCCTnkwCrdPuw3ZhVttMT+jrESCwYIMakOhuXsZbcQFcvdiYjAErKInYCjhDJwWJDjOdPY+H5ztgBRPcXlsjPbu6MdKltXqNZ401cOu9AAIo1w3xxzYyTVyqDC3uTsNHKrVvxHnPDRCObE0lE4Q1KmA2pweqdsrDhjiiU8aUOwnVfMZZ30r4OYy+paFDHBOmr4ahYVSVFpzVxj/ryQjurXtVt0qSIMZL2e+4lLrbQyKnWa6Fpd8Ok0hmiStf6LAA2FeWWTUMYcPteULt2K2L9nptC+12B34TmDn+1sWHgTKRho8DfdRPE44WuTwFYx+mKPaxvbuPQKn7QKVt02FSfhu7fePdMAXzrc7eijS7/oc5zfTtprvCzCndzm8W1VSmuzPjbw4z/jCRdfYP3w/+rJP1h4+TBFY0RXWIijulfZB/BAzfKHAs2J+4bt7hUR7+A8Auhp6BX3riAAAAAElFTkSuQmCC",
        "claude": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEXnbFX/mWafPz+RSCS/f3//AP/MZjP/qqoAAADZd1fkfFvYdlXceFjZdlb/f3/ad1fad1f/AADRdFLpgF3deVisVlW+fz7//wDhelrhe1r/qlX/VVXOa07/////fz/ie1q2bUh/fwB/f3/wg2Die1rjfVl/AADgeViqqlXPZ2f/fwB/Pz+ZZjO0d1KqVSrKbVKRK63LAAAAMHRSTlMHBQgHBAEFAwD8+y7RbgJNjwEU/64EBAGv0gMDEwEEkQkCAv9TNgJzAwUCBAUJBiVNg4XGAAADyElEQVR42nVWiXajOgxl3jbCG2DA7EmaJl2nM///d+9KNmRp69PTmERXu67IaDsPVCpVtksVHzvymha6P9l2a6lQef5oaZRHR3pQBb79FkC/DAC5OXQR8NTUea7p+C2gemgYAK2T+KfxsALcOLpPgEBlzYCG3OqgMr+Se6zwHpB0slYIjALoRWwkvd/rCEuAqhKlVkUTiHTHD6qEXfwVSj0av3QboBOrlXuVsHNdueigsvgMpPnbWsCrhcOBIS+SWNbbInAGFOTaKM/gMQEcrA97Nt1Ss5pw1OPqAfSDSqEll5yoqJuZgqskbpj4SU9wz7x30yG6CY/eaAOI1ICyItQ6mqCD4fB/xFzj+o+r1ix1H6ZOXtJuNtEEzfxFFxOXK+XXtsq4AOfopupnSqnV7BxiLqL/SiMjl8J1dNhHxKApY5/hDIt6r9YMhZteQhEK+Unhp5hajQ+TkgZ4uGu+aiLdrG7xpS6hoUkBD76LPVt11dZLKMqzGKkNR6FMjDYF0FLnQuBmmrbmOyK9fTQiYmaTt+SnKPPbz9cDNHKKNr2bvJGh89qWvckHm7WuDWEXJueO0xbJNaA4nG054FJzbCa7mb/lCyM9Jy+VA1nMbN+UpbVFobWfD+8w3tyZiP+h3/RWV1leKzkxUtMA/CkM/NiXhfZSB65YhNQ4j3zu5M3enkV2yV5bZGkuisJaW5Zl3/T4M+ZGvDzNzBDz36l02fETtxX3Lhk+A8d64tboXDuF3S6EsZ1+EAjiThiuxjZjrxt/ndYJY8P9cZ1X8+dsUbA11+qqDhhjOg1ot7q/9BF3HjKdQKxrA0wszm2nnv8M1600xOk/aK738+oS1KMrZHQ0GXVpViXd6oM0VPDrPLSpuXmAeGqUxihYmR1YxagGqo4B3Tl1WeTZ2HSsXijSMiu1JdOxHtRGYsyoDHiLA6oU0swkxeyKyW49dDyWf/URcWHvij7EVXBGaD03sgfJKOOFpOAPGELtyXUbYHk1NfMY7YIEgJsG/mkUBmGgIC4ksJA/nWdyyw5rMa8tzTwVPb0KiTKrwWW1bx+qm4UyySJAAG4Msk9pHIUoxSI6ZC/sGgHdCOY8RoUeNPVkWPGua73hTHlHv/f18H67srplNhLASxWJFVvoZXVqB7cKkOrtjitTjYTP446eItfO9PBpi8a1yWoBsQLlNTbK9uaNOLafAamiE9uKy1TWjcL93y8WO2lRist/RtZVlV45Tv7rV4fISyLCffqRVvlyWer3AJfeRPCaodTQdquWqfvWQuJl1Alj80Zfnf8Bw/pvVRtDJOwAAAAASUVORK5CYII=",
        "copilot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAADgX5z5k2Hvb2INX9ZosW0ystM6rayUuE1FrozUxB+0vDX3cW7IXMsmiqPXkUjMti67WcnsbVUFVqR0bwXUUzwLVrEEqKsNcXEAAP9dol+xVF+cw1MTYLn///8Aqv8A//+mXi+urBj/AADba2LSWaEMXdBrGGNsW8RVqqqopyG6xDjni03//wDcxx0Af/+nWYlWAAAAMHRSTlMA/fz8+/79/f3+/fwI/lEn+vqcEgnxagcKAQ8a/uIBAwEcGQFpXKMQ2ANf9aEBaAJoF3mEAAACLElEQVR42pWWjXKqMBBGFwIVISJVtCDoLWj1Vq2+/9t1NwTyQ7jjPeOMo34nm82CCqB4fvT8ETyL9Rqm+Xa//Swn8p9QfKQ62zTF9fFRTqyfvtns90EQnN2GKx90nKEsX8q/7aXhWL+AYkY480GwdjQM85mtKGELT7tAOlPI/GzIB+dyPVVAc3SBEho7SOfIzETtCJv4LHThgAXmI0XLB2J++hHNB9yCeU47LBCGtrMPpg2AUGA42Oq2A/4SIneBIw19Fw4oZSvX+oLFwPs7NbzrCxhOCoe1uBkWC8/DpGTRrVKHoe1A0d0enkRWoBo/ENVRZBnQj8rTIEWUiDp0Q5wdDcizEEIdRbZDcbxvLp5LuCphcHbyiMbCF0BiCOTUXZyPd+R5KNxuSZKYimjh6MqjkCckmI4oUEHlEC5wTRRdvKazph2dHALAI86yzFDq/qpfOfIXEmLLaSGnC40zVwEUJL1zk2d0PDGBfUgQKyPTBdwRY7ZTAeSxTpbEidgR8IqZdDs66CViaie+Ypjj0E4+s/FWGM/hqiv4SsIcQkXjRxp4PCDzsYlsJdkw5o8NTvMXU6LJ3n1B99GG+b7+etiRIG/bFp/u2sdK0CSO14uiAa4Lvg32ZH2HcyrhLCA5yZZfFprD0RJACS8UwIks/ylUfPzbtfKnd8Sdv77+ZAGA5TjOZQlHgbsrT0Onm2Czcaw/wQ80TZO3S1ga5NN/UZb/9TZxzCHPuYle4BfyLzaFFrW5BgAAAABJRU5ErkJggg==",
        "deepseek": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAABXh/1Vhf5/f/9Whf4AAP9Whf5Whf1Whv0+fv9VhP1Vqv9VVf9TiP9Ufv9dkP8A//////9nl/9glf9Mkf8Af/8/v/9Tf/tmZv8zZsxVVapIbf9Vf9RVqqpiif9///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC1qlwpAAAAMHRSTlMA/DACjgFur88ETwMDEg7/AQEF/ggCBCMFBQMHBgMNAgAAAAAAAAAAAAAAAAAAAACJtpLGAAACQ0lEQVR42uVWx2LbMAwF96YkjySd+f+/LLhEUrbVnFucTBHjASAeDPAfiHBfUGLGiZX91RVz5uPDOGbW/nGDIG8vnA4HKrlSFjCGAXm1a+xqrHnH39RKFEulIoQsmqZLwfRV4Z0oar7ZoVOuk9pCmsT0VcBv/KlosjQbWlmV9B1ETo5iHLpbIeQDjxlxkIRk/+96eTDgAB4jFIMrRwgqQdUAd6DkmSAQJ8Smy0mS4lPBxoImz4WCMXAAazEuX14Y4G08hNcXEJS8Fgs/QC5TUABFTi3iCMrCJ5wFyC4j2Fa499QbeW6ATotPZUMqdEbEaYjByhfFUpRX9OUh6ZJJajidSsjllB11dTBSVPYmVp+aT9VUkDG/COtuIMGUJ+vHlLSmg4Vq+pCfzf5sXdehmvtuz8F0Az3Mjhm8Shb2Lllos60z3D7A37pFevv1oG8gqgLvSbQYdsdB26B01BmlvtzFMN5PmjlgCDPCzERMPUzTQDp5jkKjgwSVPTwwKgYDO1cN3Irh5CHAAGDzuoC6lADIQQ7pcQSF8Qdu8zW+hbfMW8gQwLwIU8a/Rs5rM4pMh/Rnl1TlaTRlDd5kdRdVL+DObgmgCnDbu6Ed9CY0wtWNWKCMML47P/QvHIkYYh0exdtISFSi+0jxKMRsEWpVOrlqLm2yTh+uJIA4xHg221dNYyJ+xelBH/MQ07RVIOZsAflE+RVCzhvdwvfVGJEe19MdtGH5cfckwbXyc18jJ7twKrdjX1ifKzPGe29wNYp/+K/EHwZNEla8Os9fAAAAAElFTkSuQmCC",
        "gemini": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEVmW9ddbt4cWJ9oYMwZc99eUa2FY99uat8nar0xcswwd9RRPI5/f3+qqv//AP8dHToeMGoXUHISl+xFgvCRbdoAAABOduNpceh2beg7e+Eze900gecAAP+Jaux/f/+Fcvb///8A//8zd9ZVqv9UVKtxZ92KauiqVf8wZbc/f78medcndc1TbNYAf38/P78/f/8YcJZnAAAAMHRSTlMipxxhGSee1mNp0QwCAwEICwsM/wcA/v78/Pn9AfcC/wEBkAMJixYDLwQXr20CBARdwiQkAAAB/klEQVR42rWW2XbqMAxFnREKbaHtVTxnDlOg/P/fVU7a0JIYzMPVA84KZ1uyLMshMGWvEMf4M2Vk6qWCpdZLHFyBHDZab3D4b8AzRFpHOLgCnxBoHeDgCrxAnGUeDq4AkJnWs3/Oaa0V0YwxompHYAtexhht8MEJCCHC+RlltUqdgC00WUc0U/+OX6VAWGeUEkjvA2q7NitAOaPeiqi7QNoHRDs7jl2QkT6gg94Q+5sApiVgF32SJAGcbwC1Qj39rU+SI+S1BXjFfWroxUHSmwewP40BlWKpES8b6ZHYAVShGgCV589bk4yoYRn7G88vBKrqVBQKyPexWpFePqVPPngZ+r2uILDcbKIgnumM2fSJ4JIvyrl/OPhAYm0s08yu51wIIaUUUoj2B8hu6f8AGBIxIVFTPLb5h5DWw6IBF23TcynK8G1Y9JDWupnSYzC8NCmq3vu0DlWHGxd5Yz2X7dXGXUoD+9CRjvQllkZhK74cjld6/mQvPmNnCK7159sHaH/xYeJ5unOAOh/ekE85mn+qCRAkZr2+XVXKpc3svveL71zaDOYcyg9hHJT46AKowu/qR/hKuTVjdIF1Oe3A0u5DU0I75TtfKPuFlIvQ/Z42MVkisl2KcynnD1yKJ/CF8OHkDBRwkPIAxQPAuxDhA4CCNyHWD3ycoLRtp/XwBftmxlqmTjDYAAAAAElFTkSuQmCC",
        "grok": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADDIYgjAAAAMHRSTlMB/CrSinKvUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6SXQAAAABN0lEQVR42rWVSZLDMAhFxXz/GyfulmUbPklpEZaqBxJfDGP81NhjjxeyLZ7IN+MT78WnLoNQdXdVSzx+UDhd5nbjCeJCyS4eKaQZJ1m8AL6El1g8uIAF4pOnz/H9rZONO18lWuqIcdLzMM28nbzhdxaHk+cmL20E7fjiMI+j1S05BJLiobPDFzHgXdA/SI0y+YDBRlX0nxdePxGj/g7nO7WJBspFbkGBTMXh4J3HNwe+85YSVJB0XLxEjmbAQRfvtSwZ1LacvIG6h8Vtf7wwyM9x8R0ODhsxcL9JO0i6htPm3DqHwI3e3vzUzgQ37kptyhOuZqa3IVuHWFz31vFaJ8YstgZHvJ7HVnG0RmyFiYI7Y36lpY83wT0b6dqY+ojiJRsftl2zHWVnm5Zq/ma6t93fL7LxW3sB4KIF5XfjW5QAAAAASUVORK5CYII=",
        "meta-ai": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAAAPY+Alj+8IN8gLGHAJL7YFdPoAB/8PXasKIqEWYtQMLKQaZdRKrvUPLaMA//9TqeBUqfxsxvhVqNYLqv9ode96//+Q0fY2keMJL8YxjdZUYJ0OI3UFdH9sHQ5ra3uX0uj///8NOcIUUrRqAGpBeMp0yuyqqv//AAANQ70NQb4AqqpxVThVqqpkpr2q//9p543oAAAAMHRSTlMA+/f3DO0FAQsWoJhn9GABnQf0WQMKAu+ep2MNUgMFBagBZFECSaIDAbzSAwkDQgNKezivAAACsUlEQVR42u1W2ZabMAyVF4yNAUMICVknmU5npvv//11lyzYkTc9p30cPwci60pUsmQB8SPk/xj9+XfF30984eHsDuPb9A0f9o+WjVZQNwM/LZbu9vA5n/xKVcnhdNd20/551eWtYbbfblZdmAHhCnbvCgKqmaTjnA7gFrdLbr3iSpgM4gAPotrNyeHdu4b9DLyyKRxwQgfYNTyrOu/fMSsMQzAsvIiI23p4xsbO7XdDxLmV+gt7bi6KwbWs9gnlW3YozIdozWphdQAwhNXDuKdiLwvhXaSOiadC9hFIpBfAc4h7ciBZr2Hs+opBgUABaQqByh86DkzVURAoBrtQUwIAMmwospclQZWIZlQwqjYg+BmjnzYTIKgAFtddNaO5igLnvkFogxfdIN4lDUigalxTgefaGq4qKr51KujWFqHFZBYBxcu6zz0wwYjAuwnpVBfASDnMH2ZdTo6cYQtQzwp1DWAkynH1b6jm/yh86kZJjeZM2+0QPFmuK8g0J+VO0jDivc/8EyzoCcgKlOviURCuJlEp5Ry4VAapc1D5USFg88Ji3ytNOlhU9VGI6hjYxoKW4I/WyANQxQqnOjAJoHUPwk4p7ZHoLoFL4PpRAHeJD6ATg94ADaEZ9hTan0tC0qcTXA24oOTdSo4Msg8tISvppRg3niyphZqd18IElpUPBnqbjw90S9Kj5XFbsQo1xax4zTiUzqVJKxTmrgarH0FxPcfJUmU+3pTT2+DKEKwR72lKjdVNDV4GZ+xBJWUJM09Q0IQXsfroneJhiIRZjFpq6yBcTD72H2VtqTUY9dHvja5CFYFm+4MQTQpB5ceOfEMfZ31eDl5iX1t94eJEV7Z9fFIxh47aVeQjk0VrbHiErFqLi9lHO2xruF0uRiaVauJMaRf7tYyYN7hr58Rfgn+U3dEQerQyCKkcAAAAASUVORK5CYII=",
        "mistral": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAAD6Ug//fwD7UxD5UQ79Tgz4UQ7/AAD5UQ3/PgD3UQ2/PwD/VQD5UQ7/TAnfPwDaSAD/SCT/bSQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABS6mZ2AAAAMHRSTlMA/QItsypnAY8ERwQDyRoIBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABMC3zzAAAA3klEQVR42u2W4RKCIAyAl6CDAq3e/2HDDdKdO8X6k17f8cO5+0SQgQDnoSFQSyHnvno8wrMdMb2W7Q0lH/P3AXMhLODyYZZzBppjCMGHRM4047UP6z0orAnxSpjxzRAMR3FFyDi4QWpO3Dya4Aef2p4eiHrBdoStFlT+wnu1ivnMsxu366HjqNuuB+uJInC0WdN+6sFXbQI1AhYBlwIWAefb63zQOAkoBp3ngIhlnRKOq99xlFORI9C+kVoPGV0I95DaDkGr6R8W2iXp5KK9NZ9Vkk/PWwmK81Zyhn+MFxLSDLUqWmfBAAAAAElFTkSuQmCC",
        "perplexity": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAAAeuM0A//8dt8wgw9oet8wdt8sgvdMatsweuM0izeUet80zmcwetssAqv8Af38Af/8Cvb4tydEAqqocxs8it84gt80Af78Av/8ktrYercoqqqoqqtQersUguM4AAP8AmZkfwNYgvdMn19cj0OcAmf8AzP8gus8gu9AAAAAAAAAAAAAAAAAAAAAAAAAAAABiX1MhAAAAMHRSTlMA+QEw/rV1/RDP/4YFTgMCAgUIAw4STgQEBxAGBiZ5AQXxLwb/BQWG1gAAAAAAAAB/v0TpAAACsUlEQVR42n2W57qkIAyGA9IUG5Yz7dQ92+7/CjcBURxx82OeEb/XSMkXAXxwMBZ4Fy6gg0LKGeIl8BGaAjVJcJiYBejjVSHEpkBQsQNgmJDjMogAYz+iYoTRihyAhMG7EYiKDpwULAswUc7QPgEOilLoDDAxJpEo4LIDHDRMMJsFRNMsxArwHqcrdGOyr6Qb/7QCrhHARbOanlHkgRcS4vPgNSh+wySFkHcYzwCY4a0UrIGeFCOYUgh7g1+nGaC9eEIFBS4Pe8fd7A8AxyDg44qrgo/VihSNpmSug5bTJW93KeBOGTjlwn3SkuFS0nTDYfEZtnCP4bumVarNMNTz9S417pTW5RvgwDDMNQH198MtgCwpGCvXYD7KdIB+5QLgWlRV5X+WCMB27W8KUa6AVFapdxXDBsCqJKySImaQP9Vu/rDMQe5H36sVqGy9xs3d8TRLfxTl3d22OzYFoF6ry8hlH5SmAol1WkMWWPRh4QPR/w/wejwZHQHdjsgCUT+EDAMVQyRyQL/oeayHNiEyQNS3ScVtxBHY9ElNbzkOAN/0qQlEgj8Dr1SO9P7PvhSICQUpoODzsen3RhbmgUd7D5BVKrjCEcAiRKc0sH8l56hEuzYHtF2jmXEuAei0cvKlCIQijgAggP9VJZN6UGoDOo7+hfV/TQAUbPWANiGEWAEOHb40Ee3HCqBArxUnv3yBLYDfEF9ACnoeAYqvmGGayRq8kVH7MMFm0DT/+O7TwotmXjKlBbgAfDWyBn3VfuKAzzDsfDI6H1ll8Tda5Y2ceIbRA5MXHbz1RvYdzRi4RWcxOEjA3otXu2+8Ptg9NtvQHfgZcGgoIx0jfMAJkGtZIWUjskCuKTo/KVzkLJBru5el65ockG3sfmPywMmnwwizFFng7OOEelIOOP/8oXa9Av8A4/omRQSG324AAAAASUVORK5CYII=",
        "poe": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAAAkFBMVEUAAABcW91iYetcW9x/f/8/P79bWuAAAP9bWtxeXeFYWNlVVfdcW91mZs5cW91cW91VVapcWtx/f3////9gX+VmZu4AAH9eXeNeXOFdXOFcXOAzM8w/P/9dXOFmVeVISLZmM/9gV9tgWt1mZplgYOUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJUkPOAAAAMHRSTlMA/P5oAgQqAS78EAawBozNA0wCAf0MAo/VUmcFBKcPBwUdLQUyAAAAAAAAAAAAAACGby6jAAACAElEQVR42tVVyZakIBBMEIsdodWyrN5m+/9vnGSxn1Wivr7NxAkhA5LIMAH4h8F1uwvNt/HseLvNMgc1N3u4z5/wdMYLiBvdx3AT0D8Q+rGj5AC00/1jhoKc4ALXFUHz+SReBq5XhB/Q0GMCbeB10Ye9MVAdHY7iB7wE+LeWF4GVoV0Ql12I0FGjSz1UMxlSPvehDSXG3RUU/ckHKIbQLYBlX7AArY4DBRbTorQTkPSnBnSuN4xqvbEaIdeYgSmBRQNusz/eyc31PMXwnrkbef+Zamy5yzouhHR5/tFRKanLSnBw8SvX2C7CrwkaQpyUZIxp4HE4REVDTJfVCO0yOaIZox8TAdfaY4IkKhPUimAPCWJ7gj1MSUVnXkEva3uEazY57dosa5v/kV+RXiXggsNqygA+uQFCLK5LlbNwfyBMqXCIeZrE8sfjLaZpzpX+nQsnCbhScc9XDeF5ANwXazh09kAwDYGewwbElB1X/UmPVqXpVxASLToY9BaI0Jhow0OgqU0T/sTD0rkowdTs96XGRV2WLJm3PWZ4AgOM+a/+Z/l5E+jX3dKf9yXx0F5PG1kxZIUgq9Hxp7rWWqWU9f2l0z2vEKQMotqd1Pa5uBQP7sDzGgETbVkVvHoCNar2lu28YBcyPCl3/IIiAQ3rv/HmomfPHtINXr4X7j38r/gLONgYIs/lpzoAAAAASUVORK5CYII=",
    },
}

TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}</title>
<style>
:root{
  color-scheme:light;
  --page:#f6f6f3;--surface:#ffffff;--surface-2:#fafaf8;--line:rgba(11,11,11,.09);--grid:#e8e7e1;--axis:#c3c2b7;
  --ink:#0b0b0b;--ink-2:#52514e;--ink-3:#898781;
  --accent:#2a78d6;--accent-soft:#e8f1fc;
  --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4;--s6:#008300;--s7:#4a3aa7;--s8:#898781;
  --good:#0ca30c;--good-ink:#006300;--good-bg:#e7f6e7;
  --warn:#fab219;--warn-ink:#8a5a00;--warn-bg:#fff4dc;
  --bad:#d03b3b;--bad-ink:#b02727;--bad-bg:#fbe9e9;
  --info-bg:#eaf2fc;--info-ink:#1c5cab;
  --tile:#ffffff;--shadow:0 1px 2px rgba(0,0,0,.04),0 1px 0 rgba(0,0,0,.02);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --page:#0d0d0d;--surface:#1a1a19;--surface-2:#202020;--line:rgba(255,255,255,.10);--grid:#2c2c2a;--axis:#383835;
    --ink:#ffffff;--ink-2:#c3c2b7;--ink-3:#898781;
    --accent:#3987e5;--accent-soft:#1d2a3b;
    --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s7:#9085e9;--s8:#6f6d68;
    --good-ink:#3fc63f;--good-bg:#132a13;--warn-ink:#f5c04d;--warn-bg:#2e2410;--bad-ink:#f07a7a;--bad-bg:#331616;
    --info-bg:#16243a;--info-ink:#86b6ef;--tile:#f4f4f2;--shadow:none;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --page:#0d0d0d;--surface:#1a1a19;--surface-2:#202020;--line:rgba(255,255,255,.10);--grid:#2c2c2a;--axis:#383835;
  --ink:#ffffff;--ink-2:#c3c2b7;--ink-3:#898781;
  --accent:#3987e5;--accent-soft:#1d2a3b;
  --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s7:#9085e9;--s8:#6f6d68;
  --good-ink:#3fc63f;--good-bg:#132a13;--warn-ink:#f5c04d;--warn-bg:#2e2410;--bad-ink:#f07a7a;--bad-bg:#331616;
  --info-bg:#16243a;--info-ink:#86b6ef;--tile:#f4f4f2;--shadow:none;
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--page);color:var(--ink);font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:20px 16px 48px}
a{color:var(--accent)}
/* header */
header.top{display:flex;gap:16px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;margin-bottom:14px}
header h1{font-size:22px;margin:0 0 2px;letter-spacing:-.01em}
header .site{font-size:14px;color:var(--ink-2);word-break:break-all}
.meta{display:flex;flex-wrap:wrap;gap:6px 8px;margin-top:10px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;background:var(--surface);border:1px solid var(--line);font-size:12px;color:var(--ink-2);white-space:nowrap}
.chip b{color:var(--ink);font-weight:600}
.srcs{display:flex;gap:8px;align-items:center}
.logo{flex:none;display:inline-grid;place-items:center;border-radius:8px;background:var(--tile);border:1px solid var(--line);overflow:hidden}
.logo img{width:72%;height:72%;object-fit:contain;display:block}
.logo.letter{border:none;color:#fff;font-weight:700}
/* tabs */
nav.tabs{position:sticky;top:0;z-index:5;display:flex;gap:4px;overflow-x:auto;padding:6px;margin:0 0 18px;background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
.tab{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border:0;border-radius:8px;background:transparent;color:var(--ink-2);font:inherit;font-weight:600;cursor:pointer;white-space:nowrap}
.tab:hover{background:var(--surface-2);color:var(--ink)}
.tab[aria-selected="true"]{background:var(--accent-soft);color:var(--ink)}
.tab .logo{width:22px;height:22px;border-radius:6px}
.panel{display:none}.panel.on{display:block}
/* layout */
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.kpis{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin-bottom:14px}
@media(max-width:860px){.g2,.g3{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:var(--shadow);min-width:0}
.card h2{font-size:15px;margin:0 0 2px;display:flex;align-items:center;gap:8px}
.card .sub{color:var(--ink-3);font-size:12px;margin:0 0 12px}
.section-title{display:flex;align-items:center;gap:10px;margin:26px 0 12px}
.section-title h2{font-size:18px;margin:0}
.section-title .sub{color:var(--ink-3);font-size:13px}
/* KPI tile */
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow);min-width:0}
.kpi .lbl{font-size:12px;color:var(--ink-2);display:flex;align-items:center;gap:6px}
.kpi .val{font-size:24px;font-weight:650;letter-spacing:-.02em;margin:4px 0 4px}
.kpi .row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--ink-3)}
.kpi .hint{font-size:11px;color:var(--ink-3);margin-top:4px}
.delta{white-space:nowrap;display:inline-flex;align-items:center;gap:3px;padding:1px 7px;border-radius:999px;font-weight:600;font-size:12px;font-variant-numeric:tabular-nums}
.delta.up{background:var(--good-bg);color:var(--good-ink)}
.delta.down{background:var(--bad-bg);color:var(--bad-ink)}
.delta.flat{background:var(--surface-2);color:var(--ink-3)}
/* overview source cards */
.src-card .head{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.src-card .head h2{margin:0}
.src-card .mini{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 14px}
.mini .l{font-size:12px;color:var(--ink-2)}.mini .v{font-size:19px;font-weight:650;letter-spacing:-.01em}
.mini .d{margin-left:6px}
.go{margin-top:12px;font-size:12px;background:none;border:0;padding:0;color:var(--accent);cursor:pointer;font:inherit;font-weight:600}
.hl{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.hl li{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:10px;background:var(--surface-2);border:1px solid var(--line)}
.hl .ic{flex:none;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700}
.ic.good{background:var(--good-bg);color:var(--good-ink)}.ic.bad{background:var(--bad-bg);color:var(--bad-ink)}
.ic.warn{background:var(--warn-bg);color:var(--warn-ink)}.ic.info{background:var(--info-bg);color:var(--info-ink)}
/* tables */
.tbl-wrap{overflow-x:auto;margin:0 -4px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:8px 6px;border-bottom:1px solid var(--grid);text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-3);font-weight:600}
th:first-child,td:first-child{text-align:left}
td.k{max-width:380px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
tr:last-child td{border-bottom:0}
.barcell{position:relative}
.barcell i{position:absolute;left:0;top:50%;height:16px;transform:translateY(-50%);background:var(--accent-soft);border-radius:0 4px 4px 0;z-index:0}
.barcell span{position:relative;z-index:1}
.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:600}
.pill.good{background:var(--good-bg);color:var(--good-ink)}.pill.warn{background:var(--warn-bg);color:var(--warn-ink)}.pill.bad{background:var(--bad-bg);color:var(--bad-ink)}
.empty{padding:22px;text-align:center;color:var(--ink-3);font-size:13px;border:1px dashed var(--line);border-radius:10px}
/* bar list */
.bars{display:grid;gap:9px}
.bar .t{display:flex;justify-content:space-between;gap:10px;font-size:13px;margin-bottom:3px}
.bar .t span:last-child{color:var(--ink-2);font-variant-numeric:tabular-nums}
.bar .track{height:10px;border-radius:5px;background:var(--surface-2);overflow:hidden}
.bar .fill{height:100%;border-radius:0 4px 4px 0;background:var(--s1)}
/* charts */
.chart{position:relative}
.chart svg{display:block;width:100%;height:auto;overflow:visible}
.chart text{fill:var(--ink-3);font-size:10.5px}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--ink-2);margin:0 0 8px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
.tip{position:absolute;pointer-events:none;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:7px 9px;font-size:12px;box-shadow:0 4px 14px rgba(0,0,0,.12);white-space:nowrap;display:none;z-index:4}
.tip b{display:block;margin-bottom:2px}
.tip .r{display:flex;align-items:center;gap:6px;justify-content:space-between}
.tip .r i{width:8px;height:8px;border-radius:2px;display:inline-block}
/* AI */
.ai-strip{display:flex;flex-wrap:wrap;gap:8px}
.ai-chip{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line);font-size:12px}
.ai-chip b{font-variant-numeric:tabular-nums}
.plat{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.pcard{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--surface)}
.pcard .top{display:flex;gap:10px;align-items:center;margin-bottom:10px}
.pcard .nm{font-weight:650;font-size:15px}.pcard .sr{font-size:11px;color:var(--ink-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:170px}
.pcard .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;font-size:12px;color:var(--ink-2)}
.pcard .stats b{display:block;font-size:16px;color:var(--ink);font-variant-numeric:tabular-nums}
.pcard .share{height:6px;border-radius:3px;background:var(--surface-2);margin:10px 0 8px;overflow:hidden}
.pcard .share i{display:block;height:100%}
.pcard ol{margin:6px 0 0;padding-left:18px;font-size:12px;color:var(--ink-2)}
.pcard ol li{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lg{display:inline-flex;gap:3px;align-items:center}
/* PSI */
.seg{display:inline-flex;border:1px solid var(--line);border-radius:9px;padding:3px;background:var(--surface-2)}
.seg button{border:0;background:transparent;padding:5px 12px;border-radius:7px;font:inherit;font-size:12px;font-weight:600;color:var(--ink-2);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--surface);color:var(--ink);box-shadow:var(--shadow)}
.vitals{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.vital{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--surface)}
.vital .n{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--ink-2)}
.vital .v{font-size:24px;font-weight:650;margin:4px 0 8px;letter-spacing:-.02em}
.meter{position:relative;height:8px;border-radius:4px;display:flex;gap:2px}
.meter span{height:100%;border-radius:2px}
.meter .m{position:absolute;top:-4px;width:3px;height:16px;border-radius:2px;background:var(--ink);box-shadow:0 0 0 2px var(--surface)}
.vital .th{display:flex;justify-content:space-between;font-size:10.5px;color:var(--ink-3);margin-top:6px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font-weight:650;font-size:13px}
.badge.good{background:var(--good-bg);color:var(--good-ink)}.badge.bad{background:var(--bad-bg);color:var(--bad-ink)}.badge.warn{background:var(--warn-bg);color:var(--warn-ink)}
.rings{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center}
@media(max-width:520px){.rings{grid-template-columns:repeat(2,1fr)}}
.ring svg{width:84px;height:84px}
.ring .lb{font-size:12px;color:var(--ink-2);margin-top:2px}
/* reviews */
.stars{color:#eda100;letter-spacing:1px}
.rv{display:grid;gap:10px}
.rv .it{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--surface-2);font-size:13px}
.rv .it .m{display:flex;justify-content:space-between;font-size:12px;color:var(--ink-3);margin-bottom:4px}
.big{font-size:40px;font-weight:700;letter-spacing:-.03em;line-height:1}
footer{margin-top:28px;font-size:12px;color:var(--ink-3);line-height:1.6}
footer p{margin:4px 0}
.note{font-size:12px;color:var(--ink-3);margin-top:8px}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<div class="tip" id="tip"></div>
<script id="report-data" type="application/json">{{REPORT_DATA_JSON}}</script>
<script id="logo-data" type="application/json">{{LOGOS_JSON}}</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('report-data').textContent);
const LG=JSON.parse(document.getElementById('logo-data').textContent);
const M=D.meta||{},W=D.windows||{};
const AI_COLOR={chatgpt:'--s1',gemini:'--s2',perplexity:'--s3',claude:'--s4',copilot:'--s5','meta-ai':'--s6',grok:'--s7',other:'--s8'};
const AI_LETTER={you:['Y','#7c3aed']};
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const n0=v=>v==null||isNaN(v)?'–':Math.round(v).toLocaleString('en-US');
const cmp=v=>{if(v==null||isNaN(v))return'–';const a=Math.abs(v);return a>=1e6?(v/1e6).toFixed(a>=1e7?1:2)+'M':a>=1e4?(v/1e3).toFixed(a>=1e5?0:1)+'K':n0(v)};
const pc=(v,d=1)=>v==null||isNaN(v)?'–':(v*100).toFixed(d)+'%';
const p1=v=>v==null||isNaN(v)||!v?'–':v.toFixed(1);
const dur=s=>{if(!s&&s!==0)return'–';s=Math.round(s);const m=Math.floor(s/60);return m?`${m}m ${String(s%60).padStart(2,'0')}s`:`${s}s`};
const sec=v=>v==null?'–':(v<1?Math.round(v*1000)+' ms':v.toFixed(2)+' s');
const fd=d=>{if(!d)return'';const x=new Date(d+'T00:00:00');return isNaN(x)?d:x.toLocaleDateString('en-US',{month:'short',day:'numeric'})};
const fdy=d=>{if(!d)return'';const x=new Date(d+'T00:00:00');return isNaN(x)?d:x.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})};
const path=u=>{try{const x=new URL(u);return x.pathname+(x.search||'')}catch(e){return u}};
const el=(h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstElementChild};

function logo(key,size=28,group='platforms',name){
  const src=(LG[group]||{})[key];
  if(src)return `<span class="logo" style="width:${size}px;height:${size}px" title="${esc(name||key)}"><img src="${src}" alt="${esc(name||key)}"></span>`;
  const L=AI_LETTER[key]||[(name||key||'?')[0].toUpperCase(),'#6f6d68'];
  return `<span class="logo letter" style="width:${size}px;height:${size}px;background:${L[1]};font-size:${size*.45}px" title="${esc(name||key)}">${esc(L[0])}</span>`;
}
const ailogo=(id,s,name)=>logo(id,s,'ai',name);
function delta(c,p,lowerBetter=false,mode='pct'){
  if(p==null||c==null||(mode==='pct'&&!p))return '<span class="delta flat">new</span>';
  let d=mode==='pct'?(c-p)/Math.abs(p):(c-p);
  if(Math.abs(d)<(mode==='pct'?0.0005:mode==='pp'?0.00005:0.05))return '<span class="delta flat">±0</span>';
  const good=lowerBetter?d<0:d>0;
  const txt=mode==='pct'?(Math.abs(d)*100).toFixed(1)+'%':mode==='pp'?(Math.abs(d)*100).toFixed(Math.abs(d)<0.001?2:1)+' pp':Math.abs(d).toFixed(1);
  return `<span class="delta ${good?'up':'down'}" title="vs previous period">${d>0?'▲':'▼'} ${txt}</span>`;
}
function kpi(lbl,cur,prev,fmt,opt={}){
  return `<div class="kpi"><div class="lbl">${opt.icon||''}${esc(lbl)}</div><div class="val">${fmt(cur)}</div>
  <div class="row">${opt.nodelta?'':delta(cur,prev,opt.lower,opt.mode||'pct')}${opt.nodelta?'':`<span>prev ${fmt(prev)}</span>`}</div>${opt.hint?`<div class="hint">${esc(opt.hint)}</div>`:''}</div>`;
}
function table(cols,rows,opt={}){
  if(!rows||!rows.length)return `<div class="empty">${esc(opt.empty||'No data for this period.')}</div>`;
  const mx={};cols.forEach(c=>{if(c.bar)mx[c.k]=Math.max(...rows.map(r=>+r[c.k]||0),1)});
  return `<div class="tbl-wrap"><table><thead><tr>${cols.map(c=>`<th>${esc(c.h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${cols.map((c,i)=>{
    const raw=r[c.k];const v=c.f?c.f(raw,r):esc(raw);
    if(c.bar)return `<td class="barcell"><i style="width:${(raw/mx[c.k]*70).toFixed(1)}%"></i><span>${v}</span></td>`;
    return `<td class="${i===0?'k':''}" ${i===0?`title="${esc(raw)}"`:''}>${v}</td>`}).join('')}</tr>`).join('')}</tbody></table></div>`;
}
function bars(items,fmt,colorVar='--s1'){
  if(!items.length)return '<div class="empty">No data for this period.</div>';
  const mx=Math.max(...items.map(i=>i.v),1);
  return `<div class="bars">${items.map(i=>`<div class="bar"><div class="t"><span>${i.label}</span><span>${fmt(i.v)}${i.extra?` · ${i.extra}`:''}</span></div><div class="track"><div class="fill" style="width:${(i.v/mx*100).toFixed(1)}%;background:var(${i.color||colorVar})"></div></div></div>`).join('')}</div>`;
}
const tip=document.getElementById('tip');
function showTip(host,html,x,y){tip.innerHTML=html;tip.style.display='block';const r=host.getBoundingClientRect();const tw=tip.offsetWidth;let left=r.left+window.scrollX+x+14;if(left+tw>window.scrollX+document.documentElement.clientWidth-8)left=r.left+window.scrollX+x-tw-14;tip.style.left=left+'px';tip.style.top=(r.top+window.scrollY+y-10)+'px'}
function hideTip(){tip.style.display='none'}
function niceStep(v){if(v<=0)return 1;const p=Math.pow(10,Math.floor(Math.log10(v)));const f=v/p;return (f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10)*p}
/* line / stacked column chart, single y axis */
function chart(host,dates,series,opt={}){
  if(!dates.length){host.innerHTML='<div class="empty">No data for this period.</div>';return}
  const Wd=720,H=opt.h||220,pl=44,pr=10,pt=10,pb=24,iw=Wd-pl-pr,ih=H-pt-pb;
  const stacked=opt.type==='stack';
  const tot=dates.map((_,i)=>stacked?series.reduce((a,s)=>a+(s.values[i]||0),0):Math.max(...series.map(s=>s.values[i]||0)));
  const mxv=Math.max(...tot,0)*1.04;let ystep=niceStep(mxv/4)||1;if(ystep<1&&!opt.frac)ystep=1;let ymax=Math.max(ystep,Math.ceil(mxv/ystep)*ystep),ymin=0;
  const nt=Math.round((ymax-ymin)/ystep);
  const y=v=>pt+ih-(v-ymin)/(ymax-ymin)*ih;
  const step=iw/dates.length,x=i=>pl+step*i+step/2;
  let s=`<svg viewBox="0 0 ${Wd} ${H}" role="img" aria-label="${esc(opt.label||'chart')}">`;
  for(let k=0;k<=nt;k++){const v=ymin+ystep*k,yy=y(v);s+=`<line x1="${pl}" x2="${Wd-pr}" y1="${yy}" y2="${yy}" stroke="var(--grid)" stroke-width="1"/><text x="${pl-6}" y="${yy+3.5}" text-anchor="end">${opt.yfmt?opt.yfmt(v):cmp(v)}</text>`}
  const every=Math.ceil(dates.length/7);
  dates.forEach((d,i)=>{if(i%every===0)s+=`<text x="${x(i)}" y="${H-6}" text-anchor="middle">${fd(d)}</text>`});
  if(stacked){
    const bw=Math.max(2,Math.min(22,step-2));
    dates.forEach((d,i)=>{let acc=0;series.forEach(se=>{const v=se.values[i]||0;if(!v)return;const y1=y(acc+v),y0=y(acc);s+=`<rect x="${x(i)-bw/2}" y="${y1}" width="${bw}" height="${Math.max(0,y0-y1-1)}" rx="2" fill="var(${se.color})"/>`;acc+=v})});
  }else{
    series.forEach(se=>{const pts=se.values.map((v,i)=>`${x(i).toFixed(1)},${y(v||0).toFixed(1)}`).join(' ');
      if(opt.area&&series.length===1)s+=`<polygon points="${x(0)},${y(ymin)} ${pts} ${x(dates.length-1)},${y(ymin)}" fill="var(${se.color})" opacity=".10"/>`;
      s+=`<polyline points="${pts}" fill="none" stroke="var(${se.color})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`});
  }
  s+=`<line class="xh" x1="0" x2="0" y1="${pt}" y2="${pt+ih}" stroke="var(--axis)" stroke-width="1" style="display:none"/>`;
  s+=`<rect class="hit" x="${pl}" y="${pt}" width="${iw}" height="${ih}" fill="transparent"/></svg>`;
  const lg=series.length>1?`<div class="legend">${series.map(se=>`<span><i style="background:var(${se.color})"></i>${se.logo||''}${esc(se.name)}</span>`).join('')}</div>`:'';
  host.innerHTML=lg+`<div class="chart">${s}</div>`;
  const svg=host.querySelector('svg'),xh=svg.querySelector('.xh'),hit=svg.querySelector('.hit');
  hit.addEventListener('mousemove',ev=>{const r=svg.getBoundingClientRect(),sx=(ev.clientX-r.left)*(Wd/r.width);let i=Math.floor((sx-pl)/step);i=Math.max(0,Math.min(dates.length-1,i));
    xh.setAttribute('x1',x(i));xh.setAttribute('x2',x(i));xh.style.display='';
    const f=opt.fmt||n0;const rows=series.map(se=>`<div class="r"><span><i style="background:var(${se.color})"></i> ${esc(se.name)}</span><b style="margin:0 0 0 12px;display:inline">${f(se.values[i]||0)}</b></div>`).join('');
    showTip(host.querySelector('.chart'),`<b>${fdy(dates[i])}</b>${rows}${stacked?`<div class="r"><span>Total</span><b style="display:inline;margin-left:12px">${f(tot[i])}</b></div>`:''}`,(x(i))*(r.width/Wd),ev.clientY-r.top)});
  hit.addEventListener('mouseleave',()=>{xh.style.display='none';hideTip()});
}
function ring(v,label){
  const st=v>=90?'good':v>=50?'warn':'bad',col=st==='good'?'var(--good)':st==='warn'?'var(--warn)':'var(--bad)';
  const R=34,C=2*Math.PI*R,frac=Math.max(0,Math.min(100,v||0))/100;
  return `<div class="ring"><svg viewBox="0 0 84 84" role="img" aria-label="${esc(label)} ${Math.round(v)}"><circle cx="42" cy="42" r="${R}" fill="none" stroke="var(--grid)" stroke-width="7"/><circle cx="42" cy="42" r="${R}" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${C*frac} ${C}" transform="rotate(-90 42 42)"/><text x="42" y="48" text-anchor="middle" style="font-size:20px;font-weight:700;fill:var(--ink)">${v==null?'–':Math.round(v)}</text></svg><div class="lb">${esc(label)}</div></div>`;
}
const VT={lcp:{n:'Largest Contentful Paint',s:'LCP',g:2.5,p:4,f:sec,core:1},inp:{n:'Interaction to Next Paint',s:'INP',g:.2,p:.5,f:sec,core:1},cls:{n:'Cumulative Layout Shift',s:'CLS',g:.1,p:.25,f:v=>v==null?'–':v.toFixed(2),core:1},fcp:{n:'First Contentful Paint',s:'FCP',g:1.8,p:3,f:sec},ttfb:{n:'Time to First Byte',s:'TTFB',g:.8,p:1.8,f:sec}};
const vstat=(k,v)=>v==null?null:v<=VT[k].g?'good':v<=VT[k].p?'warn':'bad';
const SL={good:'Good',warn:'Needs improvement',bad:'Poor'},SI={good:'✓',warn:'!',bad:'✕'};
function vital(k,v){
  const t=VT[k],st=vstat(k,v),max=t.p*1.6,pos=v==null?0:Math.min(v/max,1)*100;
  return `<div class="vital"><div class="n"><span><b style="color:var(--ink)">${t.s}</b> · ${t.n}</span>${st?`<span class="pill ${st}">${SI[st]} ${SL[st]}</span>`:''}</div>
  <div class="v">${v==null?'–':t.f(v)}</div>
  <div class="meter"><span style="width:${t.g/max*100}%;background:var(--good)"></span><span style="width:${(t.p-t.g)/max*100}%;background:var(--warn)"></span><span style="flex:1;background:var(--bad)"></span>${v==null?'':`<i class="m" style="left:calc(${pos}% - 1.5px)"></i>`}</div>
  <div class="th"><span>Good ≤ ${t.f(t.g)}</span><span>Poor > ${t.f(t.p)}</span></div></div>`;
}

/* ---------------- HEADER ---------------- */
const app=document.getElementById('app');
const cw=W.current||{},pw=W.previous||{},gw=W.gsc_current||{};
app.append(el(`<header class="top"><div><h1>SEO Performance Report</h1><div class="site">${esc(M.site||'')}</div>
<div class="meta"><span class="chip">Period <b>${fdy(cw.startDate)} – ${fdy(cw.endDate)}</b></span><span class="chip">vs <b>${fdy(pw.startDate)} – ${fdy(pw.endDate)}</b></span>
<span class="chip">Search Console window <b>${fd(gw.startDate)} – ${fd(gw.endDate)}</b></span><span class="chip">Generated <b>${esc(M.run_at||'')}</b></span></div></div>
<div class="srcs">${logo('gsc',34,'platforms','Google Search Console')}${logo('ga4',34,'platforms','Google Analytics 4')}${logo('psi',34,'platforms','PageSpeed Insights')}${logo('gbp',34,'platforms','Google Business Profile')}</div></header>`));
const TABS=[['overview','Overview',null],['gsc','Search Console','gsc'],['ga4','Analytics & AI Traffic','ga4'],['psi','Page Speed','psi'],['gbp','Business Profile','gbp']];
const nav=el(`<nav class="tabs" role="tablist">${TABS.map(([id,l,lg],i)=>`<button class="tab" role="tab" id="t-${id}" aria-controls="p-${id}" aria-selected="${i===0}" data-t="${id}">${lg?logo(lg,22):'<span class="logo" style="width:22px;height:22px;background:var(--accent);border:0"><svg viewBox="0 0 16 16" width="12" height="12" fill="#fff"><rect x="1" y="1" width="6" height="6" rx="1.5"/><rect x="9" y="1" width="6" height="6" rx="1.5"/><rect x="1" y="9" width="6" height="6" rx="1.5"/><rect x="9" y="9" width="6" height="6" rx="1.5"/></svg></span>'}${l}</button>`).join('')}</nav>`);
app.append(nav);
const P={};TABS.forEach(([id],i)=>{P[id]=el(`<section class="panel ${i===0?'on':''}" role="tabpanel" id="p-${id}" aria-labelledby="t-${id}"></section>`);app.append(P[id])});
const drawn={};
function sel(id){nav.querySelectorAll('.tab').forEach(b=>b.setAttribute('aria-selected',b.dataset.t===id));Object.entries(P).forEach(([k,p])=>p.classList.toggle('on',k===id));if(!drawn[id]){drawn[id]=1;(RENDER[id]||(()=>{}))()}window.scrollTo({top:0,behavior:'smooth'})}
nav.addEventListener('click',e=>{const b=e.target.closest('.tab');if(b)sel(b.dataset.t)});
nav.addEventListener('keydown',e=>{const ids=TABS.map(t=>t[0]);const cur=ids.indexOf(nav.querySelector('[aria-selected="true"]').dataset.t);if(e.key==='ArrowRight'||e.key==='ArrowLeft'){const n=ids[(cur+(e.key==='ArrowRight'?1:ids.length-1))%ids.length];sel(n);nav.querySelector(`[data-t="${n}"]`).focus()}});

const G=D.gsc||{},A=D.ga4||{},AI=D.ai||{},PS=D.psi||{},B=D.gbp||{};
const gk=G.kpis||{},ak=A.kpis||{},aik=AI.kpis||{},bk=B.kpis||{};
const z={cur:null,prev:null};const K=(o,k)=>o[k]||z;
const HAS_GBP=(D.connected||['gmb']).includes('gmb');
const NO_GBP=`<div class="empty" style="text-align:left;display:flex;gap:12px;align-items:center">${logo('gbp',36)}<div><b style="color:var(--ink)">Google Business Profile isn't connected.</b><br>Add the Google My Business connector in Two Minute Reports and enable your location to see profile views, calls, directions and reviews here.</div></div>`;

/* ---------------- OVERVIEW ---------------- */
function rOverview(){
  const p=P.overview;
  const hl=(D.highlights||[]);
  const srcLogo=s=>s==='ai'?'':logo(s,20);
  p.append(el(`<div class="card" style="margin-bottom:14px"><h2>Key takeaways</h2><p class="sub">What changed in the last 28 days and where to act first</p>
  ${hl.length?`<ul class="hl">${hl.map(h=>`<li><span class="ic ${h.tone||'info'}">${{good:'▲',bad:'▼',warn:'!',info:'i'}[h.tone||'info']}</span><span style="flex:1">${esc(h.text)}</span>${h.src&&h.src!=='ai'?srcLogo(h.src):h.src==='ai'?ailogo((AI.platforms[0]||{}).id||'chatgpt',20):''}</li>`).join('')}</ul>`:'<div class="empty">No highlights.</div>'}</div>`));
  const mini=(l,c,pv,f,lower,mode)=>`<div><div class="l">${l}</div><div class="v">${f(c)}<span class="d">${delta(c,pv,lower,mode)}</span></div></div>`;
  const m=(PS.crux||{}).mobile,lm=(PS.lab||{}).mobile;
  const cwvOk=m?(m.lcp<=2.5&&m.inp<=.2&&m.cls<=.1):null;
  const cards=[
    ['gsc','Google Search Console','Organic search visibility',[mini('Clicks',K(gk,'clicks').cur,K(gk,'clicks').prev,cmp),mini('Impressions',K(gk,'impressions').cur,K(gk,'impressions').prev,cmp),mini('Avg CTR',K(gk,'ctr').cur,K(gk,'ctr').prev,v=>pc(v,2),false,'pp'),mini('Avg position',K(gk,'position').cur,K(gk,'position').prev,p1,true,'abs')]],
    ['ga4','Google Analytics 4','Site traffic & engagement',[mini('Sessions',K(ak,'sessions').cur,K(ak,'sessions').prev,cmp),`<div><div class="l">Organic search sessions</div><div class="v">${cmp(A.organic_sessions)}<span class="d" style="font-size:12px;color:var(--ink-3)">${K(ak,'sessions').cur?pc(A.organic_sessions/K(ak,'sessions').cur,0)+' of total':''}</span></div></div>`,mini('Engagement rate',K(ak,'engagement_rate').cur,K(ak,'engagement_rate').prev,v=>pc(v),false,'pp'),mini('Key events',K(ak,'key_events').cur,K(ak,'key_events').prev,cmp)]],
    ['psi','PageSpeed Insights','Core Web Vitals & Lighthouse',[`<div><div class="l">Core Web Vitals (mobile)</div><div class="v" style="font-size:15px;margin-top:4px">${cwvOk==null?'–':`<span class="badge ${cwvOk?'good':'bad'}">${cwvOk?'✓ Passed':'✕ Failed'}</span>`}</div></div>`,`<div><div class="l">Performance (mobile)</div><div class="v">${lm?Math.round(lm.performance):'–'}<span class="d" style="font-size:12px;color:var(--ink-3)"> / 100</span></div></div>`,`<div><div class="l">LCP (real users)</div><div class="v">${m?sec(m.lcp):'–'}</div></div>`,`<div><div class="l">SEO score (mobile)</div><div class="v">${lm?Math.round(lm.seo):'–'}<span class="d" style="font-size:12px;color:var(--ink-3)"> / 100</span></div></div>`]],
    ['gbp','Google Business Profile','Local visibility & actions',[mini('Profile views',K(bk,'views_total').cur,K(bk,'views_total').prev,cmp),mini('Total actions',K(bk,'actions_total').cur,K(bk,'actions_total').prev,cmp),mini('Calls',K(bk,'actions_phone').cur,K(bk,'actions_phone').prev,cmp),`<div><div class="l">Rating</div><div class="v">${(B.reviews||{}).rating?(B.reviews.rating).toFixed(1):'–'} <span class="stars" style="font-size:14px">★</span><span class="d" style="font-size:12px;color:var(--ink-3)">${n0((B.reviews||{}).count)} reviews</span></div></div>`]],
  ];
  const tabFor={gsc:'gsc',ga4:'ga4',psi:'psi',gbp:'gbp'};
  p.append(el(`<div class="grid g2">${cards.map(([k,t,s,items])=>`<div class="card src-card"><div class="head">${logo(k,36)}<div><h2>${t}</h2><div class="sub" style="margin:0">${s}</div></div></div>${k==='gbp'&&!HAS_GBP?'<div class="empty">Not connected in Two Minute Reports.</div>':`<div class="mini">${items.join('')}</div>`}<button class="go" data-go="${tabFor[k]}">Open ${t.replace('Google ','')} →</button></div>`).join('')}</div>`));
  // AI strip
  const pl=(AI.platforms||[]).filter(x=>x.sessions>0);
  p.append(el(`<div class="card" style="margin-top:14px"><h2>${logo('ga4',20)} AI assistant traffic</h2><p class="sub">Sessions referred by AI assistants (GA4) · ${cmp(K(aik,'sessions').cur)} sessions · ${pc(K(aik,'share').cur,2)} of all traffic ${delta(K(aik,'sessions').cur,K(aik,'sessions').prev)}</p>
  ${pl.length?`<div class="ai-strip">${pl.map(x=>`<span class="ai-chip">${ailogo(x.id,22,x.name)}${esc(x.name)} <b>${cmp(x.sessions)}</b>${delta(x.sessions,x.prev)}</span>`).join('')}</div>`:'<div class="empty">No AI-assistant referrals in this period.</div>'}
  <button class="go" data-go="ga4">See AI traffic details →</button></div>`));
  // dual small trends
  const tr=el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>${logo('gsc',20)} Organic clicks per day</h2><p class="sub">Google Search Console</p><div id="ov1"></div></div><div class="card"><h2>${logo('ga4',20)} Sessions per day</h2><p class="sub">Google Analytics 4 · all channels</p><div id="ov2"></div></div></div>`);
  p.append(tr);
  chart(tr.querySelector('#ov1'),(G.trend||[]).map(r=>r.d),[{name:'Clicks',color:'--s1',values:(G.trend||[]).map(r=>r.clicks)}],{area:1,h:180,label:'Clicks per day'});
  chart(tr.querySelector('#ov2'),(A.trend||[]).map(r=>r.d),[{name:'Sessions',color:'--s3',values:(A.trend||[]).map(r=>r.sessions)}],{area:1,h:180,label:'Sessions per day'});
  p.addEventListener('click',e=>{const b=e.target.closest('[data-go]');if(b)sel(b.dataset.go)});
}

/* ---------------- GSC ---------------- */
function posPill(v){const st=v<=3?'good':v<=10?'warn':'bad';return `<span class="pill ${st}">${p1(v)}</span>`}
function rGsc(){
  const p=P.gsc;
  p.append(el(`<div class="kpis">${kpi('Clicks',K(gk,'clicks').cur,K(gk,'clicks').prev,cmp,{hint:'Visits from Google Search'})}${kpi('Impressions',K(gk,'impressions').cur,K(gk,'impressions').prev,cmp,{hint:'Times the site appeared in results'})}${kpi('Average CTR',K(gk,'ctr').cur,K(gk,'ctr').prev,v=>pc(v,2),{mode:'pp',hint:'Clicks ÷ impressions'})}${kpi('Average position',K(gk,'position').cur,K(gk,'position').prev,p1,{lower:1,mode:'abs',hint:'Lower is better (1 = top)'})}</div>`));
  const c=el(`<div class="grid g2"><div class="card"><h2>Clicks per day</h2><p class="sub">Organic clicks from Google Search</p><div id="g1"></div></div><div class="card"><h2>Impressions per day</h2><p class="sub">How often the site was shown</p><div id="g2"></div></div></div>`);p.append(c);
  const T=G.trend||[];
  chart(c.querySelector('#g1'),T.map(r=>r.d),[{name:'Clicks',color:'--s1',values:T.map(r=>r.clicks)}],{area:1,label:'Clicks per day'});
  chart(c.querySelector('#g2'),T.map(r=>r.d),[{name:'Impressions',color:'--s7',values:T.map(r=>r.impressions)}],{area:1,label:'Impressions per day'});
  const qc=[{h:'Query',k:'key'},{h:'Clicks',k:'clicks',f:cmp,bar:1},{h:'Impressions',k:'impressions',f:cmp},{h:'CTR',k:'ctr',f:v=>pc(v,2)},{h:'Position',k:'position',f:posPill}];
  p.append(el(`<div class="card" style="margin-top:14px"><h2>Top search queries</h2><p class="sub">Ranked by clicks · position pill: green top 3, amber 4–10, red 11+</p>${table(qc,[...(G.queries||[])].sort((a,b)=>b.clicks-a.clicks).slice(0,15))}</div>`));
  p.append(el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>Striking-distance keywords</h2><p class="sub">Position 4–20 with the most impressions — the fastest ranking wins</p>${table([{h:'Query',k:'key'},{h:'Impr.',k:'impressions',f:cmp,bar:1},{h:'Clicks',k:'clicks',f:cmp},{h:'Pos.',k:'position',f:posPill}],(G.striking||[]).slice(0,10),{empty:'No queries between positions 4 and 20.'})}</div>
  <div class="card"><h2>CTR opportunities</h2><p class="sub">Top-5 positions with CTR under 2% — rewrite titles & meta descriptions</p>${table([{h:'Query',k:'key'},{h:'Impr.',k:'impressions',f:cmp,bar:1},{h:'CTR',k:'ctr',f:v=>pc(v,2)},{h:'Pos.',k:'position',f:posPill}],(G.low_ctr||[]),{empty:'No low-CTR queries in the top 5 — titles are doing their job.'})}</div></div>`));
  p.append(el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>Top pages</h2><p class="sub">Pages earning the most organic clicks</p>${table([{h:'Page',k:'key',f:v=>esc(path(v))},{h:'Clicks',k:'clicks',f:cmp,bar:1},{h:'Impr.',k:'impressions',f:cmp},{h:'CTR',k:'ctr',f:v=>pc(v,2)},{h:'Pos.',k:'position',f:posPill}],(G.pages||[]).slice(0,12))}</div>
  <div class="card"><h2>Clicks by device</h2><p class="sub">Share of organic clicks</p>${(()=>{const dv=G.devices||[];const t=dv.reduce((a,b)=>a+b.clicks,0)||1;const nm={MOBILE:'Mobile',DESKTOP:'Desktop',TABLET:'Tablet'};return bars(dv.map((d,i)=>({label:nm[String(d.key).toUpperCase()]||d.key,v:d.clicks,extra:`${pc(d.clicks/t)} · pos ${p1(d.position)}`,color:['--s1','--s2','--s3'][i%3]})),cmp)})()}</div></div>`));
}

/* ---------------- GA4 + AI ---------------- */
function rGa4(){
  const p=P.ga4;
  p.append(el(`<div class="kpis">${kpi('Sessions',K(ak,'sessions').cur,K(ak,'sessions').prev,cmp)}${kpi('Users',K(ak,'total_users').cur,K(ak,'total_users').prev,cmp)}${kpi('New users',K(ak,'new_users').cur,K(ak,'new_users').prev,cmp)}${kpi('Engagement rate',K(ak,'engagement_rate').cur,K(ak,'engagement_rate').prev,v=>pc(v),{mode:'pp',hint:'Sessions >10s, 2+ pages or a key event'})}${kpi('Avg session duration',K(ak,'average_session_duration').cur,K(ak,'average_session_duration').prev,dur)}${kpi('Key events',K(ak,'key_events').cur,K(ak,'key_events').prev,cmp,{hint:'Conversions marked as key events'})}</div>`));
  const c=el(`<div class="grid g2"><div class="card"><h2>Sessions per day</h2><p class="sub">All channels</p><div id="a1"></div></div><div class="card"><h2>Traffic by channel</h2><p class="sub">Sessions · engagement rate</p><div id="a2"></div></div></div>`);p.append(c);
  const T=A.trend||[];
  chart(c.querySelector('#a1'),T.map(r=>r.d),[{name:'Sessions',color:'--s3',values:T.map(r=>r.sessions)}],{area:1,label:'Sessions per day'});
  const ch=(A.channels||[]).slice(0,8);const tt=ch.reduce((a,b)=>a+b.sessions,0)||1;
  c.querySelector('#a2').innerHTML=bars(ch.map(x=>({label:esc(x.name),v:x.sessions,extra:`${pc(x.sessions/tt)} · ER ${pc(x.engagement_rate)}`,color:x.name==='Organic Search'?'--s1':'--s8'})),cmp);
  p.append(el(`<div class="card" style="margin-top:14px"><h2>Organic landing pages</h2><p class="sub">Where organic-search visitors land, and whether they convert</p>${table([{h:'Landing page',k:'page'},{h:'Sessions',k:'sessions',f:cmp,bar:1},{h:'Engagement',k:'engagement_rate',f:v=>pc(v)},{h:'Avg duration',k:'duration',f:dur},{h:'Key events',k:'key_events',f:cmp}],(A.organic_pages||[]).slice(0,12))}</div>`));
  // AI section
  const pl=(AI.platforms||[]);
  const strip=['chatgpt','gemini','perplexity','claude','copilot','meta-ai','grok','deepseek','mistral','poe'].map(i=>ailogo(i,22)).join('');
  p.append(el(`<div class="section-title"><h2>AI Traffic</h2><div class="lg">${strip}</div></div>`));
  p.append(el(`<p class="sub" style="margin:-6px 0 12px;color:var(--ink-3);font-size:13px">Visits referred by AI assistants (ChatGPT, Gemini, Perplexity, Claude, Copilot and others), detected from GA4 session source. Paid placements are excluded.</p>`));
  p.append(el(`<div class="kpis">${kpi('AI sessions',K(aik,'sessions').cur,K(aik,'sessions').prev,cmp)}${kpi('Share of all sessions',K(aik,'share').cur,K(aik,'share').prev,v=>pc(v,2),{mode:'pp'})}${kpi('AI users',K(aik,'users').cur,K(aik,'users').prev,cmp)}${kpi('AI key events',K(aik,'key_events').cur,K(aik,'key_events').prev,cmp)}${kpi('AI engagement rate',K(aik,'engagement_rate').cur,K(aik,'engagement_rate').prev,v=>pc(v),{mode:'pp',hint:`Site average ${pc(K(ak,'engagement_rate').cur)}`})}</div>`));
  if(!pl.length){p.append(el(`<div class="card"><div class="empty">No AI-assistant referrals were detected in this period.</div></div>`));return}
  p.append(el(`<div class="card"><h2>AI platforms</h2><p class="sub">Sessions, change vs previous period, engagement and top landing pages per assistant</p><div class="plat">${pl.map(x=>`<div class="pcard"><div class="top">${ailogo(x.id,40,x.name)}<div style="min-width:0"><div class="nm">${esc(x.name)}</div><div class="sr" title="${esc(x.sources.join(', '))}">${esc(x.sources.join(', ')||'no sessions this period')}</div></div><div style="margin-left:auto">${delta(x.sessions,x.prev)}</div></div>
  <div class="stats"><div>Sessions<b>${cmp(x.sessions)}</b></div><div>Engaged<b>${pc(x.engagement_rate,0)}</b></div><div>Key events<b>${cmp(x.key_events)}</b></div></div>
  <div class="share" title="${pc(x.share)} of AI sessions"><i style="width:${(x.share*100).toFixed(1)}%;background:var(${AI_COLOR[x.id]||'--s8'})"></i></div><div style="font-size:11px;color:var(--ink-3)">${pc(x.share)} of AI traffic · avg ${dur(x.duration)}</div>
  ${x.top_pages.length?`<ol>${x.top_pages.map(t=>`<li title="${esc(t.page)}">${esc(t.page)} <span style="color:var(--ink-3)">· ${cmp(t.sessions)}</span></li>`).join('')}</ol>`:''}</div>`).join('')}</div></div>`));
  // stacked trend: top 5 platforms in fixed order + Other
  const top=pl.filter(x=>x.sessions>0).slice(0,5).map(x=>x.id);const order=['chatgpt','gemini','perplexity','claude','copilot','meta-ai','grok'].filter(i=>top.includes(i)).concat(top.filter(i=>!['chatgpt','gemini','perplexity','claude','copilot','meta-ai','grok'].includes(i)));
  const TR=AI.trend||[];const nm=Object.fromEntries(pl.map(x=>[x.id,x.name]));
  const ser=order.map((id,i)=>({name:nm[id],color:AI_COLOR[id]||['--s5','--s6','--s7'][i%3],logo:ailogo(id,16,nm[id]),values:TR.map(r=>r.by[id]||0)}));
  const oth=TR.map(r=>Object.entries(r.by).filter(([k])=>!order.includes(k)).reduce((a,[,v])=>a+v,0));
  if(oth.some(v=>v>0))ser.push({name:'Other AI',color:'--s8',values:oth});
  const t2=el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>AI sessions per day</h2><p class="sub">Stacked by assistant</p><div id="ai1"></div></div><div class="card"><h2>Share of AI traffic</h2><p class="sub">Which assistants send the most visits</p><div id="ai2"></div></div></div>`);p.append(t2);
  chart(t2.querySelector('#ai1'),TR.map(r=>r.d),ser,{type:'stack',label:'AI sessions per day'});
  t2.querySelector('#ai2').innerHTML=bars(pl.filter(x=>x.sessions>0).map(x=>({label:`${ailogo(x.id,18,x.name)} ${esc(x.name)}`,v:x.sessions,extra:pc(x.share),color:AI_COLOR[x.id]||'--s8'})),cmp);
  t2.querySelectorAll('#ai2 .bar .t span:first-child').forEach(s=>{s.style.display='inline-flex';s.style.alignItems='center';s.style.gap='6px'});
  const pc2=[{h:'Landing page',k:'page'},{h:'AI sessions',k:'sessions',f:cmp,bar:1},{h:'From',k:'by',f:by=>`<span class="lg">${Object.entries(by).sort((a,b)=>b[1]-a[1]).slice(0,4).map(([id,v])=>`<span title="${esc(nm[id]||id)}: ${n0(v)}">${ailogo(id,20,nm[id])}</span>`).join('')}</span>`},{h:'Engagement',k:'engagement_rate',f:v=>pc(v)},{h:'Key events',k:'key_events',f:cmp}];
  p.append(el(`<div class="card" style="margin-top:14px"><h2>Pages AI assistants send visitors to</h2><p class="sub">Landing pages ranked by AI-referred sessions, with the assistants behind them</p>${table(pc2,(AI.pages||[]).slice(0,15))}</div>`));
}

/* ---------------- PSI ---------------- */
function rPsi(){
  const p=P.psi;const cr=PS.crux||{},lab=PS.lab||{};
  const url=(lab.mobile||lab.desktop||{}).url||(cr.mobile||cr.desktop||{}).origin||M.psi_url||'';
  p.append(el(`<div class="card" style="margin-bottom:14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap">${logo('psi',36)}<div style="flex:1;min-width:200px"><h2 style="margin:0">PageSpeed Insights</h2><div class="sub" style="margin:0">Tested: <b style="color:var(--ink)">${esc(url)}</b> · field data = real Chrome users (rolling 28 days) · lab data = Lighthouse audit run today</div></div><div class="seg" role="group" aria-label="Device"><button aria-pressed="true" data-ff="mobile">Mobile</button><button aria-pressed="false" data-ff="desktop">Desktop</button></div></div>`));
  const body=el('<div></div>');p.append(body);
  const draw=ff=>{
    const c=cr[ff],l=lab[ff];
    const pass=c?(vstat('lcp',c.lcp)==='good'&&vstat('inp',c.inp)==='good'&&vstat('cls',c.cls)==='good'):null;
    body.innerHTML='';
    body.append(el(`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px"><div><h2>Core Web Vitals — real users</h2><p class="sub" style="margin:0">Google uses these as a ranking signal. All three core metrics must be “Good” to pass.</p></div>${pass==null?'':`<span class="badge ${pass?'good':'bad'}">${pass?'✓ Core Web Vitals passed':'✕ Core Web Vitals failed'}</span>`}</div>
    ${c?`<div class="vitals">${['lcp','inp','cls'].map(k=>vital(k,c[k])).join('')}</div><div class="vitals" style="margin-top:12px">${['fcp','ttfb'].map(k=>vital(k,c[k])).join('')}</div>`:'<div class="empty">Not enough real-user traffic for Chrome UX Report field data on this site.</div>'}</div>`));
    body.append(el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>Lighthouse scores</h2><p class="sub">Lab audit · 90–100 good · 50–89 needs improvement · 0–49 poor</p>${l?`<div class="rings">${ring(l.performance,'Performance')}${ring(l.seo,'SEO')}${ring(l.accessibility,'Accessibility')}${ring(l.best_practices,'Best practices')}</div>`:'<div class="empty">No Lighthouse result.</div>'}</div>
    <div class="card"><h2>Lab timings</h2><p class="sub">Mobile vs desktop, simulated load</p>${(()=>{const m=lab.mobile||{},d=lab.desktop||{};const th={lcp:[2.5,4],fcp:[1.8,3],si:[3.4,5.8],tbt:[200,600],cls:[.1,.25],ttfb:[.8,1.8]};
      const f={lcp:sec,fcp:sec,si:sec,tbt:v=>v==null?'–':Math.round(v)+' ms',cls:v=>v==null?'–':v.toFixed(3),ttfb:sec};
      const st=(k,v)=>v==null?'':v<=th[k][0]?'good':v<=th[k][1]?'warn':'bad';
      const nmx={lcp:'Largest Contentful Paint',fcp:'First Contentful Paint',si:'Speed Index',tbt:'Total Blocking Time',cls:'Cumulative Layout Shift',ttfb:'Server response (TTFB)'};
      return `<div class="tbl-wrap"><table><thead><tr><th>Metric</th><th>Mobile</th><th>Desktop</th></tr></thead><tbody>${Object.keys(nmx).map(k=>`<tr><td>${nmx[k]}</td><td><span class="pill ${st(k,m[k])}">${f[k](m[k])}</span></td><td><span class="pill ${st(k,d[k])}">${f[k](d[k])}</span></td></tr>`).join('')}</tbody></table></div>`})()}</div></div>`));
  };
  draw('mobile');
  p.querySelector('.seg').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;p.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',x===b));draw(b.dataset.ff)});
  p.append(el(`<p class="note">Thresholds follow Google’s Core Web Vitals guidance: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (75th percentile of real users).</p>`));
}

/* ---------------- GBP ---------------- */
function rGbp(){
  const p=P.gbp;const R=B.reviews||{};
  if(!HAS_GBP){p.append(el(`<div class="card">${NO_GBP}</div>`));return}
  p.append(el(`<div class="kpis">${kpi('Profile views',K(bk,'views_total').cur,K(bk,'views_total').prev,cmp,{hint:'Search + Maps'})}${kpi('Views on Search',K(bk,'views_search').cur,K(bk,'views_search').prev,cmp)}${kpi('Views on Maps',K(bk,'views_maps').cur,K(bk,'views_maps').prev,cmp)}${kpi('Website clicks',K(bk,'actions_website').cur,K(bk,'actions_website').prev,cmp)}${kpi('Calls',K(bk,'actions_phone').cur,K(bk,'actions_phone').prev,cmp)}${kpi('Direction requests',K(bk,'actions_driving_directions').cur,K(bk,'actions_driving_directions').prev,cmp)}</div>`));
  const c=el(`<div class="grid g2"><div class="card"><h2>Profile views per day</h2><p class="sub">Google Search vs Google Maps</p><div id="b1"></div></div><div class="card"><h2>Customer actions</h2><p class="sub">What people did after finding the profile · ${delta(K(bk,'actions_total').cur,K(bk,'actions_total').prev)} total</p><div id="b2"></div></div></div>`);p.append(c);
  const T=B.trend||[];
  chart(c.querySelector('#b1'),T.map(r=>r.d),[{name:'Search',color:'--s1',values:T.map(r=>r.search)},{name:'Maps',color:'--s2',values:T.map(r=>r.maps)}],{label:'Profile views per day'});
  c.querySelector('#b2').innerHTML=bars([['Website clicks','actions_website','--s1'],['Calls','actions_phone','--s2'],['Direction requests','actions_driving_directions','--s3']].map(([l,k,col])=>({label:l,v:K(bk,k).cur||0,extra:`prev ${cmp(K(bk,k).prev)}`,color:col})),cmp);
  const dist=R.dist||{};const dn=Object.values(dist).reduce((a,b)=>a+b,0)||0;
  p.append(el(`<div class="grid g2" style="margin-top:14px"><div class="card"><h2>Search terms that found the profile</h2><p class="sub">Search impressions by keyword</p>${table([{h:'Search term',k:'term'},{h:'Impressions',k:'impressions',f:v=>v<15?'< 15':cmp(v),bar:1}],(B.keywords||[]).slice(0,12),{empty:'Google has not reported search terms for this period yet.'})}</div>
  <div class="card"><h2>Reviews</h2><p class="sub">Overall rating and reviews received in this period</p>
   <div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap;margin-bottom:14px"><div><div class="big">${R.rating?R.rating.toFixed(1):'–'}</div><div class="stars" aria-label="${R.rating||0} stars">${'★'.repeat(Math.round(R.rating||0))}<span style="color:var(--grid)">${'★'.repeat(5-Math.round(R.rating||0))}</span></div><div class="sub" style="margin:2px 0 0">${n0(R.count)} total reviews</div></div>
   <div style="flex:1;min-width:180px">${[5,4,3,2,1].map(s=>`<div style="display:flex;align-items:center;gap:8px;font-size:12px;margin:3px 0"><span style="width:22px;color:var(--ink-2)">${s}★</span><div class="track" style="flex:1;height:8px;border-radius:4px;background:var(--surface-2);overflow:hidden"><div style="height:100%;width:${dn?(dist[s]||0)/dn*100:0}%;background:var(--s4)"></div></div><span style="width:24px;text-align:right;color:var(--ink-3)">${dist[s]||0}</span></div>`).join('')}<div class="sub" style="margin:6px 0 0">${n0(R.new_in_period)} new in period${R.reply_rate!=null?` · ${pc(R.reply_rate,0)} replied`:''}</div></div></div>
   ${(R.recent||[]).length?`<div class="rv">${R.recent.slice(0,3).map(r=>`<div class="it"><div class="m"><span class="stars">${'★'.repeat(r.stars||0)}</span><span>${fdy(r.date)}${r.replied?' · replied':' · <b style="color:var(--warn-ink)">no reply</b>'}</span></div>${esc(r.comment||'(rating only, no comment)')}</div>`).join('')}</div>`:''}</div></div>`));
  if((B.locations||[]).length>1)p.append(el(`<div class="card" style="margin-top:14px"><h2>Locations</h2><p class="sub">Performance per business location</p>${table([{h:'Location',k:'name'},{h:'Views',k:'views_total',f:cmp,bar:1},{h:'Δ views',k:'views_total',f:(v,r)=>delta(v,r.prev_views)},{h:'Actions',k:'actions_total',f:cmp},{h:'Δ actions',k:'actions_total',f:(v,r)=>delta(v,r.prev_actions)},{h:'Calls',k:'actions_phone',f:cmp},{h:'Website',k:'actions_website',f:cmp}],B.locations)}</div>`));
}

const RENDER={overview:rOverview,gsc:rGsc,ga4:rGa4,psi:rPsi,gbp:rGbp};
drawn.overview=1;rOverview();
app.append(el(`<footer><p><b>Sources:</b> Google Search Console (${esc(M.gsc_label||'')}), Google Analytics 4 (${esc(M.ga4_label||'')}), PageSpeed Insights / Chrome UX Report, Google Business Profile (${HAS_GBP?esc(M.gbp_label||''):'not connected'}) — via Two Minute Reports.</p>
<p>Search Console data lags 2–3 days, so its window ends earlier. Deltas compare with the previous period of equal length. AI traffic is matched on GA4 session source (e.g. chatgpt.com, perplexity.ai, gemini.google.com); assistants that hide the referrer show up as Direct and can't be counted.</p>${(D.missing||[]).length?`<p>Some data was unavailable this run: ${esc(D.missing.join(', '))}.</p>`:''}</footer>`));
})();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
```
<!-- seo_report.py:end -->
