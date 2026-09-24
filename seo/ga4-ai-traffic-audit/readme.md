# AI Traffic Audit (GA4) — Claude Skill

Audits how much website traffic comes from AI assistants and which landing pages each AI platform sends visitors to, using Google Analytics 4 through the Two Minute Reports (TMR) MCP.

## What it produces

Every run returns two outputs:

1. **Inline insights**: AI sessions and their share of the site total, the leading platforms, the biggest changes vs the previous 30 days, and one recommended action.
2. **Dashboard artifact** with the AI platform logos:
   - KPI tiles: AI sessions (with change vs previous period), share of site sessions, AI users, AI key events, AI engagement rate
   - AI platform leaderboard: one card per assistant showing sessions, share, change, engagement, key events and its top 5 pages
   - Daily AI sessions, stacked by platform
   - Pages × AI platforms matrix with logo column headers, heat-shaded cells and click-to-filter by platform

## Platforms detected

ChatGPT, Gemini, Claude, Perplexity, Copilot, Meta AI, Grok, DeepSeek, Mistral, Poe, You.com. A session is matched to a platform from its GA4 **Session source**.

## Requirements

- Two Minute Reports MCP connected to Claude: https://twominutereports.com/help/mcp/claude
- A Google Analytics 4 property enabled in TMR

## Date windows

- The last 30 full days, ending yesterday, compared with the 30 days before that. Dates are recalculated on every run.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Runtime instructions for Claude |
| `queries.json` | The four locked GA4 query templates (field IDs + relative date specs) |
| `config.json` | Saved end-user settings (empty by default) |
| `references/build_dashboard.py` | Classifies sources into AI platforms, computes KPIs, renders the dashboard |
| `references/dashboard_template.html` | Dashboard layout and styles |
| `references/logos/` | AI platform and GA4 logos, embedded into each dashboard |

## Implementation notes

- The TMR GA4 connector applies multiple filters with AND, so the queries only exclude `google`, `(direct)`, `bing` and `(not set)`. The script then classifies the remaining sources. To add a new AI platform, add one entry to `PLATFORMS` in `build_dashboard.py` and put its logo in `references/logos/`.
- Visits from AI apps that strip referrers land in (direct) and are not counted, so the figures are a minimum.
- The Perplexity, DeepSeek, Mistral and Poe marks come from Simple Icons (CC0; see `references/logos/SIMPLE-ICONS-LICENSE.md`). The other logos were supplied by the skill author. All trademarks belong to their owners and are used only to identify the traffic sources.

## Install

Claude → Settings → Capabilities → Skills → Upload `tmr-ga4-ai-traffic-audit.zip`.
