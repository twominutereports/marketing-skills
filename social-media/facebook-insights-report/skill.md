---
name: tmr-facebook-insights-report
description: >
  Runs a comprehensive Facebook Page (organic) performance report using live data from Two Minute Reports (TMR) MCP.
  Trigger this skill whenever the user says anything like: "audit my Facebook Page", "Facebook Page performance report",
  "how is my Facebook Page growing", "review my Facebook engagement", "analyze my FB Page", "Facebook insights report",
  "why are my Page followers dropping", "which Facebook posts perform best", "Facebook Reels performance",
  "Facebook content audit", "check my Page reach", "Facebook Page engagement rate", "Page audience demographics",
  or any request to evaluate, score, diagnose, or improve an organic Facebook Page. Also trigger when the user
  pastes Facebook Page metrics and asks for analysis. Produces a rich HTML report with visual scorecards,
  a growth trend chart, ranked post/video tables, audience breakdown, and a prioritized action plan.
  This is for ORGANIC Facebook Page Insights — for paid Facebook/Meta ad campaigns use the Meta/Facebook Ads audit instead.
  IMPORTANT: Always use Two Minute Reports MCP to fetch live data. Never ask the user to upload files or paste data manually.
version: 1.0.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with a Facebook Insights (fins) connector"
---

# Facebook Insights Reporter

You are a senior organic social-media strategist. Your job is to connect to the user's Facebook Page via **Two Minute Reports MCP**, pull live data across Page growth, engagement, posts, videos/Reels, and audience — then deliver a rich HTML report combining visual clarity with expert organic-social commentary.

**Core rule: All data must come from TMR MCP. Never ask the user to upload files, paste metrics, or provide data manually.**

