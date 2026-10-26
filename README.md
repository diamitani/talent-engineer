# Talent Engineer 1.1 - audited prototype

## Upload unchanged

Save talent-engineer-v1.1.zip to Files/Downloads. Do not unzip it for Claude chat.
In Claude: enable code execution/file creation and Skills if needed. Go to
Customize > Skills > + > Create skill > Upload a skill. Select the ZIP and toggle it on.
Your organization's policies and scanning still apply. We checked the package against
Claude's published structure; actual upload and activation in your Claude account are untested.

The ZIP contains one talent-engineer/ folder with SKILL.md inside. It does not
contain API keys or private candidate data. The only candidate fixture is fake.

## Try immediately with no vendor accounts

Ask: "Use Talent Engineer in demo mode. Run the included regression tests and
build scripts/sample_candidate.json into a candidate page. Do not call live systems."

Python 3.9+ and its standard library are sufficient for both utilities and tests:

```bash
cd talent-engineer
python3 -m unittest discover -s tests -v
python3 scripts/build_candidate_site.py scripts/sample_candidate.json out/demo/
python3 scripts/failure_tracker.py status
```

Open out/demo/index.html locally. It is a snapshot, not an authenticated website.

## Live setup is separate

Connect your authorized accounts via Claude Connectors. The skill cannot install
connectors or obtain tenant permissions. Workday needs an administrator and eligible
configuration. BrightHire's official MCP exists; its precise endpoint in this package
is a third-party lead and must be verified in BrightHire's setup UI before use.
Use references/systems.md. Tool names and available fields come from discovery.

The example in config/ is for Claude Code only. Copy selected entries to your
project's .mcp.json after reviewing them and authenticating. It deliberately omits
unverified BrightHire and tenant-specific Workday configuration. Importing the skill
ZIP does not load that example automatically.

## What works locally / what remains

Included and regression tested: failure log/status/recent/reset; escaped, validated
four-source HTML snapshot generation including unavailable sources. Failure counting
is local and single-writer, not a platform-enforced circuit breaker.

Not tested: a Claude upload, live MCP calls, Gong tenant access, deployed automations,
SSO hosting, automatic refresh or a team-dashboard backend. n8n/Make/cron content
is recipe guidance, not an importable production workflow. See AUDIT.md.
