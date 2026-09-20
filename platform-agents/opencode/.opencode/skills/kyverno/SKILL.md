---
name: "kyverno"
description: "Kyverno Kubernetes policy engine. Real kyverno CLI. Use when working with kyverno, security or when the user mentions kyverno, security."
---

Kyverno Kubernetes policy engine. Real kyverno CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `brew install kyverno-cli`
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

# Kyverno

Kyverno Kubernetes policy engine using real CLI.

## When to Use

- Kubernetes policies
- Admission control
- Policy enforcement
- Generate resources

## Commands

```bash
# Install
brew install kyverno-cli  # macOS
helm install kyverno kyverno/kyverno -n kyverno --create-namespace

# Apply policy
kyverno apply policy.yaml -r resource.yaml

# Test policy
kyverno test policy.yaml

# Validate
kyverno validate policy.yaml

# Generate
kyverno generate policy.yaml -r resource.yaml

# List policies
kubectl get clusterpolicies

# Check violations
kubectl get policyreport
```

## Policy Types

```yaml
# Validate
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: enforce
  rules:
    - name: check-for-labels
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Labels are required"
        pattern:
          metadata:
            labels:
              app: "?*"

# Mutate
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-labels
spec:
  rules:
    - name: add-app-label
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              app: "{{request.object.metadata.name}}"

# Generate
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-networkpolicy
spec:
  rules:
    - name: generate-networkpolicy
      match:
        any:
          - resources:
              kinds:
                - Namespace
      generate:
        kind: NetworkPolicy
        name: default-deny
        namespace: "{{request.object.metadata.name}}"
        data:
          spec:
            podSelector: {}
            policyTypes:
              - Ingress
              - Egress
```

## Testing

```bash
# Test policy
kyverno test policy.yaml

# Test file
cat > test.yaml <<EOF
- name: test-policy
  policy: policy.yaml
  resources:
    - name: pod-with-labels
      kind: Pod
      apiVersion: v1
      data:
        metadata:
          labels:
            app: test
  result: pass
EOF

# Run tests
kyverno test test.yaml
```

## Examples

```bash
# Apply policy
kyverno apply policy.yaml -r resource.yaml

# Test policy
kyverno test policy.yaml

# Validate
kyverno validate policy.yaml
```

## CI/CD

```yaml
# GitHub Actions
- name: Apply policies
  run: |
    kyverno apply policy.yaml -r resource.yaml

# GitLab CI
policy:
  stage: security
  script:
    - kyverno apply policy.yaml -r resource.yaml
```

## Capabilities

### kyverno
Kyverno Kubernetes policy engine. Real kyverno CLI.

**Commands:**
- `brew install kyverno-cli`
- `helm install kyverno kyverno/kyverno -n kyverno --create-namespace`
- `kyverno apply policy.yaml -r resource.yaml`
- `kyverno test policy.yaml`
- `kyverno validate policy.yaml`
- `kyverno generate policy.yaml -r resource.yaml`
- `kubectl get clusterpolicies`
- `kubectl get policyreport`
- `kyverno test policy.yaml`
- `cat > test.yaml <<EOF`
- `- name: test-policy`
- `policy: policy.yaml`
- `resources:`
- `- name: pod-with-labels`
- `kind: Pod`
- `apiVersion: v1`
- `data:`
- `metadata:`
- `labels:`
- `app: test`
- `result: pass`
- `EOF`
- `kyverno test test.yaml`
- `kyverno apply policy.yaml -r resource.yaml`
- `kyverno test policy.yaml`
- `kyverno validate policy.yaml`

**Examples:**
- brew install kyverno-cli
- helm install kyverno kyverno/kyverno -n kyverno --create-namespace
- kyverno apply policy.yaml -r resource.yaml

## References
- [kyverno Skill Documentation](skills/security/kyverno.md)
