# Changelog

The version is `kb_version` in `kb-manifest.json`. Harness Forge pins a
snapshot of one released version and records its commit in its own
`snapshot/kb-manifest.json`.

Each pull request that changes `docs/`, `rules/`, `schemas/`,
`policy/`, `checks/`, `fixtures/` or `kb-manifest.json` raises
`kb_version` and adds a dated section for that version at the top of
this file. During 0.x, changed facts, rules, questions, checker
behavior or versions, and schemas raise the minor version; editorial or
metadata corrections with no such change raise the patch version.
Changes outside those paths need no new version. After the merge, the
merge commit is tagged `v<version>` and gets a GitHub release whose
notes are its section here, before the next pull request that changes
those paths merges. Release tags are never moved.

## 0.6.0 (2026-10-25)

- Security guidance for skills (#11), researched from newly fetched
  sources (`docs/research-notes/agent-harness-security-2026-10-25.md`)
  in `docs/guide/security.md`: repository metadata (commit messages,
  author names and emails, branch names) is untrusted input; untrusted
  material embedded in output sits in a container it cannot end, which
  is syntax containment, not protection from its instructions, and a
  prompt saved for another session states its own trust boundary; write
  destinations are resolved, links included, and a check before the
  write is not race-free containment; credential files the task does not
  need are not read. Tag and file names were not found as untrusted
  input in the fetched sources and are not claimed.
- `rules/security.yaml`: new `security.writes.within-boundary`,
  `security.embedded-content.contained` and
  `security.secrets.no-unneeded-reads` (should, warning, judged), and
  `security.untrusted-input.as-data` names repository metadata.
  `docs/sources.md` adds `cwe.mitre.org` and `spec.commonmark.org`.
- `rules/selection.yaml`: every outside control has a readable `name`
  and the `reason` it is recommended, from the guide sections its rule
  cites (harness-forge#53). `checks/catalog.yaml`: `selection.match`
  1.6.0 requires both; `outside.readme-coverage` 1.3.0 reads Harness
  Forge's readable entry form beside the earlier one.
- Minor, because rules, a checker's parameters and checker versions
  changed.

## 0.5.0 (2026-10-24)

- `checks/catalog.yaml`: `skills.name-format` is version 1.1.0. Harness
  Forge's checker matches the whole name, so a name with a trailing line
  break is refused by the pattern itself (harness-forge#51). Minor,
  because a checker version changed.

## 0.4.0 (2026-10-24)

- `schemas/`: the six schema copies follow Harness Forge's move from JSON
  Schema Draft 2020-12 to Draft-07 (harness-forge#56): `prefixItems`
  becomes array-form `items` with `additionalItems`, `$defs` becomes
  `definitions`, and each schema refers to itself by its absolute `$id`.
  The documents they describe are unchanged. Minor, because the schemas
  changed.

## 0.3.0 (2026-10-24)

- `docs/best-practices/plugins.md` (practice 3 and the release
  checklist) and `docs/guide/plugins.md`: plugin release tags. The pages
  asked for a `<plugin>--v<version>` tag on every release. Updates
  follow the version, so ordinary marketplace updates impose no
  tag-naming requirement; Claude Code resolves git-backed plugin
  dependency ranges against `<plugin>--v<version>` tags, which is when
  its dependency documentation asks for them. Minor,
  because the guidance changed meaning.

## 0.2.0 (2026-10-23)

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
- `rules/skills.yaml`, `rules/selection.yaml`: the skill layout rules
  apply by where a skill lives. A part fact `skill_home` (`repository`
  or `plugin`, derived by Forge, never asked) limits
  `skills.portable.layout` to a skill in `.agents/skills/`. The new
  rule `skills.portable.plugin-layout` (checker `links.plugin-layout`
  1.0.0) requires a plugin skill in `skills/<name>/` under a plugin
  root that holds the `plugin.json` manifest Codex reads, or
  `.codex-plugin/plugin.json`. Before, a skill shipped in a plugin
  failed the repository layout rule. `docs/concepts/skills.md` says
  that a plugin skill needs no `.agents/skills/` copy or
  `.claude/skills/` link; two new fixtures cover the plugin layout.
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

First release, tagged `v0.1.0` afterwards at `9a9063d`, the commit
Harness Forge pinned at publication.

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
