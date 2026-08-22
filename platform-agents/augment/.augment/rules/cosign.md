---
type: agent_requested
description: "Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance."
---

# cosign

Generate key pairs, sign images, and verify signatures against keys or keyless providers. Attach and verify SLSA provenance and custom attestations. provenance.

## Instructions

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

**Commands:**
- `cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest`
- `cosign verify-attestation --key cosign.pub ghcr.io/org/app:latest`
- `cosign verify-attestation --type slsaprovenance --key cosign.pub ghcr.io/org/app:latest`
- `cosign attest-blob --key cosign.key --type custom attest.txt`

**Examples:**
- cosign attest --key cosign.key --type slsaprovenance --predicate provenance.json ghcr.io/org/app:latest
- cosign verify-attestation --type slsaprovenance --key cosign.pub ghcr.io/org/app:latest