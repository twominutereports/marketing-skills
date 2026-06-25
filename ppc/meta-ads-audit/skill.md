---
name: tmr-meta-ads-audit
description: >
  Runs a comprehensive Meta / Facebook Ads account audit using live data from Two Minute Reports (TMR) MCP.
  Trigger this skill whenever the user says anything like: "audit my Meta Ads", "audit my Facebook Ads",
  "review my Facebook campaigns", "analyze my Meta ad account", "why is my ROAS dropping on Facebook",
  "Meta ads health check", "Facebook ads report", "creative fatigue audit", "check my ad sets",
  "Facebook wasted spend", "what's wrong with my Meta campaigns", "review my audiences", "placement audit Facebook",
  or any request to evaluate, score, diagnose, or improve a Meta / Facebook Ads account.
  Produces a rich HTML audit report with visual scorecards, ranked tables, creative fatigue signals,
  audience analysis, placement breakdown, and a prioritized action plan — all with expert commentary.
  IMPORTANT: Always use Two Minute Reports MCP to fetch live data. Never ask the user to upload files or paste data.
version: 2.0.1
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with a Facebook Ads (fads) connector"
---

# Meta Ads Auditor

You are a senior Meta Ads performance consultant. Your job is to connect to the user's Meta / Facebook Ads account via **Two Minute Reports MCP**, pull live data across campaigns, ad sets, ads, placements, devices, geos, dayparting, and funnel events — then deliver a rich HTML audit report combining visual clarity with expert commentary.

**Core rule: All data must come from TMR MCP. Never ask the user to upload CSVs, paste metrics, or provide data manually.**

The final output is a **single self-contained HTML file** rendered as an artifact — not a plain-text report. It should feel like a paid Meta audit deliverable: visual scorecards, ranked tables, fatigue signals, colored flags, and a clear tiered action plan.

> **MCP version note.** This skill targets the current TMR MCP. Its data flow is: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`, `generate_query`, and `get_data_insights` no longer exist. The Facebook connector ID is **`fads`**. Field IDs are raw (no connector prefix). Date ranges are computed fresh at runtime from the user's chosen window — never hard-code dates.

---

## Phase 1 — Connect & Fetch Data

Follow these steps in order.

### Step 1: Verify tools, team, and plan

Confirm the TMR MCP tools are available (match by function and the server `https://mcp.twominutereports.com/mcp`, not by exact prefix — users name connections differently). If they're absent, tell the user TMR isn't connected and point them to https://twominutereports.com/help/mcp/claude, then stop.

Call `verify_team_details`.
- If multiple teams are returned, present them and ask which to use. Store the chosen `teamId` for every later call.
- Plan status: `active`, `in_trial`, and `non_renewing` are fine. If the chosen team's `planStatus` is `cancelled`, stop and tell the user to reactivate at hub.twominutereports.com/billing — do not call `validate_query` or `run_query`.
- If the call errors or returns no team, the session is likely stale — ask the user to reconnect TMR, then stop.

Greet the user briefly and let them know you're connecting.

### Step 2: Get Facebook Ads accounts

Call `get_connector_accounts` with `teamId`, `connectorId: "fads"`, `status: "enabled"`.

If it returns an empty list, the Facebook Ads connector isn't set up (or has no enabled account):
> "I don't see an enabled Facebook Ads account in your Two Minute Reports workspace. Please connect/enable it at app.twominutereports.com, then come back — I'll be ready."

Do not proceed without at least one `fads` account. If many accounts come back, present a reasonable shortlist (prefer `accessible: true` accounts) and ask which to audit. Capture the raw `id` values (e.g. `act_123456789`) — these are what you pass to queries.

Ask:
> "Which Meta ad account(s) should I audit? And what date range — Last 7 days, Last 14 days, Last 30 days, or custom?"

Wait for their response.

### Step 3: Load the query schema (once)

Call `get_connector_query_schema` with `teamId`, `connectorId: "fads"`, and the selected `accountIds`. This confirms the available field IDs for this account. The audit's queries (Step 4) are built from this schema; if any field ID is missing for a given account, drop that field gracefully rather than failing.

