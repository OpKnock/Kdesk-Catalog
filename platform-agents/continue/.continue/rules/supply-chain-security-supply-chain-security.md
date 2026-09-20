---
name: "supply-chain-security-supply-chain-security"
description: "Secures the software supply chain with dependency auditing, SBOM generation, signing, and provenance verification across ecosystems."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# supply-chain-security-supply-chain-security

Secures the software supply chain with dependency auditing, SBOM generation, signing, and provenance verification across ecosystems.

## Instructions

# Supply Chain Security

Protect the software supply chain from dependency to deployment.

## What This Skill Does

- Audits dependencies for known vulnerabilities per ecosystem
- Generates SBOMs in standard formats
- Signs artifacts and images for tamper evidence
- Verifies provenance before deployment

## When to Use

- Onboarding dependency scanning for a repo
- Meeting SLSA/Sigstore requirements
- Auditing third-party dependencies

## Real Commands

```bash
# Audit dependencies
npm audit --audit-level=high
pip-audit -r requirements.txt
govulncheck ./...
cargo audit

# Scan for vulns incl. secrets
 trivy fs --scanners vuln,secret,config .
osv-scanner scan -r .

# SBOM + signing
syft . -o cyclonedx-json > sbom.cdx.json
cosign sign --key cosign.key ghcr.io/org/app:latest
cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest

# Verify
slsa-verifier verify-artifact dist.tgz \
  --provenance-path dist.intoto.jsonl --source-uri github.com/org/repo
```

## Pipeline Shape

```yaml
stages:
  audit: [npm audit, pip-audit]
  sbom: [syft . -o cyclonedx-json > sbom.cdx.json]
  sign: [cosign sign --key cosign.key image]
  verify: [slsa-verifier verify-artifact dist.tgz --provenance-path ...]
```

## Best Practices

- Pin dependencies to lockfiles and review updates
- Scan at PR time; re-scan before release
- Generate and store SBOMs with every release artifact
- Sign releases with cosign and verify at deploy
- Use Dependabot/Renovate for automated update PRs

## Capabilities

### dependency-auditing
Audit dependencies across package ecosystems.

**Commands:**
- `npm audit --json`
- `npm audit fix --force`
- `pip-audit`
- `govulncheck ./...`
- `cargo audit`

**Examples:**
- npm audit --audit-level=high
- pip-audit -r requirements.txt
- govulncheck ./...

### sbom-and-signing
Generate SBOMs and sign artifacts for provenance.

**Commands:**
- `syft . -o cyclonedx-json > sbom.cdx.json`
- `cosign generate-key-pair`
- `cosign sign --key cosign.key ghcr.io/org/app:latest`
- `cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest`
- `slsa-verifier verify-artifact dist.tgz --provenance-path dist.intoto.jsonl --source-uri github.com/org/repo`

**Examples:**
- syft . -o cyclonedx-json > sbom.cdx.json
- cosign sign --key cosign.key ghcr.io/org/app:latest
- slsa-verifier verify-artifact dist.tgz --provenance-path dist.intoto.jsonl --source-uri github.com/org/repo

### vuln-scanning
Scan repos and dependencies for known vulnerabilities.

**Commands:**
- `trivy fs --scanners vuln,secret,config .`
- `osv-scanner scan -r .`
- `safety check -r requirements.txt`
- `dependabot CLI`

**Examples:**
- trivy fs --scanners vuln,secret .
- osv-scanner scan -r .
- safety check -r requirements.txt