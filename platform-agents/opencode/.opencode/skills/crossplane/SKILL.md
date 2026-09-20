---
name: "crossplane"
description: "Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation. Use when working with provider and config, composites and claims, devops or when the user mentions provider and config, composites and claims, devops."
---

Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm install crossplane crossplane-stable/crossplane -n cros`, `kubectl apply -f xrd.yaml`
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
