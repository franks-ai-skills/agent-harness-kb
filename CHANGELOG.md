# Changelog

The version is `kb_version` in `kb-manifest.json`. Harness Forge pins a
snapshot of one commit and records that commit in its own
`snapshot/kb-manifest.json`.

## Unreleased

- `rules/selection.yaml`: a part fact `side_effects` asks whether a
  part changes external state, such as committing, pushing, deploying,
  editing an issue or sending a message, or needs timing the model
  should not choose. When it holds, a model-invoked skill, instructions
  and a subagent are ruled out and a user-invoked skill is preferred,
  as for an irreversible action, but without the outside gate. Before,
  selection could recommend a model-invoked skill for a reversible
  change that `skills.invocation.side-effects-user-invoked` then failed.
  Every selection fixture answers the fact; two new fixtures cover a
  user-started and a model-started side effect.
- `rules/selection.yaml`: every recommended control lists each of the
  seven gate conditions its family needs. Code owners on the agent's
  configuration gain the bypass, approval, broader-credential and plan
  conditions; merge rules and the event gate gain the broader-credential
  condition, and the event gate the definition conditions; the
  compromise-resistant gate gains the approval and check conditions; and
  outer isolation the bypass condition.
- `rules/outside-controls.yaml`: `outside.merge.requester-cannot-approve`,
  `outside.ci.source-pinned` and `outside.ci.workflow-protected` say when
  they apply, since a generic or mixed gate need not use approval, checks
  or CODEOWNERS.
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
