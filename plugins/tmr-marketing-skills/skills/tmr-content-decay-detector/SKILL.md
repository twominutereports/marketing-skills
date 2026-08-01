---
name: tmr-content-decay-detector
description: Use this skill when the user asks to detect content decay, find declining pages, audit SEO performance drops, identify pages losing organic traffic, run a content decay audit, check which blog posts or landing pages are losing clicks or sessions, or surface pages with falling rankings and engagement. Requires Google Search Console and Google Analytics 4. Produces a severity-scored decay report with root cause diagnosis (visibility loss, SERP issue, tracking mismatch, or engagement decay) plus an HTML dashboard artifact with a prioritized action table.
version: 2.0.0
compatibility: "Requires the current Two Minute Reports MCP (server https://mcp.twominutereports.com/mcp) connected with Google Search Console (gsc) and Google Analytics 4 (ga4) connectors"
---

# Content Decay Detector

> **MCP version note.** This skill targets the current TMR MCP. Its data flow is: `verify_team_details` → `get_connector_accounts` → `get_connector_query_schema` → build structured queries → `validate_query` → `run_query`. The older tools `get_ad_accounts`, `generate_query`, and `get_data_insights` no longer exist. Connector IDs: **`gsc`** (Search Console), **`ga4`** (Analytics). Field IDs are raw. The two natural-language prompts from the previous version are now structured queries (stored in `queries.json`, mirrored in step 6), each run for the current and previous window. Date ranges are computed fresh at runtime.

## Purpose

Detect content decay across your website by combining Google Search Console (GSC) and Google Analytics 4 (GA4) data. The skill compares the last 30 days against the prior 30-day period, identifies candidate pages with meaningful organic decline, scores each page by severity, diagnoses the root cause using a structured case-matching framework (visibility loss, SERP issue, tracking mismatch, or engagement decay), and surfaces a prioritised action list — inline in chat plus a full HTML dashboard.

This is not a simple traffic comparison. The skill uses explicit decay logic: a page must fail a threshold test on clicks OR organic sessions to enter the candidate list, and root cause is inferred from the pattern of clicks vs impressions vs CTR vs sessions vs engagement — not from any single metric in isolation.

## Connectors required

This skill uses the following TMR connectors:
- Google Search Console (`gsc`)
- Google Analytics 4 (`ga4`)

Both are mandatory. The skill will not proceed if either is unavailable. GSC reveals SEO visibility trends (ranking, impressions, CTR); GA4 reveals business impact (sessions, engagement, conversions). Together they enable real insight; neither alone is sufficient.

---

## Runtime procedure

Follow these steps in order. Do not skip steps. Do not rearrange.

### 1. Check that TMR's tools are available

Inspect your available tools. The current Two Minute Reports MCP exposes these tool names: `verify_team_details`, `list_connectors`, `get_connector_accounts`, `get_connector_query_schema`, `validate_query`, `run_query`. The prefix may vary — users name their MCP connections differently (e.g., "Two Minute Reports", "TMR", "TwoMinuteReports", or a custom name). Match by tool function and the Two Minute Reports MCP server (URL: `https://mcp.twominutereports.com/mcp`), not by exact prefix.

**If none of these tools are present**, tell the user:

> *"This skill needs Two Minute Reports to be connected to your Claude account, but I don't see it in your available tools.*
>
> *Two Minute Reports is an analytics platform that lets you query your marketing data (ads, analytics, e-commerce, etc.) from inside Claude. You'll need to connect it once, then this skill will work.*
>
> *Here's the setup guide: https://twominutereports.com/help/mcp/claude*
>
> *Once it's connected, run this skill again."*

If a `suggest_connectors` capability is available, use it to surface a one-tap connect option. Then stop.

If the tools ARE present, hold the resolved prefix internally and continue.

---

### 2. Verify team details and authentication

Call `verify_team_details`.

