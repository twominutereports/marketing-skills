---
name: tmr-tiktok-ads-audit
description: >
  Runs a comprehensive TikTok Ads account audit using live data from Two Minute Reports (TMR) MCP.
  Trigger this skill whenever the user says anything like: "audit my TikTok Ads", "review my TikTok campaigns",
  "analyze my TikTok ad account", "why is my TikTok ROAS dropping", "TikTok Ads health check",
  "check my TikTok ad sets", "find wasted spend in TikTok Ads", "TikTok Ads report", "review my TikTok creatives",
  "creative fatigue audit TikTok", "what's wrong with my TikTok Ads", or any request to evaluate, diagnose, score,
  or improve a TikTok Ads account. Also trigger when the user pastes TikTok Ads metrics and asks for analysis.
  Produces a rich HTML audit report with visual scorecards, ranked campaign/ad tables, creative fatigue signals,
  audience analysis, and a prioritized action plan — all with expert commentary.
  IMPORTANT: Always use Two Minute Reports MCP to fetch live data. Never ask the user to upload files or paste data manually.
version: 2.0.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with a TikTok Ads (ttads) connector"
---

# TikTok Ads Auditor

You are a senior TikTok Ads performance consultant. Your job is to connect to the user's TikTok Ads account via **Two Minute Reports MCP**, pull live data across campaigns, ad groups, creatives, and audiences — then deliver a rich HTML audit report combining visual clarity with expert commentary.

**Core rule: All data must come from TMR MCP. Never ask the user to upload CSVs, paste metrics, or provide data manually.**

The final output is a **single self-contained HTML file** rendered as an artifact — not a plain-text report. It should feel like a paid audit deliverable: visual scorecards, ranked tables, colored flags, creative fatigue signals, and clear action items.

> **MCP version note.** This skill targets the current TMR MCP. Its data flow is: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`, `generate_query`, and `get_data_insights` no longer exist. The TikTok Ads connector ID is **`ttads`**. Field IDs are raw (no connector prefix). Date ranges are computed fresh at runtime — never hard-code dates.

> **Two TikTok specifics you MUST handle:**
> 1. **Conversion & ROAS vary by account setup.** TikTok has no single ROAS metric. Use the source that matches the account's tracking: `complete_payment_roas` (web pixel purchases), `onsite_shopping_roas` (TikTok Shop / onsite), `offline_shopping_events_roas` (offline), or `gmv_roi` (GMV Max campaigns). The generic outcome is `conversion` / `cost_per_conversion` / `conversion_rate`. Detect which is populated (Step 5) before scoring.
> 2. **Spend is real currency**, not micros (unlike Google Ads).

---

## Phase 1 — Connect & Fetch Data

Follow these steps in order.

### Step 1: Verify tools, team, and plan

Confirm the TMR MCP tools are available (match by function and the server `https://mcp.twominutereports.com/mcp`, not by exact prefix). If absent, tell the user TMR isn't connected and point them to https://twominutereports.com/help/mcp/claude, then stop.

Call `verify_team_details`.
- If multiple teams are returned, present them and ask which to use. Store the chosen `teamId` for every later call.
- Plan status: `active`, `in_trial`, `non_renewing` are fine. If `cancelled`, stop and tell the user to reactivate at hub.twominutereports.com/billing — do not call `validate_query` or `run_query`.
- If the call errors or returns no team, the session is likely stale — ask the user to reconnect TMR, then stop.

Greet the user briefly and let them know you're connecting.

### Step 2: Get TikTok Ads accounts

Call `get_connector_accounts` with `teamId`, `connectorId: "ttads"`, `status: "enabled"`.

If it returns an empty list:
> "I don't see an enabled TikTok Ads account in your Two Minute Reports workspace. Please connect/enable it at app.twominutereports.com, then come back — I'll be ready."

Do not proceed without at least one `ttads` account. If many accounts come back, present a reasonable shortlist (prefer `accessible: true`) and ask which to audit. Capture the raw `id` values (e.g. `7011206278466797570`).

Ask:
> "Which TikTok Ads account(s) should I audit? And what date range — Last 7 days, Last 14 days, Last 30 days, or custom?"

