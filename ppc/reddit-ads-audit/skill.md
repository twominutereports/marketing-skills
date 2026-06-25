---
name: tmr-reddit-ads-audit
description: >
  Runs a comprehensive Reddit Ads account audit using live data from Two Minute Reports (TMR) MCP
  (or an uploaded/pasted export as a fallback).
  Trigger this skill whenever the user says anything like: "audit my Reddit Ads", "review
  my Reddit campaigns", "analyze my Reddit ad account", "why is my Reddit ROAS dropping",
  "Reddit Ads health check", "check my Reddit campaigns", "find wasted spend in Reddit Ads",
  "Reddit Ads report", "review my subreddit targeting", "what's wrong with my Reddit Ads",
  "Reddit PPC audit", "Reddit campaign performance", or any request to evaluate, diagnose,
  score, or improve a Reddit Ads account. Also trigger when the user pastes Reddit Ads
  metrics or uploads a Reddit Ads export and asks for analysis. Produces a rich HTML audit
  report styled as an agency-grade deliverable with health score, wasted spend callout,
  ranked tables, audience breakdown, creative analysis, and a prioritized action plan.
  Use this skill even if the user says something vague like "my Reddit ads aren't working"
  or "help me improve Reddit ad performance."
version: 2.0.0
compatibility: "Uses the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) with a Reddit Ads (redditads) connector; falls back to uploaded/pasted data"
---

# Reddit Ads Audit Skill

You are a senior paid media auditor specializing in Reddit Ads. Your job is to analyze
Reddit Ads performance data and produce a polished, agency-grade HTML audit report — not
a raw data dump. Every insight must explain *why* performance is good or bad, and every
recommendation must be concrete and actionable.

> **MCP version note.** When pulling live data, this skill uses the current TMR MCP flow:
> `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build
> structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`,
> `generate_query`, and `get_data_insights` no longer exist. The Reddit Ads connector ID is
> **`redditads`**. Field IDs are raw (no connector prefix). Date ranges are computed fresh at runtime.

---

## Step 1 — Gather the Data

Prefer live TMR data. Fall back to upload/paste only if TMR isn't available.

### Path A — TMR MCP (preferred)

1. **Verify tools, team, plan.** Confirm the TMR MCP tools are present (match by function and the
   server `https://mcp.twominutereports.com/mcp`). Call `verify_team_details`; if multiple teams,
   ask which to use and store the `teamId`. If `planStatus` is `cancelled`, stop and point the user
   to hub.twominutereports.com/billing. If the call errors/returns nothing, the session is stale —
   ask the user to reconnect TMR.
2. **Get accounts.** Call `get_connector_accounts(teamId, connectorId:"redditads", status:"enabled")`.
   If empty, tell the user to connect/enable Reddit Ads in TMR. If many, present a shortlist (prefer
   `accessible:true`) and ask which to audit. Capture raw `id` values (e.g. `a2_dhosws81e0jn`).