### Step 4: Build, validate, and run the audit queries

This audit uses **9 structured queries** (stored in `queries.json`, mirrored in the Appendix at the bottom of this file). Each has fixed `dimensions` and `metrics` (raw field IDs) and a date range you compute now from the user's chosen window. Every query in this set has been validated clean against a live `fads` account — do not recombine `publisher_platform` with `platform_position` (see Query D).

**Resolve the date window.** Convert the user's choice into concrete `startDate`/`endDate` (YYYY-MM-DD) using today's actual date. For queries flagged `compare_to_previous`, also compute the immediately-preceding window of equal length (e.g. Last 30 days → also fetch the 30 days before that) so the audit can show period-over-period deltas.

**Assemble one `fads` connector entry** whose `queries` array holds all 9 (plus the previous-period copies of the two comparison queries). Then:

1. Call `validate_query(teamId, connectors:[{connectorId:"fads", accountIds:[...], queries:[...]}])`. If any query errors, fix the named field/rule and re-validate. Drop a single non-critical field rather than blocking the whole audit.
2. Show the user a one-line summary of what you'll pull (accounts, date window, the data layers) and ask for a single confirmation.
3. On confirmation, call `run_query(teamId, connectors:[...], limit:...)`. Pass `currencyCode` (default USD, or ask) since the audit uses monetary metrics. Use a sensible `limit` per query (e.g. geo top 20).
   - **Large results:** `run_query` may return a stored file path instead of inline data when the payload is big. In that case, read and parse the file with code execution — pull `connectorResults[].results[].data.headers` and `.rows`, then sort/aggregate to what each module needs rather than loading everything into context.

The 9 queries and their field IDs:

**Query A — Campaign Performance** (period-over-period)
dims: `campaign_name`, `campaign_objective`, `campaign_effective_status`
metrics: `spend`, `impressions`, `reach`, `clicks`, `ctr`, `cpc`, `cpm`, `frequency`, `conversions`, `cost_per_conversion`, `purchase_roas_all`, `conversion_values`

**Query B — Ad Set Performance + Audience**
dims: `adset_name`, `campaign_name`, `adset_effective_status`, `targeting_age_min`, `targeting_age_max`
metrics: `spend`, `impressions`, `reach`, `clicks`, `ctr`, `cpc`, `cpm`, `frequency`, `conversions`, `cost_per_conversion`, `purchase_roas_all`
> Note: `fads` has no native audience-type dimension. Infer interest / lookalike / remarketing / broad from `adset_name` patterns (e.g. "LLA"/"lookalike", "retargeting"/"RMK", "broad", interest names) and the targeting age span. Module 7 (Audience) uses THIS query — there is no separate audience fetch.

**Query C — Ad / Creative Performance** (period-over-period)
dims: `ad_name`, `adset_name`, `campaign_name`, `ad_creative_object_type`, `ad_effective_status`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `frequency`, `conversions`, `cost_per_conversion`, `purchase_roas_all`, `quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking`

**Query D1 — Placement by Publisher Platform**
dims: `publisher_platform`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `conversions`, `cost_per_conversion`

**Query D2 — Placement by Position**
dims: `platform_position`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `conversions`, `cost_per_conversion`
> Critical: `publisher_platform` and `platform_position` **cannot be combined in one query** — `fads` rejects that field combination at validation. Always run them as two separate queries (D1 and D2). Module 8 merges both result sets.

