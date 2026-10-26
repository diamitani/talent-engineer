# Connection notes - checked October 26, 2026

Public documentation supports four MCP offerings. That does not establish access to
Gong's tenants or guarantee the required tools/fields. Discover each tenant's actual
read tools; do not copy tool names from a directory as a contract.

| System | Grounded access path | Limits / setup |
| --- | --- | --- |
| Greenhouse | Official remote MCP: https://mcp.greenhouse.io/mcp. Vendor also documents https://mcp.us.greenhouse.io/mcp for clients/region. OAuth. | Open beta; Core/Plus/Pro; Site Admin controls access/scopes. Confirm region with admin. |
| Gem | Official GeMCP: https://mcp.gem.com/mcp. Published Claude connector; individual OAuth and Gem permissions. | Organization may disable MCP; confirm account and approved AI client. |
| BrightHire | Official MCP confirmed by vendor. OAuth, existing permissions, candidate/interview questions and summaries. | https://app.brighthire.ai/mcp/v1 is listed by a third-party directory, not confirmed by the fetched vendor setup page. Use the official connector/setup UI or ask the vendor/admin to verify the URL before connecting. No claim about public REST API availability is needed. |
| Workday | Agent Gateway and Agent-Ready MCP tools. Admin guide examples include https://us.agent.workday.com/mcp and a tenant-specific URL pattern. | Extend Professionals; Agent System of Record, external-agent registration, skill security and OAuth. Subscription/enablement requirements apply. Admin must provide actual endpoint and renewable auth. Requisition, offer or worker tools are not guaranteed. |

Never put long-lived tokens in this package or chat. Workday access-token refresh
is part of a deployed adapter, not handled by these local scripts. API fallbacks
require documentation and admin approval for the exact tenant. An export is a valid
read-only fallback if marked export/not-live, permissioned and timestamped.

## Smoke tests

Discover tools in the client first. Then choose one minimal authorized read: one
open job in Greenhouse, one accessible project/job in Gem, one limited interview
summary in BrightHire, and one allowed Workday tool. Workday tools/list is discovery,
not proof that recruiting objects are available. Empty results may be valid.
Record source, account/tenant and timestamp. Do not label a system connected until
an authorized read succeeds. No live tests were done for this package.

## Sources

- Claude authoring and package specification: https://claude.com/docs/skills/how-to
- Claude upload / capabilities / policy: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Greenhouse: https://support.greenhouse.io/hc/en-us/articles/52096319906971-Set-up-Greenhouse-MCP-with-supported-AI-tools
- Gem setup: https://help.gem.com/databases/gem-help-center/getting-started-with-gemcp
- Gem use cases: https://help.gem.com/databases/gem-help-center/gemcp-prompt-examples-and-use-cases
- BrightHire official: https://brighthire.com/request-a-demo/mcp/ and https://brighthire.com/insights/
- BrightHire endpoint lead, third-party only: https://agentready.co/connectors/brighthire
- Workday admin guide (updated October 9, 2026): https://doc.workday.com/admin-guide/en-us/workday-ai/agents/external-agents/connect-an-external-agent-with-workday-mcp.html
