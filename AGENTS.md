# AGENTS.md

A **public** collection of Claude skills for marketers, owned by `twominutereports` rather than
`gox-ai`. Each skill connects Claude to a customer's real marketing data through the Two Minute
Reports MCP server, so someone can get a PPC or SEO audit without exporting a spreadsheet or writing
a query.

This repo is a **product surface**: customers reach these skills directly from GitHub, and it is
public, so everything committed here is published. There is no build and no package.json — the
content *is* the deliverable.

```
ppc/            google-ads, meta-ads, linkedin-ads, reddit-ads, tiktok-ads audits
seo/            traffic analysis, rank tracking, content decay, local SEO, GSC+GA4 reporting
social-media/   facebook / instagram insights reports
ecommerce/      shopify store audit
plugins/        tmr-marketing-skills — the packaged plugin
scripts/        build-plugin.mjs
.claude-plugin/ marketplace.json
```

---

## Public means public

- **Never commit a credential, an internal URL, a customer name, or an account id**, including in an
  example. A skill's examples are read by everyone who opens the repo.
- Refer to product surfaces the way customers do: **Google Data Studio**, not Looker Studio; the
  **Hub** at hub.twominutereports.com; the add-on as the **Google Sheets add-on**.
- A skill promises a capability. If the MCP tool it depends on is not live in production, the skill
  is not ready to merge — a published skill that fails on first use is worse than an absent one.

## A skill's shape

Mirror an existing one in the same category rather than inventing a layout. When adding a skill,
update `README.md`'s category table in the same commit — that table is how anyone finds it — and
`.claude-plugin/marketplace.json` plus `plugins/tmr-marketing-skills/` if it ships in the plugin.

Name the connectors and metrics a skill needs explicitly, so a reader can tell before running it
whether their account has the data.

---

## Before you stage anything

There is nothing to build or lint. Instead:

- **Run the skill end to end against a real account** through the TMR MCP server, and say in the PR
  which connector and which account type you used.
- Check every MCP tool name and argument against the live server, not against another skill's copy
  of it — a stale tool name fails at the user's first prompt.

**Never commit or push without being asked.** Stop at the working tree and say what changed.

---

## Filing a PR

The weekly changelog and the product-knowledge record are **generated from merged PR bodies**
(`tmr-iris/scripts/harvest-week.mjs`). Nothing else feeds them. A PR that skips this is not badly
formatted — it is invisible to the record of what the product did that week.

Title: `type(scope): what changed, in the imperative`. It becomes the changelog line, so it has to
read on its own without the body. Types: `feat` `fix` `refactor` `docs` `chore` `test` `perf`
`revert`.

Body opens with one paragraph on what changed and why, then:

```markdown
## Impact

- **User-facing:** yes — <what a person sees or can do differently> | no
- **Surfaces:** hub | website | sheets add-on | data studio | data studio popup | dash | docs | public skills | mcp | public api | none
- **Deploy coupling:** none | must ship with <repo>#<number>, because <reason>
- **Risk:** <what breaks if this is wrong, and how to undo it>

## Verification

<commands run and their result — and what was NOT verified>
```

This repo's usual answer for **Surfaces** is `public skills`.

`User-facing` is parsed and splits the changelog into what customers got versus internal work, so
answer it honestly: "no" for instrumentation, refactors, tooling, schemas and tests. An initiative
is a bet that something changes for a customer, and this is where that claim is made or not made.

**Deploy coupling:** a skill depends on MCP tools served by `tmr_data_service`. If it uses a tool,
argument or field that is not yet in production, this PR must not merge before that one — name it.
Because the repo is public and unversioned, merging *is* shipping: there is no deploy step to hold
it back.

Then, **only when the PR contains one**, add any of these. Their content is lifted verbatim into the
product record, so write for someone who was not in the conversation:

- `## Product decision` — a choice about how the product behaves, and the reasoning.
- `## Ruled out` — a hypothesis tested and rejected, **with the evidence**. Nobody writes these down
  and they are the most expensive knowledge to lose: the same dead hypothesis gets re-tested every
  few months.
- `## Correction` — a previously-believed fact that turned out false. Say what was believed, what is
  true, and how the error happened; the third part is what stops it recurring.

A product fact that arrives in conversation and has no PR goes to
`tmr-iris/packages/agent/docs/product/` instead.

Full spec with examples: `tmr-iris/packages/agent/docs/PR_CONVENTIONS.md`.
