---
type: agent_requested
description: "Feature flag management: launch, evaluate, and retire flags with LaunchDarkly, toggling features by environment and user segments."
---

# Feature Flags

Feature flag management: launch, evaluate, and retire flags with LaunchDarkly, toggling features by environment and user segments.

## Instructions

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