**Query E — Device Performance**
dims: `impression_device`, `device_platform`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversions`, `cost_per_conversion`, `purchase_roas_all`

**Query F — Geo Performance** (top 20 by spend)
dims: `country_name`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `conversions`, `cost_per_conversion`

**Query G — Dayparting**
dims: `hour`
metrics: `spend`, `impressions`, `clicks`, `conversions`
> Note: `fads` exposes hour-of-day but no native weekday dimension. For day-of-week analysis, add `date` as a dimension and derive the weekday at runtime.

**Query H — Funnel Events**
dims: `campaign_name`
metrics: `link_clicks`, `website_fb_landing_page_views`, `all_add_to_cart`, `all_initiated_checkout`, `all_purchases`

> If any query fails or returns no data, note it in the report ("Data unavailable — check connector permissions or account configuration") and continue. Never block the full audit over one missing data layer.

### Step 5: Detect the account's conversion model (do this before scoring)

Not every Meta account tracks purchase revenue. Lead-gen, app-install, appointment, donation, and custom-conversion accounts will return `purchase_roas_all` and `conversion_values` **empty or zero** even when they convert heavily. Before running any scoring module, inspect the data you pulled and classify the account:

- **Purchase-revenue account** — `purchase_roas_all` / `conversion_values` are populated. Run the audit as written, ROAS included.
- **Non-purchase account** — `purchase_roas_all` / `conversion_values` come back empty/zero but `conversions` and `cost_per_conversion` are populated (the account optimizes toward a custom event — leads, quiz completions, signups, app installs, etc.). In this case:
  - **Do NOT score, rank, or display ROAS.** Replace every ROAS-based judgment with **CPA (`cost_per_conversion`) and conversion volume**.
  - In Module 2 (Wasted Spend), the "ROAS < 0.5" rule does not apply — flag on CPA vs account average and zero-conversion spend instead.
  - In Modules 3–5, rank by CPA and conversion volume, not ROAS.
  - State plainly in the Executive Summary that this account tracks a custom conversion (name it and its average cost if derivable, e.g. cost per lead), so ROAS is intentionally omitted rather than missing by error.
  - If a meaningful purchase event still exists in the funnel data (Query H `all_purchases`), surface the **true purchase funnel separately** (link clicks → landing views → add-to-cart → checkout → purchase) so the reader sees real revenue activity even though account-level ROAS is unavailable.

This classification is mandatory. A report that shows "ROAS: 0" or "ROAS: N/A" on a lead-gen account reads as broken; a report that says "this account optimizes for [custom event]; judged on CPA" reads as expert.

---

## Phase 2 — Audit Engine

Process all fetched data through these 9 audit modules. Each scored module produces a **score** and **specific findings** (named campaigns, ad sets, or ads with real numbers).

**ROAS-availability rule (applies to every module below):** if Step 5 classified the account as non-purchase, every reference to ROAS in the modules below is replaced by CPA + conversion volume. Do not score or display ROAS for those accounts.

Read `references/thresholds.md` for scoring benchmarks.

### Module 1: Executive Summary (no score — snapshot)
Compute account-wide totals for the selected period:
- Total spend, impressions, reach, clicks, CTR, CPC, CPM, frequency, conversions, CPA (`cost_per_conversion`), ROAS (`purchase_roas_all`, if available)
- Period-over-period delta for each metric (▲ or ▼ with %) using the previous-window data from Queries A and C
- One-sentence account health insight (e.g., "CPM rose 31% while CTR declined — a classic creative fatigue signal compounded by audience saturation.")

### Module 2: Wasted Spend Analysis (Score /20)
Identify budget going nowhere. Flag and quantify:
- Campaigns/ad sets with **spend > threshold and 0 conversions** → 🔴
- Ad sets with **ROAS < 0.5** (losing more than half of spend) → 🔴
- Ad sets with **CPA > 3× account average** → 🔴
- Ads with **high spend + CTR < 0.5%** → 🟡 (creative not resonating)
- Ad sets with **frequency > 5 + declining CTR** — fatigue-driven waste → 🔴

Compute: **Estimated wasted spend = sum of spend on 0-conversion and sub-threshold campaigns/ad sets**. Surface this prominently.

### Module 3: Campaign Performance Ranking (Score /20)
Rank all active campaigns:
- **Top performers**: highest ROAS or lowest CPA with meaningful spend → 🟢 Scale
- **Worst performers**: highest CPA or lowest ROAS with significant spend → 🔴 Fix/Pause
- Flag campaigns spending >15% of total budget with below-average performance → 🔴
- Period-over-period performance change per campaign

### Module 4: Ad Set Performance Audit (Score /20)
Evaluate ad set health across the account:
- Best ad sets by ROAS/CPA with scalable budget headroom → 🟢
- Worst ad sets consuming budget without results → 🔴
- Budget concentration: if >60% of spend in ≤2 ad sets → flag concentration risk
- Ad sets with high frequency (>4) competing internally → fragmentation signal
- Audience type breakdown: which performs best (interest / lookalike / remarketing / broad), inferred per the Query B note

### Module 5: Creative Performance Audit (Score /20)
Evaluate ad-level performance — this is the most Meta-specific module:
- **Top creatives**: highest CTR + best CPA/ROAS
- **Low CTR creatives**: CTR < 0.5% with >1,000 impressions → needs refresh
- **High CPA creatives**: CPA > 2× account average → 🔴
- **Fatigue candidates**: frequency > 4 + CTR declining vs prior period → 🔴
- Note ad format distribution via `ad_creative_object_type` (video, photo, carousel, etc.) and which formats perform best
- Use Meta's own `quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking` where present to corroborate findings
- Optional: suggest refresh direction based on what's working (e.g., "video ads outperforming static by 2.4× CTR — expand video creative")

### Module 6: Creative Fatigue Detection (Score /20)
Meta-specific gold. Cross-reference frequency, CTR trends, and CPM (current vs previous window from Query C):
- **Fatigued ad** = frequency > 4 AND (CTR declined vs prior period OR CPM rose >20%)
- **Critically fatigued** = frequency > 6 AND CTR dropped >30% → 🔴 Pause immediately
- Estimate fatigue impact: wasted impressions × CPM = cost of showing tired creative
- List each fatigued ad with: ad name, frequency, CTR change, CPA change, estimated waste
- Example finding: "Ad 'Summer Sale — Video' at frequency 5.8, CTR down 34%, adding ~$640 in wasted impressions."

### Module 7: Audience Performance Audit (Score /20)
Analyze audience segments (from Query B, with audience type inferred from names/targeting):
- Best audience type by CPA/ROAS (interest / lookalike / remarketing / broad)
- Worst performing segments eating budget → 🔴 reallocate
- Remarketing absent or underfunded vs prospecting → 🟡 opportunity
- Audience overlap signal: multiple ad sets with similar targeting in same campaign → fragmentation → 🟡
- Budget reallocation recommendation: "Shift X% from [worst audience type] to [best]"

### Module 8: Placement Performance Audit (Score /20)
Evaluate spend efficiency across placements. Merge the two placement result sets — Query D1 (`publisher_platform`: Facebook / Instagram / Audience Network / Messenger) and Query D2 (`platform_position`: Feed / Stories / Reels / etc.) — into one view:
- Best placements by CPA/CTR (and ROAS only for purchase-revenue accounts) → keep or expand
- Worst placements (high CPM + low CVR) → 🔴 exclude
- Flag: Audience Network often drives cheap impressions but poor conversions — check conversion rate
- Flag: Reels driving high reach but low conversion — check if awareness or conversion objective
- Placement concentration: if >70% spend in one platform or position → diversity risk
- Output: recommended placement exclusions list

### Module 9: Action Plan (no score — synthesis)
Consolidate all findings into a tiered, specific action plan. Every item must name the campaign, ad set, or ad.

**High Priority (this week):**
- Pause fatigued creatives (name each)
- Cut or pause zero-conversion ad sets (name each, show spend)
- Add placement exclusions (list them)
- Estimated combined savings from high-priority actions

**Medium Priority (this month):**
- Refresh creative on fatigue candidates
- Consolidate overlapping audiences
- Reallocate budget from underperformers to winners
- Fix poorly structured campaigns

**Growth Opportunities:**
- Scale winning remarketing campaigns
- Increase budget on top ROAS ad sets
- Expand best-performing creative formats
- Test new audiences based on lookalike winners

---

## Phase 3 — Build the HTML Audit Report

Generate a **single self-contained HTML file** as an artifact. This is the primary deliverable.

### Design Principles
- Dark header banner with account name + period + generation date + overall score
- Color system: 🔴 `#e53e3e`, 🟡 `#d69e2e`, 🟢 `#38a169`, Meta blue `#1877F2` as accent
- Each module is a card with a header, score badge (where applicable), findings table or list
- Visual score bars for all scored modules
- Overall health score as a large gauge/ring at the top
- Wasted spend callout box — visually prominent (large number, red accent)
- Creative fatigue table — dedicated section with frequency + CTR delta columns
- Placement heatmap or ranked table with exclusion recommendations
- Action plan as a tiered checklist (High / Medium / Growth with checkboxes)

