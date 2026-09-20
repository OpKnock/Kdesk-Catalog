---
name: "crossplane"
description: "Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# crossplane

Builds control planes with Crossplane: install providers, create composite resources (XRs), manage resource claims, and trace reconciliation.

## Instructions

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