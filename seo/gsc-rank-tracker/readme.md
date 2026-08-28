# GSC Rank Tracker - Claude Skill

A Claude skill that turns your own Google Search Console data into a keyword rank tracker. Give it your target keywords, a country, and a lookback window, and it charts how each keyword has ranked over time - sampled twice a month - as an inline read of the biggest movers plus a large color-coded rank-grid dashboard artifact. No page URLs needed, and no paid rank-tracker subscription.

## Requirements & Setup

**Prerequisites**

- Claude.ai Pro, Team, or Enterprise account
- [Two Minute Reports](https://twominutereports.com) MCP connected in Claude Settings
- Google Search Console linked within Two Minute Reports, with at least one enabled property

**Installing a skill in Claude**

1. Download all files in the skill's folder from this repository (skill.md plus any queries.json and references/)
2. Go to [claude.ai/customize/skills](https://claude.ai/customize/skills)
3. Click the **+** icon → **Create skill** → **Upload a skill**
4. Select the downloaded `skill.md` file
5. Start chatting - each skill's README lists the trigger phrases you can use

## Usage

Just say: `Track my rankings` or `Run the rank tracker` or `Show me my keyword position history`

Claude will then ask you three things before it pulls anything:

1. **Which keywords?** - paste them one per line, keywords only. Each keyword is tracked site-wide, so no URL is required. (Power-user extra: add ` | https://full/url` after a keyword to pin it to one page.)
2. **Which country?** - converted to an ISO-3166 alpha-3 code, so India becomes `ind`, the United States `usa`, the United Kingdom `gbr`.
3. **How far back?** - last 1 month, last 3 months, or last 6 months. Sampling is fixed at twice a month either way.

Answer once and Claude can remember the setup for future runs. Say `change config` any time to reset it.

## What It Covers

| Section              | What You Get                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| KPI Tiles            | Keywords tracked, keywords ranking on page one, keywords improving vs the last snapshot, keywords not ranking now   |
| Rank Grid            | One row per keyword, one column per snapshot (newest to oldest), color-coded by position band                       |
| Latest Rank & Change | Current position as a large pill, with a up/down indicator showing movement since the previous snapshot             |
| Movement Read        | A short written summary naming your strongest keyword, the biggest gainer, and the keywords on the watch list       |
| Recommended Action   | One concrete, data-backed next step you can act on this week                                                       |

**How the numbers are built**

- Rankings come from Search Console's **average position** - Google's own logged data, filtered to the exact keyword, your chosen country, and the date
- Snapshots are anchored to the **1st and 15th** of each month, so 1 month is roughly 2 columns, 3 months roughly 6, and 6 months roughly 12
- Each snapshot value is the **impression-weighted average position** across that window, so high-volume days count for more
- **N/R** means zero impressions for that exact keyword in that country during that window
- GSC data lags 2-3 days, so the newest snapshot ends a few days before today
- Position bands: green = top 10, yellow = 11-20, orange = 21-50, red = 50+, grey = N/R

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
