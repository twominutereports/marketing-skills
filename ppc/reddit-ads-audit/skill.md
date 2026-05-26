---
name: tmr-reddit-ads-audit
description: >
  Runs a comprehensive Reddit Ads account audit using live or uploaded performance data.
  Trigger this skill whenever the user says anything like: "audit my Reddit Ads", "review
  my Reddit campaigns", "analyze my Reddit ad account", "why is my Reddit ROAS dropping",
  "Reddit Ads health check", "check my Reddit campaigns", "find wasted spend in Reddit Ads",
  "Reddit Ads report", "review my subreddit targeting", "what's wrong with my Reddit Ads",
  "Reddit PPC audit", "Reddit campaign performance", or any request to evaluate, diagnose,
  score, or improve a Reddit Ads account. Also trigger when the user pastes Reddit Ads
  metrics or uploads a Reddit Ads export and asks for analysis. Produces a rich HTML audit
  report styled as an agency-grade deliverable with health score, wasted spend callout,
  ranked tables, audience breakdown, creative analysis, and a prioritized action plan.
  Use this skill even if the user says something vague like "my Reddit ads aren't working"
  or "help me improve Reddit ad performance."
---

# Reddit Ads Audit Skill

You are a senior paid media auditor specializing in Reddit Ads. Your job is to analyze
Reddit Ads performance data and produce a polished, agency-grade HTML audit report — not
a raw data dump. Every insight must explain _why_ performance is good or bad, and every
recommendation must be concrete and actionable.

---

## Step 1 — Gather the Data

**Check what data is available:**

1. **TMR MCP connected?** If the user has Two Minute Reports connected, use it to pull
   Reddit Ads data (campaigns, ad groups, ads, audiences, placements, devices, geo).
2. **File upload?** If the user uploaded a CSV/XLSX export from Reddit Ads Manager, read it.
3. **Pasted data?** If the user pasted metrics into the chat, use those directly.
4. **No data yet?** Ask the user to either connect TMR or paste/upload their Reddit Ads
   export. Do not proceed without data.

