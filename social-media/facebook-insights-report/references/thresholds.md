# Facebook Insights Report — Scoring Thresholds & Benchmarks

This report covers **organic** Facebook Page performance (no paid ads, no spend). It orients around three pillars: **growth** (followers/fans), **engagement** (post engagements and reactions relative to organic reach), and **content** (which posts and videos/Reels perform). Benchmarks are general guidelines — frame findings against the Page's own trend and size, not as absolute truths. Organic Facebook reach has declined industry-wide for years; judge relative to the Page's recent baseline.

## Core derived metrics
- **Engagement rate (by organic impressions)** = `page_post_engagements` ÷ `page_posts_impressions_organic`. The cleanest organic content-quality signal available on this connector.
- **Net follower growth** = `page_daily_follows` − `page_daily_unfollows` for the period.
- **Follower churn** = unfollows ÷ starting followers.
- **Post engagement** per post = likes + reactions + comments + shares (+ clicks as a secondary signal).
- **Reaction mix** = distribution across like / love / wow / haha / sorry / anger (sentiment signal).

## Engagement benchmarks (organic Facebook Pages)
- **Strong (🟢):** engagement-by-impressions > 5%, or post engagement clearly above the Page's own median.
- **Average:** 1–5%.
- **Weak (🔴):** < 1% with meaningful impressions — content–audience mismatch.
- Facebook organic reach is structurally low; a "healthy" Page is judged more on trend and on per-post outliers than on absolute reach.

## Growth signals
- **Healthy (🟢):** positive net follower growth and unfollows < 30% of follows.
- **Watch (🟡):** flat net growth, or unfollows 30–60% of follows.
- **Critical (🔴):** negative net growth, or unfollows > follows (shrinking Page).
- Organic impressions trending down at steady posting cadence → 🟡 (declining distribution / content fatigue).

## Content & format signals
- **Shares are the highest-value interaction** on Facebook — they expand reach beyond existing fans. A post with strong shares relative to likes is a distribution winner; make more like it → 🟢.
- **Video / Reels:** `blue_reels_play_count` and video views vs static-post engagement. If Reels/video out-perform static posts on reach but are rarely posted → 🟡 opportunity.
- **Format mix:** if the Page posts only one `post_status_type` (e.g. only links, no native video/photo) → 🟡 (native video and photos typically out-reach link posts).
- **Low performers:** posts with impressions but bottom-quartile engagement → review hook, copy, or topic.
- **Reaction sentiment:** a spike in "anger"/"sorry" reactions relative to positive ones → 🟡 worth a qualitative look at what triggered it.
- **Posting cadence:** very few posts in the period with flat impressions → 🟡 (consistency drives organic reach).

## Audience signals
- Country/city concentration from the demographics breakdown: if reach concentrates in a geo that doesn't match the brand's target market → 🟡 mismatch.
- Use audience geo to sanity-check content–audience fit, not as a standalone score.

## Page-health extras (lifetime snapshot)
- **Star rating** (`page_overall_star_rating`, `page_rating_count`): a low or declining rating with enough reviews → 🟡/🔴 reputation flag (note it; it sits outside content performance).
- **Talking-about count** (`page_talking_about_count`): a buzz proxy — rising is 🟢.

## Severity scoring (per scored module, /20 unless noted)
- Start at 20; deduct per flag, weighted by impact on growth/engagement.
- 🔴 deducts more than 🟡. A healthy module scores 18–20.
- Roll section scores into an overall /100 health score in the header.

## Data-availability notes
- **Lifetime metrics** (`page_followers_count`, `page_fan_count`, `page_talking_about_count`, star rating) are point-in-time snapshots, not period sums — use them for the current headline; use `page_daily_follows` / `page_daily_unfollows` for period change.
- **Demographics (country/city)** cannot be combined with each other or with lifetime/post/video metric groups — each is a separate single-pivot query paired with a `page_insights` metric (e.g. organic impressions). They are current snapshots.
- This connector exposes **organic impressions** (`page_posts_impressions_organic`), not a single unified "reach" figure — use organic impressions as the distribution denominator and label it accurately.
