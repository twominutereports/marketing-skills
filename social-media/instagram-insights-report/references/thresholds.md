# Instagram Insights Report — Scoring Thresholds & Benchmarks

This report covers **organic** Instagram performance (no paid ads, no spend). It orients around three pillars: **growth** (followers, reach), **engagement** (interactions relative to reach/followers), and **content** (which posts and formats perform). Benchmarks are general guidelines — always frame findings relative to the account's own trend and size, not as absolute truths. Engagement norms fall as follower count rises.

## Core derived metrics
- **Engagement rate (by reach)** = (likes + comments + saves + shares) ÷ reach. The most honest content-quality signal.
- **Engagement rate (by followers)** = total interactions ÷ followers. Use for benchmarking against peers.
- **Net follower growth** = new followers − unfollowers for the period.
- **Follower churn** = unfollowers ÷ starting followers.
- **Profile-view → follow rate** = new followers ÷ profile views (a proxy for how well the profile converts visitors).
- **Reach rate** = reach ÷ followers (how far content travels beyond the existing audience).

## Engagement-rate benchmarks (by followers, organic)
- **Strong (🟢):** > 3% for accounts < 10k; > 1.5% for 10k–100k; > 1% for > 100k.
- **Average:** roughly half the above.
- **Weak (🔴):** < 0.5% regardless of size, with meaningful reach — content–audience mismatch.

## Growth signals
- **Healthy (🟢):** positive net growth and unfollowers < 30% of new followers.
- **Watch (🟡):** flat net growth, or unfollowers 30–60% of new followers.
- **Critical (🔴):** negative net growth, or unfollowers > new followers (shrinking).
- Reach trending down period-over-period while posting cadence holds → 🟡 (declining distribution / possible content fatigue).

## Content & format signals
- **Saves and shares are the highest-value interactions** — Instagram's algorithm weights them heavily for distribution. A post with high saves/shares but modest likes is a distribution winner; feature more like it → 🟢.
- **Reels reach vs feed reach:** if Reels reach substantially exceeds feed reach (common), under-investment in Reels → 🟡 opportunity.
- **Format mix:** if the account posts only one `media_product_type` (e.g. all feed, no Reels) → 🟡 (missing the format the algorithm favors for reach).
- **Low performers:** posts with reach but bottom-quartile engagement rate → review hook, caption, or topic.
- **Posting cadence:** very low post count in the period with flat reach → 🟡 (consistency drives reach).

## Audience signals
- Audience concentration: if one country or one age band dominates while the brand targets a different market → 🟡 mismatch.
- Use audience composition (age/gender/geo) to sanity-check content–audience fit, not as a score on its own.

## Severity scoring (per scored module, /20 unless noted)
- Start at 20; deduct for each flag, weighted by impact on growth/engagement.
- 🔴 deducts more than 🟡. A healthy module scores 18–20.
- Roll section scores into an overall /100 health score in the header.

## Data-availability notes
- **Story insights are only available for the last 24 hours** via the connector — a multi-week report cannot include historical Stories. Omit Stories from period reporting (or note "Stories: last 24h only") rather than implying historical story data.
- **Lifetime metrics** (`account_followers_count`, `account_follows_count`, `account_media_count`) are point-in-time snapshots, not period sums — use them for the current headline, not for period deltas (use `account_new_followers` / `account_unfollowers` / `account_growth` for period change).
- Audience demographics are current snapshots, not time-series.
