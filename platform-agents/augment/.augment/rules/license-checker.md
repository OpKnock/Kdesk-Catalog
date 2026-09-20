---
type: agent_requested
description: "Audits npm dependency licenses with license-checker, detecting incompatible, missing, or unknown licenses before release."
---

# License Checker

Audits npm dependency licenses with license-checker, detecting incompatible, missing, or unknown licenses before release.

## Instructions

# License Checker

Audits every transitive npm dependency and reports its SPDX license so you can enforce
legal compliance in CI.

## When to Use

- Before shipping a package or SaaS product to check license compatibility
- Enforcing an allow-list (MIT/Apache/BSD only) on a monorepo
- Detecting copyleft (GPL/AGPL) or unknown licenses sneaking in via transitive deps
- Generating a license report for legal or compliance review

## Real Commands

```bash
# Install
npm install --save-dev license-checker

# Human-readable tree of every package and its license
npx license-checker --start

# Summary counts per license type
npx license-checker --summary

# Fail the build if any license is outside the allow-list
npx license-checker --onlyAllow "MIT;Apache-2.0;ISC;BSD-2-Clause;BSD-3-Clause"

# Fail on copyleft regardless of allow-list
npx license-checker --failOn "GPL;AGPL;LGPL"

# Production-only JSON report for legal
npx license-checker --production --json --out license-audit.json

# CSV report suitable for spreadsheets
npx license-checker --csv --out licenses.csv
```

## CI Integration

```yaml
# GitHub Actions
- name: License audit
  run: npx license-checker --onlyAllow "MIT;Apache-2.0;ISC;BSD-3-Clause"

# GitLab CI
license-audit:
  stage: security
  script:
    - npx license-checker --summary
    - npx license-checker --onlyAllow "MIT;Apache-2.0;ISC"
```

## Best Practices

- Pin the checker version; license data changes as packages publish
- Run against `--production` for releases and full tree for dev tooling
- Review `--excludePackages` carefully; it bypasses the allow-list entirely
- Treat packages with `UNKNOWN` licenses as a review task, not an auto-pass
- Re-run after every dependency bump; a new transitive dep can add a copyleft license

## Example Response

When a copyleft license is found the exit code is non-zero and stdout lists the offending
packages with `license-checker --summary` style counts, so the agent reports the exact
package name and version to remove or replace.

## Capabilities

### audit-licenses
Generate license inventories and enforce allowed-license policies for npm projects

**Commands:**
- `npx license-checker --summary`
- `license-checker --csv --out /tmp/licenses.csv`
- `license-checker --onlyAllow "MIT;Apache-2.0;ISC;BSD-3-Clause"`
- `license-checker --production --json --out license-audit.json`
- `license-checker --excludePackages "lodash@4.17.21" --failOn "GPL"`

**Examples:**
- npx license-checker --onlyAllow 'MIT;Apache-2.0'
- license-checker --start --production --csv > licenses.csv
- license-checker --summary | head -40