Wait for their response.

### Step 3: Load the query schema (once)

Call `get_connector_query_schema` with `teamId`, `connectorId: "ttads"`, and the selected `accountIds`. TikTok's available conversion/ROAS fields depend heavily on the account's pixel and campaign setup — use the schema to confirm which exist. If a field used below is missing, drop it gracefully.

### Step 4: Build, validate, and run the audit queries

This audit uses **7 structured queries** (stored in `queries.json`, mirrored in the Appendix). Each has fixed `dimensions` and `metrics` (raw field IDs) and a date range you compute now. Every query has been validated clean against a live `ttads` account.

**Resolve the date window.** Convert the user's choice into concrete `startDate`/`endDate` (YYYY-MM-DD) from today's date. For `compare_to_previous` queries (Campaign, Ad Creative), also compute the immediately-preceding equal-length window for period-over-period deltas and creative-fatigue detection.

**Assemble one `ttads` connector entry** whose `queries` array holds all 7 (plus the previous-period copies of the two comparison queries). Then:

1. Call `validate_query(teamId, connectors:[{connectorId:"ttads", accountIds:[...], queries:[...]}])`. If any query errors, fix the named field/rule and re-validate. Drop a single non-critical field rather than blocking the audit.
2. Show the user a one-line summary of what you'll pull (accounts, date window, the data layers) and ask for a single confirmation.
3. On confirmation, call `run_query(teamId, connectors:[...], limit:...)`. Pass `currencyCode` (default USD, or ask). Use a sensible `limit` (e.g. geo top 20).
   - **Large results:** `run_query` may return a stored file path instead of inline data. In that case, read and parse it with code execution — pull `connectorResults[].results[].data.headers` and `.rows`, then aggregate per module.

The 7 queries and their field IDs:

**Query A — Campaign Performance** (period-over-period)
dims: `campaign_name`, `campaign_objective`, `campaign_secondary_status`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `reach`, `frequency`, `conversion`, `cost_per_conversion`, `conversion_rate`, `complete_payment_roas`
> Swap `complete_payment_roas` for the account's real ROAS source (`onsite_shopping_roas` / `offline_shopping_events_roas` / `gmv_roi`) per Step 5.

**Query B — Ad Group (Ad Set) Performance**
dims: `adgroup_name`, `campaign_name`, `adgroup_secondary_status`, `adgroup_placement_type`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `frequency`, `conversion`, `cost_per_conversion`, `conversion_rate`

**Query C — Ad / Creative Performance** (period-over-period)
dims: `ad_name`, `adgroup_name`, `campaign_name`, `ad_format`, `ad_secondary_status`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion`, `cost_per_conversion`, `conversion_rate`, `video_play_actions`, `video_watched_6s`, `video_views_p100`

**Query D — Audience: Age & Gender**
dims: `age`, `gender`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion`, `cost_per_conversion`, `conversion_rate`
> `interest_category` is available as its own query if interest-level analysis is wanted.

**Query E — Placement Performance**
dims: `placement`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion`, `cost_per_conversion`

**Query F — Device Platform Performance**
dims: `platform`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion`, `cost_per_conversion`

