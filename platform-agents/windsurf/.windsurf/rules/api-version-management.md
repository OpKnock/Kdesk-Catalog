---
trigger: glob
description: "Manages API version lifecycles: deprecation headers, sunset dates, changelogs, and retirement processes with RFC 8594 Deprecation header conventions. Use when working with deprecation headers, lifecycle track or when the user mentions deprecation headers, lifecycle track."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Manages API version lifecycles: deprecation headers, sunset dates, changelogs, and retirement processes with RFC 8594 Deprecation header conventions.

## Agentic Workflow: Read -> Reason -> Act (api-version-management)

You are **api-version-management** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-version-management`
- Domain: Manages API version lifecycles: deprecation headers, sunset dates, changelogs, and retirement processes with RFC 8594 Deprecation header conventions.
- **deprecation-headers**: Signal deprecation with standard headers — `curl -sI http://localhost:8080/v1/users | grep -iE '^(deprecation|sunset|link):'`
- **lifecycle-track**: Track versions through the lifecycle — `git tag -a v1.0.0 -m 'v1 initial release'`
- Check `knowledge` and `prerequisites: node.js, python, openapi, postman`

### 2. Reason — think for `api-version-management`
- For `deprecation-headers`: Signal deprecation with standard headers — decide which checks to run
- For `lifecycle-track`: Track versions through the lifecycle — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-version-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-version-management:49653cd6`

# API Version Management

Version lifecycle management.

## What This Skill Does
- Signals deprecation with standard headers
- Schedules sunset dates per version
- Maintains changelogs and retirement flows

## When to Use
- Deprecating an API version
- Communicating removals to consumers
- Auditing version lifecycle

## Real Commands

```bash
curl -sI https://api.example.com/v1/users | grep -iE '^(deprecation|sunset|link):'
```

## Deprecation Flow
1. Announce deprecation with headers
2. Publish the changelog entry
3. Warn clients with metrics
4. Retire after the sunset date

## Testing
- Verify headers on every deprecated route
- Check sunset dates are RFC 1123 valid
- Test the retired version returns 410 Gone

## Best Practices
- Give 6-12 months deprecation windows
- Count traffic per version before removal
- Keep retirement logs for compliance

## Capabilities

### deprecation-headers
Signal deprecation with standard headers

**Parameters:**
- `header` (string): deprecation, sunset, or link
- `version` (string): Affected version
- `date` (string): Sunset date in RFC 1123 format

**Commands:**
- `curl -sI http://localhost:8080/v1/users | grep -iE '^(deprecation|sunset|link):'`
- `curl -s -D- http://localhost:8080/v1/users | grep -i '^link:'`
- `node -e "const d=new Date(); d.setMonth(d.getMonth()+6); console.log('Sunset:', d.toUTCString())"`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/v1/users`

**Examples:**
- Deprecation: true warns clients of planned removal
- Sunset: 2026-08-19 communicates removal time
- Link: demo-changelog; rel="sunset" points to details

### lifecycle-track
Track versions through the lifecycle

**Commands:**
- `git tag -a v1.0.0 -m 'v1 initial release'`
- `git tag -a v2.0.0 -m 'v2 GA'`
- `git tag -l 'v*' --sort=-v:refname | head -5`
- `curl -s http://localhost:8080/changelog | jq '.versions[0]'`

**Examples:**
- -cli --help
- -api --help

## References
- [RFC 8594 - Sunset Header](https://www.rfc-editor.org/rfc/rfc8594)
- [GitHub Deprecation Policy](https://docs.github.com/en/rest/about-the-rest-api/breaking-changes)
