---
name: tmr-seo-analytics-report
description: Use this skill when the user asks to generate an SEO report, run an SEO + analytics performance report, check search console and GA4 performance, create a client SEO report, or analyze organic search visibility combined with website analytics. Covers Google Search Console metrics (impressions, clicks, CTR, average position, top pages by clicks, weekly search trends) and GA4 metrics (sessions, users, key events, bounce rate, top landing pages by sessions and key events, month-over-month landing page performance, and AI traffic from known AI referrers). Produces an inline insights summary plus a full HTML dashboard artifact.
version: 2.0.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with Google Search Console (gsc) and Google Analytics 4 (ga4) connectors"
---

# SEO + Analytics Performance Report

> **MCP version note.** This skill targets the current TMR MCP. Its data flow is: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`, `generate_query`, and `get_data_insights` no longer exist. Connector IDs: **`gsc`** (Search Console), **`ga4`** (Analytics). Field IDs are raw. The natural-language prompts from the previous version are now 9 validated structured queries (stored in `queries.json`, mirrored in step 5). Date ranges are computed fresh at runtime.

## Purpose

Generate a comprehensive SEO + Analytics Performance Report by combining Google Search Console (GSC) and GA4 data. The report gives marketers and agency teams a full-funnel view of their site's organic performance — from search visibility to on-site behavior to conversions — including AI traffic as an emerging channel.

Trigger phrases: "generate my SEO report", "run the SEO + analytics report", "show me my search console and GA4 performance", "create my client SEO report", "check my organic performance".

## Connectors required

This skill uses the following TMR connectors:
- Google Search Console (`gsc`)
- Google Analytics 4 (`ga4`)

The runtime procedure below verifies these are available before doing any analytical work. Do not attempt to proceed with partial connector availability.

---

## Runtime procedure

Follow these steps in order. Do not skip steps. Do not rearrange.

### 1. Check that TMR's tools are available

Inspect your available tools. The current Two Minute Reports MCP exposes these tool names: `verify_team_details`, `list_connectors`, `get_connector_accounts`, `get_connector_query_schema`, `validate_query`, `run_query`. The prefix may vary — users name their MCP connections differently (e.g., "Two Minute Reports", "TMR", "TwoMinuteReports", or a custom name). Match by tool function and the Two Minute Reports MCP server (URL: `https://mcp.twominutereports.com/mcp`), not by exact prefix.

**If none of these tools are present in your available tool list**, the user has not connected the Two Minute Reports MCP to their Claude account. Tell them:

> *"This skill needs Two Minute Reports to be connected to your Claude account, but I don't see it in your available tools.*
>
> *Two Minute Reports is an analytics platform that lets you query your marketing data (ads, analytics, e-commerce, etc.) from inside Claude. You'll need to connect it once, then this skill (and any other TMR skills) will work.*
>
> *Here's the setup guide: https://twominutereports.com/help/mcp/claude*
>
> *Once it's connected, run this skill again."*

If a `suggest_connectors` capability is available in your environment, also use it to surface a one-tap connect option for the Two Minute Reports MCP. Then stop — do not attempt any further steps in this conversation.

If the tools ARE present, hold onto the resolved tool prefix internally and continue.

### 2. Verify team details and authentication

Call the `verify_team_details` tool from the Two Minute Reports MCP.

- **If it returns multiple teams**, present them and ask which to use. Store the chosen `teamId` for every subsequent call.
- **If the call succeeds and returns a single team**, tell the user which team is active, store its `teamId`, and continue to step 3.
- **Plan status:** `active`, `in_trial`, and `non_renewing` are fine. If the chosen team's `planStatus` is `cancelled`, stop and tell the user: *"Your Two Minute Reports plan is cancelled, so I can't pull data. Reactivate it at hub.twominutereports.com/billing, then run this skill again."* Do not call `validate_query` or `run_query`.
- **If the call fails with an authentication, permission, or session error, OR returns an empty/missing team**, tell the user:

  > *"Two Minute Reports is connected, but I couldn't verify your team details — your session may have expired or the connection needs to be re-authenticated. Please reconnect Two Minute Reports, then run this skill again. Setup reference: https://twominutereports.com/help/mcp/claude"*

  If `suggest_connectors` is available, trigger it for the Two Minute Reports MCP. Then stop.

- **If the call fails for any other reason** (network, server down), tell the user *"Couldn't reach Two Minute Reports right now — please try again in a moment."* and stop.