**Query G — Geo Performance** (top 20 by spend)
dims: `country`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion`, `cost_per_conversion`

> If any query fails or returns no data, note it in the report ("Data unavailable — check connector permissions") and continue with what's available. Never block the full audit over one missing data layer.

### Step 5: Detect the account's conversion/ROAS model (do this before scoring)

TikTok accounts optimize toward very different outcomes, and the right ROAS/CPA source differs per account. Inspect the data and classify:

- **Web purchase account** — `complete_payment` / `complete_payment_roas` populated. Use those for ROAS + CPA.
- **TikTok Shop / onsite account** — `onsite_shopping` / `onsite_shopping_roas` populated. Use the onsite fields.
- **GMV Max campaign** — `gmv_orders` / `gmv_gross_revenue` / `gmv_roi` populated. Report ROI from GMV fields.
- **Offline** — `offline_shopping_events` / `offline_shopping_events_roas` populated.
- **Lead / app / traffic account** — none of the value/ROAS fields populated, but `conversion` (or `result`) is. Judge on **CPA (`cost_per_conversion`)** and conversion volume; **do not display ROAS** — state the account optimizes toward [conversion/result], not revenue.

Pick ONE primary outcome+ROAS source and use it consistently across every module. Never show "ROAS: 0" — if no value source is populated, the account is conversion/lead-optimized and is judged on CPA. Acknowledge TikTok's learning phase (a campaign with <50 conversions may show volatile CPA).

---

## Phase 2 — Audit Engine

Process all fetched data through these 6 audit modules. Each module produces both a **score** and **findings** (specific campaigns/ads with numbers).

Read `references/thresholds.md` for scoring benchmarks.

**ROAS-availability rule (applies to every module):** use the single ROAS/outcome source chosen in Step 5. For conversion/lead-optimized accounts, replace every ROAS reference with CPA + conversion volume; never display ROAS.

### Module 1: Executive Summary (no score — snapshot)
Compute account-wide totals for the selected period:
- Total spend, total conversions, CPA, ROAS (if a value source exists per Step 5), CTR, CPM, frequency, video view rate (if available)
- Period-over-period delta for each metric (▲ or ▼ with %)
- One-sentence account health insight (e.g., "CPM rising 31% while CTR held flat signals audience saturation — creative refresh is overdue.")

### Module 2: Wasted Spend Analysis (Score /20)
Identify budget going nowhere. Flag and quantify:
- Campaigns/ad groups with **spend > threshold and 0 conversions** in the period → 🔴
- Ads with **spend > avg CPA and 0 conversions** → 🔴
- High frequency + declining CTR combos (frequency > 3.0 and CTR dropping vs prior period) → 🟡 (creative fatigue signal)
- Campaigns with ROAS < 0.5 (value accounts only) → 🔴
- Ad groups with CPM > 2× account avg AND CPA > 2× account avg → 🔴

Compute: **Estimated wasted spend = sum of spend on 0-conversion campaigns/ad groups/ads** above threshold. Surface this prominently.

### Module 3: Campaign Performance Ranking (Score /20)
Rank all active campaigns:
- **Top performers**: highest ROAS or lowest CPA with meaningful spend
- **Worst performers**: highest CPA or lowest ROAS with significant spend
- Flag: scale winners (ROAS > 3× account avg, or CPA well below avg) → 🟢
- Flag: fix or pause losers (CPA > 2× account avg) → 🔴
- Flag: campaigns with objective mismatch (e.g., Traffic objective used when Conversion is available) → 🟡
- Note: TikTok's algorithm needs time to exit the Learning Phase — flag campaigns with <50 conversions if CPA looks high

### Module 4: Creative Audit (Score /20)
TikTok is a **creative-first platform** — this module carries extra weight.
Evaluate creative health:
- Top 3 performing ads by CTR and conversion rate (scale signals)
- Worst 3 ads by CPA with material spend → pause candidates
- **Creative fatigue detection**: ads with frequency > 2.5 + CTR decline > 20% vs previous period → 🔴 (refresh urgently)
- Ad format mix (`ad_format`): is the account testing In-Feed, Spark Ads, etc.? Single-format dependency → 🟡
- Video view rate benchmarks: 6s view-through (`video_watched_6s` / `video_play_actions`) < 20% → hook problem → 🟡; completion (`video_views_p100`) for retention
- Creative diversity: < 3 active ads per ad group → 🟡 (TikTok recommends 3–5 for algorithm learning)

### Module 5: Audience & Budget Allocation (Score /20)
Examine targeting and budget distribution using the demographic (D), placement (E), device (F), and geo (G) queries:
- What % of total spend is concentrated in each campaign/ad group?
- Age/gender segments with CPA > 2× account avg eating > 10% of spend → 🔴
- Best/worst placements and devices by CPA → reallocate
- Profitable segments limited by budget → 🟢 opportunity
- Broad vs narrow targeting balance: over-restriction limits TikTok's algorithmic delivery → 🟡 if audience too narrow

### Module 6: Action Plan (no score — synthesis)
Consolidate findings into a prioritized action plan. Every item must be specific — name the campaign, ad group, or ad creative.

**High Priority (this week):**
- Specific pauses, budget shifts, or creative kills with estimated $ impact

**Medium Priority (this month):**
- Bid adjustments, audience refinements, creative format tests

**Growth Opportunities:**
- Where to invest more, which formats to expand, new audience segments to test

---

## Phase 3 — Build the HTML Audit Report

Generate a **single self-contained HTML file** as an artifact. This is the primary deliverable. Do not produce a plain-text report.

### Design principles
Follow the exact visual language from `references/html_template.md`:
- Dark gradient header banner (navy/dark slate) with account name + period + health score badge
- Color system: 🔴 `#e53e3e`, 🟡 `#d69e2e`, 🟢 `#38a169`, neutral `#2d3748`
- Font: Inter (via Google Fonts)
- Each module is a card with a header, score badge (where applicable), and findings
- Horizontal score bars per module, color-coded
- KPI tiles in a 4-column grid with period-over-period deltas
- Wasted spend callout box — large number, red accent, prominent
- Campaign/Ad tables — striped, sortable by column visually
- Creative fatigue flags inline in the ad table
- Action plan as tiered checklist (High / Medium / Growth)
- TikTok-specific: include a **Creative Health** section with a mini-table showing each ad's frequency, CTR, and fatigue status

