# Shopify Store Audit — Scoring Thresholds

Reference benchmarks for scoring each module. All thresholds are based on Shopify industry averages.

---

## Module 2: Funnel Conversion Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Store CVR | > 3.5% | 1.5–3.5% | < 1.5% |
| Add-to-cart rate | > 8% | 4–8% | < 4% |
| Cart-to-checkout rate | > 60% | 40–60% | < 40% |
| Checkout-to-purchase | > 70% | 50–70% | < 50% |
| Product page CVR | > 5% | 2–5% | < 2% |

**Scoring:**
- All metrics healthy: 18–20
- One metric in yellow: 14–17
- Two+ metrics in yellow or one in red: 8–13
- Two+ metrics in red: 0–7

---

## Module 3: Checkout Friction Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Checkout abandonment rate | < 55% | 55–70% | > 70% |
| Cart abandonment rate | < 65% | 65–80% | > 80% |
| Discount usage rate | < 15% | 15–30% | > 30% |
| Cart-to-checkout rate | > 60% | 40–60% | < 40% |

**Scoring:**
- All metrics healthy: 17–20
- One yellow: 13–16
- One red or two yellows: 8–12
- Two+ red: 0–7

---

## Module 4: Mobile Experience Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Mobile vs Desktop CVR gap | < 20% worse | 20–50% worse | > 50% worse |
| Mobile bounce rate vs desktop | < 10pt gap | 10–20pt gap | > 20pt gap |
| Mobile add-to-cart rate | > 4% | 2–4% | < 2% |
| Mobile revenue share vs session share | < 20pt gap | 20–35pt gap | > 35pt gap |

**Scoring:**
- All metrics healthy: 17–20
- One yellow: 13–16
- One red or two yellows: 8–12
- Two+ red: 0–7

---

## Module 5: Product Performance Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Product page CVR (top products) | > 5% | 2–5% | < 2% |
| % products with >100 sessions & 0 orders | < 5% | 5–15% | > 15% |
| Revenue concentration (top 3 products) | < 40% | 40–65% | > 65% |
| SKUs with 0 orders in period | < 20% | 20–40% | > 40% |

**Scoring:**
- All metrics healthy: 17–20
- One yellow: 13–16
- One red or two yellows: 8–12
- Two+ red: 0–7

---

## Module 6: Traffic Source Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Organic search CVR | > 2.5% | 1–2.5% | < 1% |
| Email CVR (if channel present) | > 3% | 1.5–3% | < 1.5% |
| Paid social CVR | > 1% | 0.5–1% | < 0.5% |
| Direct traffic % of total | < 40% | 40–60% | > 60% |
| Number of channels contributing >5% revenue | ≥ 3 | 2 | 1 |

**Scoring:**
- All metrics healthy: 17–20
- One yellow: 13–16
- One red or two yellows: 8–12
- Two+ red: 0–7

---

## Module 7: Cart Abandonment Audit (Score /20)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Cart abandonment rate | < 65% | 65–78% | > 78% |
| Checkout abandonment rate | < 55% | 55–70% | > 70% |
| Recovery email present (inferred) | Yes | Unknown | No |
| AOV with discount vs without | < 10% gap | 10–20% gap | > 20% gap |

**Scoring:**
- All metrics healthy: 17–20
- One yellow: 13–16
- One red or two yellows: 8–12
- Two+ red: 0–7

---

## Module 8: Geographic & Device Audit (Score /10)

| Metric | 🟢 Healthy | 🟡 Needs Work | 🔴 Critical |
|---|---|---|---|
| Top geo CVR vs account avg | < 20% below avg | 20–40% below | > 40% below |
| Mobile revenue share gap | < 20pt | 20–35pt | > 35pt |
| Revenue concentration in 1 country | < 60% | 60–80% | > 80% |

**Scoring:**
- All metrics healthy: 9–10
- One yellow: 6–8
- One red or two yellows: 3–5
- Two+ red: 0–2

---

## Overall Health Score Calculation

Sum all module scores out of their maximums, scale to 100:

| Modules | Max |
|---|---|
| Funnel Conversion | 20 |
| Checkout Friction | 20 |
| Mobile Experience | 20 |
| Product Performance | 20 |
| Traffic Source | 20 |
| Cart Abandonment | 20 |
| Geographic & Device | 10 |
| **Total** | **130 → scale to 100** |

`health_score = Math.round((raw_total / 130) * 100)`

| Score | Label |
|---|---|
| 80–100 | 🟢 Healthy |
| 60–79 | 🟡 Needs Work |
| 40–59 | 🔴 Critical |
| 0–39 | 🔴🔴 Emergency |

---

## Revenue Leak Estimation

Use these formulas to compute the "Estimated Recoverable Revenue" callout:

**From checkout abandonment:**
`checkout_abandoned_revenue = (checkout_starts - purchases) × AOV`
`recoverable = checkout_abandoned_revenue × 0.15` (conservative 15% recovery rate)

**From mobile CVR gap:**
`mobile_sessions × (desktop_CVR - mobile_CVR) × AOV = mobile_revenue_gap`

**From high-traffic zero-conversion products:**
`sum(sessions × account_avg_CVR × AOV)` for products with 0 orders

**Total recoverable = max(checkout recovery + mobile gap + product fixes)**
Present conservatively and explain the assumption.