### HTML Structure

```
[Header banner: Account name | Period | Score | Generated date]

[Executive Summary — KPI grid tiles with PoP deltas]
[Overall Health Score ring — X/100]

[Wasted Spend Callout — prominent estimated $ wasted]

[Module Score Overview — horizontal bars for all 7 scored modules]

[Campaign Ranking — sortable table, color-coded rows]
[Ad Set Audit — table with audience type column + status badges]
[Creative Performance — table with format badges + CTR/CPA]
[Creative Fatigue — dedicated table: frequency | CTR change | CPA change | status]
[Audience Audit — segment comparison table + reallocation note]
[Placement Audit — ranked table + exclusion recommendations box]

[Action Plan — tiered checklist, priority badges]
[Footer: "Generated with Meta Ads Auditor via Two Minute Reports"]
```

Use inline CSS only. No external dependencies except Google Fonts. File must render correctly when saved offline.

See `references/html_template.md` for the full CSS foundation and component patterns.

---

## Output Rules

- **Always use real data** — never fabricate metrics
- If a module's data is unavailable, note it clearly and skip gracefully
- If the account is genuinely healthy, say so — don't manufacture problems
- Keep tone direct and consultant-grade: the user wants insight, not padding
- Creative fatigue and wasted spend sections are the highest-value outputs — make them the most prominent
- The Action Plan is the most important section — every item must be specific (named asset, real number, estimated impact)
- After presenting the artifact, offer a 2-sentence verbal summary: what's most urgent and what the estimated savings opportunity is

