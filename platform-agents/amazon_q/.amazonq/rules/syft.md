Generate SBOMs from images, directories, and binaries. Emit SBOMs in standardized formats. and syft formats.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `syft alpine:latest`, `syft alpine:latest -o spdx-json > sbom.spdx.json`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Syft

Generate SBOMs from images, filesystems, and binaries.

## What This Skill Does

- Catalogs packages, languages, and licenses from many sources
- Emits SPDX, CycloneDX, and syft JSON formats
- Scopes image scans to squashed or all layers
- Attests SBOMs with cosign for supply-chain integrity

## When to Use

- Generating SBOMs for compliance and vulnerability matching
- Shipping SBOMs alongside releases
- Feeding grype or other scanners with an offline SBOM

## Real Commands

```bash
# Basic SBOMs
syft alpine:latest
syft .
syft /usr/local/bin/app

# Standardized output
syft alpine:latest -o spdx-json > sbom.spdx.json
syft alpine:latest -o cyclonedx-json > sbom.cdx.json

# All-layer scanning
syft nginx:latest --scope all-layers

# Exclusions
syft . --exclude './vendor/**'

# Attested SBOM
syft attest --key cosign.key alpine:latest -o cyclonedx-json
```

## Best Practices

- Generate at build time and store with the artifact
- Prefer CycloneDX or SPDX for interoperability
- Use --scope all-layers for runtime-relevant findings
- Feed the SBOM to grype for vuln matching and re-scan later
- Attest SBOMs so consumers can verify authenticity

## Capabilities

### sbom-generation
Generate SBOMs from images, directories, and binaries.

**Parameters:**
- `target` (string): Image, directory, archive, or binary to catalog
- `scope` (string): Squashed or all-layers for images
- `exclude` (array): Glob patterns to exclude

**Commands:**
- `syft alpine:latest`
- `syft .`
- `syft --scope all-layers nginx:latest`
- `syft /usr/local/bin/app`
- `syft docker-archive:myimage.tar`

**Examples:**
- syft alpine:latest -o cyclonedx-json
- syft . --exclude './vendor/**'
- syft nginx:latest --scope all-layers

### sbom-output
Emit SBOMs in standardized formats.

**Parameters:**
- `format` (string): Output format: spdx-json, cyclonedx-json, syft-json, table
- `output` (string): Output file path

**Commands:**
- `syft alpine:latest -o spdx-json > sbom.spdx.json`
- `syft alpine:latest -o cyclonedx-json > sbom.cdx.json`
- `syft alpine:latest -o syft-json > sbom.syft.json`
- `syft attest --key cosign.key alpine:latest -o cyclonedx-json`

**Examples:**
- syft alpine:latest -o spdx-json > sbom.spdx.json
- syft alpine:latest -o cyclonedx-json > sbom.cdx.json
- syft attest --key cosign.key alpine:latest

## References
- [Syft GitHub](https://github.com/anchore/syft)
- [SPDX Specification](https://spdx.dev/specifications/)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)