- **Multiple teams** → present them, ask which to use, store the chosen `teamId` for all later calls.
- **Single team success** → note the team name, store its `teamId`, continue.
- **Plan status** → `active`, `in_trial`, `non_renewing` are fine. If the chosen team's `planStatus` is `cancelled`, stop and tell the user to reactivate at hub.twominutereports.com/billing — do not call `validate_query` or `run_query`.
- **Auth / session failure or empty team** → tell the user:

  > *"Two Minute Reports is connected, but I couldn't verify your team — your session may have expired. Please reconnect Two Minute Reports, then run this skill again. Setup reference: https://twominutereports.com/help/mcp/claude"*

  If `suggest_connectors` is available, trigger it for Two Minute Reports. Stop.

- **Any other failure** → *"Couldn't reach Two Minute Reports right now — please try again in a moment."* Stop.

---

### 3. Verify both required connectors are provisioned in TMR

Call `get_connector_accounts` once per connector, with `teamId`:
- `get_connector_accounts(teamId, connectorId: "gsc", status: "enabled")`
- `get_connector_accounts(teamId, connectorId: "ga4", status: "enabled")`

- **Both return accounts** → continue. (GSC account IDs are site URLs like `https://example.com/`; GA4 account IDs are numeric property IDs.)
- **Either is missing or empty** → tell the user which connector is missing and ask them to add it inside Two Minute Reports, then stop. Do not attempt a partial run.

---

### 4. Locate skill folder and load configuration

Look for this skill's install folder:
1. `/mnt/skills/user/tmr-content-decay-detector/`
2. If not found, `find /mnt/skills -name "tmr-content-decay-detector" -type d 2>/dev/null`, use first result.
3. If still not found, skip all config read/write and fall through to interactive account selection.

Hold the resolved path as `<install-path>`.

Try to read `<install-path>/config.json`.

**If `saved: true`:**
- Tell the user: *"Using your saved configuration: [list account labels]. Say 'change config' to update."*
- Use stored accounts and `auto_confirm_query`.

**If `saved: false`, file missing, or unreadable:**
- Reuse the `get_connector_accounts` responses from step 3.
- Present accounts grouped by connector. Ask:

  > *"Which Google Search Console property and GA4 property would you like to analyse? Pick one each — ideally matching the same website."*

  Wait for selection.

---

### 5. Choose the decay window

Ask the user:

> *"Which comparison window would you like?*
> *• Last 30 days vs previous 30 days (default)*
> *• Last 60 days vs previous 60 days*
> *• Last 90 days vs previous 90 days"*

Use the chosen window for all queries. If the user says nothing or presses ahead, default to 30 days.

---

### 6. Build, validate, and run the two data-collection queries

The previous version sent two natural-language prompts to `generate_query`; the new MCP has no such tool, so each pull is an explicit structured query. Resolve the chosen window (and its immediately-preceding equal-length window) from today's actual date, then run each query for **both** the current and previous window so the decay logic in step 7 can compute period-over-period deltas. GSC data lags ~2–3 days — consider ending the current window a couple of days before today.

**Procedure:** assemble one `gsc` entry and one `ga4` entry → `validate_query(teamId, connectors:[...])` (fix any flagged field/rule and re-validate) → unless `auto_confirm_query` is `true`, show a one-line summary and wait for confirmation → `run_query(teamId, connectors:[...], limit:...)` (no `currencyCode` — no monetary metrics). If a result returns as a stored file path, parse it with code execution.

#### Query A — GSC page-level decay signals (→ **GSC_DATA**)
- connector `gsc`, account = selected site URL
- dims: `page` · metrics: `clicks`, `impressions`, `ctr`, `position`
- run once for the current window, once for the previous window

#### Query B — GA4 organic session and engagement decay (→ **GA4_DATA**)
- connector `ga4`, account = selected property ID
- dims: `landing_page`, `session_default_channel_grouping` · metrics: `sessions`, `engaged_sessions`, `key_events`
- run once for the current window, once for the previous window
- **Organic-only handling:** the channel dimension is included so you can **keep only the `Organic Search` rows during synthesis** (step 7). This avoids guessing connector-side filter syntax and is robust. Aggregate organic sessions/engaged sessions/key events per `landing_page` from those rows.

> Hold both datasets (current + previous for each) for the decay logic in step 7.

---

### 7. Apply the Content Decay Detection logic