### 3. Verify required connectors are provisioned in TMR

Call `get_connector_accounts` from the Two Minute Reports MCP once per connector, with `teamId`:
- `get_connector_accounts(teamId, connectorId: "gsc", status: "enabled")`
- `get_connector_accounts(teamId, connectorId: "ga4", status: "enabled")`

- **If BOTH return at least one enabled account**, continue to step 4. (GSC account IDs are site URLs like `https://example.com/`; GA4 account IDs are numeric property IDs.)
- **If either connector returns empty**, tell the user:

  > *"This skill needs both Google Search Console and Google Analytics 4 to be set up inside Two Minute Reports, but one or both aren't connected yet. Please open Two Minute Reports, add the missing connector(s) to your workspace, then come back and run this skill again."*

  Stop. Do not proceed with partial connector availability.

- **If a call fails entirely** (vs returning empty), use the step 2 reconnect message.

### 4. Locate skill folder and load configuration

Locate this skill's install folder to read/write `config.json`. Try in order:

1. `/mnt/skills/user/tmr-seo-analytics-report/`
2. If not found, run `find /mnt/skills -name "tmr-seo-analytics-report" -type d 2>/dev/null` and use the first result
3. If still not found, treat as "no install folder available" — skip all config read/write and skip the save prompt in step 7

Hold the resolved path as `<install-path>` internally.

Then read `<install-path>/config.json`.

**If the file exists, is readable, and has `saved: true`:**

- Tell the user: *"Using your saved configuration: accounts [list labels], no currency required for this report. Say 'change config' if you want to update these."*
- Use the stored `accounts` and `auto_confirm_query` values for the rest of this run.
- If the user says "change config", fall through to the collection flow below and re-ask the save question in step 7.

**If the file exists but `saved: false`, OR doesn't exist, OR can't be read:**

- Reuse the `get_connector_accounts` responses from step 3 — do not call again.
- Present the accounts grouped by connector and ask: *"Which account(s) would you like to analyze? Pick one per connector (e.g., your GSC property and your GA4 property for the same website)."*
- Wait for their selection.

This skill does not use currency metrics — do not ask for currency.

### 5. Build, validate, and run the queries

This skill runs **9 structured queries** across the `gsc` and `ga4` connectors (stored in `queries.json`, mirrored below). The previous version sent natural-language prompts to `generate_query`; the new MCP has no such tool, so each data pull is an explicit query built from raw field IDs and validated before running.

**Resolve date windows from today's actual date** (GSC data lags ~2–3 days; if the most recent days look empty, that's expected):
- 90-day window for Q1–Q4, Q6, Q7.
- The two most recent **full calendar months** for Q5 (GA4 MoM) and Q8a/Q8b (GSC page MoM). Example: if today is in June, the two months are April (M1) and May (M2).

**Procedure:**
a. Assemble the connector entries — one `gsc` entry and one `ga4` entry — with the user's selected accounts and the queries below.
b. Call `validate_query(teamId, connectors:[...])`. If any query errors, fix the named field/rule and re-validate.
c. If `auto_confirm_query` is `true`, skip confirmation. Otherwise present a one-line summary of what will be pulled and ask for explicit confirmation.
d. Call `run_query(teamId, connectors:[...], limit:...)`. No `currencyCode` is needed (this report uses no monetary metrics). If a result returns as a stored file path, parse it with code execution (`connectorResults[].results[].data` → `headers`/`rows`).
e. Hold all returned data for synthesis in step 6.

**GSC queries** (account = site URL):
- **Q1 — GSC totals (90d):** dims none · metrics `clicks`, `impressions`, `ctr`, `position`
- **Q3 — GSC pages (90d):** dims `page` · metrics `clicks`, `impressions`, `ctr`, `position` (take top 5 by clicks in synthesis)
- **Q6 — GSC weekly (90d):** dims `week_start_date` · metrics `impressions`, `clicks`
- **Q8a — GSC pages, month 1:** dims `page` · metrics `impressions`, `clicks` · dateRange = first of the last two full calendar months
- **Q8b — GSC pages, month 2:** dims `page` · metrics `impressions`, `clicks` · dateRange = second of the last two full calendar months

