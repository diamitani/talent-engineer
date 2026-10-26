# Audit - version 1.1, October 26, 2026

## Fixed

- Replaced a shell example containing unquoted pipe characters with a valid command.
- Made HTML values safe for numbers/nulls and escaped all displayed input. Hidden
  unavailable-source items no longer risk accidental rendering. Unknown sources,
  missing timestamps and impossible evidence ratios fail validation.
- Changed misleading "live" labels to snapshot/export/unavailable; removed the
  implied fixed hiring cutoff. Evidence completeness is not candidate quality.
- Made a relative failure-log filename work; malformed logs now fail visibly.
  Resets retain audit history instead of deleting it. Empty logs say connection
  unverified. Failure counts use the last 24 hours since a confirmed reset.
- Clarified that the failure stop rule is instruction-driven, not an MCP interceptor,
  and that chat-local storage is not a durable organizational monitoring system.
- Removed unverified BrightHire and placeholder Workday endpoints from the sample
  executable configuration. Kept BrightHire's endpoint as a labeled third-party
  lead in documentation only. Official MCP existence is confirmed by BrightHire.
- Separated skill upload from OAuth connector setup, Workday admin work, runner
  deployment, scheduled jobs and SSO hosting. Removed "connect and it works" claims.
- Added stable-ID identity-matching, data-minimization and prompt-injection rules.
- Added README, references, 17 regression tests and explicit test prompts.

## Local verification

17 unittest cases passed: fake-data rendering, unavailable-data hiding, HTML escaping,
numeric/null values, missing sources, snapshot labels, invalid ratios, required
fetch timestamps, export labels, invalid JSON CLI, unverified health, three-error
STOP count, rolling-day expiry, history-preserving reset, corrupt logs, relative
log path/full CLI round-trip and invalid CLI category. Python compilation, YAML
frontmatter, matching folder/name, description limit, JSON config, static file
references and ZIP integrity were checked. Demo inspected at phone and desktop sizes.

## Not verified / not supplied

No upload/activation in Patrick's Claude account, no live Gong tenant calls, no vendor
admin approvals. No importable n8n/Make workflow, deployed scheduler, dashboard
backend, authenticated hosting, automatic page update or live MCP adapter. Recipes
can guide building them. No end-to-end live-system claim is made. Installation
follows published Claude documentation; organization policies may prevent instant use.
