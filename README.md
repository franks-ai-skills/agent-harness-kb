# Agent Harness KB

Researched knowledge base on configuring coding-agent harnesses (Claude
Code, Codex, OpenCode), and the rules Harness Forge extracts from it.

- `docs/`: the research. Start at `docs/overview.md`.
- `rules/`, `checks/catalog.yaml`, `schemas/`, `policy/severity.md`:
  extracted rules, checker catalog, formats and severity policy.
- `CHANGELOG.md`: the released versions and the version policy. Each
  release is tagged `v<version>`.
- `kb-manifest.json`: KB version and the migration record of the
  research copied from playground on 2026-10-09. Its source commit is
  the one playground's history rewrite of 2026-10-16 gave the copied
  commit `a2892b6`; playground's
  [`plans/history-rewrite-2026-10-16.md`](https://github.com/franks-ai-skills/playground/blob/ai-stuff/plans/history-rewrite-2026-10-16.md)
  maps both. `history-rewrite-2026-10-16.md` maps this repository's own
  rewritten commits.

Implementation follows the approved
[plan](https://github.com/franks-ai-skills/playground/blob/ai-stuff/plans/2026-10-07-harness-forge-thin-slice.md)
in the playground repository. Harness Forge pins a snapshot of a
released version of this repository; install Forge as its
[README](https://github.com/franks-ai-skills/harness-forge#installation)
describes.

## Forge worker isolation gap

The knowledge base does not run workers. Its consumer, Harness Forge,
has adopted the owner-approved `best-effort-v1` policy for workers in
Claude Code and Codex: complete tool absence and file/context/network
isolation are not guaranteed. See Forge's
[worker isolation limitations](https://github.com/franks-ai-skills/harness-forge#worker-isolation-limitations).
This runtime-policy decision does not change the researched KB rules or
turn an unproven security claim into a verified fact.

Forge's public account contract assumes standard vendor CLIs and the
user's existing login at vendor-default locations; an API-key login can
cost extra, and Forge asks before continuing with one. Temporary worker
restrictions remain required, with their gaps documented. The owner's
personal configuration is only a temporary local-development exception;
it is not a KB recommendation, public dependency or installation step.

## License

[AGPL-3.0-only](LICENSE). The rule files Harness Forge copies into the
files it generates (`rules/skills.yaml`, `rules/security.yaml`,
`rules/outside-controls.yaml` and `rules/selection.yaml`) are also
licensed under the
[Harness Forge Generated Output Exception](LICENSE-OUTPUT-EXCEPTION),
which their notice names. The pages in `docs/` quote their sources;
the quoted passages remain their authors' and are not licensed by this
repository. Contributions:
[CONTRIBUTING.md](CONTRIBUTING.md).