**GA4 queries** (account = numeric property ID):
- **Q2 — GA4 totals (90d):** dims none · metrics `sessions`, `total_users`, `key_events`, `bounce_rate`
- **Q4 — GA4 landing pages (90d):** dims `landing_page` · metrics `sessions`, `key_events` (take top 5 by sessions and top 5 by key events in synthesis)
- **Q5 — GA4 landing page × month (last 2 full months):** dims `landing_page`, `month_name` · metrics `sessions`
- **Q7 — GA4 session source (90d):** dims `session_source` · metrics `sessions`, `total_users`, `new_users`, `bounce_rate`, `key_events`

> **AI-referrer handling (Q7):** Pull ALL session sources, then **filter to known AI referrers during synthesis** — `chatgpt.com`, `gemini.google.com`, `claude.ai`, `perplexity.ai`, `copilot.com`, `notebooklm.google.com` (match on the source string, allowing for `/referral` suffixes). This avoids connector-side filter syntax and is robust. If none of these sources appear, report AI traffic as zero/none rather than omitting the section.

> **Keyword deduplication rule (apply during synthesis in step 6):** The Page dimension acts as a proxy for the primary keyword for that page. One page = one keyword slot. Sort all pages by total impressions descending across both periods (Q8a + Q8b). Derive each page's keyword from its URL path (last meaningful slug segment, hyphens → spaces). If two pages map to the same readable keyword, keep the one with higher impressions and skip the other. This ensures each keyword in the Best/Worst tables represents a distinct page and topic.

---

### 6. Produce the dual output

Once all queries have returned data, produce BOTH outputs simultaneously.

#### Insights (inline chat)

Write a 150–300 word insights summary inline in chat. Structure:

1. **Headline finding** — what's the single most important thing the user should know about their organic performance?
2. **Search visibility** — key GSC numbers (impressions, clicks, CTR, avg position) and what they indicate.
3. **On-site behaviour** — GA4 sessions, users, key events, bounce rate and what they mean together.
4. **Top pages** — which pages are driving the most value (clicks, sessions, conversions)?
5. **MoM shifts** — which landing pages are growing or declining, and by how much?
6. **AI traffic** — which AI platform is sending the most traffic, and is it converting?
7. **One action** — a single concrete recommendation the marketer can act on this week.

Match the tone, voice, structure, and rhythm of this sanitized template. Replace `[brackets]` with the user's actual data:

---

*Organic performance over the last [reporting period] shows [X] impressions and [N] clicks from Google Search Console, at an average CTR of [Y%] and average position [P]. [Positive/negative framing based on benchmarks — e.g. "CTR is below the [X%] threshold typical for position [P], suggesting title and meta description optimisation could unlock meaningful click gains."].*

*On-site, GA4 recorded [N] sessions and [N] total users, with [N] key events and a [Y%] bounce rate. [Interpretation — e.g. "Bounce rate is [above/below] the [X%] benchmark for organic traffic, indicating [strong/weak] content-to-intent match."].*

*Top pages by clicks: [page 1] ([N] clicks), [page 2], [page 3]. Top landing pages by sessions: [page 1] ([N] sessions), [page 2]. The [top conversion page] leads on key events with [N], making it the site's most valuable organic entry point.*

*Month-over-month, [best performer] grew sessions by [X%] ([N] → [N]) — worth understanding what drove that. [Worst performer] dropped [X%] — worth diagnosing whether this is a ranking loss, seasonality, or content decay.*

*AI referrals totalled [N] sessions across [N] platforms. [Top AI source] led with [N] sessions and [N] key events — [interpretation, e.g. "the highest conversion rate among AI sources, suggesting strong brand-content alignment with that platform's audience"]. Overall AI traffic is [growing/steady/small] as a share of organic.*

*Recommended action: [one specific, actionable next step based on the data — e.g. "Prioritise improving the meta title for [top impression page] — it has [N] impressions but only [Y%] CTR, meaning small copy improvements could drive significant click volume without any ranking work."].*

---

#### Dashboard (artifact)

Produce a NEW artifact for this run using the title format:

`SEO + Analytics Performance Report — YYYY-MM-DD HH:MM — [primary GSC property]`

Do not update or replace any prior artifact, even if a similar one exists in the conversation.

Use this scaffold. Replace every `{{PLACEHOLDER}}` with the user's actual data. Do not modify the layout, CSS, or structure:

