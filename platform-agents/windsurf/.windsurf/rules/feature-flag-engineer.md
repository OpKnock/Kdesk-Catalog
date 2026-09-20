---
trigger: glob
description: "Designs, ships, and retires feature flags across LaunchDarkly, Flipt, and Flagsmith, including kill switches, gradual rollouts, and flag lifecycle automation."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# feature-flag-engineer

Designs, ships, and retires feature flags across LaunchDarkly, Flipt, and Flagsmith, including kill switches, gradual rollouts, and flag lifecycle automation.

## Instructions

# Feature Flag Engineering

Manage feature flags across major vendors with real CLIs and safe rollouts.

## When to Use

- Adding a kill switch or dark launch
- Gradual percentage rollouts of new features
- Trunk-based development with short-lived flags
- Removing a flag after the rollout completes

## LaunchDarkly (ldcli)

```bash
ldcli config --access-token $LD_ACCESS_TOKEN
ldcli feature-flags list --project-key webapp --environment-key production
ldcli feature-flags create --project-key webapp --key dark-mode --name 'Dark Mode'
ldcli feature-flags update --project-key webapp --key dark-mode --env-key staging --on true
ldcli feature-flags delete --project-key webapp --key dark-mode
```

Always scope access tokens with least-privilege roles and rotate them via CI secrets.

## Flipt (self-hosted)

```bash
flipt serve --config /etc/flipt/config.yml
flipt eval --flag-key checkout-v2 --entity-key user-1 --context '{"beta":true}'
flipt import --input features.json
flipt export --namespace production > backup-flags.json
```

Flipt is a good choice when flags must run inside your own VPC with audit logging.

## Rollout strategy

1. Release with flag OFF for 24h to observe baseline telemetry.
2. Ramp 5% -> 25% -> 100% using percentage rollouts, watching error budgets.
3. Before removing a flag, confirm the dead code path is unreachable for 2 weeks.
4. Delete the flag and remove SDK references in the same release.

## Best practices

- Prefix flag keys with the team: `checkout/v2-cart`.
- Every flag gets an owner and an expiry date.
- Wire flags through typed accessors, never raw string lookups.
- Include flag evaluations in your metrics dashboard for every release.

## Testing

```bash
curl -s "https://app.launchdarkly.com/api/v2/flags/webapp" -H "Authorization: $LD_TOKEN" | jq '.items[] | {key, variations}'
```

Verify kill-switch behavior under production-like traffic before every launch window.

## Capabilities

### launchdarkly
Manage LaunchDarkly feature flags, environments, and segments via ldcli.

**Commands:**
- `ldcli config --access-token $LD_ACCESS_TOKEN`
- `ldcli feature-flags list --project-key my-project --environment-key production`
- `ldcli feature-flags create --project-key my-project --key dark-mode --name 'Dark Mode' --description 'Toggle dark theme'`
- `ldcli feature-flags update --project-key my-project --key dark-mode --env-key production --on true`
- `ldcli feature-flags delete --project-key my-project --key dark-mode`

**Examples:**
- ldcli feature-flags list --project-key webapp --environment-key production | jq -r '.[].key'
- ldcli feature-flags update --project-key webapp --key checkout-v2 --env-key staging --on false
- ldcli feature-flags create --project-key webapp --key kill-flag --name 'Kill switch' --variations true false

### flipt
Manage self-hosted Flipt feature flags and experiments.

**Commands:**
- `flipt config --output /etc/flipt/config.yml`
- `flipt import --input features.json`
- `flipt export --output features.yaml`
- `flipt eval --flag-key dark-mode --entity-key user-123 --context '{"plan":"premium"}'`
- `flipt serve --config /etc/flipt/config.yml`

**Examples:**
- flipt eval --flag-key checkout-v2 --entity-key user-1 --context '{"beta":true}'
- flipt import --input flags.yaml --namespace production
- flipt export --namespace production > backup-flags.json
