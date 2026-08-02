# HTML Audit Report Template — TikTok Ads

This file contains the CSS foundation, component patterns, and structural guide for the TikTok Ads Audit HTML report. Use this as your starting point and populate with real data.

## CSS Variables & Base Styles

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TikTok Ads Audit — [Account Name]</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #e53e3e;
    --red-light: #fff5f5;
    --yellow: #d69e2e;
    --yellow-light: #fffff0;
    --green: #38a169;
    --green-light: #f0fff4;
    --blue: #3182ce;
    --blue-light: #ebf8ff;
    --tiktok: #fe2c55;       /* TikTok brand red */
    --tiktok-dark: #010101;  /* TikTok brand black */
    --tiktok-cyan: #25f4ee;  /* TikTok brand cyan */
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

  /* Layout */
  .container { max-width: 1100px; margin: 0 auto; padding: 24px 20px; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }

  /* Header — dark gradient matching reference design */
  .audit-header {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    color: white; padding: 32px 40px; border-radius: 12px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .audit-header .label-tag {
    font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
    color: #a0aec0; margin-bottom: 8px;
  }
  .audit-header h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
  .audit-header .meta { font-size: 13px; color: #a0aec0; margin-top: 4px; }
  .date-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.15); border-radius: 6px;
    padding: 4px 10px; font-size: 12px; font-weight: 500; margin-top: 10px;
  }
  .health-badge {
    text-align: center; background: rgba(255,255,255,0.1);
    border-radius: 10px; padding: 16px 24px;
  }
  .health-badge .score { font-size: 42px; font-weight: 800; line-height: 1; }
  .health-badge .score.needs-work { color: var(--yellow); }
  .health-badge .score.healthy { color: var(--tiktok-cyan); }
  .health-badge .score.critical { color: var(--red); }
  .health-badge .label { font-size: 12px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
  .health-badge .status { font-size: 11px; color: var(--yellow); margin-top: 2px; }

  /* Cards */
  .card {
    background: var(--white); border-radius: 10px; border: 1px solid var(--border);
    padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .card-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border);
  }
  .card-title { font-size: 15px; font-weight: 700; color: var(--dark); }
  .card-subtitle { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .section-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--muted); margin-bottom: 12px; margin-top: 4px;
  }

  /* Score bar */
  .score-bar-wrap { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
  .score-bar-label { font-size: 13px; color: var(--mid); width: 200px; flex-shrink: 0; }
  .score-bar-track { flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 99px; transition: width 0.3s; }
  .score-bar-value { font-size: 13px; font-weight: 600; width: 50px; text-align: right; }

  /* KPI Tiles */
  .kpi-tile {
    background: var(--white); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; text-align: left;
  }
  .kpi-tile .kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--muted); }
  .kpi-tile .kpi-value { font-size: 26px; font-weight: 800; color: var(--dark); line-height: 1.1; margin: 4px 0; }
  .kpi-tile .kpi-delta { font-size: 12px; font-weight: 600; }
  .delta-up { color: var(--red); }
  .delta-down-good { color: var(--green); }
  .delta-up-good { color: var(--green); }
  .delta-down-bad { color: var(--red); }
  .delta-neutral { color: var(--muted); }

  /* Wasted Spend Callout */
  .waste-callout {
    background: #fff5f5; border: 2px solid var(--red); border-radius: 10px;
    padding: 20px 28px; margin-bottom: 20px;
  }
  .waste-callout-inner { display: flex; align-items: center; gap: 20px; margin-bottom: 14px; }
  .waste-callout .waste-icon { font-size: 36px; }
  .waste-callout .waste-amount { font-size: 40px; font-weight: 800; color: var(--red); line-height: 1; }
  .waste-callout .waste-label { font-size: 14px; font-weight: 700; color: var(--red); margin-top: 2px; }
  .waste-callout .waste-desc { font-size: 13px; color: #742a2a; margin-top: 4px; }
  .waste-tags { display: flex; flex-wrap: wrap; gap: 8px; }
  .waste-tag {
    display: inline-flex; align-items: center; gap: 4px;
    background: white; border: 1px solid #fca5a5; border-radius: 6px;
    padding: 4px 10px; font-size: 12px; color: #742a2a; font-weight: 500;
  }
  .waste-tag.yellow { border-color: #fcd34d; color: #92400e; background: #fffbeb; }

  /* Snapshot block */
  .snapshot-block {
    background: #f8f9ff; border: 1px solid #e0e7ff; border-radius: 8px;
    padding: 14px 18px; margin-top: 16px; font-size: 13px; line-height: 1.7; color: var(--mid);
  }
  .snapshot-block strong { color: var(--dark); }

  /* Takeaway block */
  .takeaway-block {
    background: #f5f3ff; border-left: 3px solid #7c3aed;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin-top: 14px;
    font-size: 13px; line-height: 1.6; color: #4c1d95;
  }
  .takeaway-block strong { font-weight: 700; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: var(--bg); font-weight: 600; font-size: 11px; text-transform: uppercase;
       letter-spacing: 0.5px; color: var(--muted); padding: 8px 12px; text-align: left;
       border-bottom: 1px solid var(--border); }
  td { padding: 9px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--bg); }
  .campaign-name { font-weight: 600; color: var(--dark); }
  .campaign-sub { font-size: 11px; color: var(--muted); margin-top: 1px; font-weight: 400; }

  /* Status badges */
  .badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px;
           border-radius: 99px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .badge-red { background: #fff5f5; color: var(--red); }
  .badge-yellow { background: #fffff0; color: #b7791f; }
  .badge-green { background: #f0fff4; color: var(--green); }
  .badge-gray { background: var(--bg); color: var(--muted); }
  .badge-enabled { background: #f0fff4; color: var(--green); }
  .badge-paused { background: var(--bg); color: var(--muted); }
  .fatigue-flag {
    display: inline-flex; align-items: center; gap: 4px;
    background: #fff5f5; border: 1px solid #fca5a5;
    border-radius: 4px; padding: 2px 7px; font-size: 11px; color: var(--red); font-weight: 600;
  }

  /* Score badge (top right of card) */
  .module-score {
    font-size: 13px; font-weight: 700; padding: 4px 12px;
    border-radius: 99px; white-space: nowrap;
  }
  .module-score.green { background: #f0fff4; color: var(--green); }
  .module-score.yellow { background: #fffff0; color: #b7791f; }
  .module-score.red { background: #fff5f5; color: var(--red); }

  /* Action Plan */
  .action-section { margin-bottom: 16px; }
  .action-priority-header {
    font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
    padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; display: inline-block;
  }
  .priority-high { background: #fff5f5; color: var(--red); }
  .priority-medium { background: #fffff0; color: #b7791f; }
  .priority-growth { background: #f0fff4; color: var(--green); }
  .action-item {
    display: flex; align-items: flex-start; gap: 10px; padding: 10px 0;
    border-bottom: 1px solid var(--border);
  }
  .action-item:last-child { border-bottom: none; }
  .action-check {
    width: 18px; height: 18px; border: 2px solid var(--border); border-radius: 4px;
    flex-shrink: 0; margin-top: 2px; cursor: pointer; appearance: none;
  }
  .action-check:checked { background: var(--green); border-color: var(--green); }
  .action-text { font-size: 13px; line-height: 1.5; }
  .action-impact { font-size: 11px; color: var(--muted); margin-top: 2px; }

  /* Footer */
  .audit-footer {
    text-align: center; font-size: 12px; color: var(--muted); margin-top: 32px;
    padding-top: 20px; border-top: 1px solid var(--border);
  }
</style>
</head>
```

---

## Score Color Logic

```javascript
function scoreColor(score, max=20) {
  const pct = score / max;
  if (pct >= 0.80) return 'var(--green)';
  if (pct >= 0.55) return 'var(--yellow)';
  return 'var(--red)';
}

function moduleScoreClass(score, max=20) {
  const pct = score / max;
  if (pct >= 0.80) return 'green';
  if (pct >= 0.55) return 'yellow';
  return 'red';
}
```

---

## Component Snippets

### Header
```html
<div class="audit-header">
  <div>
    <div class="label-tag">TIKTOK ADS AUDIT REPORT</div>
    <h1>🎵 [Account Name]</h1>
    <div class="meta">Account ID: XXXX · [Workspace Name]</div>
    <div class="date-badge">📅 [Date Range]</div>
    <div class="meta" style="margin-top:6px;">Generated: [Date]</div>
  </div>
  <div class="health-badge">
    <div class="score needs-work">[Score]<span style="font-size:18px;font-weight:400;">/100</span></div>
    <div class="label">Health Score</div>
    <div class="status">⚠️ Needs Work</div>
  </div>
</div>
```

### KPI Tile
```html
<div class="kpi-tile">
  <div class="kpi-label">Total Spend</div>
  <div class="kpi-value">$12,450</div>
  <div class="kpi-delta delta-up">▲ 14% vs prev period</div>
</div>
```

### Score Bar
```html
<div class="score-bar-wrap">
  <div class="score-bar-label">🔥 Wasted Spend Analysis</div>
  <div class="score-bar-track">
    <div class="score-bar-fill" style="width: 55%; background: var(--yellow);"></div>
  </div>
  <div class="score-bar-value" style="color: var(--yellow);">11/20</div>
</div>
```

### Wasted Spend Callout
```html
<div class="waste-callout">
  <div class="waste-callout-inner">
    <div class="waste-icon">🔥</div>
    <div>
      <div class="waste-amount">~$3,240</div>
      <div class="waste-label">Estimated Wasted Spend (30-Day Period)</div>
      <div class="waste-desc">Spend on zero-conversion campaigns, fatigued creatives with frequency > 3.0, and underperforming placements with ROAS &lt; 0.3x.</div>
    </div>
  </div>
  <div class="waste-tags">
    <span class="waste-tag">🔴 Campaign A (Paused) — ~$800 spent</span>
    <span class="waste-tag">🔴 Ad: "Summer Reel v1" — Frequency 4.2, CTR -34%</span>
    <span class="waste-tag yellow">🟡 Pangle Placement — 8 days ROAS &lt;0.5x — ~$240</span>
  </div>
</div>
```

### Campaign Table Row
```html
<tr>
  <td>
    <div class="campaign-name">Brand Awareness - US</div>
    <div class="campaign-sub">AWARENESS_REACH</div>
  </td>
  <td><span class="badge badge-enabled">● ENABLED</span></td>
  <td>$2,100</td>
  <td>4,812</td>
  <td style="color: var(--green); font-weight:600;">$0.43</td>
  <td>~3.1x avg</td>
  <td>1.8%</td>
  <td><span class="badge badge-green">🟢 Scale</span></td>
</tr>
```

### Creative Fatigue Row
```html
<tr>
  <td>
    <div class="campaign-name">Summer Reel v1</div>
    <div class="campaign-sub">In-Feed · Brand Awareness</div>
  </td>
  <td>$840</td>
  <td>0.6%</td>   <!-- CTR -->
  <td>4.2</td>    <!-- Frequency -->
  <td>12%</td>    <!-- 6s View Rate -->
  <td>$3.80</td>  <!-- CPA -->
  <td><span class="fatigue-flag">⚠️ Fatigued</span></td>
</tr>
```

### Action Item
```html
<div class="action-item">
  <input type="checkbox" class="action-check">
  <div>
    <div class="action-text"><strong>Pause "Summer Reel v1" creative in Campaign X</strong> — frequency at 4.2, CTR declined 34%, CPA up 2.8× vs prior period.</div>
    <div class="action-impact">Estimated savings: ~$840/month | Replace with fresh hook-first creative following TikTok's 3-second rule</div>
  </div>
</div>
```

### Snapshot Block
```html
<div class="snapshot-block">
  <strong>Account Health Snapshot:</strong> The Brand campaign is the engine of this account — delivering ~2,123 conversions at an outstanding avg. CPA of $0.43. Creative fatigue is the primary risk: 3 of 5 active In-Feed ads show frequency > 3.0 with CTR declines > 20%. The Retargeting ad group is structurally sound but CPA is 2.3× higher than Prospecting. Two paused campaigns are still accruing minor spend at 9.99% impression share — a cleanup opportunity.
</div>
```

### Takeaway Block
```html
<div class="takeaway-block">
  <strong>Key takeaway:</strong> The account has a strong converting core but is dragged down by creative fatigue and two paused campaigns still accruing spend. Refreshing the top 3 fatigued creatives and reallocating their budgets to the Brand campaign could push the score to 80+.
</div>
```

---

## Section Order in Final HTML

1. `<header class="audit-header">` — Account name, period, date, overall score badge
2. `.grid-4` KPI tiles — Spend, Conversions, CPA, CPM, CTR, Frequency (with PoP deltas)
3. `.waste-callout` — Estimated wasted spend (first thing after KPIs)
4. Module Scorecard card — horizontal bars for all 4 scored modules + takeaway
5. Campaign Ranking card — table sorted by ROAS/CPA, section label "MODULE 2 — CAMPAIGN PERFORMANCE RANKING"
6. Creative Audit card — table with fatigue flags, view rate, CTR — section label "MODULE 3 — CREATIVE AUDIT"
7. Audience & Budget Allocation card — spend % table + demographic breakdown
8. Placement Performance card — table by placement type
9. Action Plan card — tiered checklist
10. Footer

Keep sections stacked vertically. Do not use JavaScript tabs or collapsibles in V1.
