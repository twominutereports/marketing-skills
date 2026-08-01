# Google Ads Audit Thresholds & Scoring Guide

## Module Scoring (each /20)

### Module 2: Wasted Spend
| Condition | Score Impact |
|-----------|-------------|
| Wasted spend < 5% of total budget | Full marks |
| Wasted spend 5–15% of total budget | -5 |
| Wasted spend 15–30% of total budget | -10 |
| Wasted spend > 30% of total budget | -15 |
| 🔴 Campaigns with >$50 spend and 0 conversions | -3 each (cap at -8) |
| 🔴 Search terms clearly off-topic (>10 found) | -3 |

### Module 3: Campaign Performance
| Condition | Score Impact |
|-----------|-------------|
| Top campaign ROAS > 3.0 | +3 |
| Majority of campaigns CPA < 2× account avg | Full marks |
| 1–2 campaigns CPA 2–3× avg | -5 |
| 3+ campaigns CPA > 2× avg | -10 |
| 🔴 Any campaign CPA > 4× account avg with >5% spend share | -6 |

### Module 4: Budget Allocation
| Condition | Score Impact |
|-----------|-------------|
| Top 2 campaigns < 50% of spend, both performing | Full marks |
| Top 2 campaigns 50–70% of spend | -3 |
| Top 2 campaigns > 70% of spend (concentration risk) | -8 |
| 🔴 >60% spend in underperformers | -12 |
| 🟢 Profitable campaign limited by budget (ROAS > 2.5, low spend share) | Note as opportunity |

### Module 5: Keyword Audit
| Condition | Score Impact |
|-----------|-------------|
| < 5 keywords with spend > avg CPA and 0 conversions | Full marks |
| 5–15 waste keywords | -5 |
| > 15 waste keywords | -10 |
| 🔴 QS < 5 keywords with > 2% spend share | -4 each (cap at -8) |
| Average keyword CTR < 2% (search) | -3 |

### Module 6: Search Terms Audit
| Condition | Score Impact |
|-----------|-------------|
| < 10 irrelevant terms in period | Full marks |
| 10–30 irrelevant terms | -5 |
| > 30 irrelevant/wasted terms | -12 |
| No negative keyword strategy evident | -5 |
| Good converting terms not yet added as exact keywords | -2 (note as opportunity) |

---

## Overall Health Score
Sum of 5 module scores (max 100). 

| Score | Status | Label |
|-------|--------|-------|
| 80–100 | 🟢 | Healthy — account is well-managed |
| 60–79 | 🟡 | Needs Work — several issues to address |
| 40–59 | 🔴 | Critical — significant waste or structural problems |
| < 40 | 🔴🔴 | Emergency — account needs immediate restructuring |

---

## Industry Benchmark Reference

Use these as fallback when account averages are insufficient (e.g., single campaign accounts):

| Metric | Weak | Average | Strong |
|--------|------|---------|--------|
| CTR (Search) | < 2% | 2–5% | > 5% |
| CTR (Display) | < 0.3% | 0.3–0.7% | > 0.7% |
| CPC (Search, general) | > $5 | $1–5 | < $1 |
| Conversion Rate | < 2% | 2–5% | > 5% |
| Quality Score | < 5 | 5–7 | > 7 |
| ROAS (eCommerce) | < 2.0 | 2–4 | > 4 |
| Impression Share (brand) | < 70% | 70–90% | > 90% |

---

## Wasted Spend Thresholds

A keyword or search term is a **waste candidate** if:
- Spend in period > **account average CPA** AND conversions = 0
- For campaigns: Spend > **5% of total budget** AND conversions = 0

A search term is **irrelevant** if:
- Intent is clearly unrelated to the business (e.g., a B2B SaaS account getting "free download" or "DIY" queries)
- Use judgment — do not flag branded terms of competitors as irrelevant unless spend is material

---

## Bid Adjustment Signals (for Device/Geo commentary)

| Condition | Suggested Action |
|-----------|-----------------|
| Mobile CPA > 2× Desktop CPA | -20% to -40% mobile bid adjustment |
| Mobile CPA < 0.8× Desktop CPA | Consider +15% mobile bid adjustment |
| Geo CPA < 0.7× account avg with volume | Increase geo bid or create dedicated campaign |
| Geo CPA > 2× account avg with >3% spend | Negative geo or exclusion |
