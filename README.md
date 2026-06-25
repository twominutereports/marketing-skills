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

- Claude.ai Pro, Team, or Enterprise account
- [Two Minute Reports](https://twominutereports.com) MCP connected in Claude Settings
- The relevant data source (Google Analytics, Search Console, etc.) linked within Two Minute Reports

**Installing a skill in Claude**

1. Download all files in the skill's folder from this repository (skill.md plus any queries.json and references/)
2. Go to [claude.ai/customize/skills](https://claude.ai/customize/skills)
3. Click the **+** icon → **Create skill** → **Upload a skill**
4. Select the downloaded `skill.md` file
5. Start chatting — each skill's README lists the trigger phrases you can use

## Repository Structure

```
marketing-skills/
├── seo/
│   ├── website-traffic-analysis/   # Traffic trends, CTR diagnostics, 30-day action plan
│   ├── seo-analytics-report/       # Full-funnel GSC + GA4 report with AI traffic breakdown
│   ├── content-decay-detector/     # Severity-scored decay detection with root cause diagnosis
│   └── local-seo-audit/            # Combined GMB + GSC + GA4 local audit with health score
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
