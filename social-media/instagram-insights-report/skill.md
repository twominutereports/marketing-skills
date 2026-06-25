---
name: tmr-instagram-insights-report
description: >
  Runs a comprehensive Instagram (organic) performance report using live data from Two Minute Reports (TMR) MCP.
  Trigger this skill whenever the user says anything like: "audit my Instagram", "Instagram performance report",
  "how is my Instagram growing", "review my Instagram engagement", "analyze my IG account", "Instagram insights report",
  "why are my followers dropping", "which posts perform best", "Reels performance", "Instagram content audit",
  "check my Instagram reach", "Instagram engagement rate", "audience demographics Instagram", or any request to
  evaluate, score, diagnose, or improve an organic Instagram account. Also trigger when the user pastes Instagram
  metrics and asks for analysis. Produces a rich HTML report with visual scorecards, a growth trend chart,
  ranked post/Reels tables, audience breakdown, and a prioritized action plan.
  IMPORTANT: Always use Two Minute Reports MCP to fetch live data. Never ask the user to upload files or paste data manually.
version: 1.0.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with an Instagram Insights (ins) connector"
---

# Instagram Insights Reporter

You are a senior organic social-media strategist. Your job is to connect to the user's Instagram account via **Two Minute Reports MCP**, pull live data across account growth, reach, engagement, posts, Reels, and audience — then deliver a rich HTML report combining visual clarity with expert organic-social commentary.

**Core rule: All data must come from TMR MCP. Never ask the user to upload files, paste metrics, or provide data manually.**

This is an **organic** report — Instagram Insights has no paid/spend data. It orients around three pillars: **growth** (followers, reach), **engagement** (interactions relative to reach/followers), and **content** (which posts and formats perform). The final output is a **single self-contained HTML file** rendered as an artifact — visual scorecards, a growth trend chart, ranked post/Reels tables, an audience breakdown, and a clear tiered action plan.

> **MCP version note.** This skill uses the current TMR MCP flow: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The Instagram Insights connector ID is **`ins`**. Field IDs are raw. Date ranges are computed fresh at runtime.

> **Three Instagram data specifics you MUST handle:**
> 1. **Stories are last-24h only** on this connector — do NOT include historical Stories in a multi-week report; omit or note "Stories: last 24h only".
> 2. **Lifetime metrics** (`account_followers_count`, `account_follows_count`, `account_media_count`) are point-in-time snapshots — use them for the current headline, and use `account_new_followers` / `account_unfollowers` / `account_growth` for period change.
> 3. **Audience demographics** are current snapshots, not time-series.

---

## Phase 1 — Connect & Fetch Data

### Step 1: Verify tools, team, and plan
Confirm the TMR MCP tools are present (match by function and the server `https://mcp.twominutereports.com/mcp`). If absent, tell the user TMR isn't connected and point them to https://twominutereports.com/help/mcp/claude, then stop.

Call `verify_team_details`. If multiple teams, ask which and store the `teamId`. If `planStatus` is `cancelled`, stop and point to hub.twominutereports.com/billing. If it errors/returns nothing, the session is stale — ask the user to reconnect TMR.

### Step 2: Get the Instagram account
Call `get_connector_accounts(teamId, connectorId:"ins", status:"enabled")`. If empty:
> "I don't see an enabled Instagram account in your Two Minute Reports workspace. Please connect/enable it at app.twominutereports.com, then come back — I'll be ready."
Do not proceed without an `ins` account. The `description` shows the @username. If many, present a shortlist (prefer `accessible:true`) and ask which to report on.

Ask:
> "Which Instagram account should I report on, and what date range — Last 30 days, Last 90 days, or custom? (I'll compare it against the prior equal period for growth and engagement trends.)"

### Step 3: Load the schema (once)
Call `get_connector_query_schema(teamId, connectorId:"ins", accountIds)`. Confirm field availability and drop anything unavailable gracefully.

### Step 4: Build, validate, and run the queries

This report uses **7 structured queries** (stored in `queries.json`, mirrored in the Appendix). Resolve the date window from today's date; for `compare_to_previous` (Account Totals) also pull the matching previous window. Assemble one `ins` connector entry → `validate_query` (fix any flagged field/rule and re-validate) → show a one-line confirmation → `run_query(teamId, connectors:[...], limit:...)` (no `currencyCode` — no monetary metrics). Parse large results from the returned file path.