```html
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
.report { padding: 1rem 0; font-family: var(--font-sans); }

/* ── Header ── */
.meta-header { display: flex; justify-content: space-between; align-items: flex-start; padding-bottom: 1.25rem; border-bottom: 1px solid var(--color-border-tertiary); margin-bottom: 2rem; }
.meta-title { font-size: 20px; font-weight: 600; color: var(--color-text-primary); display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.meta-dates { font-size: 12px; color: var(--color-text-secondary); text-align: right; flex-shrink: 0; line-height: 1.6; }

/* ── Badges ── */
.badge { font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px; letter-spacing: 0.02em; }
.badge-gsc { background: #E1F5EE; color: #0F6E56; }
.badge-ga4 { background: #E6F1FB; color: #185FA5; }
.badge-ai  { background: #EEEDFE; color: #534AB7; }

/* ── Section ── */
.section { margin-bottom: 2.5rem; }
.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 1.25rem; }
.section-bar { width: 4px; height: 20px; background: #1D9E75; border-radius: 3px; flex-shrink: 0; }
.section-title { font-size: 16px; font-weight: 600; color: var(--color-text-primary); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

/* ── KPI grid — 2 columns matching screenshot ── */
.kpi-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.kpi-card {
  background: var(--color-background-primary);
  border: 1px solid var(--color-border-tertiary);
  border-radius: 14px;
  padding: 22px 24px 20px;
  position: relative;
  min-height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.kpi-source { position: absolute; top: 14px; right: 14px; }
.kpi-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  padding-right: 44px;
  margin-bottom: 10px;
  line-height: 1.3;
}
.kpi-value {
  font-size: 36px;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.kpi-sub {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 6px;
  font-weight: 400;
}

/* ── Chart cards ── */
.chart-card {
  background: var(--color-background-primary);
  border: 1px solid var(--color-border-tertiary);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 14px;
}
.chart-title { font-size: 13px; font-weight: 600; color: var(--color-text-primary); margin-bottom: 4px; }
.chart-sub { font-size: 11px; color: var(--color-text-secondary); margin-bottom: 14px; line-height: 1.4; }

/* ── Bar chart rows ── */
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.bar-label { font-size: 11px; color: var(--color-text-secondary); width: 170px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; text-align: right; }
.bar-track { flex: 1; height: 10px; background: var(--color-background-secondary); border-radius: 5px; overflow: hidden; min-width: 0; }
.bar-fill { height: 100%; border-radius: 5px; }
.bar-val { font-size: 11px; font-weight: 500; color: var(--color-text-primary); width: 50px; text-align: left; flex-shrink: 0; }

/* ── Two-column layout ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

/* ── MoM table ── */
.mom-table { width: 100%; font-size: 12px; border-collapse: collapse; table-layout: fixed; }
.mom-table th { color: var(--color-text-secondary); font-weight: 600; font-size: 11px; padding: 6px 8px; border-bottom: 1px solid var(--color-border-tertiary); text-align: left; text-transform: uppercase; letter-spacing: 0.05em; }
.mom-table td { padding: 7px 8px; color: var(--color-text-primary); vertical-align: middle; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mom-table tr:not(:last-child) td { border-bottom: 1px solid var(--color-border-tertiary); }
.pill-up { display: inline-block; background: #EAF3DE; color: #3B6D11; font-size: 10px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }
.pill-dn { display: inline-block; background: #FCEBEB; color: #A32D2D; font-size: 10px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }

/* ── Weekly chart ── */
.chart-wrap { position: relative; width: 100%; height: 140px; }

/* ── AI section ── */
.ai-kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 14px; }
.ai-table { width: 100%; font-size: 12px; border-collapse: collapse; }
.ai-table th { color: var(--color-text-secondary); font-weight: 600; font-size: 11px; padding: 7px 10px; border-bottom: 1px solid var(--color-border-tertiary); text-align: right; text-transform: uppercase; letter-spacing: 0.05em; }
.ai-table th:first-child { text-align: left; }
.ai-table td { padding: 8px 10px; color: var(--color-text-primary); text-align: right; font-size: 12px; }
.ai-table td:first-child { text-align: left; }
.ai-table tr:not(:last-child) td { border-bottom: 1px solid var(--color-border-tertiary); }
.ai-pill { display: inline-block; background: var(--color-background-secondary); border: 1px solid var(--color-border-tertiary); border-radius: 8px; padding: 3px 9px; font-size: 11px; font-weight: 500; color: var(--color-text-primary); }
.br-warn { color: #BA7517; font-weight: 500; }
.br-ok   { color: #3B6D11; font-weight: 500; }

/* ── Keyword tables ── */
.kw-table { width: 100%; font-size: 12px; border-collapse: collapse; table-layout: fixed; }
.kw-table th { color: var(--color-text-secondary); font-weight: 600; font-size: 11px; padding: 6px 8px; border-bottom: 1px solid var(--color-border-tertiary); text-align: left; text-transform: uppercase; letter-spacing: 0.05em; }
.kw-table th:not(:first-child) { text-align: right; width: 70px; }
.kw-table td { padding: 8px 8px; color: var(--color-text-primary); vertical-align: middle; }
.kw-table td:not(:first-child) { text-align: right; }
.kw-table tr:not(:last-child) td { border-bottom: 1px solid var(--color-border-tertiary); }
.kw-cell { display: flex; flex-direction: column; gap: 2px; }
.kw-label { font-size: 12px; font-weight: 500; color: var(--color-text-primary); }
.kw-page  { font-size: 10px; color: var(--color-text-secondary); font-family: monospace; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 240px; display: block; }
</style>

<div class="report">
  <h2 class="sr-only">SEO and Analytics Performance Report combining Google Search Console and GA4 data</h2>

  <!-- METADATA HEADER -->
  <div class="meta-header">
    <div>
      <div class="meta-title">
        SEO + Analytics Performance Report
        <span class="badge badge-gsc">GSC</span>
        <span class="badge badge-ga4">GA4</span>
      </div>
      <div style="font-size:12px;color:var(--color-text-secondary);margin-top:4px;">Two Minute Reports · {{GSC_PROPERTY}}</div>
    </div>
    <div class="meta-dates">{{DATE_RANGE}}<br>Last updated: {{RUN_DATE}}</div>
  </div>

  <!-- EXECUTIVE SUMMARY -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">Executive summary</div></div>
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-gsc">GSC</span></div><div class="kpi-label">Impressions</div><div class="kpi-value">{{GSC_IMPRESSIONS}}</div><div class="kpi-sub">Last 90 days</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-gsc">GSC</span></div><div class="kpi-label">Clicks</div><div class="kpi-value">{{GSC_CLICKS}}</div><div class="kpi-sub">Last 90 days</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-gsc">GSC</span></div><div class="kpi-label">Click-through rate</div><div class="kpi-value">{{GSC_CTR}}</div><div class="kpi-sub">Avg across queries</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-gsc">GSC</span></div><div class="kpi-label">Avg position</div><div class="kpi-value">{{GSC_AVG_POSITION}}</div><div class="kpi-sub">All queries</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-ga4">GA4</span></div><div class="kpi-label">Sessions</div><div class="kpi-value">{{GA4_SESSIONS}}</div><div class="kpi-sub">Last 90 days</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-ga4">GA4</span></div><div class="kpi-label">Total users</div><div class="kpi-value">{{GA4_USERS}}</div><div class="kpi-sub">Last 90 days</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-ga4">GA4</span></div><div class="kpi-label">Key events</div><div class="kpi-value">{{GA4_KEY_EVENTS}}</div><div class="kpi-sub">Last 90 days</div></div>
      <div class="kpi-card"><div class="kpi-source"><span class="badge badge-ga4">GA4</span></div><div class="kpi-label">Bounce rate</div><div class="kpi-value">{{GA4_BOUNCE_RATE}}</div><div class="kpi-sub">Avg across sessions</div></div>
    </div>
  </div>

  <!-- TOP LANDING PAGES -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">Top 5 landing pages</div></div>
    <div class="two-col">
      <div class="chart-card">
        <div class="chart-title">Top pages by clicks</div>
        <div class="chart-sub">Source: Google Search Console</div>
        <!-- Render top 5 pages by GSC clicks as bar rows. Max bar width = 100% for rank 1. -->
        <!-- For each page: <div class="bar-row"><div class="bar-label">{{PAGE_PATH}}</div><div class="bar-track"><div class="bar-fill" style="width:{{PCT}}%;background:#1D9E75;"></div></div><div class="bar-val">{{CLICKS}}</div></div> -->
        {{TOP_PAGES_BY_CLICKS_BARS}}
      </div>
      <div class="chart-card">
        <div class="chart-title">Top pages by sessions</div>
        <div class="chart-sub">Source: GA4</div>
        {{TOP_PAGES_BY_SESSIONS_BARS}}
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-title">Top pages by key events</div>
      <div class="chart-sub">Source: GA4</div>
      {{TOP_PAGES_BY_EVENTS_BARS}}
    </div>
  </div>

  <!-- LANDING PAGE MoM -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">Landing page performance — {{MOM_LABEL}} <span class="badge badge-ga4">GA4</span></div></div>
    <div class="two-col">
      <div class="chart-card">
        <div class="chart-title">Best performers</div>
        <div class="chart-sub">Top 5 by session growth, {{MOM_PERIOD}}</div>
        <table class="mom-table">
          <colgroup><col style="width:55%"><col style="width:15%"><col style="width:15%"><col style="width:15%"></colgroup>
          <tr><th>Page</th><th>{{MONTH_1}}</th><th>{{MONTH_2}}</th><th>Growth</th></tr>
          <!-- For each best performer row: <tr><td>{{PAGE}}</td><td>{{M1_SESSIONS}}</td><td>{{M2_SESSIONS}}</td><td><span class="pill-up">+{{PCT}}%</span></td></tr> -->
          {{BEST_PERFORMERS_ROWS}}
        </table>
      </div>
      <div class="chart-card">
        <div class="chart-title">Worst performers</div>
        <div class="chart-sub">Top 5 by session decline, {{MOM_PERIOD}}</div>
        <table class="mom-table">
          <colgroup><col style="width:55%"><col style="width:15%"><col style="width:15%"><col style="width:15%"></colgroup>
          <tr><th>Page</th><th>{{MONTH_1}}</th><th>{{MONTH_2}}</th><th>Loss</th></tr>
          {{WORST_PERFORMERS_ROWS}}
        </table>
      </div>
    </div>
  </div>

  <!-- KEYWORD PERFORMERS -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">Keyword performers — {{KW_PERIOD_LABEL}} <span class="badge badge-gsc">GSC</span></div></div>
    <div style="font-size:11px;color:var(--color-text-secondary);margin-bottom:14px;margin-top:-8px;">One primary keyword per page (highest impressions). Secondary keywords for the same page are excluded.</div>

    <!-- IMPRESSIONS -->
    <div class="two-col" style="margin-bottom:14px;">
      <div class="chart-card" style="margin-bottom:0;">
        <div class="chart-title">↑ Best — Impression gainers</div>
        <div class="chart-sub">Top 5 pages by impression increase, {{KW_PERIOD_M1}} vs {{KW_PERIOD_M2}}</div>
        <table class="kw-table">
          <colgroup><col style="width:52%"><col style="width:16%"><col style="width:16%"><col style="width:16%"></colgroup>
          <tr><th>Keyword / Page</th><th>Before</th><th>After</th><th>Change</th></tr>
          <!-- For each row: <tr><td><div class="kw-cell"><span class="kw-label">{{KEYWORD}}</span><span class="kw-page">{{PAGE_PATH}}</span></div></td><td>{{IMP_BEFORE}}</td><td>{{IMP_AFTER}}</td><td><span class="pill-up">{{PCT}}</span></td></tr> -->
          {{KW_BEST_IMP_ROWS}}
        </table>
      </div>
      <div class="chart-card" style="margin-bottom:0;">
        <div class="chart-title">↓ Worst — Impression drops</div>
        <div class="chart-sub">Top 5 pages by impression decline, {{KW_PERIOD_M1}} vs {{KW_PERIOD_M2}}</div>
        <table class="kw-table">
          <colgroup><col style="width:52%"><col style="width:16%"><col style="width:16%"><col style="width:16%"></colgroup>
          <tr><th>Keyword / Page</th><th>Before</th><th>After</th><th>Change</th></tr>
          <!-- For each row: <tr><td><div class="kw-cell"><span class="kw-label">{{KEYWORD}}</span><span class="kw-page">{{PAGE_PATH}}</span></div></td><td>{{IMP_BEFORE}}</td><td>{{IMP_AFTER}}</td><td><span class="pill-dn">{{PCT}}</span></td></tr> -->
          {{KW_WORST_IMP_ROWS}}
        </table>
      </div>
    </div>

    <!-- CLICKS -->
    <div class="two-col">
      <div class="chart-card" style="margin-bottom:0;">
        <div class="chart-title">↑ Best — Click gainers</div>
        <div class="chart-sub">Top 5 pages by click increase, {{KW_PERIOD_M1}} vs {{KW_PERIOD_M2}}</div>
        <table class="kw-table">
          <colgroup><col style="width:52%"><col style="width:16%"><col style="width:16%"><col style="width:16%"></colgroup>
          <tr><th>Keyword / Page</th><th>Before</th><th>After</th><th>Change</th></tr>
          {{KW_BEST_CLK_ROWS}}
        </table>
      </div>
      <div class="chart-card" style="margin-bottom:0;">
        <div class="chart-title">↓ Worst — Click drops</div>
        <div class="chart-sub">Top 5 pages by click decline, {{KW_PERIOD_M1}} vs {{KW_PERIOD_M2}}</div>
        <table class="kw-table">
          <colgroup><col style="width:52%"><col style="width:16%"><col style="width:16%"><col style="width:16%"></colgroup>
          <tr><th>Keyword / Page</th><th>Before</th><th>After</th><th>Change</th></tr>
          {{KW_WORST_CLK_ROWS}}
        </table>
      </div>
    </div>
  </div>

  <!-- SEARCH VISIBILITY TRENDS -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">Search visibility trends <span class="badge badge-gsc">GSC</span></div></div>
    <div class="chart-card">
      <div class="chart-title">Weekly impressions & clicks</div>
      <div class="chart-sub">Source: Google Search Console · Last 13 weeks</div>
      <div class="chart-wrap">
        <canvas id="weeklyChart"></canvas>
      </div>
    </div>
  </div>

  <!-- AI TRAFFIC -->
  <div class="section">
    <div class="section-header"><div class="section-bar"></div><div class="section-title">AI traffic <span class="badge badge-ai">GA4 · AI</span></div></div>
    <div class="ai-kpi-grid">
      <div class="kpi-card"><div class="kpi-label">AI sessions</div><div class="kpi-value">{{AI_TOTAL_SESSIONS}}</div><div class="kpi-sub">Known AI referrers</div></div>
      <div class="kpi-card"><div class="kpi-label">AI total users</div><div class="kpi-value">{{AI_TOTAL_USERS}}</div><div class="kpi-sub">Known AI referrers</div></div>
      <div class="kpi-card"><div class="kpi-label">AI new users</div><div class="kpi-value">{{AI_NEW_USERS}}</div><div class="kpi-sub">Known AI referrers</div></div>
      <div class="kpi-card"><div class="kpi-label">AI key events</div><div class="kpi-value">{{AI_KEY_EVENTS}}</div><div class="kpi-sub">Known AI referrers</div></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">AI referral sources — detailed breakdown</div>
      <div class="chart-sub">Source: GA4 · Filtered to known AI platforms · {{DATE_RANGE}}</div>
      <table class="ai-table">
        <tr><th>Source</th><th>Sessions</th><th>Users</th><th>New users</th><th>Bounce rate</th><th>Key events</th></tr>
        <!-- For each AI source row. Color bounce rate: class="br-warn" if >45%, class="br-ok" if <=45% -->
        <!-- <tr><td><span class="ai-pill">{{SOURCE}}</span></td><td>{{SESSIONS}}</td><td>{{USERS}}</td><td>{{NEW_USERS}}</td><td class="{{BR_CLASS}}">{{BOUNCE_RATE}}</td><td>{{KEY_EVENTS}}</td></tr> -->
        {{AI_SOURCE_ROWS}}
      </table>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
// Populate with real weekly data from Q6 results
// {{WEEKLY_CHART_LABELS}} = JSON array of week label strings e.g. ["Feb 2","Feb 9",...]
// {{WEEKLY_IMPRESSIONS_DATA}} = JSON array of impression integers
// {{WEEKLY_CLICKS_DATA}} = JSON array of click integers
const el = document.getElementById('weeklyChart');
const wrap = el.parentElement;
el.style.display = 'block';
el.width = wrap.offsetWidth || 600;
el.height = 130;

new Chart(el, {
  type: 'line',
  data: {
    labels: {{WEEKLY_CHART_LABELS}},
    datasets: [
      {
        label: 'Impressions',
        data: {{WEEKLY_IMPRESSIONS_DATA}},
        borderColor: '#1D9E75',
        backgroundColor: 'rgba(29,158,117,0.07)',
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        borderWidth: 2,
        yAxisID: 'y'
      },
      {
        label: 'Clicks',
        data: {{WEEKLY_CLICKS_DATA}},
        borderColor: '#378ADD',
        backgroundColor: 'transparent',
        fill: false,
        tension: 0.4,
        pointRadius: 2,
        borderWidth: 2,
        borderDash: [4,3],
        yAxisID: 'y2'
      }
    ]
  },
  options: {
    responsive: false,
    plugins: {
      legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 16, padding: 10 } },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 40 } },
      y: { position: 'left', grid: { color: 'rgba(128,128,128,0.1)' }, ticks: { font: { size: 9 }, callback: v => v >= 1000 ? Math.round(v/1000)+'k' : v } },
      y2: { position: 'right', grid: { display: false }, ticks: { font: { size: 9 } } }
    }
  }
});
</script>
```

