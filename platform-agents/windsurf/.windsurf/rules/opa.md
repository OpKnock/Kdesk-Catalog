---
trigger: glob
description: "Evaluate Rego queries against data and inputs. Run Rego unit tests, format code, and build bundles. Serve policies over HTTP handling live decisions. workflows.'"
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

# opa

Evaluate Rego queries against data and inputs. Run Rego unit tests, format code, and build bundles. Serve policies over HTTP handling live decisions. workflows.'

## Instructions

# OPA

Policy-as-code with the Open Policy Agent and Rego.

## What This Skill Does

- Evaluates Rego queries against JSON data and inputs
- Writes and runs unit tests for policies
- Formats and validates Rego with canonical style
- Builds deployable bundles and serves decisions over HTTP

## When to Use

- Authorization decisions for APIs or infrastructure
- Validating configs before deployment
- Building policy bundles for Gatekeeper, Envoy, or custom agents

## Real Commands

```bash
# Evaluate
opa eval -i input.json -d policy.rego 'data.example.allow'
opa eval --format raw -d policy.rego 'data.example.msg'

# Test
opa test -v ./policies
opa test policy_test.rego policy.rego

# Format and validate
opa fmt -w policies/
opa fmt --diff policy.rego
opa check policy.rego

# Build and serve
opa build -b policies/ -o bundle.tar.gz
opa run -s -w -b bundle.tar.gz
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"input": {"user": "alice", "action": "read"}}' \
  http://localhost:8181/v1/data/example/allow
```

## Sample Policy

```rego
package example

import rego.v1

default allow := false

allow if {
  input.action == "read"
  input.user in data.authorized_users
}
```

## Best Practices

- Format with opa fmt before merging
- Cover every rule with test_* cases and run opa test in CI
- Keep bundles small; watch mode for local dev only
- Version bundles and pin hashes at deploy time
- Use data-driven configs rather than many hardcoded rules

## Capabilities

### policy-evaluation
Evaluate Rego queries against data and inputs.

**Commands:**
- `opa eval 'data.policies.allow'`
- `opa eval -i input.json -d policies.rego 'data.example.allow'`
- `opa eval --format pretty 'data.servers[i].id' -d example.rego`
- `opa eval -b bundle.tar.gz 'data.main.allow'`

**Examples:**
- opa eval -i input.json -d policy.rego 'data.example.allow'
- opa eval --format raw 'data.example.msg' -d policy.rego
- opa eval 'x := 5; y := x * 2'

### testing-and-linting
Run Rego unit tests, format code, and build bundles.

**Commands:**
- `opa test policy_test.rego policy.rego`
- `opa test -v ./policies`
- `opa fmt -w policy.rego`
- `opa fmt --diff policy.rego`
- `opa check policy.rego`
- `opa build -b policies/ -o bundle.tar.gz`

**Examples:**
- opa test -v ./policies
- opa fmt -w policies/
- opa build -b policies/ -o bundle.tar.gz

### server-mode
Serve policies over HTTP for live decisions.

**Commands:**
- `opa run --server`
- `opa run -s -w -b bundle.tar.gz`
- `curl -s -X POST -H 'Content-Type: application/json' -d '{"input": {"user": "alice"}}' http://localhost:8181/v1/data/example/allow`
- `opa run --server --addr 127.0.0.1:9191`

**Examples:**
- opa run -s -w -b bundle.tar.gz
- curl -s -X POST http://localhost:8181/v1/data/example/allow -d '{"input":{}}'
- opa run --server --addr 127.0.0.1:9191
