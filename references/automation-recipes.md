# Automation designs, not importable workflows

These are starting recipes requiring a deployed runner and target-platform tests.
Do not activate them just because a connector is available in Claude. Each runner
needs its own authorized access, pagination/delta handling, timezone, durable state,
retry/backoff, redacted error log and an alert destination approved by the team.

1. Feedback drafter: after a verified completed interview or proposed decision,
   gather permitted evidence and draft a note. A proposed 48-hour target is configurable,
   not Gong policy. A recruiter approves the exact message and recipient before send.
2. Evidence review flag: compute documented rubric coverage, never candidate worth.
   A proposed 60% flag needs team calibration. Flag for human review only; do not
   intercept or change a rejection automatically without an authorized implemented gate.
3. Debrief packet: when all expected scorecards arrive, merge source-linked evidence
   and conflicts, using verified application and requisition IDs.
4. Stalled-candidate alert: run on an agreed schedule/calendar and SLA, with an owner.
5. Req reconciliation: compare authoritative Workday/Greenhouse mappings; report
   conflicts without overwriting either source.

Use an idempotency key such as application_id + event_type + source_event_id. Persist
processing state and check it before effects. Approval must bind the exact payload
and recipient; a changed draft requires new approval. Failed/expired approvals must
not send. Test duplicate events and a failed connector.

n8n and Make designs must use node/module schemas from the actual target version.
MCP calls may require a supported client node or an approved adapter, not generic
HTTP JSON guessed from tool names. A local Python tracker cannot be invoked directly
by a hosted runner without a deployed service or worker. Use that runner's durable
error store and a permissioned alert route instead. Claude scheduled tasks depend
on host support; a cron string alone does not create one. This package does not
include a scheduler, webhook receiver or MCP-to-API bridge.