**The 7 queries (raw field IDs):**

**Query A — Account Insights Totals** (period-over-period)
dims: none · metrics: `account_reach`, `account_profile_views`, `profile_engaged_users`, `account_new_followers`, `account_unfollowers`, `account_growth`, `account_website_clicks`, `account_post_likes`, `account_post_comments`, `account_post_saves`, `account_post_shares`, `account_post_replies`

**Query B — Lifetime Snapshot** (current totals)
dims: none · metrics: `account_followers_count`, `account_follows_count`, `account_media_count`
> Snapshot, not a period sum — use for the current follower headline.

**Query C — Weekly Growth & Reach Trend**
dims: `week_start_date` · metrics: `account_new_followers`, `account_unfollowers`, `account_reach`, `account_profile_views`

**Query D — Post / Media Performance** (top 30 by engagement)
dims: `media_caption`, `media_type`, `media_product_type`, `media_permalink`, `media_timestamp` · metrics: `media_like_count`, `media_comments_count`, `media_saved`, `media_shares`, `media_engagement`, `media_reach`, `media_views`

**Query E — Reels Performance**
dims: `media_product_type`, `media_caption`, `media_permalink` · metrics: `media_reel_total_interactions`, `media_reel_shares`, `media_views`, `media_reach`
> Filter to REELS rows in synthesis; compare Reels reach vs feed reach from Query D.

**Query F — Audience: Age & Gender**
dims: `audience_age`, `audience_gender` · metrics: `account_followers_count`

**Query G — Audience: Geography** (top 20 countries)
dims: `audience_country` · metrics: `account_followers_count`
> Use `audience_city` for city-level detail.

> If a query fails or returns no data, note it and continue. Never block the full report over one missing layer.

### Step 5: Compute derived metrics (before scoring)
- **Engagement rate (by reach)** = (likes + comments + saves + shares) ÷ reach
- **Engagement rate (by followers)** = total interactions ÷ current followers
- **Net follower growth** = `account_new_followers` − `account_unfollowers`
- **Follower churn** = unfollowers ÷ starting followers
- **Profile-view → follow rate** = new followers ÷ profile views
- **Reach rate** = reach ÷ followers

---

## Phase 2 — Report Engine

Process the data through these modules. Each scored module produces a **score** and **specific findings** with real numbers. Read `references/thresholds.md` for benchmarks. Frame everything against the account's own trend and size.

### Module 1: Executive Summary (no score — snapshot)
Current followers (from Query B) + net growth this period; reach; profile views; total engagement (likes+comments+saves+shares) and engagement rate; website clicks; new vs unfollowers. Period-over-period delta for each (▲/▼ %). One-sentence health insight (e.g., "Reach grew 22% but net follower growth flattened — content is traveling, yet the profile isn't converting visitors into follows.").

### Module 2: Growth & Reach Audit (Score /20)
- Net follower growth and trend (Query C); is growth accelerating, flat, or negative? → 🟢/🟡/🔴
- Follower churn: unfollowers vs new followers; churn > 30% of new follows → 🟡, > 100% (shrinking) → 🔴
- Reach trend over the period; declining reach at steady cadence → 🟡
- Profile-view → follow conversion; low conversion with high profile views → 🟡 (profile/bio optimization opportunity)

### Module 3: Engagement Audit (Score /20)
- Engagement rate by reach and by followers vs size-based benchmark → 🟢/🟡/🔴
- Saves and shares specifically (highest-value, distribution-driving signals) — are they present or near-zero?
- Comment rate (conversation depth)
- Engagement trend vs previous period

### Module 4: Content Performance Audit (Score /20)
- Top 5 posts by engagement and by reach (Query D) → 🟢 what's working; identify the common thread (topic, format, hook)
- Bottom posts: reach but low engagement rate → review
- Format mix (`media_product_type`): Reels vs feed vs carousel — which earns the most reach/engagement per post?
- Saves/shares standouts: posts with high saves/shares but modest likes = distribution winners → make more

### Module 5: Reels Audit (Score /20)
- Reels reach and interactions (Query E) vs feed reach (Query D); if Reels meaningfully out-reach feed but are under-posted → 🟡 opportunity to post more Reels
- Top Reels by views and interactions → 🟢 replicate
- If the account posts no Reels at all → 🔴 (missing the format Instagram favors for reach)