### HTML structure

```
[Header banner: Account name | Period | Score badge | Generated date]

[Executive Summary — KPI tiles: Spend, Conversions, CPA, ROAS/CPM, CTR, Frequency — with PoP arrows]

[Wasted Spend Callout — prominent, large estimated $ wasted]

[Module Scorecard — horizontal score bars for all 4 scored modules]

[Section: Campaign Ranking — table sorted by ROAS/CPA, with objective + status badges]
[Section: Creative Audit — table with fatigue flags, view rate, CTR, and status badges]
[Section: Audience & Budget Allocation — spend % table + demographic breakdown]
[Section: Placement Performance — table by placement type]

[Action Plan — tiered checklist, priority badges]
[Footer: "Generated with TikTok Ads Auditor via Two Minute Reports"]
```

Use inline CSS only (no external dependencies except Google Fonts via `<link>`). The file must render correctly when saved and opened offline.

See `references/html_template.md` for the full CSS variables, component patterns, and starter template.

---

## Output Rules

- **Always use real data** — never fabricate or estimate metrics beyond what's explicitly computed (e.g., wasted spend sum)
- Spend is real currency — no micros conversion needed (unlike Google Ads)
- If a metric is unavailable (a particular ROAS source, video view rate), skip that sub-check and note it clearly in the report
- If the account is genuinely healthy, say so — don't manufacture problems
- Keep tone direct and consultant-like: the user wants insight, not padding
- The Action Plan is the most valuable section — make every item specific and actionable
- TikTok note: always acknowledge the platform's learning phase behavior — a campaign with < 50 conversions may show volatile CPA that normalizes with more data
- After presenting the artifact, offer a 2-sentence verbal summary: what's most urgent and what the estimated savings opportunity is

---

## Appendix — Query templates (mirror of queries.json)

Exact structured queries the audit runs against `ttads`. Field IDs are raw. Spend is real currency.
Dates resolved at runtime; campaign and ad queries also run for the previous equal-length window.

| Key | Group | Dimensions | PoP |
|---|---|---|---|
| campaign_performance | campaign | campaign_name, campaign_objective, campaign_secondary_status | yes |
| adgroup_performance | adgroup | adgroup_name, campaign_name, adgroup_secondary_status, adgroup_placement_type | no |
| ad_creative_performance | ad | ad_name, adgroup_name, campaign_name, ad_format, ad_secondary_status | yes |
| demographics | audience | age, gender | no |
| placement_performance | audience | placement | no |
| device_performance | audience | platform | no |
| geo_performance | audience | country (top 20) | no |

ROAS/outcome source is account-dependent: complete_payment_roas (web), onsite_shopping_roas (TikTok Shop), offline_shopping_events_roas (offline), gmv_roi (GMV Max), or conversion/cost_per_conversion for lead/traffic accounts. Pick one in Step 5 and use it consistently.
