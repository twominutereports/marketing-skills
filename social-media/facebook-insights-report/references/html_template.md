# HTML Audit Report Template

This file contains the CSS foundation, component patterns, and structural guide for the Google Ads Audit HTML report. Use this as your starting point and populate with real data.

## CSS Variables & Base Styles

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Google Ads Audit — [Account Name]</title>
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

  /* Header */
  .audit-header {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    color: white; padding: 32px 40px; border-radius: 12px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .audit-header h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
  .audit-header .meta { font-size: 13px; color: #a0aec0; margin-top: 4px; }
  .health-badge {
    text-align: center; background: rgba(255,255,255,0.1);
    border-radius: 10px; padding: 16px 24px;
  }
  .health-badge .score { font-size: 42px; font-weight: 800; line-height: 1; }
  .health-badge .label { font-size: 12px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

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

  /* Score bar */
  .score-bar-wrap { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
  .score-bar-label { font-size: 13px; color: var(--mid); width: 180px; flex-shrink: 0; }
  .score-bar-track { flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 99px; transition: width 0.3s; }
  .score-bar-value { font-size: 13px; font-weight: 600; width: 50px; text-align: right; }

  /* KPI Tiles */
  .kpi-tile {
    background: var(--white); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; text-align: center;
  }
  .kpi-tile .kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--muted); }
  .kpi-tile .kpi-value { font-size: 26px; font-weight: 800; color: var(--dark); line-height: 1.1; margin: 4px 0; }
  .kpi-tile .kpi-delta { font-size: 12px; font-weight: 600; }
  .delta-up { color: var(--red); } /* CPA going up = bad */
  .delta-down-good { color: var(--green); } /* CPA going down = good */
  .delta-up-good { color: var(--green); } /* Conversions going up = good */
  .delta-down-bad { color: var(--red); }

  /* Wasted Spend Callout */
  .waste-callout {
    background: #fff5f5; border: 2px solid var(--red); border-radius: 10px;
    padding: 20px 28px; margin-bottom: 20px; display: flex; align-items: center; gap: 24px;
  }
  .waste-callout .waste-icon { font-size: 36px; }
  .waste-callout .waste-amount { font-size: 36px; font-weight: 800; color: var(--red); }
  .waste-callout .waste-label { font-size: 14px; font-weight: 600; color: var(--red); }
  .waste-callout .waste-desc { font-size: 13px; color: #742a2a; margin-top: 4px; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: var(--bg); font-weight: 600; font-size: 11px; text-transform: uppercase;
       letter-spacing: 0.5px; color: var(--muted); padding: 8px 12px; text-align: left;
       border-bottom: 1px solid var(--border); }
  td { padding: 9px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--bg); }

  /* Status badges */
  .badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px;
           border-radius: 99px; font-size: 11px; font-weight: 600; }
  .badge-red { background: #fff5f5; color: var(--red); }
  .badge-yellow { background: #fffff0; color: #b7791f; }
  .badge-green { background: #f0fff4; color: var(--green); }
  .badge-gray { background: var(--bg); color: var(--muted); }

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
  .action-check { width: 18px; height: 18px; border: 2px solid var(--border); border-radius: 4px;
                  flex-shrink: 0; margin-top: 1px; cursor: pointer; }
  .action-text { font-size: 13px; line-height: 1.5; }
  .action-impact { font-size: 11px; color: var(--muted); margin-top: 2px; }

  /* Negatives block */
  .negatives-block {
    background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; font-family: monospace; font-size: 12px; white-space: pre-wrap;
    max-height: 200px; overflow-y: auto; color: var(--mid);
  }
  .copy-btn {
    background: var(--blue); color: white; border: none; border-radius: 6px;
    padding: 6px 14px; font-size: 12px; font-weight: 600; cursor: pointer; margin-bottom: 8px;
  }
  .copy-btn:hover { background: #2b6cb0; }

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

When filling score bars and badges, use this mapping:

```javascript
function scoreColor(score, max=20) {
  const pct = score / max;
  if (pct >= 0.85) return 'var(--green)';
  if (pct >= 0.60) return 'var(--yellow)';
  return 'var(--red)';
}

function statusBadge(value, type) {
  // type: 'cpa' | 'roas' | 'ctr' | 'general'
  // Return badge class based on whether value is good/warning/bad
}
```

---

## Component Snippets

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
  <div class="score-bar-label">Wasted Spend Analysis</div>
  <div class="score-bar-track">
    <div class="score-bar-fill" style="width: 60%; background: var(--yellow);"></div>
  </div>
  <div class="score-bar-value" style="color: var(--yellow);">12/20</div>
</div>
```

### Wasted Spend Callout
```html
<div class="waste-callout">
  <div class="waste-icon">🔥</div>
  <div>
    <div class="waste-amount">$3,240</div>
    <div class="waste-label">Estimated Wasted Spend</div>
    <div class="waste-desc">Across 8 campaigns and 47 keywords with zero conversions in the period.</div>
  </div>
</div>
```

### Campaign Table Row (with status badge)
```html
<tr>
  <td><strong>Brand - Exact</strong></td>
  <td>$2,100</td>
  <td>4.8</td>  <!-- ROAS -->
  <td>$8.40</td> <!-- CPA -->
  <td>6.2%</td>  <!-- CTR -->
  <td><span class="badge badge-green">🟢 Scale</span></td>
</tr>
```

### Action Item
```html
<div class="action-item">
  <input type="checkbox" class="action-check">
  <div>
    <div class="action-text"><strong>Pause "Generic Broad" keyword in Campaign X</strong> — spent $480 with 0 conversions over 30 days.</div>
    <div class="action-impact">Estimated savings: ~$480/month | Redirect to "Brand Exact" which converts at $12 CPA</div>
  </div>
</div>
```

### Copy Negatives Button
```html
<button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('negatives').innerText)">
  📋 Copy Negative Keywords
</button>
<div class="negatives-block" id="negatives">
free
cheap
diy
jobs
salary
tutorial
</div>
```

---

## Section Order in Final HTML

1. `<header class="audit-header">` — Account name, period, date, overall score badge
2. `.grid-4` KPI tiles — Spend, Conversions, CPA, ROAS/CTR (whichever available), with PoP deltas
3. `.waste-callout` — Estimated wasted spend (make it the first thing they see after KPIs)
4. Score overview card — horizontal bars for all 5 scored modules
5. Campaign Ranking card — full table, sorted by ROAS/CPA
6. Budget Allocation card — spend % table or bar breakdown
7. Keyword Audit card — table with status badges + pause list
8. Search Terms Audit card — table + negatives copy block
9. Action Plan card — tiered checklist
10. Footer

Keep sections collapsible is optional. For V1, just stack them vertically.
