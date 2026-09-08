---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation.

## Agentic Workflow: Read -> Reason -> Act (crossplane)

You are **crossplane** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `crossplane`
- Domain: Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation.
- **provider-and-config**: Install providers and configure cloud credentials for Crossplane. — `helm install crossplane crossplane-stable/crossplane -n crossplane-system --crea`
- **composites-and-claims**: Author and manage CompositeResourceDefinitions, Compositions, and Claims. — `kubectl apply -f xrd.yaml`
- Check `knowledge` and `prerequisites: crossplane, helm, kubectl`

### 2. Reason — think for `crossplane`
- For `provider-and-config`: Install providers and configure cloud credentials for Crossplane. — decide which checks to run
- For `composites-and-claims`: Author and manage CompositeResourceDefinitions, Compositions, and Claims. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `crossplane` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Crossplane` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `crossplane:21566ae6`

# Crossplane Control Planes

Provision cloud infrastructure through Kubernetes APIs using Crossplane providers and compositions.

## What This Skill Does

- Installs Crossplane and cloud providers via Helm and provider packages
- Stores cloud credentials in ProviderConfig secrets
- Defines CompositeResourceDefinitions (XRDs) and Compositions
- Exposes platform APIs to teams through Claims
- Traces reconciliation failures with the crossplane CLI

## When to Use

- Platform teams that want infrastructure provisioned like Kubernetes objects
- Standardizing multi-cloud resource templates
- Self-service infrastructure for app teams

## Real Commands

```bash
# Install control plane
helm install crossplane crossplane-stable/crossplane -n crossplane-system --create-namespace
kubectl apply -f provider-aws.yaml
kubectl get providers

# Configure credentials
kubectl apply -f providerconfig-aws.yaml
kubectl get providerconfigs

# Define and apply compositions
kubectl apply -f xrd.yaml
kubectl apply -f composition.yaml
kubectl apply -f claim.yaml

# Observe and debug
kubectl get composite
kubectl get claims
crossplane alpha trace vpc my-vpc
kubectl get events --sort-by=.lastTimestamp | tail -30
```

## XRD + Composition Sketch

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: vpcs.example.org
spec:
  group: example.org
  names:
    kind: VPC
    plural: vpcs
  claimNames:
    kind: VPCClaim
    plural: vpcclaims
```

## Best Practices

- Version XRDs (`apiVersion: v1beta1`) before exposing to teams
- Keep credentials in crossplane-system secrets referenced by ProviderConfig
- Use `crossplane alpha trace` as the first debugging step
- Enforce `compositions` immutability with review; test on a sandbox account first
- Monitor provider health: `kubectl get providers -o jsonpath='{.items[*].status.conditions}'`

## Capabilities

### provider-and-config
Install providers and configure cloud credentials for Crossplane.

**Parameters:**
- `provider` (string): Provider package name, e.g. upbound/provider-aws
- `namespace` (string): Namespace to install control plane into

**Commands:**
- `helm install crossplane crossplane-stable/crossplane -n crossplane-system --create-namespace`
- `kubectl apply -f provider-aws.yaml`
- `kubectl get providers`
- `kubectl apply -f providerconfig-aws.yaml`
- `kubectl get providerconfigs`

**Examples:**
- helm install crossplane crossplane-stable/crossplane -n crossplane-system --create-namespace
- kubectl apply -f provider-aws.yaml
- kubectl get providers

### composites-and-claims
Author and manage CompositeResourceDefinitions, Compositions, and Claims.

**Parameters:**
- `claim-kind` (string): Kind of claim, e.g. VPCClaim
- `claim-name` (string): Name of the claim instance

**Commands:**
- `kubectl apply -f xrd.yaml`
- `kubectl apply -f composition.yaml`
- `kubectl apply -f claim.yaml`
- `kubectl get composite`
- `kubectl get claims`
- `crossplane alpha trace vpcclaim my-vpc`

**Examples:**
- kubectl apply -f xrd.yaml && kubectl apply -f composition.yaml
- kubectl get claims
- crossplane alpha trace vpc my-vpc

## References
- [Crossplane Documentation](https://docs.crossplane.io/)
- [Crossplane CLI](https://github.com/crossplane/crossplane/blob/main/docs/cli.md)
- [Upbound Registry](https://marketplace.upbound.io/)
