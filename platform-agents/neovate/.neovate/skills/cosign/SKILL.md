---
name: "cosign"
description: "Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance. Use when working with image signing, attestations, security or when the user mentions image signing, attestations, security."
license: "MIT"
compatibility: "Requires cosign."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(cosign:*)"
---

Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance.

## Agentic Workflow: Read -> Reason -> Act (cosign)

You are **cosign** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `cosign`
- Domain: Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance.
- **image-signing**: Generate key pairs, sign images, and verify signatures against keys or keyless providers. — `cosign generate-key-pair`
- **attestations**: Attach and verify SLSA provenance and custom attestations. — `cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json`
- Check `knowledge` and `prerequisites: cosign`

### 2. Reason — think for `cosign`
- For `image-signing`: Generate key pairs, sign images, and verify signatures against keys or keyless providers. — decide which checks to run
- For `attestations`: Attach and verify SLSA provenance and custom attestations. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cosign` tools
- Tools: `Glob`, `Grep`, `Read`, `Cosign` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cosign:ab2e2ca1`

# cosign

Sign and verify container images and blobs for software supply chain integrity.

## What This Skill Does

- Generates and manages cosign key pairs
- Signs OCI images with key-based or keyless (OIDC) flows
- Verifies signatures, certificates, and transparency log entries
- Attaches and verifies SLSA provenance and SBOM attestations
- Inspects where signatures are stored with triangulate

## When to Use

- Images must be verifiable before deployment in production
- SBOMs and provenance need tamper-evident attestation
- A verification policy is required in CI/CD

## Real Commands

```bash
# Key-based signing
cosign generate-key-pair
cosign sign --key cosign.key ghcr.io/org/app:latest
cosign verify --key cosign.pub ghcr.io/org/app:latest

# Keyless signing (defaults to OIDC + Fulcio)
cosign sign ghcr.io/org/app:latest
cosign verify ghcr.io/org/app:latest

# Attestations
cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest
cosign verify-attestation --type slsaprovenance --key cosign.pub ghcr.io/org/app:latest

# Blob signing
cosign sign-blob --key cosign.key artifact.txt
cosign verify-blob --key cosign.pub --signature artifact.txt.sig artifact.txt

# Find where the signature lives
cosign triangulate ghcr.io/org/app:latest
```

## Best Practices

- Store the private key offline or in KMS (--key gcpkms:// / azurekms://)
- Enable transparency log upload by default; disable only for private registries
- Sign the SBOM and provenance, then verify at deploy time
- Rotate keys periodically and re-sign released tags if required
- Verify in production with a policy engine (Kyverno/Sigstore policy controller)

## Capabilities

### image-signing
Generate key pairs, sign images, and verify signatures against keys or keyless providers.

**Parameters:**
- `image` (string): Container image reference to sign or verify
- `key` (string): Path to the signing private key or public key
- `tlogUpload` (boolean): Whether to upload to the transparency log

**Commands:**
- `cosign generate-key-pair`
- `cosign sign --key cosign.key ghcr.io/org/app:latest`
- `cosign verify --key cosign.pub ghcr.io/org/app:latest`
- `cosign sign --key cosign.key --tlog-upload=false ghcr.io/org/app:latest`
- `cosign triangulate ghcr.io/org/app:latest`

**Examples:**
- cosign generate-key-pair
- cosign sign --key cosign.key ghcr.io/org/app:latest
- cosign verify --key cosign.pub ghcr.io/org/app:latest

### attestations
Attach and verify SLSA provenance and custom attestations.

**Parameters:**
- `type` (string): Attestation type: slsaprovenance, spdx, custom
- `predicate` (string): Path to the JSON predicate file

**Commands:**
- `cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest`
- `cosign verify-attestation --key cosign.pub ghcr.io/org/app:latest`
- `cosign verify-attestation --type slsaprovenance --key cosign.pub ghcr.io/org/app:latest`
- `cosign attest-blob --key cosign.key --type custom attest.txt`

**Examples:**
- cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest
- cosign verify-attestation --type slsaprovenance --key cosign.pub ghcr.io/org/app:latest

## References
- [cosign Documentation](https://docs.sigstore.dev/cosign/)
- [Sigstore Overview](https://docs.sigstore.dev/)
