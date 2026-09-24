---
name: tmr-ga4-ai-traffic-audit
description: Use this skill when the user asks for an AI traffic audit in GA4 — how much traffic ChatGPT, Gemini, Perplexity, Claude, Copilot, Meta AI, Grok or DeepSeek send, which landing pages each AI assistant sends visitors to, AI referral share of sessions, engagement and key events, and change vs the previous 30 days. Trigger on "AI traffic audit", "traffic from ChatGPT", "which pages get AI traffic", "LLM referral traffic", "AI search referrals in GA4". Produces an inline insights summary plus a dashboard artifact with AI platform logos and a page × platform matrix.
version: 1.0.0
---

# AI Traffic Audit (GA4)

## Purpose

Show a marketer how much of their website traffic comes from AI assistants, which AI platforms send it (ChatGPT, Gemini, Perplexity, Claude, Copilot, Meta AI, Grok, DeepSeek, Mistral, Poe, You.com), and exactly which landing pages each platform sends visitors to — with engagement, key events and change vs the previous 30 days. The dashboard shows every AI platform by its logo so the page × platform picture is readable at a glance.

## Connectors required

This skill uses the following TMR connector:
- Google Analytics 4 (`ga4`)

The runtime procedure below verifies it is available before doing any analytical work. Do not attempt to proceed with partial connector availability.

## Files in this skill

- `queries.json` — the four locked query templates (field IDs + relative date specs).
- `config.json` — saved end-user settings (accounts, auto-confirm).
- `references/build_dashboard.py` — classifies GA4 session sources into AI platforms, computes KPIs and renders the dashboard.
- `references/dashboard_template.html` — the dashboard scaffold (layout, CSS, charts). Do not edit per run.
- `references/logos/` — AI platform logos + GA4 logo. The script embeds them as data URIs so the dashboard is self-contained.

## Runtime procedure

Follow these steps in order. Do not skip steps. Do not rearrange.

### 1. Check that TMR's tools are available

Inspect your available tools. The current Two Minute Reports MCP exposes these tool names: `verify_team_details`, `list_connectors`, `get_connector_accounts`, `get_connector_query_schema`, `validate_query`, `run_query`. The prefix may vary — users name their MCP connections differently (e.g., "Two Minute Reports", "TMR", "TwoMinuteReports", or a custom name). Match by tool function and the Two Minute Reports MCP server (URL: `https://mcp.twominutereports.com/mcp`), not by exact prefix. If the tools are deferred, load them with your tool-search tool first.

**If none of these tools are present**, tell the user:

> *"This skill needs Two Minute Reports to be connected to your Claude account, but I don't see it in your available tools.*
>
> *Two Minute Reports is an analytics platform that lets you query your marketing data (ads, analytics, e-commerce, etc.) from inside Claude. You'll need to connect it once, then this skill (and any other TMR skills) will work.*
>
> *Here's the setup guide: https://twominutereports.com/help/mcp/claude*
>
> *Once it's connected, run this skill again."*

If a `suggest_connectors` capability is available, also use it to surface a one-tap connect option for the Two Minute Reports MCP. Then stop.

### 2. Verify team and plan status

Call `verify_team_details`.

- **Multiple teams** → present them and ask which to use (flag any `cancelled` team). Store the chosen `teamId`.
- **One team** → use it and tell the user which team is active.
- `active`, `in_trial`, `non_renewing` are fine. If `cancelled`, stop: *"Your Two Minute Reports plan is cancelled, so I can't pull data. Reactivate it at hub.twominutereports.com/billing, then run this skill again."*
- **Auth/permission/session error or no teams** → *"Two Minute Reports is connected, but I couldn't verify your team details — your session may have expired or the connection needs to be re-authenticated. Please reconnect Two Minute Reports with the account that holds your TMR team, then run this skill again. Setup reference: https://twominutereports.com/help/mcp/claude"* (trigger `suggest_connectors` if available). Stop.
- **Other failure** → *"Couldn't reach Two Minute Reports right now — please try again in a moment."* Stop.

### 3. Verify GA4 is provisioned in TMR

Call `get_connector_accounts(teamId, connectorId:"ga4", status:"enabled")`.

- At least one account → continue.
- No accounts → *"This skill needs Google Analytics 4 to be set up inside Two Minute Reports, but it isn't connected with an enabled property yet. Please open Two Minute Reports, add Google Analytics 4 (and enable a property), then come back and run this skill again."* Stop.
- Call fails entirely → treat like a step 2 session failure.

### 4. Locate skill folder and load configuration

