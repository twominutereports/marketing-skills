# TikTok Ads Audit Thresholds & Scoring Guide

## Module Scoring (each /20)

### Module 2: Wasted Spend
| Condition | Score Impact |
|-----------|-------------|
| Wasted spend < 5% of total budget | Full marks |
| Wasted spend 5–15% of total budget | -5 |
| Wasted spend 15–30% of total budget | -10 |
| Wasted spend > 30% of total budget | -15 |
| 🔴 Campaigns with >$50 spend and 0 conversions | -3 each (cap at -8) |
| 🔴 Frequency > 4.0 with no creative refresh | -4 |
| 🔴 ROAS < 0.5 with > 5% spend share | -5 |

### Module 3: Campaign Performance
| Condition | Score Impact |
|-----------|-------------|
| Top campaign ROAS > 3.0 | +3 |
| Majority of campaigns CPA < 2× account avg | Full marks |
| 1–2 campaigns CPA 2–3× avg | -5 |
| 3+ campaigns CPA > 2× avg | -10 |
| 🔴 Any campaign CPA > 4× account avg with >5% spend share | -6 |
| 🟡 Campaign using Traffic objective when Conversion available | -3 |
| 🟡 Campaign < 50 conversions (learning phase) | Note only, no score penalty |

### Module 4: Creative Audit
| Condition | Score Impact |
|-----------|-------------|
| 3+ active ads per ad group, diverse formats | Full marks |
| < 3 active ads per ad group | -4 |
| Single format dependency (only In-Feed, no Spark/TopView testing) | -3 |
| 🔴 Any ad with frequency > 2.5 AND CTR decline > 20% | -5 each (cap at -10) |
| 🔴 6-second view-through rate < 15% on majority of ads | -5 (hook problem) |
| 🟡 6-second view-through rate 15–25% | -2 |
| Top ad CTR > 3% with ROAS > account avg | +2 |

### Module 5: Audience & Budget Allocation
| Condition | Score Impact |
|-----------|-------------|
| Balanced distribution, top 2 campaigns < 60% of spend | Full marks |
| Top 2 campaigns 60–75% of spend | -3 |
| Top 2 campaigns > 75% of spend (concentration risk) | -8 |
| 🔴 >60% spend in underperformers | -12 |
| 🟡 Audience overlap detected across ad groups (same interest layers) | -3 |
| 🟡 Audience too narrow (< 500K estimated reach) | -4 |
| 🟢 Profitable segment limited by budget | Note as opportunity |

---

## Overall Health Score
Sum of 4 module scores (max 80) scaled to 100.

| Score | Status | Label |
|-------|--------|-------|
| 80–100 | 🟢 | Healthy — account is well-managed |
| 60–79 | 🟡 | Needs Work — several issues to address |
| 40–59 | 🔴 | Critical — significant waste or structural problems |
| < 40 | 🔴🔴 | Emergency — account needs immediate restructuring |

---

## TikTok Industry Benchmark Reference

Use these as fallback when account averages are insufficient:

| Metric | Weak | Average | Strong |
|--------|------|---------|--------|
| CTR (In-Feed) | < 0.5% | 0.5–1.5% | > 1.5% |
| CPM | > $15 | $8–15 | < $8 |
| CPC | > $2.00 | $0.50–2.00 | < $0.50 |
| Conversion Rate | < 1% | 1–3% | > 3% |
| ROAS (eCommerce) | < 1.5 | 1.5–3.5 | > 3.5 |
| 6-Second View-Through Rate | < 15% | 15–30% | > 30% |
| Video Completion Rate | < 10% | 10–25% | > 25% |
| Frequency (30-day) | > 4.0 (fatigue risk) | 2.0–3.5 | < 2.0 |

---

## Creative Fatigue Detection

A creative is **fatigued** if TWO or more of these are true:
- Frequency > 2.5 in the audit period
- CTR declined > 20% vs prior period
- Video view rate declined > 15% vs prior period
- CPA increased > 30% vs prior period

A creative is a **scale signal** if:
- CTR > 1.5× account average
- 6s view-through rate > 25%
- CPA < 0.8× account average

---

## Wasted Spend Thresholds

A creative or ad group is a **waste candidate** if:
- Spend in period > **account average CPA** AND conversions = 0
- For campaigns: Spend > **5% of total budget** AND conversions = 0

A placement is **underperforming** if:
- CPM > 2× account average AND CPA > 2× account average
- ROAS < 0.5 with material spend

---

## Bid & Budget Signals

| Condition | Suggested Action |
|-----------|-----------------|
| iOS CPA > 2× Android CPA | Review iOS-specific SKAN signal loss; consider Android-first budget |
| Mobile CPA < desktop CPA | TikTok is mobile-first; confirm desktop is intentional |
| Geo CPA < 0.7× account avg with volume | Increase geo bid or create dedicated campaign |
| Geo CPA > 2× account avg with >3% spend | Exclude geo or reduce bid |
| Frequency > 3.5, no new creatives in 14 days | 🔴 Upload fresh creatives immediately |