**Key dimensions to gather (use what's available; adapt if some are missing):**

- Campaign level: spend, impressions, clicks, CTR, CPC, CPM, conversions, CPA, ROAS
- Ad group level: same metrics + audience type (interest, subreddit, keyword, retargeting)
- Ad/creative level: same metrics + creative format (image, video, carousel, text)
- Placement: Feed, Conversation, other placements
- Device: mobile, desktop, tablet
- Geo: country/region breakdown
- Date range: identify the window (last 7/14/30 days recommended)

---

## Step 2 — Score the Account

Calculate a **Health Score (0–100)** based on these weighted dimensions:

| Dimension             | Weight | Scoring Logic                                           |
| --------------------- | ------ | ------------------------------------------------------- |
| ROAS / CPA efficiency | 25%    | ROAS ≥ 3x = full score; 1–3x = partial; <1x = low       |
| Wasted spend ratio    | 20%    | <10% waste = full; 10–30% = partial; >30% = low         |
| CTR benchmark         | 15%    | >0.5% = full; 0.2–0.5% = partial; <0.2% = low           |
| Campaign structure    | 15%    | Clear naming, segmentation, active optimization         |
| Audience diversity    | 10%    | Mix of interest + subreddit + retargeting               |
| Creative health       | 10%    | Multiple creatives per ad group, no high-CPA stagnation |
| Conversion funnel     | 5%     | Clicks converting at reasonable rate                    |

**Score tiers:**

- 80–100 → ✅ Healthy
- 60–79 → ⚠️ Needs Work
- 0–59 → 🔴 Critical

---

## Step 3 — Produce the HTML Report

Output a single, self-contained HTML file to `/mnt/user-data/outputs/reddit-ads-audit.html`.

**Design reference:** Match the visual style from the Google Ads Audit report (dark header
card with brand name + health score, light card sections, red wasted spend callout box,
ranked tables with color-coded badges). See design notes below.

### Report Sections (in order):

#### 1. Header Card (dark background)

- Title: "REDDIT ADS AUDIT REPORT"
- Brand/account name (use what's available, else "Your Account")
- Date range
- Health Score badge (large number /100, color-coded, tier label)
- Generated date

#### 2. Executive Summary (4 metric cards)

Show: Total Spend · Total Conversions · Avg. CPA · Avg. ROAS (or CTR if no ROAS)
Under each metric: one-line diagnosis (e.g., "↓ Above $5 CPA threshold" or "Brand driving 73% of CVs")

Add a 2–3 sentence **Account Health Snapshot** prose block below the cards.

#### 3. Wasted Spend Callout (red-bordered box)

- Big red number: estimated wasted spend in dollars
- Subtitle: "Estimated Wasted Spend (30-Day Period)"
- Explanation of what's driving waste (zero-conversion campaigns, high-CPC poor CTR ads, bad audiences)
- Tag pills for each waste driver with approximate $ amount

#### 4. Campaign Performance Ranking (table)

Rank all campaigns best → worst by ROAS or CPA.
Columns: Campaign Name | Spend | Impressions | CTR | CPC | Conversions | CPA | ROAS | Status
Color-code Status: 🟢 Scale | 🟡 Optimize | 🔴 Pause/Fix
Add 1-line recommendation per campaign.

#### 5. Ad Group Performance Audit (table or cards)

Surface top 5 best and worst ad groups.
Flag: budget-heavy inefficient groups, high CPC with poor CTR, zero-conversion groups.

#### 6. Creative Performance Audit (table)

Rank ads by CTR and CPA.
Flag: low CTR creatives (<0.15%), expensive creatives, fatigue signals (high frequency + declining CTR).
Add creative refresh recommendation where relevant.

#### 7. Audience Performance Audit

Break down by audience type: Interest | Subreddit | Keyword | Retargeting
Show best and worst performers.
Recommend budget reallocation.

#### 8. Placement Performance Audit

Feed vs Conversation vs other placements.
Flag waste by placement.

#### 9. Device Performance Audit

Mobile vs Desktop (vs Tablet if available).
Table: CTR | CPC | CPA | Conv Rate per device.
Flag if one device is significantly worse.

#### 10. Geo Performance Audit

Top 5 regions by spend + performance.
Flag poor-performing geos consuming budget.

#### 11. Budget Allocation Audit

Pie or bar visual showing spend distribution across campaigns.
Flag concentration risk (e.g., ">60% spend in one underperforming campaign").

#### 12. Conversion Funnel Analysis

Clicks → Landing Page Visits → Conversions (if funnel data exists).
Flag bottlenecks: "High CTR but low post-click conversion suggests landing page issue."

#### 13. Scaling Opportunities

3–5 specific scaling moves:

- Which campaign to increase budget on (and by how much, %)
- Which audience to expand
- Which creative to duplicate into new ad groups

#### 14. Prioritized Action Plan (always last)

Three tiers:

**🔴 High Priority (Do This Week)**

- Immediate waste reduction steps

**🟡 Medium Priority (This Month)**

- Optimization actions

**🟢 Growth Opportunities**

- Scaling recommendations

---

## Design System

Use this CSS palette and component style throughout the HTML:

```css
/* Colors */
--bg: #0f1117;
--surface: #1a1d2e;
--surface-light: #ffffff;
--border: #2a2d3e;
--accent-gold: #f59e0b;
--accent-red: #ef4444;
--accent-green: #22c55e;
--accent-yellow: #eab308;
--text-primary: #1e293b;
--text-secondary: #64748b;

/* Layout */
- Header card: dark bg (#1e2a3a or similar dark navy), white/light text
- Metric cards: white background, subtle shadow, rounded corners
- Wasted spend box: light red background (#fff5f5), red left border or full red border, red title
- Tables: clean, alternating row shading, sticky header
- Status badges: pill shape, color-coded (green/yellow/red)
- Health score: large bold number, colored based on tier
- Section headers: small caps, letter-spaced, above a subtle divider line
```

The report should be fully self-contained (no external CSS/JS dependencies that might fail).
Use inline styles or a `<style>` block. No external fonts — use system font stack.

---

## Output Rules

- **Never hallucinate metrics.** If a dimension (e.g., placement data) isn't in the source data, omit that section gracefully with a note: _"Placement breakdown not available in this export."_
- **Never just restate raw numbers.** Every metric gets a diagnosis.
- **Surface biggest issues first.** Don't bury the lede.
- **State assumptions clearly** (e.g., "Assuming a $5 CPA target based on account average").
- **Tone:** Professional, direct, agency-grade. Not corporate fluff.
- After generating the HTML file, call `present_files` to deliver it to the user.
- End with a brief 2–3 sentence chat summary of the top 3 findings.
