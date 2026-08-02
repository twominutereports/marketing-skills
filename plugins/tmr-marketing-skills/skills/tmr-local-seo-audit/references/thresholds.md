# Local SEO Audit — Scoring Thresholds & Benchmarks

This audit combines **three Google sources** to measure a local business's complete search presence:
- **Google Business Profile (GMB)** — how the business shows up on Maps & Search, and the local actions it drives (calls, website clicks, directions).
- **Google Search Console (GSC)** — organic search visibility for the website (impressions, clicks, position).
- **Google Analytics 4 (GA4)** — what visitors do on the website (sessions, engagement, key events / form submissions).

Benchmarks are general local-SEO guidelines — always frame findings against the business's own trend and market size, not as absolute truths. A single-location service business and a multi-location retailer behave very differently.

## The headline metrics (what the client asked to see)
- **Profile Viewers** → GMB `views_total` (Maps + Search profile views)
- **Calls** → GMB `actions_phone`
- **Impressions / Clicks** → GSC `impressions` / `clicks` (organic website search)
- **Sessions / Engagement Rate** → GA4 `sessions` / `engagement_rate`
- **Form Submissions / Key Events** → GA4 `key_events`
Supporting: GMB website visits, direction requests, messages; GMB search impressions & search terms; GMB reviews + star rating; GSC CTR & position; GA4 channel mix & landing pages.

## Derived / cross-source metrics
- **Profile → website rate** = GMB `actions_website` ÷ GMB `views_total` (how well the profile drives site visits).
- **Profile action rate** = GMB `actions_total` ÷ GMB `views_total` (how often a profile view turns into any action).
- **Organic CTR** = GSC `clicks` ÷ GSC `impressions`.
- **Site conversion proxy** = GA4 `key_events` ÷ GA4 `sessions`.
- **Organic share** = Organic-Search sessions ÷ total sessions (from the GA4 channel query).

## Local visibility signals (GMB views + GSC)
- **Healthy (🟢):** profile views and GSC impressions both growing period-over-period.
- **Watch (🟡):** flat views/impressions at steady activity.
- **Weak (🔴):** declining profile views or GSC impressions period-over-period — losing local visibility.
- View source mix (`view_source`): a healthy local profile gets meaningful discovery (non-branded) search, not only direct/branded lookups → heavy direct-only → 🟡 (low net-new discovery).
- GSC average position worse than 10 for core local terms with impressions → 🟡 page-2 visibility.

## Local action / engagement signals (GMB actions)
- **Profile action rate** (actions ÷ views): > 5% strong, 2–5% average, < 2% weak (🔴) — profile views aren't converting to calls/clicks/directions.
- **Calls** trend: declining calls with steady views → 🟡 (CTA / profile-completeness issue).
- If website visits dominate but calls/directions are near-zero for a business that depends on them → 🟡 (missing or wrong primary action).

## Website performance signals (GA4)
- **Engagement rate:** > 55% strong (🟢), 40–55% average, < 40% weak (🔴).
- **Site conversion proxy** (key events ÷ sessions): judge against the business's own baseline; a sharp drop with steady sessions → 🔴 (form/tracking or UX issue).
- **Organic share:** healthy local sites earn a substantial organic share; very low organic share with strong GMB visibility → 🟡 (profile traffic not reaching the analytics-tracked site, or attribution gap).
- Landing pages: high-session pages with low key events → 🟡 conversion opportunity.

## Reviews & reputation signals (GMB)
- **Avg star rating:** ≥ 4.5 strong (🟢), 4.0–4.5 watch, < 4.0 weak (🔴).
- **Review count / velocity:** very low review count for the category, or no new reviews in the period → 🟡 (reviews drive local ranking and conversion).
- (If review replies are available) low reply rate → 🟡 (responding to reviews aids local ranking and trust).

## Severity scoring (per scored module, /20 unless noted)
- Start at 20; deduct per flag weighted by impact on local discovery → action → conversion.
- 🔴 deducts more than 🟡. A healthy module scores 18–20.
- Roll the module scores into an overall **Local SEO Health Score /100** in the header.

## Data-availability & combination notes
- **GMB group rule:** the search-impressions / search-terms metrics CANNOT be combined with views/actions/reviews in one query — they are separate queries. Views, actions, and reviews can combine, but keep reviews (a running total/snapshot) separate from period views/actions for clean aggregation.
- **GMB `monthly_search_impressions`** is monthly granularity — treat as an approximate period figure, not a daily series.
- **GMB reviews totals** (`total_review_count`, `total_review_star_rating`) are running snapshots, not period sums.
- **Three different account ID shapes:** GMB = `accountId-locationId`; GSC = a site URL (`https://example.com/` or `sc-domain:example.com`); GA4 = a numeric property ID. Resolve each separately for the same client.
- All three are Google organic/profile sources — there is **no ad spend** in this audit. Do not invent paid metrics.
