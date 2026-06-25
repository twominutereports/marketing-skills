# SEO Report Generator - Claude Skill

A Claude skill that generates a full-funnel view of your site's organic performance. It combines Google Search Console and GA4 data to cover everything from search visibility and top landing pages to month-over-month shifts and AI referral traffic — delivered as an inline insights summary and a complete HTML dashboard artifact.

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

## Usage

Just say: `Generate my SEO report` or `Run the SEO + analytics report` or `Show me my organic performance`

Claude will query your connected GSC and GA4 properties and produce the full report automatically — no setup questions.

## What It Covers

| Section                      | What You Get                                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------------------------- |
| Executive Summary            | Impressions, clicks, CTR, avg position (GSC) + sessions, users, key events, bounce rate (GA4)     |
| Top Landing Pages            | Top 5 pages by clicks, by sessions, and by key events                                             |
| Month-over-Month Performance | Best and worst performing landing pages by session growth vs the prior month                      |
| Keyword Performers           | Top impression and click gainers and losers across the last two full calendar months              |
| Search Visibility Trends     | Weekly impressions and clicks chart over the last 13 weeks                                        |
| AI Traffic Breakdown         | Sessions, users, bounce rate, and key events from ChatGPT, Gemini, Claude, Perplexity, and others |
| Recommended Action           | One concrete, data-backed next step the marketer can act on this week                             |

---

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
