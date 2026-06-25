# Meta Ads Audit — HTML Template Reference

Full CSS foundation and component patterns for the Meta Ads Audit HTML deliverable.

## Base Styles

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Meta Ads Audit — [Account Name]</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #e53e3e;
    --red-bg: #fff5f5;
    --yellow: #d69e2e;
    --yellow-bg: #fffff0;
    --green: #38a169;
    --green-bg: #f0fff4;
    --meta: #1877F2;
    --meta-bg: #e8f0fe;
    --dark: #1a202c;
    --mid: #2d3748;
    --muted: #718096;
    --border: #e2e8f0;
    --bg: #f7fafc;
    --white: #ffffff;
    --font: 'Inter', -apple-system, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font); background: var(--bg); color: var(--dark); font-size: 14px; line-height: 1.6; }
  .container { max-width: 1100px; margin: 0 auto; padding: 24px 20px; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .grid-6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; }

  /* Header */
  .audit-header {
    background: linear-gradient(135deg, #1a202c 0%, #1877F2 100%);
    color: white; padding: 32px 40px; border-radius: 12px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .audit-header h1 { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
  .audit-header .meta-logo { font-size: 12px; font-weight: 700; color: #90cdf4; letter-spacing: 1px; text-transform: uppercase; }
  .audit-header .meta { font-size: 13px; color: #bee3f8; margin-top: 4px; }
  .health-ring { text-align: center; }
  .health-ring .score { font-size: 48px; font-weight: 800; line-height: 1; }
  .health-ring .label { font-size: 11px; color: #bee3f8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

  /* Cards */
  .card { background: var(--white); border-radius: 10px; border: 1px solid var(--border); padding: 20px 24px; margin-bottom: 20px; }
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
  .card-title { font-size: 15px; font-weight: 700; color: var(--dark); }
  .card-score { font-size: 13px; font-weight: 700; padding: 3px 10px; border-radius: 99px; }
  .score-green { background: var(--green-bg); color: var(--green); }
  .score-yellow { background: var(--yellow-bg); color: var(--yellow); }
  .score-red { background: var(--red-bg); color: var(--red); }

  /* Score bars */
  .score-bar-wrap { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
  .score-bar-label { font-size: 13px; color: var(--mid); width: 200px; flex-shrink: 0; }
  .score-bar-track { flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 99px; }
  .score-bar-value { font-size: 13px; font-weight: 700; width: 50px; text-align: right; }

  /* KPI Tiles */
  .kpi-tile { background: var(--white); border: 1px solid var(--border); border-radius: 8px; padding: 14px; text-align: center; }
  .kpi-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--muted); }
  .kpi-value { font-size: 22px; font-weight: 800; color: var(--dark); line-height: 1.1; margin: 4px 0; }
  .kpi-delta { font-size: 11px; font-weight: 600; }
  .up-bad { color: var(--red); }
  .up-good { color: var(--green); }
  .down-bad { color: var(--red); }
  .down-good { color: var(--green); }
  .neutral { color: var(--muted); }

  /* Wasted Spend Callout */
  .waste-callout {
    background: var(--red-bg); border: 2px solid var(--red); border-radius: 10px;
    padding: 20px 28px; margin-bottom: 20px; display: flex; align-items: center; gap: 24px;
  }
  .waste-icon { font-size: 40px; }
  .waste-amount { font-size: 40px; font-weight: 800; color: var(--red); line-height: 1; }
  .waste-label { font-size: 14px; font-weight: 700; color: var(--red); margin-top: 2px; }
  .waste-desc { font-size: 13px; color: #742a2a; margin-top: 6px; }

  /* Fatigue Alert */
  .fatigue-callout {
    background: var(--yellow-bg); border: 2px solid var(--yellow); border-radius: 10px;
    padding: 16px 24px; margin-bottom: 20px; display: flex; align-items: center; gap: 20px;
  }
  .fatigue-count { font-size: 36px; font-weight: 800; color: var(--yellow); }
  .fatigue-label { font-size: 14px; font-weight: 700; color: #b7791f; }
  .fatigue-desc { font-size: 13px; color: #744210; margin-top: 4px; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: var(--bg); font-weight: 600; font-size: 11px; text-transform: uppercase;
       letter-spacing: 0.5px; color: var(--muted); padding: 8px 12px; text-align: left;
       border-bottom: 1px solid var(--border); }
  td { padding: 9px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--bg); }
  .num { text-align: right; font-variant-numeric: tabular-nums; }

  /* Badges */
  .badge { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 99px; font-size: 11px; font-weight: 600; }
  .badge-red { background: var(--red-bg); color: var(--red); }
  .badge-yellow { background: var(--yellow-bg); color: #b7791f; }
  .badge-green { background: var(--green-bg); color: var(--green); }
  .badge-meta { background: var(--meta-bg); color: var(--meta); }
  .badge-gray { background: var(--bg); color: var(--muted); }

  /* Fatigue table special cols */
  .freq-high { color: var(--red); font-weight: 700; }
  .freq-warn { color: var(--yellow); font-weight: 700; }
  .freq-ok { color: var(--green); }
  .ctr-down { color: var(--red); }
  .ctr-up { color: var(--green); }

  /* Exclusion box */
  .exclusion-block { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px; font-size: 13px; }
  .exclusion-block ul { padding-left: 18px; margin: 0; }
  .exclusion-block li { margin: 4px 0; color: var(--red); font-weight: 500; }

  /* Action Plan */
  .action-tier-header { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 5px 12px; border-radius: 6px; display: inline-block; margin: 12px 0 8px; }
  .tier-high { background: var(--red-bg); color: var(--red); }
  .tier-medium { background: var(--yellow-bg); color: #b7791f; }
  .tier-growth { background: var(--green-bg); color: var(--green); }
  .action-item { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--border); }
  .action-item:last-child { border-bottom: none; }
  .action-check { width: 18px; height: 18px; border: 2px solid var(--border); border-radius: 4px; flex-shrink: 0; margin-top: 1px; cursor: pointer; accent-color: var(--meta); }
  .action-text { font-size: 13px; line-height: 1.5; }
  .action-impact { font-size: 11px; color: var(--muted); margin-top: 2px; }
  .savings-total { background: var(--red-bg); border: 1px solid var(--red); border-radius: 8px; padding: 12px 16px; margin-top: 12px; font-size: 14px; font-weight: 700; color: var(--red); }

  /* Footer */
  .audit-footer { text-align: center; font-size: 12px; color: var(--muted); margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border); }
</style>
</head>
```

---

## Score Color Helper (JavaScript)
```javascript
function scoreColor(score, max = 20) {
  const pct = score / max;
  if (pct >= 0.85) return { bar: 'var(--green)', text: 'var(--green)', cls: 'score-green' };
  if (pct >= 0.60) return { bar: 'var(--yellow)', text: 'var(--yellow)', cls: 'score-yellow' };
  return { bar: 'var(--red)', text: 'var(--red)', cls: 'score-red' };
}

function overallColor(score) {
  if (score >= 80) return 'var(--green)';
  if (score >= 60) return 'var(--yellow)';
  return 'var(--red)';
}

function overallLabel(score) {
  if (score >= 80) return '🟢 Healthy';
  if (score >= 60) return '🟡 Needs Work';
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
    <div class="meta-logo">Meta Ads Audit</div>
    <h1>[Account Name]</h1>
    <div class="meta">Period: [Date Range] &nbsp;·&nbsp; Generated: [Date]</div>
  </div>
  <div class="health-ring">
    <div class="score" style="color: [overallColor];">[Score]</div>
    <div style="font-size:13px; color:#bee3f8; margin-top:4px;">[overallLabel]</div>
    <div class="label">Health Score / 100</div>
  </div>
</div>
```

### KPI Grid (11 tiles for Meta)
```html
<div class="grid-6" style="margin-bottom:20px;">
  <div class="kpi-tile">
    <div class="kpi-label">Total Spend</div>
    <div class="kpi-value">$24,300</div>
    <div class="kpi-delta up-bad">▲ 12% vs prev</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">ROAS</div>
    <div class="kpi-value">2.4×</div>
    <div class="kpi-delta down-bad">▼ 18% vs prev</div>
  </div>
  <!-- repeat for: Impressions, Reach, CPM, CTR, CPC, CPA, Frequency, Conversions, CVR -->
</div>
```

### Wasted Spend Callout
```html
<div class="waste-callout">
  <div class="waste-icon">🔥</div>
  <div>
    <div class="waste-amount">$5,820</div>
    <div class="waste-label">Estimated Wasted Spend</div>
    <div class="waste-desc">Across 6 ad sets with 0 conversions and 3 critically fatigued creatives in this period.</div>
  </div>
</div>
```

### Fatigue Callout
```html
<div class="fatigue-callout">
  <div>
    <div class="fatigue-count">7 ads</div>
    <div class="fatigue-label">Creative Fatigue Detected</div>
    <div class="fatigue-desc">Average frequency 5.2 — CTR declining across fatigued placements. Immediate creative refresh needed.</div>
  </div>
</div>
```

### Creative Fatigue Table
```html
<table>
  <thead>
    <tr>
      <th>Ad Name</th>
      <th>Ad Set</th>
      <th class="num">Frequency</th>
      <th class="num">CTR Change</th>
      <th class="num">CPA Change</th>
      <th class="num">Est. Waste</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Summer Sale — Video</strong></td>
      <td>Lookalike 1%</td>
      <td class="num freq-high">5.8</td>
      <td class="num ctr-down">▼ 34%</td>
      <td class="num up-bad">▲ 28%</td>
      <td class="num">$640</td>
      <td><span class="badge badge-red">🔴 Pause Now</span></td>
    </tr>
  </tbody>
</table>
```

### Placement Exclusion Box
```html
<div class="exclusion-block">
  <strong style="font-size:13px; color:var(--dark);">Recommended Placement Exclusions:</strong>
  <ul style="margin-top:8px;">
    <li>Audience Network — Interstitial (CPA 4.2× Feed, 0 purchases in 30 days)</li>
    <li>Right Column (CTR 0.08%, no conversions)</li>
    <li>Messenger Stories (CPA $84 vs account avg $32)</li>
  </ul>
</div>
```

### Action Plan
```html
<div class="action-tier-header tier-high">🔴 High Priority — This Week</div>
<div class="action-item">
  <input type="checkbox" class="action-check">
  <div>
    <div class="action-text"><strong>Pause 5 fatigued creatives</strong> — "Summer Sale Video", "Promo Banner Q2", and 3 others with frequency >5 and CTR decline >30%.</div>
    <div class="action-impact">Estimated savings: ~$2,100/month | Reallocate to top 2 creatives performing at $14 CPA</div>
  </div>
</div>

<div class="action-tier-header tier-medium">🟡 Medium Priority — This Month</div>
<!-- medium items -->

<div class="action-tier-header tier-growth">🟢 Growth Opportunities</div>
<!-- growth items -->

<div class="savings-total">💰 Total estimated savings from high-priority actions: $5,820 / month</div>
```

---

## Section Order

1. Header banner (account, period, date, health score)
2. KPI grid — all 11 Meta metrics with PoP deltas (6-column grid)
3. Wasted Spend Callout (prominent, immediately below KPIs)
4. Creative Fatigue Callout (if fatigued ads exist)
5. Module Score Overview card — 7 horizontal score bars
6. Campaign Ranking card — table sorted by ROAS/CPA with status badges
7. Ad Set Audit card — table with audience type column
8. Creative Performance card — table with format badges
9. Creative Fatigue card — dedicated fatigue table
10. Audience Audit card — segment comparison table
11. Placement Audit card — ranked placement table + exclusion box
12. Action Plan card — tiered checklist + savings total
13. Footer

Keep all sections visible (no collapsing for V1). Stack vertically.
