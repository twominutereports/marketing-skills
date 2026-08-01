# HTML Audit Report Template — LinkedIn Ads

This file contains the CSS foundation, component patterns, and structural guide for the LinkedIn Ads Audit HTML report. Use this as your starting point and populate with real data.

The design matches the established audit report style: Inter font, dark navy header, white cards, color-coded score bars, and prominent wasted spend callout.

---

## CSS Variables & Base Styles

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LinkedIn Ads Audit — [Account Name]</title>
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
    --linkedin: #0077b5;
    --linkedin-light: #e8f4fb;
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

  /* Header — dark navy gradient matching design reference */
  .audit-header {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    color: white; padding: 32px 40px; border-radius: 12px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .audit-header .header-left { flex: 1; }
  .audit-header .report-type {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.5px; color: #a0aec0; margin-bottom: 8px;
  }
  .audit-header h1 { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }
  .audit-header .meta { font-size: 13px; color: #a0aec0; margin-top: 6px; }
  .audit-header .date-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0077b5; color: white; border-radius: 6px;
    padding: 4px 12px; font-size: 12px; font-weight: 600; margin-top: 10px;
  }
  .audit-header .generated { font-size: 11px; color: #718096; margin-top: 6px; }

  .health-badge {
    text-align: center; background: rgba(255,255,255,0.1);
    border-radius: 10px; padding: 20px 28px; min-width: 140px;
  }
  .health-badge .score {
    font-size: 46px; font-weight: 800; line-height: 1;
    color: var(--yellow); /* Updated per score — use JS or inline style */
  }
  .health-badge .score span { font-size: 20px; font-weight: 600; color: #a0aec0; }
  .health-badge .label {
    font-size: 11px; color: #a0aec0; text-transform: uppercase;
    letter-spacing: 1px; margin-top: 6px;
  }
  .health-badge .status { font-size: 12px; font-weight: 600; margin-top: 4px; }
  .status-needs-work { color: var(--yellow); }
  .status-good { color: var(--green); }
  .status-critical { color: var(--red); }

  /* Section labels (small caps above cards) */
  .section-label {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: var(--muted); margin-bottom: 12px; margin-top: 8px;
  }

  /* Cards */
  .card {
    background: var(--white); border-radius: 10px; border: 1px solid var(--border);
    padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .card-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border);
  }
  .card-title { font-size: 16px; font-weight: 700; color: var(--dark); display: flex; align-items: center; gap: 8px; }
  .card-subtitle { font-size: 12px; color: var(--muted); margin-top: 3px; }
  .card-score-badge {
    background: var(--yellow-light); color: var(--yellow);
    border: 1px solid #f6e05e; border-radius: 20px;
    padding: 4px 14px; font-size: 13px; font-weight: 700;
    white-space: nowrap;
  }
  .card-score-badge.green { background: var(--green-light); color: var(--green); border-color: #9ae6b4; }
  .card-score-badge.red { background: var(--red-light); color: var(--red); border-color: #feb2b2; }

  /* Score bars */
  .score-bar-wrap { display: flex; align-items: center; gap: 12px; margin: 10px 0; }
  .score-bar-label { font-size: 13px; color: var(--mid); width: 200px; flex-shrink: 0; }
  .score-bar-track { flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .score-bar-fill { height: 100%; border-radius: 99px; }
  .score-bar-value { font-size: 13px; font-weight: 700; width: 50px; text-align: right; }

  /* Key takeaway box */
  .takeaway-box {
    background: #f8f5ff; border-left: 3px solid #805ad5;
    border-radius: 6px; padding: 14px 18px; margin-top: 16px;
    font-size: 13px; line-height: 1.7; color: var(--mid);
  }
  .takeaway-box strong { color: #553c9a; }

  /* KPI Tiles */
  .kpi-tile {
    background: var(--white); border: 1px solid var(--border); border-radius: 8px;
    padding: 18px 16px;
  }
  .kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--muted); font-weight: 500; }
  .kpi-value { font-size: 28px; font-weight: 800; color: var(--dark); line-height: 1.1; margin: 6px 0 4px; }
  .kpi-delta { font-size: 12px; font-weight: 600; }
  .kpi-sub { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .delta-positive { color: var(--green); }
  .delta-negative { color: var(--red); }
  .delta-neutral { color: var(--muted); }

  /* Account snapshot paragraph */
  .snapshot-card {
    background: var(--white); border: 1px solid var(--border); border-radius: 10px;
    padding: 20px 24px; margin-bottom: 20px; font-size: 13px;
    line-height: 1.8; color: var(--mid);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .snapshot-card strong { color: var(--dark); }

  /* Wasted Spend Callout */
  .waste-callout {
    background: var(--red-light); border: 2px solid var(--red); border-radius: 10px;
    padding: 24px 28px; margin-bottom: 20px;
  }
  .waste-top { display: flex; align-items: flex-start; gap: 20px; }
  .waste-icon { font-size: 40px; line-height: 1; }
  .waste-amount { font-size: 40px; font-weight: 800; color: var(--red); line-height: 1; }
  .waste-label { font-size: 15px; font-weight: 700; color: var(--red); margin-top: 4px; }
  .waste-desc { font-size: 13px; color: #742a2a; margin-top: 6px; line-height: 1.6; }
  .waste-items { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
  .waste-item {
    background: white; border: 1px solid #fed7d7; border-radius: 20px;
    padding: 4px 12px; font-size: 12px; color: #742a2a; font-weight: 500;
  }
  .waste-item.yellow { background: #fffff0; border-color: #fefcbf; color: #744210; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  thead th {
    background: var(--bg); font-weight: 600; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted);
    padding: 9px 12px; text-align: left; border-bottom: 2px solid var(--border);
  }
  td { padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tbody tr:hover td { background: #fafafa; }
  td strong { font-weight: 700; color: var(--dark); }
  td .campaign-sub { font-size: 11px; color: var(--muted); font-weight: 400; margin-top: 1px; }

  /* Status badges */
  .badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 600;
  }
  .badge-green { background: var(--green-light); color: var(--green); }
  .badge-yellow { background: var(--yellow-light); color: #b7791f; }
  .badge-red { background: var(--red-light); color: var(--red); }
  .badge-gray { background: var(--bg); color: var(--muted); border: 1px solid var(--border); }
  .badge-linkedin { background: var(--linkedin-light); color: var(--linkedin); }

  /* Finding box (below tables) */
  .finding-box {
    background: #fffaf0; border-left: 3px solid var(--yellow);
    border-radius: 0 6px 6px 0; padding: 12px 16px; margin-top: 16px;
    font-size: 13px; line-height: 1.7; color: var(--mid);
  }
  .finding-box strong { color: #b7791f; }

  /* Action Plan */
  .action-section { margin-bottom: 20px; }
  .action-priority-header {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; padding: 5px 12px; border-radius: 6px;
    margin-bottom: 10px; display: inline-block;
  }
  .priority-high { background: var(--red-light); color: var(--red); }
  .priority-medium { background: var(--yellow-light); color: #b7791f; }
  .priority-growth { background: var(--green-light); color: var(--green); }
  .action-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid var(--border);
  }
  .action-item:last-child { border-bottom: none; }
  .action-check {
    width: 18px; height: 18px; border: 2px solid var(--border);
    border-radius: 4px; flex-shrink: 0; margin-top: 2px; cursor: pointer;
  }
  .action-text { font-size: 13px; line-height: 1.6; }
  .action-impact { font-size: 11px; color: var(--muted); margin-top: 3px; }

  /* Footer */
  .audit-footer {
    text-align: center; font-size: 12px; color: var(--muted);
    margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border);
  }
</style>
</head>
```

---

## Score Color Logic

```javascript
function scoreColor(score, max) {
  const pct = score / max;
  if (pct >= 0.85) return 'var(--green)';
  if (pct >= 0.60) return 'var(--yellow)';
  return 'var(--red)';
}

function overallLabel(total) {
  if (total >= 70) return { text: 'Excellent', cls: 'status-good' };
  if (total >= 55) return { text: 'Good', cls: 'status-good' };
  if (total >= 40) return { text: 'Needs Work', cls: 'status-needs-work' };
  return { text: 'Critical', cls: 'status-critical' };
}
```

---

## Component Snippets

### Header
```html
<div class="audit-header">
  <div class="header-left">
    <div class="report-type">LinkedIn Ads Audit Report</div>
    <h1>💼 [Account Name]</h1>
    <div class="meta">Account ID: [ID] · [Workspace Name]</div>
    <div class="date-badge">📅 [Start Date] – [End Date] (Last 30 Days)</div>
    <div class="generated">Generated: [Date]</div>
  </div>
  <div class="health-badge">
    <div class="score" style="color: var(--yellow);">61<span>/80</span></div>
    <div class="label">Health Score</div>
    <div class="status status-needs-work">⚠ Needs Work</div>
  </div>
</div>
```

### KPI Grid
```html
<div class="section-label">Executive Summary</div>
<div class="grid-4" style="margin-bottom: 20px;">
  <div class="kpi-tile">
    <div class="kpi-label">Total Spend</div>
    <div class="kpi-value">$8,420</div>
    <div class="kpi-sub">Last 30 days · 4 campaigns</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Total Leads</div>
    <div class="kpi-value">183</div>
    <div class="kpi-delta delta-positive">↑ Lead Gen driving 74%</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Avg. CPL</div>
    <div class="kpi-value">$46</div>
    <div class="kpi-delta delta-positive">↓ Well below $60 threshold</div>
  </div>
  <div class="kpi-tile">
    <div class="kpi-label">Avg. CTR</div>
    <div class="kpi-value">0.54%</div>
    <div class="kpi-sub">Blended across active campaigns</div>
  </div>
</div>
```

### Account Snapshot
```html
<div class="snapshot-card">
  <strong>Account Health Snapshot:</strong> The Webinar campaign is the engine of this account — delivering ~135 leads at a CPL of $38, well below the account average. The Whitepaper campaign shows strong engagement but CPL is 2.1× higher. Two campaigns are <strong>paused</strong> yet still accruing impressions, pointing to a billing/status sync issue. Creative fatigue is evident in the Demo Request campaign — frequency has exceeded 4.2× with CTR down 28% from the prior period.
</div>
```

### Wasted Spend Callout
```html
<div class="waste-callout">
  <div class="waste-top">
    <div class="waste-icon">🔥</div>
    <div>
      <div class="waste-amount">~$1,840</div>
      <div class="waste-label">Estimated Wasted Spend (30-Day Period)</div>
      <div class="waste-desc">Spend captured by paused campaigns still delivering, zero-conversion ad sets, and high-frequency creatives with declining CTR. Redirecting this to the Webinar campaign could add ~48 leads at its current CPL.</div>
    </div>
  </div>
  <div class="waste-items">
    <span class="waste-item">🔴 Demo Request (Paused) — ~$620 still spent</span>
    <span class="waste-item">🔴 Brand Awareness — $480 zero leads</span>
    <span class="waste-item waste-item yellow">🟡 Whitepaper: 6 days CPL > $90 — ~$740</span>
  </div>
</div>
```

### Module Scorecard Card
```html
<div class="card">
  <div class="card-header">
    <div>
      <div class="card-title">📊 Module Scorecard</div>
      <div class="card-subtitle">4 scored modules · Max 80 points</div>
    </div>
    <div class="card-score-badge">61 / 80 — Needs Work</div>
  </div>

  <div class="score-bar-wrap">
    <div class="score-bar-label">🔥 Wasted Spend Analysis</div>
    <div class="score-bar-track">
      <div class="score-bar-fill" style="width: 55%; background: var(--yellow);"></div>
    </div>
    <div class="score-bar-value" style="color: var(--yellow);">11/20</div>
  </div>
  <!-- repeat for other modules -->

  <div class="takeaway-box">
    <strong>Key takeaway:</strong> The account has a strong lead gen core but is dragged down by creative fatigue and paused campaigns still burning budget. Fixing those two issues alone could push the score above 70.
  </div>
</div>
```

### Campaign Rankings Table
```html
<div class="card">
  <div class="card-header">
    <div>
      <div class="card-title">📈 Campaign Rankings (Last 30 Days)</div>
      <div class="card-subtitle">Active campaigns sorted by performance</div>
    </div>
    <div class="card-score-badge green">15/20</div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Campaign</th>
        <th>Status</th>
        <th>Spend</th>
        <th>Leads</th>
        <th>CPL</th>
        <th>CTR</th>
        <th>Freq.</th>
        <th>Flag</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <strong>Webinar — Q3 2026</strong>
          <div class="campaign-sub">LEAD_GEN · Sponsored Content</div>
        </td>
        <td><span class="badge badge-green">● ENABLED</span></td>
        <td>$3,200</td>
        <td>135</td>
        <td style="color: var(--green); font-weight: 700;">$23.70</td>
        <td>0.72%</td>
        <td>2.1×</td>
        <td><span class="badge badge-green">🟢 Scale</span></td>
      </tr>
      <tr>
        <td>
          <strong>Demo Request — Enterprise</strong>
          <div class="campaign-sub">LEAD_GEN · Sponsored Content</div>
        </td>
        <td><span class="badge badge-yellow">⏸ PAUSED</span></td>
        <td style="color: var(--red);">$620 <small>(still accruing!)</small></td>
        <td>~12</td>
        <td style="color: var(--red); font-weight: 700;">$51.67</td>
        <td>0.28%</td>
        <td>4.8×</td>
        <td><span class="badge badge-red">🔴 Stop / Review</span></td>
      </tr>
    </tbody>
  </table>
  <div class="finding-box">
    <strong>Finding:</strong> The Webinar campaign is the star — at $23.70 CPL with 0.72% CTR, it should receive any freed-up budget. The Demo Request campaign being paused yet still spending $620 with frequency at 4.8× is a critical red flag requiring immediate investigation.
  </div>
</div>
```

### Action Plan
```html
<div class="card">
  <div class="card-header">
    <div>
      <div class="card-title">✅ Prioritized Action Plan</div>
      <div class="card-subtitle">Specific steps ranked by impact</div>
    </div>
  </div>

  <div class="action-section">
    <div class="action-priority-header priority-high">🔴 High Priority — This Week</div>
    <div class="action-item">
      <input type="checkbox" class="action-check">
      <div>
        <div class="action-text"><strong>Investigate and fix "Demo Request — Enterprise" paused status</strong> — campaign shows Paused but spent $620 in the period at 4.8× frequency.</div>
        <div class="action-impact">Estimated savings: ~$620/month · Root cause likely a billing issue or sub-campaign override</div>
      </div>
    </div>
  </div>

  <div class="action-section">
    <div class="action-priority-header priority-medium">🟡 Medium Priority — This Month</div>
    <div class="action-item">
      <input type="checkbox" class="action-check">
      <div>
        <div class="action-text"><strong>Refresh creatives in Whitepaper campaign</strong> — frequency at 3.9× with CTR declining 22% from prior period.</div>
        <div class="action-impact">Test 2–3 new image variants and one video creative</div>
      </div>
    </div>
  </div>

  <div class="action-section">
    <div class="action-priority-header priority-growth">🟢 Growth Opportunities</div>
    <div class="action-item">
      <input type="checkbox" class="action-check">
      <div>
        <div class="action-text"><strong>Scale Webinar campaign budget by 30–50%</strong> — CPL at $23.70 is well below the $60 target, and audience still has headroom.</div>
        <div class="action-impact">Estimated +40–65 additional leads/month at current CPL</div>
      </div>
    </div>
  </div>
</div>
```

---

## Section Order in Final HTML

1. `<div class="audit-header">` — Account name, period, date, overall score badge
2. `<div class="section-label">Executive Summary</div>` + `.grid-4` KPI tiles
3. `.snapshot-card` — Account Health Snapshot paragraph
4. `.waste-callout` — Estimated wasted spend (prominent, above the fold)
5. Module Scorecard card — horizontal bars for all 4 scored modules + key takeaway
6. Campaign Rankings card — table sorted by CPL/CTR, with objective + status badges
7. Creative Audit card — table with fatigue flags, frequency, CTR, status
8. Audience & Budget Allocation card — spend % table + demographic breakdown
9. Ad Format Performance card — table by format type (Sponsored Content, Message Ads, etc.)
10. Action Plan card — tiered checklist
11. Footer

Keep all sections stacked vertically. No tabs or collapsible sections needed for V1.
