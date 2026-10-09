# Agent Harness KB

Local bootstrap for the researched knowledge base used by Harness Forge.
The research remains in the sibling playground repository until Task 5.
This checkout contains no extracted rules or migrated research yet.

Implementation follows playground's
[approved plan](../playground/plans/2026-10-07-harness-forge-thin-slice.md).
Public links and installation instructions are added at distribution.

## Forge worker isolation gap

The knowledge base does not run workers. Its planned consumer, Harness Forge,
has adopted the owner-approved `best-effort-v1` policy for workers in
Claude Code and Codex: complete tool absence and file/context/network
isolation are not guaranteed. See the local sibling README at
`../harness-forge/README.md`, section `Worker isolation limitations`.
Public cross-repository links will be added at distribution.
This runtime-policy decision does not change the researched KB rules or
turn an unproven security claim into a verified fact.

Forge's public account contract assumes standard vendor CLIs and the
user's existing login at vendor-default locations; an API-key login can
cost extra, and Forge asks before continuing with one. Temporary worker
restrictions remain required, with their gaps documented. The owner's
personal configuration is only a temporary local-development exception;
it is not a KB recommendation, public dependency or installation step.