**Bar chart rendering instructions for top pages sections:**

When filling `{{TOP_PAGES_BY_CLICKS_BARS}}`, `{{TOP_PAGES_BY_SESSIONS_BARS}}`, `{{TOP_PAGES_BY_EVENTS_BARS}}`:
- Sort descending, take top 5
- Rank 1 bar = 100% width. All others = `(value / rank1_value) * 100`%
- Clicks bars: rank 1 color `#1D9E75`, ranks 2–5 `#5DCAA5`
- Sessions bars: rank 1 `#378ADD`, ranks 2–5 `#85B7EB`
- Key events bars: rank 1 `#7F77DD`, ranks 2–5 `#AFA9EC`
- Format large numbers with commas (e.g. `7,876`)

**MoM rendering instructions:**

When filling `{{BEST_PERFORMERS_ROWS}}` and `{{WORST_PERFORMERS_ROWS}}`:
- Use the two most recent FULL calendar months from the Q5 data
- Best = top 5 pages by absolute session increase (month 1 → month 2)
- Worst = top 5 pages by absolute session decrease
- Exclude `(not set)` landing pages
- Use `pill-up` class for growth, `pill-dn` for decline
- Round percentages to 1 decimal place

**Keyword performers rendering instructions:**

When filling `{{KW_BEST_IMP_ROWS}}`, `{{KW_WORST_IMP_ROWS}}`, `{{KW_BEST_CLK_ROWS}}`, `{{KW_WORST_CLK_ROWS}}` from Q8a and Q8b data:

