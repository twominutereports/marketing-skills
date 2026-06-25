# Shopify Store Audit — HTML Template Reference

Full CSS foundation and component patterns for the Shopify Store Audit HTML deliverable.
Modeled after the Meta Ads Audit design language — premium, consultant-grade output.

---

## Base Styles

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shopify Store Audit — [Store Name]</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #e53e3e;
    --red-bg: #fff5f5;
    --yellow: #d69e2e;
    --yellow-bg: #fffff0;
    --green: #38a169;
    --green-bg: #f0fff4;
    --shopify: #96bf48;
    --shopify-bg: #f0f7e0;
    --teal: #0d9488;
    --teal-bg: #f0fdfa;
    --dark: #0f172a;
    --mid: #334155;
    --muted: #64748b;
    --border: #e2e8f0;
    --bg: #f8fafc;
    --white: #ffffff;
    --font: 'Inter', -apple-system, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font); background: var(--bg); color: var(--dark); font-size: 14px; line-height: 1.6; }
  .container { max-width: 1100px; margin: 0 auto; padding: 24px 20px; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }

  /* Header */
  .audit-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #0d9488 100%);
    color: white; padding: 32px 40px; border-radius: 14px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .audit-header .report-type { font-size: 11px; font-weight: 700; color: #7dd3c8; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px; }
  .audit-header h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }
  .audit-header .meta { font-size: 13px; color: #94a3b8; margin-top: 8px; display: flex; gap: 12px; flex-wrap: wrap; }
  .audit-header .meta-pill { background: rgba(255,255,255,0.1); border-radius: 99px; padding: 3px 12px; font-size: 12px; color: #cbd5e1; display: flex; align-items: center; gap: 5px; }
  .health-ring { text-align: center; background: rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 24px; min-width: 130px; }
  .health-ring .score { font-size: 52px; font-weight: 800; line-height: 1; }
  .health-ring .score-denom { font-size: 18px; font-weight: 400; opacity: 0.6; }
  .health-ring .label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
  .health-ring .status { font-size: 13px; font-weight: 600; margin-top: 4px; }

  /* Section label */
  .section-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); margin-bottom: 12px; margin-top: 4px; }

  /* Cards */
  .card { background: var(--white); border-radius: 12px; border: 1px solid var(--border); padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
  .card-title { font-size: 15px; font-weight: 700; color: var(--dark); display: flex; align-items: center; gap: 8px; }
  .card-score { font-size: 13px; font-weight: 700; padding: 3px 12px; border-radius: 99px; }
  .score-green { background: var(--green-bg); color: var(--green); }
  .score-yellow { background: var(--yellow-bg); color: var(--yellow); }
  .score-red { background: var(--red-bg); color: var(--red); }

  /* Score bars */
  .score-bar-wrap { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
  .score-bar-label { font-size: 13px; color: var(--mid); width: 220px; flex-shrink: 0; }
  .score-bar-track { flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
  .score-bar-value { font-size: 13px; font-weight: 700; width: 55px; text-align: right; }

  /* KPI Tiles */
  .kpi-tile { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }
  .kpi-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--muted); margin-bottom: 6px; }
  .kpi-value { font-size: 24px; font-weight: 800; color: var(--dark); line-height: 1.1; margin: 4px 0; }
  .kpi-sub { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
  .kpi-delta { font-size: 11px; font-weight: 600; }
  .up-bad { color: var(--red); }
  .up-good { color: var(--green); }
  .down-bad { color: var(--red); }
  .down-good { color: var(--green); }
  .neutral { color: var(--muted); }

  /* Revenue Leak Callout */
  .leak-callout {
    background: var(--red-bg); border: 2px solid var(--red); border-radius: 12px;
    padding: 22px 32px; margin-bottom: 20px; display: flex; align-items: flex-start; gap: 24px;
  }
  .leak-icon { font-size: 36px; flex-shrink: 0; margin-top: 4px; }
  .leak-amount { font-size: 44px; font-weight: 800; color: var(--red); line-height: 1; }
  .leak-label { font-size: 15px; font-weight: 700; color: var(--red); margin-top: 4px; }
  .leak-desc { font-size: 13px; color: #742a2a; margin-top: 8px; line-height: 1.6; }
  .leak-pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
  .leak-pill { background: white; border: 1px solid #feb2b2; border-radius: 99px; padding: 4px 14px; font-size: 12px; font-weight: 600; color: var(--red); }
  .leak-pill.yellow { border-color: #f6e05e; color: var(--yellow); }

  /* Funnel Visualization */
  .funnel-container { display: flex; align-items: stretch; gap: 0; margin: 16px 0; }
  .funnel-step { flex: 1; text-align: center; padding: 16px 8px; position: relative; }
  .funnel-step-bar { height: 6px; border-radius: 99px; margin-bottom: 12px; }
  .funnel-step-value { font-size: 22px; font-weight: 800; color: var(--dark); }
  .funnel-step-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px; }
  .funnel-step-pct { font-size: 12px; font-weight: 600; margin-top: 6px; }
  .funnel-arrow { display: flex; align-items: center; padding: 0 4px; color: var(--muted); font-size: 18px; }
  .funnel-drop { font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 6px; background: var(--red-bg); color: var(--red); margin-top: 4px; }
  .funnel-drop.yellow-drop { background: var(--yellow-bg); color: var(--yellow); }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: var(--bg); font-weight: 600; font-size: 11px; text-transform: uppercase;
       letter-spacing: 0.5px; color: var(--muted); padding: 8px 12px; text-align: left;
       border-bottom: 1px solid var(--border); }
  td { padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--bg); }
  .num { text-align: right; font-variant-numeric: tabular-nums; }

  /* Badges */
  .badge { display: inline-flex; align-items: center; padding: 2px 9px; border-radius: 99px; font-size: 11px; font-weight: 600; }
  .badge-red { background: var(--red-bg); color: var(--red); }
  .badge-yellow { background: var(--yellow-bg); color: #b7791f; }
  .badge-green { background: var(--green-bg); color: var(--green); }
  .badge-teal { background: var(--teal-bg); color: var(--teal); }
  .badge-gray { background: var(--bg); color: var(--muted); }
  .badge-shopify { background: var(--shopify-bg); color: #5a7a00; }

  /* Device comparison */
  .device-bar { height: 10px; border-radius: 99px; margin: 4px 0; }

  /* Insight box */
  .insight-box { background: var(--teal-bg); border-left: 3px solid var(--teal); border-radius: 0 8px 8px 0; padding: 10px 14px; margin-top: 12px; font-size: 13px; color: #134e4a; }

  /* Alert box */
  .alert-box { background: var(--red-bg); border-left: 3px solid var(--red); border-radius: 0 8px 8px 0; padding: 10px 14px; margin-top: 8px; font-size: 13px; color: #742a2a; }

  /* Warning box */
  .warn-box { background: var(--yellow-bg); border-left: 3px solid var(--yellow); border-radius: 0 8px 8px 0; padding: 10px 14px; margin-top: 8px; font-size: 13px; color: #744210; }

  /* Opportunity box */
  .opportunity-box {
    background: #f0fff4; border: 2px dashed var(--green); border-radius: 10px;
    padding: 14px 20px; margin-top: 12px; font-size: 13px; color: #276749;
    display: flex; align-items: center; gap: 12px;
  }
  .opportunity-amount { font-size: 24px; font-weight: 800; color: var(--green); }

  /* Action Plan */
  .action-tier-header { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 5px 14px; border-radius: 6px; display: inline-block; margin: 14px 0 10px; }
  .tier-high { background: var(--red-bg); color: var(--red); }
  .tier-medium { background: var(--yellow-bg); color: #b7791f; }
  .tier-growth { background: var(--green-bg); color: var(--green); }
  .action-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border); }
  .action-item:last-child { border-bottom: none; }
  .action-check { width: 18px; height: 18px; border: 2px solid var(--border); border-radius: 4px; flex-shrink: 0; margin-top: 2px; cursor: pointer; accent-color: var(--teal); }
  .action-text { font-size: 13px; line-height: 1.5; }
  .action-impact { font-size: 11px; color: var(--muted); margin-top: 3px; }
  .savings-total { background: var(--green-bg); border: 1px solid var(--green); border-radius: 10px; padding: 14px 20px; margin-top: 14px; font-size: 15px; font-weight: 700; color: var(--green); display: flex; align-items: center; gap: 10px; }

  /* Footer */
  .audit-footer { text-align: center; font-size: 12px; color: var(--muted); margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border); }
</style>
</head>
```

---

## Score Color Helper (JavaScript)

```javascript
function scoreColor(score, max) {
  const pct = score / max;
  if (pct >= 0.85) return { bar: 'var(--green)', cls: 'score-green', label: `${score}/${max}` };
  if (pct >= 0.60) return { bar: 'var(--yellow)', cls: 'score-yellow', label: `${score}/${max}` };
  return { bar: 'var(--red)', cls: 'score-red', label: `${score}/${max}` };
}

function overallColor(score) {
  if (score >= 80) return 'var(--green)';
  if (score >= 60) return 'var(--yellow)';
  return 'var(--red)';
}

function overallLabel(score) {
  if (score >= 80) return '🟢 Healthy';
  if (score >= 60) return '⚠️ Needs Work';
  if (score >= 40) return '🔴 Critical';
  return '🔴🔴 Emergency';
}
```

---

## Component Snippets

### Header
```html
<div class="audit-header">
  <div>
    <div class="report-type">Shopify Store Audit</div>
    <h1>🛍️ [Store Name]</h1>
    <div class="meta" style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
      <span class="meta-pill">📅 [Date Range]</span>
      <span class="meta-pill">🔗 [Store URL / ID]</span>
      <span class="meta-pill">Generated: [Date]</span>
    </div>
  </div>
  <div class="health-ring">
    <div class="score" style="color: [overallColor];">[Score]<span class="score-denom">/100</span></div>
    <div class="label">Health Score</div>
    <div class="status">[overallLabel]</div>
  </div>
</div>
```

### KPI Grid (10 tiles)
```html
<div class="section-label">Executive Summary</div>
<div class="grid-5" style="margin-bottom:20px;">
  <div class="kpi-tile">
    <div class="kpi-label">Total Sessions</div>
    <div class="kpi-value">48,200</div>
    <div class="kpi-delta up-good">▲ 8% vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Conversion Rate</div>
    <div class="kpi-value">1.8%</div>
    <div class="kpi-delta down-bad">▼ 0.3pt vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Revenue</div>
    <div class="kpi-value">$42,100</div>
    <div class="kpi-delta up-good">▲ 5% vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">AOV</div>
    <div class="kpi-value">$48.20</div>
    <div class="kpi-delta down-bad">▼ 3% vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Orders</div>
    <div class="kpi-value">874</div>
    <div class="kpi-delta up-good">▲ 9% vs prev</div>
  </div>
  <!-- Row 2 -->
  <div class="kpi-tile">
    <div class="kpi-label">Bounce Rate</div>
    <div class="kpi-value">52%</div>
    <div class="kpi-delta up-bad">▲ 4pt vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Add to Cart Rate</div>
    <div class="kpi-value">5.2%</div>
    <div class="kpi-delta neutral">— flat</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Checkout Init Rate</div>
    <div class="kpi-value">2.8%</div>
    <div class="kpi-delta down-bad">▼ 0.4pt vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Purchase Completion</div>
    <div class="kpi-value">63%</div>
    <div class="kpi-delta neutral">— flat</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Returning Customers</div>
    <div class="kpi-value">22%</div>
    <div class="kpi-delta up-good">▲ 3pt vs prev</div>
  </div>
</div>
```

### Revenue Leak Callout
```html
<div class="leak-callout">
  <div class="leak-icon">📉</div>
  <div>
    <div class="leak-amount">~$12,400</div>
    <div class="leak-label">Estimated Recoverable Revenue (30-Day Period)</div>
    <div class="leak-desc">Based on checkout abandonment gap, mobile conversion underperformance, and 6 high-traffic products with near-zero conversion rates. Conservative 15% recovery assumption applied.</div>
    <div class="leak-pills">
      <span class="leak-pill">🔴 Checkout abandonment — $7,200 recoverable</span>
      <span class="leak-pill">🔴 Mobile CVR gap — $3,600 lost</span>
      <span class="leak-pill yellow">🟡 Zero-CVR products — $1,600 opportunity</span>
    </div>
  </div>
</div>
```

### Funnel Visualization
```html
<div class="funnel-container">
  <div class="funnel-step">
    <div class="funnel-step-bar" style="background: var(--teal);"></div>
    <div class="funnel-step-value">48,200</div>
    <div class="funnel-step-label">Sessions</div>
    <div class="funnel-step-pct neutral">100%</div>
  </div>
  <div class="funnel-arrow">→</div>
  <div class="funnel-step">
    <div class="funnel-step-bar" style="background: var(--shopify);"></div>
    <div class="funnel-step-value">19,300</div>
    <div class="funnel-step-label">Product Views</div>
    <div class="funnel-step-pct neutral">40%</div>
    <div class="funnel-drop yellow-drop">↓ 60% drop</div>
  </div>
  <div class="funnel-arrow">→</div>
  <div class="funnel-step">
    <div class="funnel-step-bar" style="background: var(--yellow);"></div>
    <div class="funnel-step-value">2,507</div>
    <div class="funnel-step-label">Add to Cart</div>
    <div class="funnel-step-pct neutral">5.2%</div>
    <div class="funnel-drop yellow-drop">↓ 87% drop</div>
  </div>
  <div class="funnel-arrow">→</div>
  <div class="funnel-step">
    <div class="funnel-step-bar" style="background: #ed8936;"></div>
    <div class="funnel-step-value">1,349</div>
    <div class="funnel-step-label">Checkout Started</div>
    <div class="funnel-step-pct neutral">2.8%</div>
    <div class="funnel-drop">↓ 46% drop ⚠️</div>
  </div>
  <div class="funnel-arrow">→</div>
  <div class="funnel-step">
    <div class="funnel-step-bar" style="background: var(--red);"></div>
    <div class="funnel-step-value">874</div>
    <div class="funnel-step-label">Purchase</div>
    <div class="funnel-step-pct down-bad">1.8%</div>
    <div class="funnel-drop">↓ 35% drop</div>
  </div>
</div>
```

### Module Score Overview Card
```html
<div class="card">
  <div class="card-header">
    <div class="card-title">📊 Module Scorecard</div>
    <div class="card-score score-yellow">58 / 100</div>
  </div>
  
  <!-- Funnel Conversion: 12/20 -->
  <div class="score-bar-wrap">
    <div class="score-bar-label">Funnel Conversion</div>
    <div class="score-bar-track">
      <div class="score-bar-fill" style="width:60%; background:var(--yellow);"></div>
    </div>
    <div class="score-bar-value" style="color:var(--yellow);">12/20</div>
  </div>
  <!-- repeat for each module -->
</div>
```

### Device Comparison Table
```html
<table>
  <thead>
    <tr>
      <th>Device</th>
      <th class="num">Sessions</th>
      <th class="num">Session %</th>
      <th class="num">CVR</th>
      <th class="num">AOV</th>
      <th class="num">Revenue</th>
      <th class="num">Rev %</th>
      <th class="num">Bounce</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>📱 Mobile</strong></td>
      <td class="num">31,330</td>
      <td class="num">65%</td>
      <td class="num down-bad"><strong>1.1%</strong></td>
      <td class="num">$44.20</td>
      <td class="num">$15,300</td>
      <td class="num">36%</td>
      <td class="num">58%</td>
      <td><span class="badge badge-red">🔴 Fix Now</span></td>
    </tr>
    <tr>
      <td><strong>🖥️ Desktop</strong></td>
      <td class="num">14,460</td>
      <td class="num">30%</td>
      <td class="num up-good"><strong>3.4%</strong></td>
      <td class="num">$52.80</td>
      <td class="num">$25,900</td>
      <td class="num">62%</td>
      <td class="num">38%</td>
      <td><span class="badge badge-green">🟢 Strong</span></td>
    </tr>
    <tr>
      <td><strong>⬜ Tablet</strong></td>
      <td class="num">2,410</td>
      <td class="num">5%</td>
      <td class="num">2.1%</td>
      <td class="num">$48.60</td>
      <td class="num">$2,460</td>
      <td class="num">6%</td>
      <td class="num">44%</td>
      <td><span class="badge badge-yellow">🟡 Monitor</span></td>
    </tr>
  </tbody>
</table>
<div class="alert-box">⚠️ Mobile has 65% of sessions but only 36% of revenue — a 29-point gap indicating significant mobile experience friction. Desktop converts 3.1× better than mobile.</div>
```

### Action Plan
```html
<div class="action-tier-header tier-high">🔴 High Priority — This Week</div>

<div class="action-item">
  <input type="checkbox" class="action-check">
  <div>
    <div class="action-text"><strong>Fix checkout abandonment leak</strong> — 65% of users who start checkout don't complete it. Audit for hidden shipping costs, missing payment methods, and forced account creation.</div>
    <div class="action-impact">💰 Estimated recovery: ~$7,200/month at 15% recovery rate | Fix: add guest checkout, show shipping costs earlier</div>
  </div>
</div>

<div class="action-item">
  <input type="checkbox" class="action-check">
  <div>
    <div class="action-text"><strong>Improve mobile conversion experience</strong> — Mobile converts at 1.1% vs 3.4% desktop — a 3.1× gap. 65% of your sessions are on mobile.</div>
    <div class="action-impact">💰 Estimated gap: ~$3,600/month in mobile revenue | Fix: mobile CTA visibility, image sizing, checkout UX</div>
  </div>
</div>

<div class="action-tier-header tier-medium">🟡 Medium Priority — This Month</div>
<!-- medium items -->

<div class="action-tier-header tier-growth">🟢 Growth Opportunities</div>
<!-- growth items -->

<div class="savings-total">
  💰 Total estimated recoverable revenue from high-priority fixes: ~$12,400 / month
</div>
```

---

## Section Order

1. Header banner (store name, period, date, health score)
2. Executive Summary — KPI grid (10 tiles, 2 rows of 5)
3. Revenue Leak Callout (prominent, immediately below KPIs)
4. Module Score Overview card — 7 horizontal score bars
5. Funnel Conversion card — funnel visualization + biggest drop-off callout
6. Checkout Friction card — abandonment stats + recovery estimate
7. Mobile Experience card — device comparison table + gap callout
8. Product Performance card — top/worst products ranked table
9. Traffic Source card — channel performance table
10. Cart Abandonment card — abandonment breakdown + opportunity estimate
11. Geographic & Device card — geo table
12. Action Plan card — tiered checklist + total savings estimate
13. Footer: "Generated with Shopify Store Auditor via Two Minute Reports"

Keep all sections visible (no collapsing for V1). Stack vertically within a single container div.
