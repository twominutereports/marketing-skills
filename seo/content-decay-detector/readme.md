# Content Decay Detector — Claude Skill

A Claude skill that identifies pages on your website that are silently losing traffic. It compares the last 30 days against the prior period across both Google Search Console and GA4, scores each declining page by severity, diagnoses the root cause, and delivers a prioritised action list alongside a full HTML dashboard.

## Requirements & Setup

**Prerequisites**

- Claude.ai Pro, Team, or Enterprise account
- [Two Minute Reports](https://twominutereports.com) MCP connected in Claude Settings
- The relevant data source (Google Analytics, Search Console, etc.) linked within Two Minute Reports

**Installing a skill in Claude**

1. Download the `.md` skill file from the skill's folder in this repository
2. Go to [claude.ai/customize/skills](https://claude.ai/customize/skills)
3. Click the **+** icon → **Create skill** → **Upload a skill**
4. Select the downloaded `skill.md` file
5. Start chatting — each skill's README lists the trigger phrases you can use

<img width="1245" height="770" alt="Image" src="https://github.com/user-attachments/assets/127aaee5-42cb-439a-abdd-60363fec27b9" />

## Usage

Just say: `Detect content decay` or `Find my declining pages` or `Run a content decay audit`

Claude will pull your GSC and GA4 data, score every candidate page, and deliver the full report automatically.

## What It Covers

| Section                   | What You Get                                                                                        |
| ------------------------- | --------------------------------------------------------------------------------------------------- |
| Decay Candidate Detection | Pages with >20% drop in clicks or organic sessions vs the prior period                              |
| Severity Scoring          | Each page scored 0–100 across clicks, sessions, impressions, and position                           |
| Root Cause Diagnosis      | Case-matched to Visibility Loss, SERP Issue, Tracking Mismatch, or Engagement Decay                 |
| Tracking Mismatch Flag    | Pages where GSC clicks are stable but GA4 sessions dropped — flagged before content action is taken |
| HTML Dashboard            | Full decay table with severity colour-coding, root cause pills, and a recommended actions panel     |
| Pattern Observation       | Whether a single root cause dominates, or decay is spread across types and URL clusters             |
| Priority Action           | One concrete next step tied to the highest-severity finding                                         |

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
