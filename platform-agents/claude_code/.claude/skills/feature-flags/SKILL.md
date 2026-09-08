---
name: "feature-flags"
description: "Feature flag management: launch, evaluate, and retire flags with LaunchDarkly, toggling features by environment and user segments. Use when working with flag ops, api or when the user mentions flag ops, api."
license: "MIT"
compatibility: "Requires grep, node. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Read Bash(curl:*) Grep Bash(node:*)"
---

Feature flag management: launch, evaluate, and retire flags with LaunchDarkly, toggling features by environment and user segments.

## Agentic Workflow: Read -> Reason -> Act (feature-flags)

You are **Feature Flags** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `feature-flags`
- Domain: Feature flag management: launch, evaluate, and retire flags with LaunchDarkly, toggling features by environment and user segments.
- **flag-ops**: Create and toggle flags in LaunchDarkly, evaluate via the SDK, and audit flag usage. — `curl -s -X POST https://api.launchdarkly.com/api/v2/flags/default -H 'Authorizat`
- Check `knowledge` and `prerequisites: grep, node`

### 2. Reason — think for `feature-flags`
- For `flag-ops`: Create and toggle flags in LaunchDarkly, evaluate via the SDK, and audit flag usage. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `feature-flags` tools
- Tools: `Glob`, `Read`, `Bash`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `feature-flags:6113d63b`

# Feature Flags

## What this skill does

Feature flags decouple deployment from release: code ships dark, and flags enable features per environment, percentage, or user segment. This skill covers LaunchDarkly flag lifecycle via the API and SDK.

## When to use

- Shipping a feature behind a kill switch
- Progressive rollouts (10% -> 50% -> 100%)
- Per-customer or per-plan feature gating

## Real commands

```bash
# Create a flag
curl -s -X POST https://api.launchdarkly.com/api/v2/flags/default -H 'Authorization: $LD_API_KEY' -H 'Content-Type: application/json' -d '{"name":"new-checkout","key":"new-checkout","variations":[{"value":false},{"value":true}]}' | jq '.key'

# Roll out to 10%
curl -s -X PATCH https://api.launchdarkly.com/api/v2/flags/default/new-checkout -H 'Authorization: $LD_API_KEY' -H 'Content-Type: application/json' -d '{"comment":"enable 10%","patch":[{"op":"replace","path":"/fallthrough/rollout","value":{"variations":[{"variation":0,"weight":90000},{"variation":1,"weight":10000}]}}]}' | jq '.key'

# Evaluate in Node
node -e "const {LDClient}=require('launchdarkly-node-server-sdk');const c=LDClient.init(process.env.LD_SDK_KEY);c.on('ready',()=>c.variation('new-checkout',{key:'user-1'},false).then(v=>{console.log('flag =',v);c.close()}))"

# Audit usage before removal
 grep -rn 'new-checkout' src/ | head -20
```

## Best practices

- Flags need a default in code (false) so SDK failure degrades safely.
- Add a permanent kill-switch flag for each new major code path.
- Remove flags within 2-4 weeks of full rollout; dead flags rot.
- Use environments to separate dev/prod toggle states.
- Never gate security-critical behavior behind a flag rollout.

## Testing

```bash
# Verify the flag toggles correctly per environment
curl -s https://app.launchdarkly.com/api/v2/flags/default/new-checkout -H 'Authorization: $LD_API_KEY' | jq '{key, on: .on}'
```

## Capabilities

### flag-ops
Create and toggle flags in LaunchDarkly, evaluate via the SDK, and audit flag usage.

**Parameters:**
- `flag-key` (string): Flag identifier used in code and API
- `percentage` (integer): Rollout percentage for the true variation
- `context-key` (string): User or context key for evaluation

**Commands:**
- `curl -s -X POST https://api.launchdarkly.com/api/v2/flags/default -H 'Authorization: $LD_API_KEY' -H 'Content-Type: application/json' -d '{"name":"new-checkout","key":"new-checkout","variations":[{"value":false},{"value":true}]}' | jq '.key'`
- `curl -s -X PATCH https://api.launchdarkly.com/api/v2/flags/default/new-checkout -H 'Authorization: $LD_API_KEY' -H 'Content-Type: application/json' -d '{"comment":"enable 10%","patch":[{"op":"replace","path":"/fallthrough/rollout","value":{"variations":[{"variation":0,"weight":90000},{"variation":1,"weight":10000}]}}]}' | jq '.key'`
- `node -e "const {LDClient}=require('launchdarkly-node-server-sdk');const c=LDClient.init(process.env.LD_SDK_KEY);c.on('ready',()=>c.variation('new-checkout',{key:'user-1'},false).then(v=>{console.log('flag =',v);c.close()}))"`
- `grep -rn 'new-checkout' src/ | head -20`
- `curl -s https://app.launchdarkly.com/api/v2/flags/default/new-checkout -H 'Authorization: $LD_API_KEY' | jq '{key, on: .on, targeting: .fallthrough.rollout}'`

**Examples:**
- curl -s -X PATCH https://api.launchdarkly.com/api/v2/flags/default/new-checkout -H 'Authorization: $LD_API_KEY' -H 'Content-Type: application/json' -d '{"comment":"enable 10%","patch":[{"op":"replace","path":"/fallthrough/rollout","value":{"variations":[{"variation":0,"weight":90000},{"variation":1,"weight":10000}]}}]}' | jq '.key'
- node -e "const {LDClient}=require('launchdarkly-node-server-sdk');const c=LDClient.init(process.env.LD_SDK_KEY);c.on('ready',()=>c.variation('new-checkout',{key:'user-1'},false).then(v=>{console.log('flag =',v);c.close()}))"
- grep -rn 'new-checkout' src/ | head -20

## References
- [LaunchDarkly REST API](https://apidocs.launchdarkly.com/)
- [LaunchDarkly Node SDK](https://docs.launchdarkly.com/sdk/server-side/node-js)