1. **Deduplication — one keyword per page:** Build a merged list of all pages from both periods. For each page, derive a human-readable keyword label from the URL path: take the last non-empty path segment, replace hyphens with spaces, strip file extensions. Examples: `/blog/google-ads-best-practices` → `google ads best practices`; `/` → `two minute reports` (or site name); `/templates/looker-studio` → `looker studio (templates)`.
2. **No duplicate pages:** Each page URL appears in at most one row across all four tables. No page is repeated even across best/worst impression vs click tables.
3. **Best impressions** = top 5 pages sorted by `(period_2_impressions - period_1_impressions)` descending, excluding pages with combined impressions < 100.
4. **Worst impressions** = top 5 pages sorted by `(period_2_impressions - period_1_impressions)` ascending (biggest drops), same minimum threshold.
5. **Best clicks** = top 5 pages sorted by `(period_2_clicks - period_1_clicks)` descending; skip pages already in best impressions top-5 only if there are enough other pages.
6. **Worst clicks** = top 5 pages sorted by `(period_2_clicks - period_1_clicks)` ascending.
7. For new pages (period 1 = 0): show `0` in Before column and use `<span class="pill-up">New</span>` in Change column.
8. Format all impression/click numbers with commas. Round percentage changes to nearest whole number.
9. Set `{{KW_PERIOD_LABEL}}` = e.g. `"Mar vs Apr"`, `{{KW_PERIOD_M1}}` = e.g. `"Mar 1–31"`, `{{KW_PERIOD_M2}}` = e.g. `"Apr 1–30"`.

---

### 7. Save configuration

After producing the dual output, ask the user:

> "Want to save your settings for future runs? This skill can remember your accounts so you don't have to pick them every time — useful for recurring reports.
>
> - Save accounts? (yes / no)
> - Auto-confirm the query on future runs? (yes / no — saves a step but you won't see the query before it runs)"

If yes to either, write to `<install-path>/config.json`:

```json
{
  "version": "2.0.0",
  "saved": true,
  "accounts": { "<connector>": [{ "label": "...", "value": "..." }] },
  "currency": null,
  "auto_confirm_query": <true or false>,
  "saved_at": "<ISO 8601 timestamp>"
}
```

If the write fails, tell the user: *"Couldn't save your settings to disk — they'll be remembered for this conversation only. You'll be asked again next time."*

On success: *"Saved. Future runs will use these settings automatically. Say 'change config' inside the skill to update."*

If `<install-path>` was not resolved in step 4, skip this step silently.