Find this skill's install folder (`<install-path>`):
1. `/mnt/skills/user/tmr-ga4-ai-traffic-audit/`
2. else `find / -type d -name "tmr-ga4-ai-traffic-audit" 2>/dev/null | head -1`
3. else: use the fallback query templates at the bottom of this file, skip config read/write and the save prompt, and build the dashboard by hand following the layout described in step 6.

Read `<install-path>/config.json`.

- **`saved: true`** → *"Using your saved configuration: property <label>. Say 'change config' if you want to update these."* Use the stored `accounts` and `auto_confirm_query`.
- **Otherwise** → reuse the step 3 response, list the GA4 properties and ask *"Which GA4 property would you like to audit?"* (one property per run gives the cleanest page matrix; if the user picks several, sum them). No currency is needed — this skill has no monetary metrics.
- Corrupt/unreadable config → *"Couldn't read your saved settings — let's set them again."* and run the collection flow.

### 5. Build, validate, and run the queries

Load the four templates from `<install-path>/queries.json`.

a. **Resolve dates from today's real date** (GA4 same-day data is partial, so end yesterday):
   - `last_n_days {n, end_offset_days}` → `endDate` = today − end_offset_days, `startDate` = endDate − (n − 1). With n=30, offset 1: the 30 full days ending yesterday.
   - `previous_n_days {n, offset_days}` → `endDate` = today − offset_days, `startDate` = endDate − (n − 1). With n=30, offset 31: the 30 days immediately before the current window.

b. **Assemble** one `ga4` connector entry with `accountIds` = the selected property ID(s) and four queries, each `{title, query:{metrics, dimensions, dateRange, filters, sort}}`. Keep the titles exactly as in `queries.json`. Raw field IDs, no prefix.

c. **Validate** with `validate_query(teamId, userQuery:<the user's request>, connectors:[…], skillId:"tmr-ga4-ai-traffic-audit")`. On errors, do not run — explain briefly that the GA4 schema may have changed and suggest contacting the skill author. Stop.

d. **Confirm** (skip if `auto_confirm_query` is true): *"I'll pull GA4 sessions, users, engaged sessions, key events and engagement time by session source and landing page for <start>–<end>, a daily trend, the site total, and the previous 30 days (<prev start>–<prev end>) for comparison, from <property>. OK?"* Wait for yes.

e. **Run** `run_query(teamId, connectors:[…], limit:5000, skillId:"tmr-ga4-ai-traffic-audit")`.
   - If the result comes back inline, save the full JSON response to `ai_traffic_result.json` in your working directory.
   - If it is too large and returned as a stored file path, use that path directly — do not load it into context.

### 6. Produce the dual output

**First, render the dashboard and get the numbers:**

```bash
python3 <install-path>/references/build_dashboard.py \
  --input <result json path> \
  --out <outputs dir>/ai-traffic-audit-<YYYY-MM-DD-HHMM>.html \
  --account "<property label>" \
  --window "<start> to <end>" \
  --compare "<prev start> to <prev end>" \
  --run-time "<YYYY-MM-DD HH:MM in the user's timezone>"
```

The script prints a JSON summary (KPIs, per-platform totals, previous-period sessions, top pages per platform, top pages with platform mix). Use only that summary for the insights — do not re-read the raw rows. Never pass `--demo` for a real run.

AI platform matching (in the script): a session counts as AI traffic when its GA4 session source contains `chatgpt`/`openai` (ChatGPT), `gemini`/`bard` (Gemini), `claude.ai`/`anthropic` (Claude), `perplexity`, `copilot`, `meta.ai`, `grok`/`x.ai`, `deepseek`, `mistral`, `poe.com`, `you.com`.

#### Insights (inline chat)

Write 150–300 words:
1. Headline finding — the single most important thing.
2. Supporting metrics — 2–3 numbers.
3. Notable changes — biggest platform shifts vs the previous 30 days.
4. Action — one concrete recommendation.

Match the tone, voice and structure of this template; fill the `[brackets]` with the user's data:

