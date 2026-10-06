# tmr-multichannel-seo-performance-report

**Version:** 1.0.0 · **Type:** TMR skill (Two Minute Reports MCP, `https://mcp.twominutereports.com/mcp`)

An SEO performance report that combines Google Search Console, Google Analytics 4 (including AI assistant traffic), PageSpeed Insights and Google Business Profile. It compares the last 28 days with the previous 28 days. Each run produces an inline insights summary in chat plus a new 5-tab HTML dashboard with every platform's logo.

## Files

| File | What it is |
|---|---|
| `skill.md` | Runtime instructions. It also embeds the dashboard renderer (`seo_report.py`), which contains the HTML template, all logos and a copy of the queries |
| `queries.json` | The 25 locked query templates: field IDs plus relative date specs, with no dates, accounts or data |
| `readme.md` | This file |

User settings are saved outside the skill, at `~/.tmr-skills/tmr-multichannel-seo-performance-report/config.json`. The renderer is written to the same folder at runtime.

## Connectors

| Connector | ID | Required | Notes |
|---|---|---|---|
| Google Search Console | `gsc` | Yes | Analytics report mode; the window ends 3 days back because of GSC data lag |
| Google Analytics 4 | `ga4` | Yes | Also powers the AI Traffic section |
| Page Speed Insights | `psi` | Yes | The URL to test is always asked from the user (or read from saved config) and never inferred |
| Google My Business | `gmb` | Optional | If no location is connected, the Business Profile tab shows a setup note |

## Dashboard tabs

1. **Overview**: key takeaways, one summary card per platform, AI-assistant strip, daily clicks and sessions
2. **Search Console**: clicks, impressions, CTR, average position (with deltas) · daily trends · top queries · striking-distance keywords (position 4–20) · CTR opportunities (top-5 positions with CTR under 2%) · top pages · device split
3. **Analytics & AI Traffic**: sessions, users, new users, engagement rate, average session duration, key events · channel mix · organic landing pages
   - **AI Traffic** section with logos for ChatGPT, Gemini, Perplexity, Claude, Copilot, Meta AI, Grok, DeepSeek, Mistral, Poe and You.com: AI sessions, share of all sessions, AI users, AI key events, AI engagement rate · platform cards · stacked daily trend · AI landing pages
4. **Page Speed**: CrUX real-user Core Web Vitals (LCP, INP, CLS, FCP, TTFB) with pass/fail, mobile/desktop toggle · Lighthouse Performance, SEO, Accessibility and Best Practices · lab timings
5. **Business Profile**: total, Search and Maps views · website clicks, calls, directions · daily trend · search terms · rating, review count, star distribution, recent reviews and reply status · per-location table

## Queries

Dates are never stored. Each template carries a `date_spec` that the renderer resolves from today's date on every run.

| Batch | Connector | Queries |
|---|---|---|
| core (limit 250) | `gsc` | KPIs current/previous · daily trend · top queries · top pages · device split |
| core | `ga4` | KPIs current/previous · daily trend · channel mix · organic landing pages |
| core | `psi` | CrUX mobile/desktop (origin) · Lighthouse mobile/desktop (URL) |
| core | `gmb` | KPIs current/previous · daily trend · search keywords · reviews summary · recent reviews |
| ai (limit 5000) | `ga4` | AI sources current/previous · AI landing pages · AI daily trend (source and medium, excluding `google` and `(direct)`) |

All 25 queries passed TMR's live `validate_query` check on 2026-10-05.

## How AI traffic is detected

The TMR MCP joins filters with AND only, so the AI queries pull non-Google, non-direct sources. The renderer then matches session source against known assistants: chatgpt/openai, gemini, perplexity, claude.ai/anthropic, copilot, meta.ai, grok/x.ai, deepseek, mistral, poe.com and you.com. ChatGPT traffic arrives with several mediums (`ai-assistant`, `referral`, `cpc`). Paid mediums (cpc/ppc/paid/display) are excluded, so the section counts only unpaid AI referrals.

## Runtime flow

1. Check the MCP is connected, verify the team and plan status, check the connectors (GMB optional)
2. Extract the renderer, then load the saved config or collect the accounts and PageSpeed URL
3. Run `seo_report.py plan`, then `validate_query` and confirm with the user, then run two `run_query` calls (core and ai)
4. Run `seo_report.py build`, write the highlights, rebuild, give the inline insights and publish the dashboard as a new artifact
5. Offer to save the config on the first run

## Logos

The platform logos (GA4, Search Console, PageSpeed Insights, Business Profile) and the AI assistant logos are embedded as data URIs inside the renderer. They identify the data sources only. The AI logos are the same set used by `tmr-ga4-ai-traffic-audit`.

## Changelog

- **1.0.0** (2026-10-05): first release