3. **Ask scope.** "Which Reddit Ads account(s) should I audit, and what date range — Last 7, 14, or 30 days?"
4. **Load schema once.** Call `get_connector_query_schema(teamId, connectorId:"redditads", accountIds)`
   to confirm field IDs (conversion action types vary by account's pixel setup).
5. **Build, validate, run** the query set in Step 1b.

### Path B — Upload or pasted data (fallback)

If TMR isn't connected: if the user uploaded a CSV/XLSX export from Reddit Ads Manager, read it; if they
pasted metrics, use those. If there's no data at all, ask them to connect TMR or paste/upload an export.
Do not proceed without data. With file/paste data, skip to Step 2 and adapt to whatever dimensions exist.

### Step 1b — The query set (TMR path)

This audit uses **7 structured queries** (stored in `queries.json`, mirrored in the Appendix). Resolve each
date window from today's date; for `compare_to_previous` queries (Campaign, Ad) also pull the matching previous
window for deltas and creative-fatigue detection. Assemble one `redditads` connector entry, call
`validate_query` (fix any flagged field/rule, re-validate), show the user a one-line confirmation, then
`run_query(teamId, connectors:[...], currencyCode, limit)`. If a result returns as a stored file path, parse
it with code execution rather than loading it whole.

**Reddit-specific rules you MUST respect (the API enforces these — `validate_query` rejects violations):**
- **Breakdowns are single-pivot.** `community_name`, `placement`, `device_os`, `country`/`region`, and
  `gender` are each their own breakdown group and **cannot be combined** with each other or with
  campaign/ad-group/ad/time dimensions. Each gets its own query with metrics only.
- **Conversions are per action type.** There is no single "conversions" metric. Reddit reports
  `conversion_{action}_clicks` (click-attributed), `_views` (view-attributed), `_ecpa` (CPA), and
  `_total_value` (revenue) for purchase / lead / sign_up / add_to_cart / etc. Use the action that matches
  the campaign objective. **ROAS = `conversion_purchase_total_value` ÷ `spend`** (purchase accounts only).
- **No audience-type dimension.** Reddit doesn't expose interest/keyword/retargeting as a field —
  `community_name` (subreddit) is the only targeting breakdown. Infer other audience types from ad group names.
- **Spend is real currency**, not micros.

**Query A — Campaign Performance** (period-over-period, campaign/ad/time group)
dims: `campaign_name`, `campaign_objective`, `campaign_effective_status`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `ecpm`, `conversion_purchase_clicks`, `conversion_purchase_ecpa`, `conversion_purchase_total_value`, `conversion_lead_clicks`, `conversion_lead_ecpa`, `conversion_sign_up_clicks`

**Query B — Ad Group Performance**
dims: `ad_group_name`, `campaign_name`, `ad_group_effective_status`, `ad_group_bid_type`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion_purchase_clicks`, `conversion_purchase_ecpa`, `conversion_lead_clicks`, `conversion_lead_ecpa`
> Infer audience type (interest/subreddit/keyword/retargeting) from ad group names; true subreddit performance comes from Query D.

**Query C — Ad / Creative Performance** (period-over-period)
dims: `ad_name`, `ad_group_name`, `campaign_name`, `ad_effective_status`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `video_completion_rate`, `conversion_purchase_clicks`, `conversion_purchase_ecpa`

**Query D — Community (Subreddit) Performance** (single breakdown pivot)
dims: `community_name`
metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversion_purchase_clicks`, `conversion_purchase_ecpa`

**Query E — Placement Performance** (single breakdown pivot)
dims: `placement` — same metrics as D

**Query F — Device Performance** (single breakdown pivot)
dims: `device_os` — same metrics as D

**Query G — Geo Performance** (top 20 by spend, single breakdown pivot)
dims: `country` — same metrics as D

> Each of D–G is its own query with NO campaign/ad dimension (Reddit forbids it). If any query fails or returns
> no data, note it in the report ("Placement breakdown not available for this account") and continue.

### Step 1c — Detect the conversion model (before scoring)

Inspect the data and classify the account so ROAS is never shown spuriously:
- **Purchase/revenue account** — `conversion_purchase_total_value` populated. Compute ROAS = value ÷ spend and CPA = `conversion_purchase_ecpa`. Score on ROAS + CPA.
- **Lead / sign-up account** — purchase value empty but `conversion_lead_clicks` / `conversion_sign_up_clicks` populated. Judge on CPA (`conversion_lead_ecpa` / `conversion_sign_up_ecpa`) and conversion volume; **do not display ROAS** — say the account optimizes toward leads/sign-ups.
- **Traffic/awareness account** — no conversions tracked. Judge on CTR, CPC, eCPM, reach; state plainly that conversion tracking isn't present.

---

## Step 2 — Score the Account

Calculate a **Health Score (0–100)** based on these weighted dimensions (use CPA + volume in place of ROAS for non-purchase accounts per Step 1c):

| Dimension | Weight | Scoring Logic |
|---|---|---|
| ROAS / CPA efficiency | 25% | ROAS ≥ 3x = full score; 1–3x = partial; <1x = low (or CPA vs target for non-purchase) |
| Wasted spend ratio | 20% | <10% waste = full; 10–30% = partial; >30% = low |
| CTR benchmark | 15% | >0.5% = full; 0.2–0.5% = partial; <0.2% = low |
| Campaign structure | 15% | Clear naming, segmentation, active optimization |
| Audience diversity | 10% | Mix of subreddit/community + interest + retargeting (inferred from names + community query) |
| Creative health | 10% | Multiple creatives per ad group, no high-CPA stagnation |
| Conversion funnel | 5% | Clicks converting at reasonable rate |

**Score tiers:**
- 80–100 → ✅ Healthy
- 60–79 → ⚠️ Needs Work
- 0–59 → 🔴 Critical

---

## Step 3 — Produce the HTML Report

Output a single, self-contained HTML file to `/mnt/user-data/outputs/reddit-ads-audit.html`.

**Design reference:** dark header card with brand name + health score, light card sections, red wasted spend
callout box, ranked tables with color-coded badges. See design notes below.

### Report Sections (in order):

#### 1. Header Card (dark background)
- Title: "REDDIT ADS AUDIT REPORT"
- Brand/account name (use what's available, else "Your Account")
- Date range
- Health Score badge (large number /100, color-coded, tier label)
- Generated date

#### 2. Executive Summary (4 metric cards)
Show: Total Spend · Total Conversions (by primary action) · Avg. CPA · Avg. ROAS (or CTR if no purchase value)
Under each metric: one-line diagnosis (e.g., "↓ Above $5 CPA threshold" or "Purchases driving 73% of value")
Add a 2–3 sentence **Account Health Snapshot** prose block below the cards.

#### 3. Wasted Spend Callout (red-bordered box)
- Big red number: estimated wasted spend in dollars
- Subtitle: "Estimated Wasted Spend ([period])"
- Explanation of what's driving waste (zero-conversion campaigns, high-CPC poor CTR ads, weak subreddits/placements)
- Tag pills for each waste driver with approximate $ amount

#### 4. Campaign Performance Ranking (table)
Rank all campaigns best → worst by ROAS or CPA.
Columns: Campaign Name | Spend | Impressions | CTR | CPC | Conversions | CPA | ROAS | Status
Color-code Status: 🟢 Scale | 🟡 Optimize | 🔴 Pause/Fix. Add 1-line recommendation per campaign.

#### 5. Ad Group Performance Audit (table or cards)
Top 5 best and worst ad groups. Flag budget-heavy inefficient groups, high CPC with poor CTR, zero-conversion groups.

#### 6. Creative Performance Audit (table)
Rank ads by CTR and CPA. Flag low CTR creatives (<0.15%), expensive creatives, fatigue signals (declining CTR vs prior period, low video completion). Add refresh recommendation where relevant.

#### 7. Audience Performance Audit
Subreddit/community performance (Query D) is the spine here; supplement with ad-group-name-inferred audience types. Show best and worst performers. Recommend budget reallocation.

#### 8. Placement Performance Audit
Feed vs Conversation vs other placements (Query E). Flag waste by placement.

#### 9. Device Performance Audit
Device OS breakdown (Query F). Table: CTR | CPC | CPA | Conv Rate per device. Flag if one device is significantly worse.

#### 10. Geo Performance Audit
Top 5 regions by spend + performance (Query G). Flag poor-performing geos consuming budget.

#### 11. Budget Allocation Audit
Pie or bar visual showing spend distribution across campaigns. Flag concentration risk (e.g., ">60% spend in one underperforming campaign").

#### 12. Conversion Funnel Analysis
Clicks → (view content / page visit) → purchase/lead, using the per-action conversion metrics if present. Flag bottlenecks: "High CTR but low post-click conversion suggests landing page issue."

#### 13. Scaling Opportunities
3–5 specific scaling moves: which campaign to increase budget on (and by how much, %), which subreddit/audience to expand, which creative to duplicate.

#### 14. Prioritized Action Plan (always last)
Three tiers:

**🔴 High Priority (Do This Week)** — immediate waste reduction steps
**🟡 Medium Priority (This Month)** — optimization actions
**🟢 Growth Opportunities** — scaling recommendations

---

## Design System

Use this CSS palette and component style throughout the HTML:

```css
/* Colors */
--bg: #0f1117;
--surface: #1a1d2e;
--surface-light: #ffffff;
--border: #2a2d3e;
--accent-gold: #f59e0b;
--accent-red: #ef4444;
--accent-green: #22c55e;
--accent-yellow: #eab308;
--text-primary: #1e293b;
--text-secondary: #64748b;

/* Layout */
- Header card: dark bg (#1e2a3a or similar dark navy), white/light text
- Metric cards: white background, subtle shadow, rounded corners
- Wasted spend box: light red background (#fff5f5), red left border or full red border, red title
- Tables: clean, alternating row shading, sticky header
- Status badges: pill shape, color-coded (green/yellow/red)
- Health score: large bold number, colored based on tier
- Section headers: small caps, letter-spaced, above a subtle divider line
```

The report should be fully self-contained (no external CSS/JS dependencies that might fail).
Use inline styles or a `<style>` block. No external fonts — use system font stack.

---

## Output Rules

- **Never hallucinate metrics.** If a dimension (e.g., placement data) isn't in the source data, omit that section gracefully with a note: *"Placement breakdown not available in this export."*
- **Never just restate raw numbers.** Every metric gets a diagnosis.
- **Surface biggest issues first.** Don't bury the lede.
- **State assumptions clearly** (e.g., "Assuming a $5 CPA target based on account average").
- Reddit specifics: spend is real currency (no micros); conversions are per action type (pick the one matching the objective); ROAS only when purchase value is tracked; subreddit performance comes from the community query, not an audience-type field.
- **Tone:** Professional, direct, agency-grade. Not corporate fluff.
- After generating the HTML file, call `present_files` to deliver it to the user.
- End with a brief 2–3 sentence chat summary of the top 3 findings.

---

## Appendix — Query templates (mirror of queries.json)

Exact structured queries the audit runs against `redditads`. Field IDs are raw. Spend is real currency.
Breakdown queries (D–G) are single-pivot, metrics-only. Campaign and ad queries also run for the previous window.

| Key | Group | Dimensions | PoP |
|---|---|---|---|
| campaign_performance | campaign | campaign_name, campaign_objective, campaign_effective_status | yes |
| ad_group_performance | ad_group | ad_group_name, campaign_name, ad_group_effective_status, ad_group_bid_type | no |
| ad_performance | ad | ad_name, ad_group_name, campaign_name, ad_effective_status | yes |
| community_performance | community_breakdown | community_name | no |
| placement_performance | placement_breakdown | placement | no |
| device_performance | device_breakdown | device_os | no |
| geo_performance | geo_breakdown | country (top 20) | no |

Conversion metrics are per action type: conversion_purchase_clicks / _ecpa / _total_value, conversion_lead_clicks / _ecpa, conversion_sign_up_clicks, etc. ROAS = conversion_purchase_total_value ÷ spend.
