---
name: "syft"
description: "Generate SBOMs from images, directories, and binaries. Emit SBOMs in standardized formats. and syft formats. Use when working with sbom generation, sbom output, security or when the user mentions sbom generation, sbom output, security."
license: "MIT"
compatibility: "Requires syft."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(syft:*)"
---

Generate SBOMs from images, directories, and binaries. Emit SBOMs in standardized formats. and syft formats.

## Agentic Workflow: Read -> Reason -> Act (syft)

You are **syft** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `syft`
- Domain: Generate SBOMs from images, directories, and binaries. Emit SBOMs in standardized formats. and syft formats.
- **sbom-generation**: Generate SBOMs from images, directories, and binaries. — `syft alpine:latest`
- **sbom-output**: Emit SBOMs in standardized formats. — `syft alpine:latest -o spdx-json > sbom.spdx.json`
- Check `knowledge` and `prerequisites: syft`

### 2. Reason — think for `syft`
- For `sbom-generation`: Generate SBOMs from images, directories, and binaries. — decide which checks to run
- For `sbom-output`: Emit SBOMs in standardized formats. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `syft` tools
- Tools: `Glob`, `Grep`, `Read`, `Syft` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `syft:b296be62`

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
