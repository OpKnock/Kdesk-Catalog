# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

Only the latest minor release line receives security fixes. The `1.0.x`
line receives fixes for critical issues only.

## Trust model

Kdesk is a **local-first developer tool**. The web dashboard (`kdesk serve`)
binds to `127.0.0.1` by default and is intended for single-user use on your
own machine. Catalog data, projects you scan, and execution history stay on
your machine; nothing is uploaded anywhere.

- Destructive operations (install, rollback, fix with dry-run off, real
  `run` executions) require explicit confirmation in the UI and default to
  dry-run / preview.
- File uploads are capped (20 files, 200 KB each), parsed with
  `yaml.safe_load`, scanned in a temporary directory, and deleted afterwards.
- Generated-file downloads are constrained to their output directories;
  path traversal outside those roots is rejected.
- If you bind the server to a non-loopback address (`--host 0.0.0.0`), you
  are exposing unauthenticated mutating endpoints to your network. Only do
  this on networks you fully trust.

## Reporting a Vulnerability

**Do not open a public issue for security reports.**

Report privately via the issue tracker using a **Security Advisory**:
https://github.com/OpKnock/Kdesk-Catalog/security/advisories/new

Include:

1. Affected version(s) and component (`kdesk doctor`, web API, converter, …)
2. Steps to reproduce (proof-of-concept preferred)
3. Impact assessment (what an attacker gains, and under what trust model)

What to expect:

- Acknowledgement within **5 business days**.
- A fix timeline once the issue is confirmed (critical issues first).
- Credit in the release notes if you want it (or anonymity — your call).

## Scope notes (honest limits)

- Kdesk validates definitions against deterministic rules (schema, policy,
  known-secret patterns, platform contracts). It is **not** a sandbox and
  does **not** execute untrusted code during scans.
- Heuristic checks (e.g. suspicious-instruction detection) are best-effort
  and may miss novel attacks. Treat findings as signals, not guarantees.
