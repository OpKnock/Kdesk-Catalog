---
trigger: glob
description: "Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance. Use when working with image signing, attestations, security or when the user mentions image signing, attestations, security."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cosign generate-key-pair`, `cosign attest --key cosign.key --type slsaprovenance --predi`
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