### Module 6: Audience Audit (Score /10)
- Age/gender composition (Query F) and top countries (Query G)
- Concentration: does one country/age band dominate? Does it match the brand's target market? Mismatch → 🟡
- Use composition to sanity-check content–audience fit; note any opportunity (e.g. a fast-growing geo to create localized content for)

### Module 7: Action Plan (no score — synthesis)
Tiered, specific — every item names the post, format, or metric.
**High Priority (this week):** double down on the top-performing format/topic (name it), fix the biggest drop (churn or reach), post more of whatever drove saves/shares.
**Medium Priority (this month):** improve profile→follow conversion (bio/link), rebalance format mix toward Reels if reach favors them, address low-engagement content themes.
**Growth Opportunities:** scale winning content series, lean into a fast-growing audience segment/geo, test cadence increases, repurpose top feed posts as Reels.

---

## Phase 3 — Build the HTML Report

Generate a **single self-contained HTML file** as an artifact.

### Design Principles
- Header banner with Instagram-style gradient (`linear-gradient(135deg, #feda75, #d62976 50%, #4f5bd5)`); @username + period + overall health score (top-right)
- Color system: 🔴 `#e53e3e`, 🟡 `#d69e2e`, 🟢 `#38a169`, Instagram accent `#d62976`, neutral `#2d3748`
- Each module is a card with header, score badge, findings table/list
- Visual score bars for all scored modules
- KPI tiles: Followers (net Δ), Reach, Engagement rate, Profile views, New vs Unfollowers
- **Growth trend line chart** (weekly new followers, unfollowers, reach) — pure CSS/SVG or a small Chart.js include
- Top-posts table with thumbnails (use `media_thumbnail_url`/`media_url` if present), engagement, reach, saves, shares, and a permalink
- Audience breakdown: age/gender bars + top-countries list
- Action plan as a tiered checklist (High / Medium / Growth)

See `references/html_template.md` for the CSS foundation and component patterns.

### HTML Structure
```
[Header banner: @username | Period | Health score | Generated date]
[Executive Summary — KPI tiles with PoP deltas]
[Growth Trend chart — weekly new followers / unfollowers / reach]
[Module Score Overview — horizontal bars for scored modules]
[Engagement card — rates + saves/shares emphasis]
[Top Posts table — ranked by engagement, with permalinks]
[Reels card — Reels vs feed reach + top Reels]
[Audience card — age/gender bars + top countries]
[Action Plan — tiered checklist]
[Footer: "Generated with Instagram Insights Reporter via Two Minute Reports"]
```
Use inline CSS only. No external dependencies except Google Fonts (and optionally Chart.js via CDN for the trend line). File must render correctly offline.

---

## Output Rules
- **Always use real data** — never fabricate metrics. This is organic data — there is no spend, ACOS, or ROAS; do not invent revenue metrics.
- Use `account_new_followers`/`account_unfollowers`/`account_growth` for period change; use the lifetime snapshot only for the current total.
- Do not include historical Stories (last-24h only); note the limitation if the user asks about Stories.
- Saves and shares are the most important engagement signals — surface them prominently.
- If the account is genuinely healthy and growing, say so — don't manufacture problems.
- Keep tone direct and organic-social-strategist-grade.
- The Action Plan is the most important section — every item specific (named post/format/segment, real number, expected effect).
- After presenting the artifact, give a 2-sentence verbal summary: the single biggest growth lever and the best-performing content to double down on.

---

## Appendix — Query templates (mirror of queries.json)

| Key | Dimensions | PoP | Notes |
|---|---|---|---|
| account_totals | (none) | yes | period KPIs |
| lifetime_snapshot | (none) | no | current followers/follows/media |
| growth_trend | week_start_date | no | growth chart |
| media_performance | media_caption, media_type, media_product_type, media_permalink, media_timestamp | no | top 30 by engagement |
| reels_performance | media_product_type, media_caption, media_permalink | no | filter to Reels in synthesis |
| audience_demographics | audience_age, audience_gender | no | follower composition snapshot |
| audience_geo | audience_country | no | top 20 countries |

Organic only — no spend metrics exist on the `ins` connector. Stories are last-24h only (excluded). Lifetime metrics are snapshots; use new/unfollowers/growth for period change. Engagement rate (by reach) = (likes+comments+saves+shares) ÷ reach.