> AI assistants sent **[N] sessions** to [site] in [reporting period] — **[X%]** of all [N] sessions, [up/down] **[Y%]** from [N] in [comparison period]. **[Top platform] leads** with [N] sessions ([X%] of AI traffic, [±Y%]), followed by [second platform] ([N]) and [third platform] ([N]); [remaining platforms] together sent [N].
>
> AI visitors are [high/low]-quality traffic: **[X%] engagement** and **[N] key events** ([N] per session) [vs site context if known]. [Top page] captures [N] of the [N] AI sessions ([X%]); the rest is a long tail of [page type] pages, and platforms differ in where they send people — [platform A] favours [page examples], while [platform B] sends users to [page examples].
>
> [Biggest shift]: [platform] moved from [N] to [N] ([±X%]) [and/while] [second shift].
>
> **Action:** [one concrete step tied to the biggest finding — e.g. protect/expand the pages a growing platform cites, investigate a declining platform's landing pages, add clear answers/structured data to high-AI-traffic pages].

Also note in one sentence that some AI apps strip referrers, so their visits land in (direct) and are not counted — the figures are a floor.

#### Dashboard (artifact)

The HTML file from the script is the dashboard. Publish it as a **new** artifact each run (never overwrite an earlier one), titled:

`AI Traffic Audit — <YYYY-MM-DD HH:MM> — <property label>`

If you can publish artifacts, publish the file; otherwise deliver the HTML file to the user. It contains: a metadata header (GA4 logo, property, window, comparison window, run time), five KPI tiles (AI sessions with change, share of site sessions, AI users, AI key events, AI engagement rate), an AI platform leaderboard (one card per platform with its logo, sessions, share, change, engagement, key events, engagement time and top 5 pages), a stacked daily trend by platform, and a filterable Pages × AI platforms matrix with platform logos as column headers. Do not modify the template or logos; only the script fills the data.

If there is no AI traffic in the window, the dashboard shows an empty state — say so plainly in the insights and suggest checking a longer window or whether AI referrals are being grouped as (direct).

### 7. Save configuration (first run only, only if no saved config existed at start)

Ask:

> "Want to save your settings for future runs? This skill can remember your GA4 property so you don't have to pick it every time — useful if you re-run this report regularly or use it in a workflow.
>
> - Save property? (yes / no)
> - Auto-confirm the query on future runs? (yes / no — saves a step but you won't see the query before it runs)"

If yes to either, write `<install-path>/config.json`:

```json
{
  "version": "1.0.0",
  "saved": true,
  "accounts": { "ga4": [{ "label": "...", "value": "..." }] },
  "currency": null,
  "auto_confirm_query": true,
  "saved_at": "<ISO 8601 timestamp>"
}
```

Wrap the write in error handling. On failure: *"Couldn't save your settings to disk — they'll be remembered for this conversation only. You'll be asked again next time you run this skill."* On success: *"Saved. Future runs of this skill will use these settings automatically. Say 'change config' inside the skill to update."* Skip this step silently if `<install-path>` was not resolved.

## Notes for end users

- The skill asks you to confirm the query before running it (unless auto-confirm is on).
- It always covers the last 30 full days vs the 30 days before. Need a different window? Ask for a different skill — skills stay specific so they're predictable.
- Every run produces both an inline insights summary and a new dashboard artifact from the same data.
- AI traffic is identified from GA4's session source. Visits from AI apps that don't pass a referrer show up as (direct) and can't be attributed, so treat the numbers as a minimum.
- Requires the Two Minute Reports MCP connected to Claude — see https://twominutereports.com/help/mcp/claude.

## Query templates

(Fallback copy of `queries.json` in case the install folder can't be located at runtime.)

```json
{
  "queries": [
    {"title": "AI Referral Source x Landing Page", "connectorId": "ga4",
     "metrics": ["sessions", "total_users", "engaged_sessions", "key_events", "user_engagement_duration"],
     "dimensions": ["session_source", "landing_page"],
     "filters": [{"filterField": "session_source", "operator": "notEquals", "expression": "google"},
                 {"filterField": "session_source", "operator": "notEquals", "expression": "(direct)"},
                 {"filterField": "session_source", "operator": "notEquals", "expression": "bing"},
                 {"filterField": "session_source", "operator": "notEquals", "expression": "(not set)"}],
     "sort": [{"sortField": "sessions", "direction": "desc"}],
     "date_spec": {"type": "last_n_days", "n": 30, "end_offset_days": 1}},
    {"title": "AI Referral Daily Trend", "connectorId": "ga4",
     "metrics": ["sessions"], "dimensions": ["date", "session_source"],
     "filters": "<same four session_source filters>",
     "date_spec": {"type": "last_n_days", "n": 30, "end_offset_days": 1}},
    {"title": "Site Total", "connectorId": "ga4",
     "metrics": ["sessions", "total_users"], "dimensions": [], "filters": [],
     "date_spec": {"type": "last_n_days", "n": 30, "end_offset_days": 1}},
    {"title": "AI Referral Sources Previous Period", "connectorId": "ga4",
     "metrics": ["sessions", "total_users", "key_events"], "dimensions": ["session_source"],
     "filters": "<same four session_source filters>",
     "date_spec": {"type": "previous_n_days", "n": 30, "offset_days": 31}}
  ]
}
```