Once both datasets are in hand, execute the following logic in your reasoning before producing any output. Do not show this working to the user — only surface the conclusions.

#### Step 7A — Build the candidate list

Join GSC_DATA and GA4_DATA on page URL (use fuzzy matching if trailing slash or protocol differs).

Flag a page as a **decay candidate** if **either** of the following is true:
- GSC clicks dropped **> 20%** period-over-period, OR
- GA4 organic sessions dropped **> 20%** period-over-period.

Discard pages with fewer than 50 combined clicks in either period (too low-traffic to score reliably).

#### Step 7B — Score each candidate

Calculate a **Decay Score** (0–100) using this weighted formula:

```
Decay Score =
  (click_drop_pct * 0.40) +
  (session_drop_pct * 0.30) +
  (impression_drop_pct * 0.20) +
  (position_decline_pct * 0.10)
```

Where each value is the percentage decline (0–100 scale; use 0 if the metric improved). Cap the score at 100.

Map the score to a **severity tier**:
- **Critical** — score ≥ 60, or any single metric dropped > 60%
- **High** — score 40–59, or any single metric dropped 40–60%
- **Medium** — score 20–39, or any single metric dropped 20–40%

Sort the candidate list: Critical first, then High, then Medium; within each tier, sort by Decay Score descending.

#### Step 7C — Diagnose root cause for each candidate

Apply the following case logic, in order. Assign the **first matching case**.

| Case | Condition | Label | Likely causes |
|---|---|---|---|
| **A — Visibility Loss** | Impressions down AND clicks down (both >15%) | Ranking decline | Algorithm update, competitor overtook, indexation issue, seasonality |
| **B — SERP Issue** | Impressions stable (< 10% change) AND CTR down > 15% | Click-through problem | Weaker title/meta, SERP feature stealing clicks, intent mismatch |
| **C — Tracking Mismatch** | GSC clicks stable (< 10% change) AND GA4 sessions down > 20% | GA4 / tracking issue | GA4 misconfiguration, attribution change, UTM stripping, tag firing issue |
| **D — Engagement Decay** | Sessions stable or only mildly down (< 20%) AND engaged sessions OR key events down > 25% | Traffic quality problem | Irrelevant queries landing, content–intent mismatch, UX regression |
| **E — Mixed / Unclear** | Doesn't cleanly match A–D | Needs investigation | Review multiple signals manually |

For Case C, explicitly flag this to the user in the insights and dashboard — it suggests a measurement problem, not a content problem, and should be investigated before taking content action.

---

### 8. Produce the dual output

#### Insights (inline chat)

Write a 200–350 word insights summary in chat. Structure:

1. **Headline** — total pages analysed, total candidates flagged, breakdown by severity tier.
2. **Top 3 decaying pages** — URL (shortened), severity, decay score, root cause label, and the single most telling signal (e.g. "CTR fell [X%] while impressions held steady → Case B").
3. **Pattern observation** — is there a dominant root cause across candidates? Any cluster (e.g. blog posts from a specific period, a URL pattern)?
4. **Priority action** — one concrete next step based on the most severe case.

