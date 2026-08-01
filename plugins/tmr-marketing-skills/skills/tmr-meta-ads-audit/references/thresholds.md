# Meta Ads Audit Thresholds & Scoring Guide

## Module Scoring (each /20, 7 scored modules = 140 max → normalize to 100)

To compute overall score: `round((sum of 7 module scores / 140) * 100)`

### Module 2: Wasted Spend
| Condition | Score Impact |
|-----------|-------------|
| Wasted spend < 5% of total budget | Full marks (20) |
| Wasted spend 5–15% | -5 |
| Wasted spend 15–30% | -10 |
| Wasted spend > 30% | -15 |
| 🔴 Ad sets with ROAS < 0.5 (>2% spend share) | -4 each (cap -8) |
| 🔴 Campaigns with >$100 spend and 0 conversions | -3 each (cap -6) |
| 🟡 High frequency + zero conversion ad sets | -3 |

### Module 3: Campaign Performance
| Condition | Score Impact |
|-----------|-------------|
| Majority of campaigns CPA < 1.5× account avg | Full marks (20) |
| 1–2 campaigns CPA 1.5–2.5× avg | -5 |
| 3+ campaigns CPA > 2× avg | -10 |
| 🔴 Any campaign CPA > 3× avg with >10% spend share | -6 |
| 🟢 Top campaign ROAS > 3.0 | +2 (bonus) |
| No ROAS data available | Evaluate by CPA/CVR only |

### Module 4: Ad Set Performance
| Condition | Score Impact |
|-----------|-------------|
| Ad sets well-distributed across funnel stages | Full marks (20) |
| >60% spend in ≤2 ad sets (concentration risk) | -6 |
| 🔴 Ad sets with CPA > 3× account avg (>5% spend) | -4 each (cap -8) |
| 🟡 High audience overlap signals detected | -4 |
| No remarketing/retargeting ad sets found | -4 |
| >10 active ad sets per campaign (fragmentation) | -3 |

### Module 5: Creative Performance
| Condition | Score Impact |
|-----------|-------------|
| Majority of ads CTR > 1%, CPA < 1.5× avg | Full marks (20) |
| >30% of spend on ads with CTR < 0.5% | -6 |
| 🔴 Multiple ads with CPA > 2× avg and >3% spend | -4 each (cap -8) |
| Only 1 creative format running (no diversity) | -3 |
| 🟢 Video ads with CTR > 2% present | +2 (bonus) |

### Module 6: Creative Fatigue
| Condition | Score Impact |
|-----------|-------------|
| All active ads frequency < 3.0 | Full marks (20) |
| 1–2 ads with frequency 3–5 | -4 |
| 3+ ads with frequency > 3 | -8 |
| 🔴 Any ad frequency > 5 with CTR decline | -6 |
| 🔴 Any ad frequency > 6 | -10 |
| CPM rising >20% period-over-period | -4 |

### Module 7: Audience Performance
| Condition | Score Impact |
|-----------|-------------|
| Remarketing outperforming prospecting (expected) | Full marks (20) |
| No remarketing campaigns active | -6 |
| Interest targeting CPA > 2× remarketing CPA | -4 |
| 🔴 Broad targeting consuming >50% budget without ROAS evidence | -6 |
| 🟡 Overlapping audience signals | -3 |
| 🟢 Lookalike audiences with ROAS > 2.5 | +2 (bonus) |

### Module 8: Placement Performance
| Condition | Score Impact |
|-----------|-------------|
| Spend spread across 3+ placements with good efficiency | Full marks (20) |
| Audience Network CPA > 3× Feed CPA with >10% spend | -5 |
| >70% spend in a single placement | -4 |
| 🔴 Placements with 0 conversions consuming >5% budget | -4 each (cap -8) |
| 🟢 Reels or Stories outperforming Feed | +2 (bonus, note as scale opportunity) |

---

## Overall Health Score

| Score | Status | Label |
|-------|--------|-------|
| 80–100 | 🟢 | Healthy — account is well-managed |
| 60–79 | 🟡 | Needs Work — several issues to address |
| 40–59 | 🔴 | Critical — significant waste or structural problems |
| < 40 | 🔴🔴 | Emergency — account needs immediate restructuring |

---

## Industry Benchmark Reference

Use these as fallbacks when account data is insufficient:

| Metric | Weak | Average | Strong |
|--------|------|---------|--------|
| CTR (Feed) | < 0.5% | 0.5–1.5% | > 1.5% |
| CTR (Stories/Reels) | < 0.3% | 0.3–0.8% | > 0.8% |
| CPM (broad/cold) | > $18 | $8–18 | < $8 |
| CPC | > $2.50 | $0.80–2.50 | < $0.80 |
| Conversion Rate | < 1% | 1–3% | > 3% |
| ROAS (eCommerce) | < 1.5 | 1.5–3.0 | > 3.0 |
| Frequency (threshold) | — | 3.0 (watch) | 5.0 (pause) |
| Frequency (critical) | > 6 | — | — |

---

## Creative Fatigue Rules

An ad is **fatigued** if ANY of these are true:
- Frequency ≥ 5.0 (automatic flag)
- Frequency ≥ 3.5 AND CTR declined >20% vs prior period
- Frequency ≥ 3.0 AND CPM increased >25% vs prior period AND CTR declined

An ad is **critically fatigued** if:
- Frequency ≥ 6.0 OR (Frequency ≥ 4.0 AND CTR declined >35%)
- Action: Pause immediately

**Fatigue waste estimate:**
```
Wasted impressions = impressions in period × (1 - (current CTR / baseline CTR))
Fatigue cost = wasted impressions × (CPM / 1000)
```
Where baseline CTR = account average CTR for the same format.

---

## Wasted Spend Thresholds

An ad set is a **waste candidate** if:
- Spend in period > **account average CPA** AND conversions = 0
- For campaigns: spend > **8% of total budget** AND conversions = 0

ROAS tiers for action:
- ROAS < 0.5 → 🔴 Pause (losing more than 50% of spend)
- ROAS 0.5–1.0 → 🔴 Fix urgently
- ROAS 1.0–1.5 → 🟡 Monitor and optimize
- ROAS > 1.5 → 🟢 Baseline healthy (industry-dependent)

---

## Placement Exclusion Signals

| Placement | When to Exclude |
|-----------|----------------|
| Audience Network | CPA > 2.5× Feed CPA with >5% spend |
| Audience Network (video) | CVR < 0.3% with >$50 spend |
| Right Column | CTR < 0.2% consistently |
| Messenger Stories | CPA > 3× account avg |
| Search Results | Low purchase intent audiences only |

---

## Audience Type Performance Expectations

Expected CPA order (best → worst for most accounts):
1. Remarketing / Custom Audiences (warm audience)
2. Lookalike Audiences (1–3% LAL)
3. Interest Targeting (relevant interests)
4. Broad Targeting (no targeting, algorithm-driven)

If this order is inverted for any pair, flag it and investigate why.

---

## Bid Adjustment Signals

| Condition | Suggested Action |
|-----------|-----------------|
| Mobile CPA > 1.5× Desktop CPA | Add mobile bid adjustment or separate campaigns |
| Desktop CPA < 0.8× Mobile | Consider desktop-only campaign for high-ticket items |
| Top geo CPA < 0.7× account avg | Create geo-specific ad set with higher budget |
| Bottom geo CPA > 2.5× avg with >3% spend | Exclude geo or reduce budget allocation |
