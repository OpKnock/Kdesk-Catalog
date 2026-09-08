---
name: "supply-chain-security-supply-chain-security"
description: "Secures the software supply chain with dependency auditing, SBOM generation, signing, and provenance verification across ecosystems. Use when working with dependency auditing, sbom and signing, vuln scanning or when the user mentions dependency auditing, sbom and signing, vuln scanning."
type: knowledge
triggers: ["supply-chain-security-supply-chain-security", "dependency-auditing", "sbom-and-signing", "vuln-scanning"]
---

Secures the software supply chain with dependency auditing, SBOM generation, signing, and provenance verification across ecosystems.

## Agentic Workflow: Read -> Reason -> Act (supply-chain-security-supply-chain-security)

You are **supply-chain-security-supply-chain-security** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `supply-chain-security-supply-chain-security`
- Domain: Secures the software supply chain with dependency auditing, SBOM generation, signing, and provenance verification across ecosystems.
- **dependency-auditing**: Audit dependencies across package ecosystems. — `npm audit --json`
- **sbom-and-signing**: Generate SBOMs and sign artifacts for provenance. — `syft . -o cyclonedx-json > sbom.cdx.json`
- **vuln-scanning**: Scan repos and dependencies for known vulnerabilities. — `trivy fs --scanners vuln,secret,config .`
- Check `knowledge` and `prerequisites: syft, grype, cosign, sigstore`

### 2. Reason — think for `supply-chain-security-supply-chain-security`
- For `dependency-auditing`: Audit dependencies across package ecosystems. — decide which checks to run
- For `sbom-and-signing`: Generate SBOMs and sign artifacts for provenance. — decide which checks to run
- For `vuln-scanning`: Scan repos and dependencies for known vulnerabilities. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `supply-chain-security-supply-chain-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Pip-audit` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `supply-chain-security-supply-chain-security:65a04884`

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

**Parameters:**
- `ecosystem` (string): Ecosystem: npm, pip, go, cargo, maven
- `auditLevel` (string): Minimum severity for npm audit exit code

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

**Parameters:**
- `image` (string): Image reference to sign
- `sbomFormat` (string): SBOM format: cyclonedx, spdx

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

**Parameters:**
- `recursive` (boolean): Scan recursively (osv-scanner -r)
- `scanner` (string): Trivy scanners to enable: vuln, secret, config, license.

**Commands:**
- `trivy fs --scanners vuln,secret,config .`
- `osv-scanner scan -r .`
- `safety check -r requirements.txt`
- `dependabot CLI`

**Examples:**
- trivy fs --scanners vuln,secret .
- osv-scanner scan -r .
- safety check -r requirements.txt

## References
- [SLSA Framework](https://slsa.dev/)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [OSV Scanner](https://google.github.io/osv-scanner/)