Match the tone and structure of this template (fill `[brackets]` with the user's actual data):

---
*[N] pages analysed across [property]. [N] decay candidates identified: [N] Critical, [N] High, [N] Medium.*

*Top decliners this period:*
*• [Page URL] — [Severity]. Decay score [X]. [Root cause label]. Key signal: [most telling metric change].*
*• [Page URL] — [Severity]. Decay score [X]. [Root cause label]. Key signal: [most telling metric change].*
*• [Page URL] — [Severity]. Decay score [X]. [Root cause label]. Key signal: [most telling metric change].*

*Pattern: [observation about whether Case A/B/C/D dominates, or whether decay is spread across types. Note any URL cluster or content type pattern.]*

*Priority action: [one specific, actionable recommendation tied to the highest-severity finding — e.g. "Audit the title tag and meta description for [page] — impressions held but CTR collapsed, suggesting a SERP presentation issue (Case B)." or "Investigate GA4 tracking on [page] before taking content action — GSC clicks are stable but GA4 sessions dropped [X%] (Case C tracking mismatch)."]*

---

#### Dashboard (HTML artifact)

Produce a **new artifact** for this run. Do not update or replace any prior run's artifact. Title format:

`Content Decay Detector — [YYYY-MM-DD HH:MM] — [GSC property label]`

The dashboard must include:

**Metadata header** (top of page): Run date/time · GSC property · GA4 property · Comparison window · Total pages analysed

**KPI tile row** (4 tiles):
- Pages Analysed
- Decay Candidates
- Critical Pages
- Dominant Root Cause

**Decay Candidate Table** — one row per candidate page, columns:
| Page URL | Severity | Decay Score | Click Δ% | Session Δ% | Impression Δ% | Position Δ | CTR Δ% | Engaged Session Δ% | Key Events Δ% | Root Cause | Likely Cause |

- Severity tiers use colour coding: Critical = red (#EF4444), High = orange (#F97316), Medium = amber (#F59E0B).
- Root cause labels display as a pill/badge.
- Sort: Critical → High → Medium, then by Decay Score descending within each tier.
- Rows with Case C (Tracking Mismatch) display a ⚠️ icon and a tooltip: *"Clicks are stable in GSC but sessions dropped in GA4 — investigate tracking before taking content action."*

**Root Cause Breakdown chart** — horizontal bar chart showing count of candidates by root cause (Case A / B / C / D / E).

**Recommended Actions panel** — for the top 3 Critical/High pages, show a one-line recommended action based on the diagnosed root cause.

Use this colour palette and typography:
- Background: `#0F172A` (dark navy)
- Card/tile background: `#1E293B`
- Primary accent: `#6366F1` (indigo)
- Text primary: `#F1F5F9`
- Text muted: `#94A3B8`
- Font: Inter or system-ui
- Severity colours: Critical `#EF4444`, High `#F97316`, Medium `#F59E0B`
- Root cause pill colours: Case A `#3B82F6`, Case B `#8B5CF6`, Case C `#EAB308`, Case D `#10B981`, Case E `#6B7280`

---

### 9. Save configuration (first run only, if no saved config existed)

After producing the dual output, ask:

> *"Want to save your settings for future runs? This skill can remember your accounts so you don't have to pick them every time.*
>
> *• Save accounts and comparison window? (yes / no)*
> *• Auto-confirm queries on future runs? (yes / no — saves a step but you won't see the query before it runs)"*

If yes, write to `<install-path>/config.json`:

```json
{
  "version": "2.0.0",
  "saved": true,
  "accounts": {
    "Google Search Console": [{ "label": "...", "value": "..." }],
    "Google Analytics 4": [{ "label": "...", "value": "..." }]
  },
  "decay_window_days": 30,
  "currency": null,
  "auto_confirm_query": false,
  "saved_at": "<ISO 8601 timestamp>"
}
```

If the write fails, tell the user: *"Couldn't save your settings to disk — they'll be remembered for this conversation only. You'll be asked again next time."* Continue normally.

If no install folder was resolved in step 4, skip silently.

---

## Decay logic quick-reference (for runtime reasoning)

```
CANDIDATE THRESHOLD
  Flag if: clicks_drop > 20% OR organic_sessions_drop > 20%
  Exclude if: combined clicks in either period < 50

DECAY SCORE (0–100)
  = (click_drop% × 0.40)
  + (session_drop% × 0.30)
  + (impression_drop% × 0.20)
  + (position_decline% × 0.10)

SEVERITY TIERS
  Critical  → score ≥ 60 OR any single metric dropped > 60%
  High      → score 40–59 OR any single metric dropped 40–60%
  Medium    → score 20–39 OR any single metric dropped 20–40%

ROOT CAUSE CASES
  A — Visibility Loss     → impressions ↓ AND clicks ↓ (both > 15%)
  B — SERP Issue          → impressions stable AND CTR ↓ > 15%
  C — Tracking Mismatch   → GSC clicks stable AND GA4 sessions ↓ > 20%  ⚠️ flag
  D — Engagement Decay    → sessions stable AND engaged sessions OR key events ↓ > 25%
  E — Mixed / Unclear     → no clean match
```
