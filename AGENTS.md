# Agent Harness KB

Researched knowledge base on configuring coding-agent harnesses: Claude
Code, Codex and OpenCode. `docs/` holds the research; `rules/`,
`checks/`, `schemas/` and `policy/` hold the rules Harness Forge extracts
from it.

## Agent harness knowledge base

- For any question or change about an agent harness (instruction
  files, settings, permissions, sandbox, MCP, skills, slash commands,
  subagents, hooks, plugins, headless or CI runs), load the
  `agent-harness` skill first. It maps each question to the page to
  read. Without skill support, start at `docs/overview.md`.
- The knowledge base reflects 2026-10-04 (Claude Code 2.1.289,
  codex-cli 0.159.2, OpenCode 1.18.34). Confirm version-sensitive
  details against the source a page cites before relying on them.
- Every claim in `docs/` needs a reliable source that was fetched and
  says what is cited. A claim that cannot be verified is dropped, not
  marked unverified, and the X platform is not a source. Before adding,
  changing or citing a source, and in every research or writing brief
  for a subagent, apply `docs/sources.md`: the full rules plus the
  trusted and rejected domains.
- When a fact in `docs/` turns out outdated, fix the vendor page with
  its new source, then every page that repeats it: `docs/concepts/`,
  `docs/best-practices/`, `docs/guide/` and `docs/overview.md`. Then
  update every rule in `rules/` that cites the changed section, and run
  `tools/validate.py`.
- This repository is the authoritative copy since 2026-10-09. The
  research came from the playground commit recorded in `kb-manifest.json`;
  playground removed its copy after this repository was published.

## Rules

- Every rule cites the KB pages it comes from and, where the page
  cites one, the primary source. Rules follow `policy/severity.md`.
- `rules/coverage.yaml` records every swept section item: the rules it
  became, or why it is not a rule.
- Rules name checkers from `checks/catalog.yaml` by id, never a script
  path. The checker implementations ship in Harness Forge.

## Repository layout rules

- This file is the only instruction file. Claude Code reads
  `AGENTS.md` only while no `CLAUDE.md` exists, so instructions for any
  harness go here.
- Skills live in `.agents/skills/<name>/` (read by Codex and
  OpenCode), each with a relative symlink at `.claude/skills/<name>`
  (read by Claude Code).
- Name subagent material `subagents.md`. Files named `agents.md` or
  `claude.md` load as instruction files on case-insensitive file
  systems.

## Account boundary

This repository supplies knowledge; it does not manage model accounts.
Every agent must keep public guidance independent of the project owner's
aliases, profile paths, plugins and shell setup. Forge assumes standard
vendor CLIs, vendor-default account locations and the user's existing
login (it asks before continuing with an API-key login), with temporary
worker restrictions and documented isolation gaps. Owner-specific setup
is a temporary local-development exception only and is documented
outside this repository.

Do not copy credentials, change login state or add API-credit fallbacks.

## Attribution

Use Conventional Commits and record AI attribution as final-paragraph
`Assisted-by: <model> (code generation)` or `(code review)` trailers.

## Pull requests and merging

Changes reach `main` only through a pull request, merged with a merge
commit (the only method this repository allows). Keep the PR
description in step with what the PR contains. Merge only after the
repository's required checks (`tools/validate.py`) pass and an
independent review of the latest pushed head finds the PR ready; a
push after that review needs a new one. The owner's AI agents (Claude
implementing, Codex planning and reviewing) follow the working mode in
[playground's AGENTS.md](https://github.com/franks-ai-skills/playground/blob/ai-stuff/AGENTS.md#working-mode-claude-and-codex-owner-2026-10-22).
