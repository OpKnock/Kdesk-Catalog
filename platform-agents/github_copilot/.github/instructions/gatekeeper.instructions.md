---
applyTo: "**/*.go **/*.r **/*.sh **/*.{yaml,yml}"
---

# gatekeeper

Enforces OPA-based admission policies in Kubernetes with Gatekeeper ConstraintTemplates and Constraints.

## Instructions

# Gatekeeper

Admission policy enforcement for Kubernetes with OPA ConstraintTemplates.

## What This Skill Does

- Installs Gatekeeper as a validating admission webhook
- Authors ConstraintTemplates using Rego
- Instantiates Constraints to enforce policies per label or namespace
- Audits violations and enforces them in dry-run or deny mode

## When to Use

- Enforcing labels, limits, or security contexts cluster-wide
- Requiring certain policies for namespace-scoped workloads
- Auditing existing workloads for violations before enabling enforcement

## Real Commands

```bash
# Install and verify
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
kubectl get pods -n gatekeeper-system
kubectl get validatingwebhookconfigurations gatekeeper-validating-webhook-configuration

# Manage constraints
kubectl get constrainttemplates
kubectl get constraints
kubectl apply -f template.yaml
kubectl apply -f constraint.yaml
kubectl describe k8srequiredlabels

# Audit violations
kubectl get k8srequiredlabels k8srequiredlabels --output=yaml | grep -A5 violations
```

## Sample ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names: { kind: K8sRequiredLabels }
      validation:
        openAPIV3Schema:
          properties:
            labels: { type: array, items: { type: string } }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing labels: %v", [missing])
        }
```

## Best Practices

- Ship templates with audit-only constraints first, then flip to deny
- Version templates like code and review Rego carefully
- Use parameters to keep one template for many constraints
- Watch the webhook audit results before enforcing on namespaces
- Combine with Gatekeeper's built-in mutation for default labels

## Capabilities

### gatekeeper-install
Install Gatekeeper and check its operational status.

**Commands:**
- `kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml`
- `kubectl get pods -n gatekeeper-system`
- `kubectl get validatingwebhookconfigurations gatekeeper-validating-webhook-configuration`
- `helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper`

**Examples:**
- kubectl apply -f gatekeeper.yaml
- kubectl get pods -n gatekeeper-system
- kubectl logs -n gatekeeper-system deploy/gatekeeper-controller-manager --tail=50

### constraint-management
Create, list, and debug ConstraintTemplates and Constraints.

**Commands:**
- `kubectl get constrainttemplates`
- `kubectl get constraints`
- `kubectl apply -f template.yaml`
- `kubectl apply -f constraint.yaml`
- `kubectl describe k8srequiredlabels`

**Examples:**
- kubectl get constrainttemplates
- kubectl get k8srequiredlabels
- kubectl describe k8srequiredlabels
