#!/usr/bin/env node
/**
 * Generates the Claude Code plugin from the skill folders in this repo.
 *
 * The category folders (ppc/, seo/, social-media/, ecommerce/) are the source of
 * truth — this script derives `plugins/tmr-marketing-skills/` from them so there is
 * never a second copy of a skill to keep in sync.
 *
 * Two things it fixes on the way through:
 *   1. `skill.md` → `SKILL.md`. Claude Code discovers skills by that exact name,
 *      and on a case-sensitive filesystem a lowercase file is simply not found.
 *   2. Skill folder names are taken from the frontmatter `name:` where present, so
 *      the installed skill matches the id the skill advertises (a few folders and
 *      frontmatter names disagree — e.g. seo/website-traffic-analysis declares
 *      `tmr-website-traffic-growth-analyst`).
 *
 * The plugin also ships `.mcp.json`, so installing it connects the TMR MCP server
 * in the same step — the skills are useless without it, and asking a user to do two
 * unrelated setups is how you lose them.
 *
 * Usage: node scripts/build-plugin.mjs [--check]
 *   --check  build into a temp dir and fail if it differs from what's committed
 *            (so CI catches a stale plugin instead of shipping one)
 */

import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { execFileSync } from "node:child_process";

const REPO_ROOT = resolve(import.meta.dirname, "..");
const CATEGORIES = ["ppc", "seo", "social-media", "ecommerce"];
const PLUGIN_NAME = "tmr-marketing-skills";
const OUT_REL = join("plugins", PLUGIN_NAME);
const MCP_URL = "https://mcp.twominutereports.com/mcp";

const CHECK = process.argv.includes("--check");

/** Reads a scalar key from a markdown file's YAML frontmatter. */
function frontmatterKey(md, key) {
  const block = /^﻿?---\s*\n([\s\S]*?)\n---\s*$/m.exec(md);
  if (!block) return null;
  const line = new RegExp(`^${key}:\\s*(.+)$`, "m").exec(block[1]);
  return line ? line[1].trim().replace(/^["']|["']$/g, "") : null;
}

/** Every skill folder in the repo: { dir, skillName, category }. */
async function discoverSkills() {
  const skills = [];
  for (const category of CATEGORIES) {
    const categoryDir = join(REPO_ROOT, category);
    if (!existsSync(categoryDir)) continue;
    const entries = await readdir(categoryDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const dir = join(categoryDir, entry.name);
      const skillMd = join(dir, "skill.md");
      if (!existsSync(skillMd)) continue;
      const md = await readFile(skillMd, "utf8");
      // Prefer the declared name so the installed skill matches its own id.
      const declared = frontmatterKey(md, "name");
      skills.push({
        dir,
        folder: entry.name,
        category,
        skillName: declared && /^[a-z0-9][a-z0-9-]*$/.test(declared) ? declared : entry.name,
      });
    }
  }
  return skills.sort((a, b) => a.skillName.localeCompare(b.skillName));
}

async function build(outRoot) {
  const skills = await discoverSkills();
  if (!skills.length) throw new Error("no skills found — is this the right repo root?");

  await rm(outRoot, { recursive: true, force: true });
  await mkdir(join(outRoot, ".claude-plugin"), { recursive: true });

  await writeFile(
    join(outRoot, ".claude-plugin", "plugin.json"),
    `${JSON.stringify(
      {
        name: PLUGIN_NAME,
        description:
          "Marketing audit and reporting skills that run on your live Two Minute Reports data.",
        version: "1.0.0",
        author: { name: "Two Minute Reports", url: "https://twominutereports.com" },
        homepage: "https://github.com/twominutereports/marketing-skills",
        license: "MIT",
      },
      null,
      2,
    )}\n`,
  );

  // Bundling the MCP server means one install gives both the skills AND the data
  // they need. Without it every skill would stop on its first tool call.
  await writeFile(
    join(outRoot, ".mcp.json"),
    `${JSON.stringify(
      { mcpServers: { "two-minute-reports": { type: "http", url: MCP_URL } } },
      null,
      2,
    )}\n`,
  );

  for (const skill of skills) {
    const dest = join(outRoot, "skills", skill.skillName);
    await mkdir(dest, { recursive: true });

    // skill.md → SKILL.md (the name Claude Code actually looks for).
    await cp(join(skill.dir, "skill.md"), join(dest, "SKILL.md"));

    // Reference files travel with the skill: 8 of the skills instruct the model to
    // read references/thresholds.md, so shipping SKILL.md alone would leave those
    // instructions pointing at nothing.
    const refs = join(skill.dir, "references");
    if (existsSync(refs)) await cp(refs, join(dest, "references"), { recursive: true });

    const queries = join(skill.dir, "queries.json");
    if (existsSync(queries)) await cp(queries, join(dest, "queries.json"));
  }

  return skills;
}

const outRoot = join(REPO_ROOT, OUT_REL);

if (CHECK) {
  const temp = join(tmpdir(), `tmr-plugin-check-${process.pid}`);
  const skills = await build(temp);
  try {
    execFileSync("diff", ["-r", temp, outRoot], { stdio: "pipe" });
    console.log(`plugin is up to date (${skills.length} skills)`);
  } catch (err) {
    console.error("plugins/ is out of date — run `node scripts/build-plugin.mjs` and commit:\n");
    console.error(err.stdout?.toString() ?? err.message);
    process.exit(1);
  } finally {
    await rm(temp, { recursive: true, force: true });
  }
} else {
  const skills = await build(outRoot);
  console.log(`built ${OUT_REL} with ${skills.length} skills:`);
  for (const s of skills) console.log(`  ${s.category}/${s.folder} → skills/${s.skillName}`);
}
