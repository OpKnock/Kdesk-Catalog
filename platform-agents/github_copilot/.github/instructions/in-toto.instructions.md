---
applyTo: "**/*.go **/*.py **/*.r **/*.sh"
---

# in-toto

Creates and verifies supply-chain integrity layouts with in-toto: step signatures, product attestation, and full-chain verification.

## Instructions

# in-toto

Supply chain integrity with cryptographically linked build steps.

## What This Skill Does

- Defines a layout of supply chain steps (clone, build, test, release)
- Records per-step product metadata signed by step owners
- Verifies the full chain: signatures, artifact hashes, and material rules
- Generates keys with in-toto-keygen and signs layouts

## When to Use

- Provenance requirements for regulated software deliveries
- Verifying that build/test/release steps ran in the intended order
- Multi-party supply chain audits

## Real Commands

```bash
# Key generation
in-toto-keygen alice

# Record steps
in-toto-run --step-name build --key build.key --products dist/ -- make build
in-toto-run --step-name test --key test.key --materials dist/ -- pytest

# Split-step recording for long steps
in-toto-record start --step-name deploy --key deploy.key
in-toto-record stop --step-name deploy --key deploy.key --products release.tgz

# Sign and verify
in-toto-sign --file root.layout --key root.key
in-toto-verify --layout root.layout --layout-keys root.pub
```

## Sample Layout (excerpt)

```python
layout = Layout(
    steps=[
        Step(name="build",
             materials=[ArtifactRule("ALLOW", "**")],
             products=[ArtifactRule("CREATE", "dist/*")],
             pubkeys=[build_pubkey])
    ],
    keys={"build": build_pubkey}
)
```

## Best Practices

- Keep step keys separate from layout root keys
- Verify in the production environment, not just in CI
- Store in-toto metadata alongside release artifacts
- Combine with SLSA provenance and cosign attestations for full coverage
- Rotate step keys and re-sign layouts on personnel changes

## Capabilities

### step-execution
Record supply chain steps with in-toto-run and in-toto-record wrappers.

**Commands:**
- `in-toto-run --step-name build --key build.key --products artifacts/ -- make build`
- `in-toto-record start --step-name test --key test.key`
- `in-toto-record stop --step-name test --key test.key --products report.xml`
- `in-toto-run --step-name lint --key lint.key --exclude coverage/ -- golangci-lint run`

**Examples:**
- in-toto-run --step-name build --key build.key --products dist/ -- npm run build
- in-toto-record start --step-name test --key test.key
- in-toto-record stop --step-name test --key test.key --products junit.xml

### layout-verification
Sign layouts and verify the whole chain against keys and rules.

**Commands:**
- `in-toto-keygen alice`
- `in-toto-sign --file root.layout --key root.key`
- `in-toto-verify --layout root.layout --layout-keys root.pub`
- `in-toto-verify --layout root.layout --layout-keys root.pub --verbose`
- `in-toto-sign --file root.layout --key alice --update`

**Examples:**
- in-toto-keygen alice
- in-toto-sign --file root.layout --key root.key
- in-toto-verify --layout root.layout --layout-keys root.pub
