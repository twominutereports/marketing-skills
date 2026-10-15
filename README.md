# Marketing Skills — Claude Skill Collection

## Overview

This repository is a curated collection of Claude skills built for marketers. Each skill connects Claude to your real marketing data via the Two Minute Reports MCP, enabling AI-driven analysis and actionable recommendations across PPC, SEO, paid media, social, email, and more — without needing to export a spreadsheet or write a single query.

## Available Skills

### SEO

| Skill | Description |
| --- | --- |
| [Website Traffic Analysis](./seo/website-traffic-analysis/) | Traffic trends, CTR diagnostics, keyword gaps, and a 30-day action plan |
| [SEO + Analytics Report](./seo/seo-analytics-report/) | Full-funnel organic report combining GSC and GA4 — visibility, top pages, MoM shifts, and AI traffic |
| [Content Decay Detector](./seo/content-decay-detector/) | Finds pages silently losing traffic, scores severity, and diagnoses the root cause |
| [Local SEO Audit](./seo/local-seo-audit/) | Combined GMB + GSC + GA4 local audit — visibility, profile actions, search, conversion, and reviews with a health score |
| [AI Traffic Audit (GA4)](./seo/ga4-ai-traffic-audit/) | How much traffic ChatGPT, Gemini, Claude, Perplexity, and other AI assistants send, which landing pages each one hits, and change vs the prior 30 days |
| [Multichannel SEO Performance Report](./seo/multichannel-seo-performance-report/) | One 5-tab report across Search Console, GA4 (with AI traffic), PageSpeed Insights / Core Web Vitals, and Google Business Profile — last 28 days vs the prior 28 |

### PPC

| Skill | Description |
| --- | --- |
| [Google Ads Auditor](./ppc/google-ads-audit/) | Campaign, keyword, and search terms audit with wasted spend breakdown |
| [Meta Ads Auditor](./ppc/meta-ads-audit/) | Campaign, creative, audience, and placement audit including creative fatigue detection |
| [TikTok Ads Auditor](./ppc/tiktok-ads-audit/) | Campaign, creative, and audience audit with creative fatigue signals |
| [LinkedIn Ads Auditor](./ppc/linkedin-ads-audit/) | B2B-focused audit across campaigns, creatives, and audiences with CPL and lead quality analysis |
| [Reddit Ads Auditor](./ppc/reddit-ads-audit/) | Full Reddit Ads audit across campaigns, ad groups, creatives, audiences, and scaling opportunities |

### Social (Organic)

| Skill | Description |
| --- | --- |
| [Facebook Insights Report](./social-media/facebook-insights-report/) | Organic Facebook Page report — growth, reach, engagement, and top-performing posts |
| [Instagram Insights Report](./social-media/instagram-insights-report/) | Organic Instagram report — growth and reach trends, engagement, post/Reels performance, and audience breakdown |

### Ecommerce

| Skill | Description |
| --- | --- |
| [Shopify Store Auditor](./ecommerce/shopify-store-audit/) | CRO audit across funnel, checkout, mobile, products, and traffic sources with a revenue-impact action plan |

## Key Capabilities (across all skills)

- **Data-first analysis** — skills pull live data directly from your connected sources; no manual exports
- **Actionable output** — every analysis ends with a prioritized, time-bound action plan
- **Plain-language interface** — trigger full analyses with a single sentence; no technical knowledge required
- **Secure by design** — OAuth 2.0 authentication throughout; data flows from source to Claude without server-side storage

## Requirements & Setup

**Prerequisites**