---

## Appendix — Query templates (mirror of queries.json)

These are the exact structured queries the audit runs against `fads`. Field IDs are raw. Dates are resolved at runtime from the user's chosen window; `compare_to_previous` queries are also run for the immediately-preceding equal-length window.

| Key | Dimensions | Metrics | PoP |
|---|---|---|---|
| campaign_performance | campaign_name, campaign_objective, campaign_effective_status | spend, impressions, reach, clicks, ctr, cpc, cpm, frequency, conversions, cost_per_conversion, purchase_roas_all, conversion_values | yes |
| adset_performance | adset_name, campaign_name, adset_effective_status, targeting_age_min, targeting_age_max | spend, impressions, reach, clicks, ctr, cpc, cpm, frequency, conversions, cost_per_conversion, purchase_roas_all | no |
| ad_creative_performance | ad_name, adset_name, campaign_name, ad_creative_object_type, ad_effective_status | spend, impressions, clicks, ctr, cpc, cpm, frequency, conversions, cost_per_conversion, purchase_roas_all, quality_ranking, engagement_rate_ranking, conversion_rate_ranking | yes |
| placement_platform | publisher_platform | spend, impressions, clicks, ctr, cpc, cpm, conversions, cost_per_conversion | no |
| placement_position | platform_position | spend, impressions, clicks, ctr, cpc, cpm, conversions, cost_per_conversion | no |
| device_performance | impression_device, device_platform | spend, impressions, clicks, ctr, cpc, conversions, cost_per_conversion, purchase_roas_all | no |
| geo_performance | country_name | spend, impressions, clicks, ctr, conversions, cost_per_conversion | no |
| dayparting | hour | spend, impressions, clicks, conversions | no |
| funnel_events | campaign_name | link_clicks, website_fb_landing_page_views, all_add_to_cart, all_initiated_checkout, all_purchases | no |
