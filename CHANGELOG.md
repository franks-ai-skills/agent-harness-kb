# Changelog

The version is `kb_version` in `kb-manifest.json`. Harness Forge pins a
snapshot of one commit and records that commit in its own
`snapshot/kb-manifest.json`.

## Unreleased

- `checks/catalog.yaml`: Harness Forge reads Markdown with the CommonMark
  parser markdown-it-py instead of its own scanner, so the checkers that
  read Markdown changed behavior: `links.relative-references` and
  `skills.reference-depth` 1.4.0, `skills.portable-body` 1.2.0,
  `outside.readme-coverage` 1.2.0.

## 0.1.0 (2026-10-16)

First release.

- `docs/`: the knowledge base researched on 2026-10-04 against Claude
  Code 2.1.289, codex-cli 0.159.2 and OpenCode 1.18.34, moved from the
  playground repository on 2026-10-09. `kb-manifest.json` records the
  source commit and the hash of every moved file.
- `rules/`: rules extracted for Harness Forge's skills slice: skills
  (30), security (5), outside controls (12) and mechanism selection
  (68), with the page coverage in `rules/coverage.yaml`.
- `checks/catalog.yaml`, `schemas/` and `policy/`: the checker catalog,
  the JSON Schema formats of every rule file and the severity policy.
- `tools/validate.py`: validates rules, catalog, coverage and links.
