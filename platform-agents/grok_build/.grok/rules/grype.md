# grype

Scan images, directories, and binaries handling known CVEs. Update the vulnerability database and scan SBOMs directly. and filesystem scanning.

## Instructions

# Grype

Vulnerability scanning powered by syft SBOMs.

## What This Skill Does

- Scans container images, filesystems, and single binaries
- Matches packages against multiple vulnerability databases
- Filters by fixability, severity, and CVE
- Works from existing SBOMs for offline or supply-chain pipelines

## When to Use

- Checking an image before deploy
- Generating a report of fixable vulnerabilities in a repo
- Re-scanning a previously generated SBOM

## Real Commands

```bash
# Scan an image
grype alpine:latest
grype --only-fixed --fail-on high myapp:latest

# Scan a project directory
grype .
grype . --exclude './vendor/**'

# All layers (catches deleted package files)
grype myapp:latest --scope all-layers

# SBOM round-trip
syft myapp:latest -o json > sbom.json
grype -q sbom:sbom.json

# Database management
grype db update
grype db status
```

## Best Practices

- Refresh the DB in CI (grype db update) or pin a DB image
- Use --only-fixed to prioritize actionable findings
- Set --fail-on high for deploy gates
- Scan the SBOM at build time and re-scan at deploy time
- Combine with syft attestation (syft attest) for signed SBOMs

## Capabilities

### vulnerability-matching
Scan images, directories, and binaries for known CVEs.

**Commands:**
- `grype alpine:latest`
- `grype .`
- `grype image:latest --scope all-layers`
- `grype --only-fixed alpine:latest`
- `grype -o table --by-cve alpine:latest`

**Examples:**
- grype myapp:latest
- grype --only-fixed myapp:latest
- grype . --exclude './vendor/**'

### db-and-sbom
Update the vulnerability database and scan SBOMs directly.

**Commands:**
- `grype db update`
- `grype db status`
- `grype -q sbom:sbom.json`
- `syft alpine:latest -o json > sbom.json`
- `grype --v 5 myapp:latest`

**Examples:**
- grype db update
- syft alpine:latest -o cyclonedx > sbom.cdx.json
- grype -q sbom:sbom.cdx.json