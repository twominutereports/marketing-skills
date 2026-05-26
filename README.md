# Marketing Skills — Claude Skill Collection

## Overview

This repository is a curated collection of Claude skills built for marketers. Each skill connects Claude to your real marketing data via the Two Minute Reports MCP, enabling AI-driven analysis and actionable recommendations across PPC, SEO, paid media, social, email, and more — without needing to export a spreadsheet or write a single query.

## Available Skills

| Skill                                                   | Description                                                                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [Website Traffic Analysis](./website-traffic-analysis/) | Automated SEO specialist — traffic trends, CTR diagnostics, keyword gaps, and 30-day action plans |

More skills are in progress. This repository will grow to cover the full marketing stack.

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

**Installing a Skill**

![Installing a skill in Claude](./assets/claude-install-skill.gif)

1. Download the `.md` skill file from the skill's folder in this repository
2. Go to [claude.ai/customize/skills](https://claude.ai/customize/skills)
3. Click the **+** icon → **Create skill** → **Upload a skill**
4. Select the downloaded `.md` file
5. Start chatting — each skill's README lists the trigger phrases you can use

## Repository Structure

```
marketing-skills/
├── website-traffic-analysis/   # SEO & web traffic skill
└── ...                         # More skills coming soon
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