- A [Two Minute Reports](https://twominutereports.com) account, with the data source the skill
  needs (Google Ads, GA4, Search Console and so on) connected in it
- An AI tool that runs skills: Claude (Pro, Max, Team or Enterprise), Claude Code, Codex, or
  ChatGPT (Business, Enterprise, Edu or Healthcare)

Skills are also built into Dash, the assistant inside Two Minute Reports, with nothing to install.

### Claude (claude.ai, desktop and mobile): one plugin for everything (recommended)

This repository is a plugin marketplace. Adding it installs **every** skill *and* the Two Minute
Reports connector, and it can keep itself up to date:

1. Open [Customize › Plugins](https://claude.ai/customize/plugins)
2. Select **Add**, then **Add marketplace**, and enter `twominutereports/marketing-skills`
3. Under **Discover**, find `tmr-marketing-skills` and select **Add**
4. Turn on **Sync automatically** for the marketplace, so new and improved skills reach you
5. Ask, e.g. *"Audit my Google Ads account"*, or type `/` and choose a skill

Plugins added here also reach Claude Code on the same account. If you already added Two Minute
Reports to Claude, keep it; nothing needs removing.

**Only want one skill?** Download it from the
[Skills tab in the Two Minute Reports Hub](https://hub.twominutereports.com/ai-tools/skills)
(its Download builds the zip), then in [Customize › Skills](https://claude.ai/customize/skills)
select **+** › **Create skill** › **Upload a skill** and choose the zip. A skill added this way
doesn't update itself.

> **Upload the folder, not just `skill.md`.** Most skills read
> `references/thresholds.md` for their scoring benchmarks; with only the markdown
> file those instructions point at nothing and the scores get invented. The file must
> also be named `SKILL.md` (uppercase), which is the name Claude looks for.

### ChatGPT: upload each skill

Skills are on ChatGPT Business, Enterprise, Edu and Healthcare plans, and ChatGPT takes one skill
at a time:

1. Download the skill's zip from the
   [Skills tab in the Two Minute Reports Hub](https://hub.twominutereports.com/ai-tools/skills)
2. In ChatGPT, open **Plugins** in the sidebar, then the **Skills** tab
3. Select **Create**, then **Upload from your computer**, and choose the zip
4. Connect Two Minute Reports in ChatGPT too, if you haven't
5. Ask, e.g. *"Audit my Google Ads account"*

An uploaded skill doesn't update itself. For a newer version, download and upload it again.

### Claude Code

Added the plugin in Claude already? It syncs to Claude Code (v2.1.273 or later), so skip this.
Otherwise, in Claude Code:

```
/plugin marketplace add twominutereports/marketing-skills
/plugin install tmr-marketing-skills@marketing-skills
/reload-plugins
```

That adds every skill and connects the Two Minute Reports MCP server. Then ask, or type
`/tmr-marketing-skills:` and choose a skill.

Claude Code doesn't update plugins from third-party marketplaces by itself. To get new skills, run
`/plugin marketplace update marketing-skills`. Copying a skill folder into `~/.claude/skills/` by
hand also works, but a copied folder never updates.

### Codex

Codex reads skills from `~/.agents/skills`. This copies every skill there:

```
cd "$(mktemp -d)" && git clone --depth 1 https://github.com/twominutereports/marketing-skills . && mkdir -p ~/.agents/skills && cp -R plugins/tmr-marketing-skills/skills/. ~/.agents/skills/
```

Codex also needs the Two Minute Reports MCP server
(`codex mcp add two-minute-reports --url https://mcp.twominutereports.com/mcp`, then
`codex mcp login two-minute-reports`). Then ask, or type `$` and choose a skill. Codex picks up
new skills on its own; if one doesn't show, restart it. To update, run the copy command again.

## Plugin build (maintainers)

`plugins/tmr-marketing-skills/` is **generated** — the category folders above are the
source of truth. After changing any `skill.md`, regenerate and commit:

```
node scripts/build-plugin.mjs
```

CI runs `--check` on every PR, so a stale plugin fails the build instead of quietly
shipping the old copy to whoever installs it. The generator lowercase→uppercase
renames `skill.md` to `SKILL.md`, names each skill folder from its frontmatter `name`,
and copies `references/` and `queries.json` alongside it.

## Repository Structure

```
marketing-skills/
├── seo/
│   ├── website-traffic-analysis/   # Traffic trends, CTR diagnostics, 30-day action plan
│   ├── seo-analytics-report/       # Full-funnel GSC + GA4 report with AI traffic breakdown
│   ├── content-decay-detector/     # Severity-scored decay detection with root cause diagnosis
│   ├── local-seo-audit/            # Combined GMB + GSC + GA4 local audit with health score
│   ├── ga4-ai-traffic-audit/       # AI platform referral traffic — sessions, landing pages, page x platform matrix
│   └── multichannel-seo-performance-report/  # GSC + GA4 + AI traffic + PageSpeed + GBP in one 5-tab dashboard
├── ppc/
│   ├── google-ads-audit/           # Campaign, keyword, and wasted spend audit
│   ├── meta-ads-audit/             # Creative, audience, and placement audit
│   ├── tiktok-ads-audit/           # Campaign, creative, and audience audit with fatigue signals
│   ├── linkedin-ads-audit/         # B2B audit with CPL and lead quality analysis
│   └── reddit-ads-audit/           # Full Reddit Ads audit with scaling opportunities
├── social-media/
│   ├── facebook-insights-report/   # Organic Facebook Page growth, reach, and engagement report
│   └── instagram-insights-report/  # Organic Instagram growth, engagement, and Reels report
└── ecommerce/
    └── shopify-store-audit/        # CRO audit across funnel, products, and traffic sources
```

📄 [Privacy Policy](https://twominutereports.com/privacy-policy) · 🔒 [Data Security](https://twominutereports.com/data-security) · 📋 [Terms of Service](https://twominutereports.com/terms-of-service)

---

## Support

📧 [support@twominutereports.com](mailto:support@twominutereports.com) · 🎫 [Submit a ticket](https://twominutereports.com/support-ticket)

---

## About Two Minute Reports

Two Minute Reports is a marketing data platform that connects 22+ data sources to Google Sheets, Looker Studio, and AI assistants. Built for agencies, marketers, and ecommerce brands.

🌐 [twominutereports.com](https://twominutereports.com) · 🔌 [MCP Server](https://twominutereports.com/mcp)

---

**Built with ❤️ for marketers who'd rather analyze data than export it.**