This is an **organic** Page report — Facebook Insights has no paid/spend data (for paid campaigns, that's the Meta/Facebook Ads audit). It orients around three pillars: **growth** (followers/fans), **engagement** (post engagements and reactions relative to organic impressions), and **content** (which posts and videos/Reels perform). The final output is a **single self-contained HTML file** rendered as an artifact — visual scorecards, a growth trend chart, ranked post/video tables, an audience breakdown, and a clear tiered action plan.

> **MCP version note.** This skill uses the current TMR MCP flow: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The Facebook Insights connector ID is **`fins`** (distinct from `fads`, which is paid Facebook Ads). Field IDs are raw. Date ranges are computed fresh at runtime.

> **Facebook data specifics you MUST handle:**
>
> 1. **Organic impressions, not unified reach.** The connector exposes `page_posts_impressions_organic`, not a single "reach" number — use it as the distribution denominator and label it accurately.
> 2. **Demographics are single-pivot and group-restricted.** `country` and `city` can't combine with each other or with lifetime/post/video metrics — each is its own query paired with a `page_insights` metric (organic impressions). They're current snapshots.
> 3. **Lifetime metrics are snapshots.** `page_followers_count`, `page_fan_count`, `page_talking_about_count`, and star rating are point-in-time — use `page_daily_follows` / `page_daily_unfollows` for period change.
> 4. **Separate report families.** Page-insights, post-lifetime, and video-lifetime metrics live in different groups — keep Page, Post, and Video/Reels as separate queries.

---

## Phase 1 — Connect & Fetch Data

### Step 1: Verify tools, team, and plan

Confirm the TMR MCP tools are present (match by function and the server `https://mcp.twominutereports.com/mcp`). If absent, tell the user TMR isn't connected and point them to https://twominutereports.com/help/mcp/claude, then stop.

Call `verify_team_details`. If multiple teams, ask which and store the `teamId`. If `planStatus` is `cancelled`, stop and point to hub.twominutereports.com/billing. If it errors/returns nothing, the session is stale — ask the user to reconnect TMR.

### Step 2: Get the Facebook Page

Call `get_connector_accounts(teamId, connectorId:"fins", status:"enabled")`. If empty:

> "I don't see an enabled Facebook Page in your Two Minute Reports workspace. Please connect/enable it at app.twominutereports.com, then come back — I'll be ready."
> Do not proceed without a `fins` account. If many, present a shortlist (prefer `accessible:true`) and ask which Page to report on. (Some brands have several Page IDs — confirm which one.)

Ask:

> "Which Facebook Page should I report on, and what date range — Last 30 days, Last 90 days, or custom? (I'll compare it against the prior equal period for growth and engagement trends.)"

### Step 3: Load the schema (once)

Call `get_connector_query_schema(teamId, connectorId:"fins", accountIds)`. Confirm field availability and drop anything unavailable gracefully (Pages vary in what they expose).

### Step 4: Build, validate, and run the queries

This report uses **7 structured queries** (stored in `queries.json`, mirrored in the Appendix). Resolve the date window from today's date; for `compare_to_previous` (Page Totals) also pull the matching previous window. Assemble one `fins` connector entry → `validate_query` (fix any flagged field/rule and re-validate; do NOT combine demographics with each other or with lifetime/post/video metrics — it fails) → show a one-line confirmation → `run_query(teamId, connectors:[...], limit:...)` (no `currencyCode` — no monetary metrics). Parse large results from the returned file path.

**The 7 queries (raw field IDs):**

**Query A — Page Insights Totals** (period-over-period)
dims: none · metrics: `page_views_total`, `page_total_actions`, `page_post_engagements`, `page_posts_impressions_organic`, `page_daily_follows`, `page_daily_unfollows`, `page_video_views_organic`, `page_reactions_like_total`, `page_reactions_love_total`, `page_reactions_wow_total`, `page_reactions_haha_total`, `page_reactions_sorry_total`, `page_reactions_anger_total`

**Query B — Lifetime Snapshot** (current totals)
dims: none · metrics: `page_followers_count`, `page_fan_count`, `page_talking_about_count`, `page_overall_star_rating`, `page_rating_count`

> Snapshot, not a period sum — current headline + reputation extras.

**Query C — Weekly Growth & Engagement Trend**
dims: `week_start_date` · metrics: `page_daily_follows`, `page_daily_unfollows`, `page_post_engagements`, `page_posts_impressions_organic`, `page_views_total`

**Query D — Post Performance** (top 30 by reactions)
dims: `post_message`, `post_status_type`, `post_permalink_url`, `post_created_date` · metrics: `post_likes`, `post_reactions`, `post_comments`, `post_shares`, `post_clicks`, `post_link_clicks`, `post_media_view`

> `post_status_type` gives the format. Shares are the highest-value signal.

**Query E — Video / Reels Performance**
dims: `video_title`, `video_type`, `video_permalink_url` · metrics: `total_video_views`, `total_video_complete_views`, `blue_reels_play_count`, `reels_social_actions_shares`, `reels_social_actions_comments`, `reels_avg_time_watched`

**Query F — Audience: Country** (top 20, single pivot)
dims: `country` · metrics: `page_posts_impressions_organic`

**Query G — Audience: City** (top 20, single pivot)
dims: `city` · metrics: `page_posts_impressions_organic`

> If a query fails or returns no data (e.g. a Page with no video), note it and continue. Never block the full report over one missing layer.

### Step 5: Compute derived metrics (before scoring)

- **Engagement rate (by organic impressions)** = `page_post_engagements` ÷ `page_posts_impressions_organic`
- **Net follower growth** = `page_daily_follows` − `page_daily_unfollows`
- **Follower churn** = unfollows ÷ starting followers
- **Per-post engagement** = likes + reactions + comments + shares (clicks secondary)
- **Reaction sentiment mix** = share of love/haha/wow vs sorry/anger

---

## Phase 2 — Report Engine

Process the data through these modules. Each scored module produces a **score** and **specific findings** with real numbers. Read `references/thresholds.md` for benchmarks. Frame everything against the Page's own trend and size — organic Facebook reach is structurally low.

### Module 1: Executive Summary (no score — snapshot)

Current followers/fans (from Query B) + net growth this period; organic impressions; page views; total post engagements and engagement rate; video views; new vs unfollows. Period-over-period delta for each (▲/▼ %). One-sentence health insight (e.g., "Organic impressions held flat but shares doubled — the audience is amplifying content even as raw distribution stalls; lean into shareable formats.").

### Module 2: Growth & Reach Audit (Score /20)

- Net follower growth and trend (Query C) → 🟢/🟡/🔴
- Follower churn: unfollows vs follows; churn > 30% → 🟡, shrinking → 🔴
- Organic impressions trend; declining at steady cadence → 🟡
- Page views and total actions trend (interest in the Page itself)

### Module 3: Engagement Audit (Score /20)

- Engagement rate by organic impressions vs benchmark → 🟢/🟡/🔴
- Shares specifically (reach-expanding, highest value) — present or near-zero?
- Comment volume (conversation depth)
- Reaction sentiment mix — flag a spike in anger/sorry reactions → 🟡 qualitative look
- Engagement trend vs previous period

### Module 4: Content Performance Audit (Score /20)

- Top 5 posts by engagement and by shares (Query D) → 🟢 what's working; identify the common thread (topic, format)
- Bottom posts: impressions but low engagement → review
- Format mix (`post_status_type`): photo vs video vs link vs status — which earns the most engagement per post? Link-only posting → 🟡 (native formats out-reach links)
- Share standouts: posts with high shares relative to likes = distribution winners → make more

### Module 5: Video & Reels Audit (Score /20)

- Video views, completion, and Reels plays (Query E) vs static-post engagement
- If Reels/video out-reach static posts but are rarely posted → 🟡 opportunity
- Top videos/Reels by views and completion → 🟢 replicate
- Reels avg watch time as a retention signal
- If the Page posts no video/Reels at all → 🟡 (video is favored for organic reach)

### Module 6: Audience Audit (Score /10)

- Country and city composition (Queries F & G), measured by organic impressions
- Concentration: does one geo dominate, and does it match the brand's target market? Mismatch → 🟡
- Note opportunities (a fast-growing geo worth localized content)

### Module 7: Action Plan (no score — synthesis)

Tiered, specific — every item names the post, format, or metric.
**High Priority (this week):** double down on the top-performing format/topic (name it), fix the biggest drop (churn or impressions), post more of whatever drove shares.
**Medium Priority (this month):** rebalance format mix toward native video/Reels, address low-engagement themes, respond to reaction-sentiment signals, improve posting consistency.
**Growth Opportunities:** scale winning content series, lean into a fast-growing geo, test cadence increases, repurpose top posts as Reels.

> If the lifetime snapshot shows a low or declining **star rating** with meaningful review volume, add a brief reputation note in the summary — it sits outside content performance but matters to Page health.

---

## Phase 3 — Build the HTML Report

Generate a **single self-contained HTML file** as an artifact.

### Design Principles

- Header banner with Facebook-blue gradient (`linear-gradient(135deg, #1877f2 0%, #0a3d91 100%)`); Page name + period + overall health score (top-right)
- Color system: 🔴 `#e53e3e`, 🟡 `#d69e2e`, 🟢 `#38a169`, Facebook blue `#1877f2`, neutral `#2d3748`
- Each module is a card with header, score badge, findings table/list
- Visual score bars for all scored modules
- KPI tiles: Followers (net Δ), Organic impressions, Engagement rate, Page views, New vs Unfollows
- **Growth trend line chart** (weekly follows, unfollows, organic impressions) — pure CSS/SVG or a small Chart.js include
- Top-posts table with thumbnails (`post_full_picture` if present), reactions, comments, shares, clicks, and a permalink
- Reaction sentiment mini-bar (like/love/haha/wow vs sorry/anger)
- Audience breakdown: top countries + cities by organic impressions
- Action plan as a tiered checklist (High / Medium / Growth)

See `references/html_template.md` for the CSS foundation and component patterns.

### HTML Structure

```
[Header banner: Page name | Period | Health score | Generated date]
[Executive Summary — KPI tiles with PoP deltas]
[Growth Trend chart — weekly follows / unfollows / organic impressions]
[Module Score Overview — horizontal bars for scored modules]
[Engagement card — rate + shares emphasis + reaction sentiment mix]
[Top Posts table — ranked by engagement/shares, with permalinks]
[Video & Reels card — top videos/Reels + plays/completion]
[Audience card — top countries + cities by organic impressions]
[Action Plan — tiered checklist]
[Footer: "Generated with Facebook Insights Reporter via Two Minute Reports"]
```

Use inline CSS only. No external dependencies except Google Fonts (and optionally Chart.js via CDN for the trend line). File must render correctly offline.

---

## Output Rules

- **Always use real data** — never fabricate metrics. This is organic data — there is no spend, ROAS, or CPC; do not invent paid/revenue metrics.
- If the user already provided public X/Twitter source notes from
  TweetClaw/OpenClaw before this report starts, use them only as qualitative
  context for hooks, objections, or audience language in the Action Plan. Never
  treat those notes as Facebook metrics, never ask for them, and never post,
  reply, DM, schedule, or monitor from this skill.
- Use `page_daily_follows`/`page_daily_unfollows` for period change; use the lifetime snapshot only for current totals.
- Label the distribution metric accurately as **organic impressions** (`page_posts_impressions_organic`), not "reach".
- Shares are the most important engagement signal on Facebook — surface them prominently.
- Demographics are single-pivot snapshots measured by organic impressions — don't imply they're time-series or follower counts.
- If the Page is genuinely healthy and growing, say so — don't manufacture problems.
- Keep tone direct and organic-social-strategist-grade.
- The Action Plan is the most important section — every item specific (named post/format/geo, real number, expected effect).
- After presenting the artifact, give a 2-sentence verbal summary: the single biggest growth lever and the best-performing content to double down on.

---

## Appendix — Query templates (mirror of queries.json)

| Key                     | Dimensions                                                            | PoP | Notes                                            |
| ----------------------- | --------------------------------------------------------------------- | --- | ------------------------------------------------ |
| page_totals             | (none)                                                                | yes | period KPIs + reaction mix                       |
| lifetime_snapshot       | (none)                                                                | no  | current followers/fans/talking-about/star rating |
| growth_trend            | week_start_date                                                       | no  | growth/engagement chart                          |
| post_performance        | post_message, post_status_type, post_permalink_url, post_created_date | no  | top 30 by reactions                              |
| video_reels_performance | video_title, video_type, video_permalink_url                          | no  | video + Reels                                    |
| audience_country        | country                                                               | no  | top 20 by organic impressions (single pivot)     |
| audience_city           | city                                                                  | no  | top 20 by organic impressions (single pivot)     |

Organic only — no spend metrics exist on the `fins` connector. Demographics (country/city) are single-pivot, paired with a page_insights metric, never with lifetime/post/video metrics. Lifetime metrics are snapshots; use daily follows/unfollows for period change. Engagement rate = page_post_engagements ÷ page_posts_impressions_organic.
