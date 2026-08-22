---
name: "consul-config"
description: "Manage API configuration and service discovery with HashiCorp Consul: KV store, watches, and env-consul templates."
type: knowledge
triggers: ["consul-config", "kv-store", "consul-template"]
---

# Consul Config

Manage API configuration and service discovery with HashiCorp Consul: KV store, watches, and env-consul templates.

## Instructions

# Consul Config

Manage API configuration centrally with Consul KV and templates.

## When to Use

- Central config that changes without redeploys
- Feature flags and per-datacenter overrides
- Service discovery combined with config

## Start Consul

```bash
consul agent -dev
```

## KV Operations

```bash
consul kv put config/api/port 8080
consul kv get config/api/port
consul kv list config/
consul kv get -recurse config/api
consul kv delete config/api/port
```

## Template

```
{"port": {{ key "config/api/port" }}, "retries": {{ keyOrDefault "config/api/feature-flags/retries" "3" }}}
```

```bash
consul-template -template "config.ctmpl:config.json" -once
consul-template -template "config.ctmpl:config.json:reload.sh"
```

## Watches

```bash
consul watch -type keyprefix -prefix config/api env
```

## Service Discovery

```bash
consul members
consul catalog services
curl http://localhost:8500/v1/kv/config/api/port
```

## Testing

```bash
consul kv put config/api/port 9090
# consul-template re-renders and optionally reloads the app
consul-template -template "config.ctmpl:config.json:reload.sh"
```

## Best Practices

- Use keyOrDefault in templates for resilient config
- Namespace keys by service: config/<service>/<key>
- Version config with K/V indexes and CAS
- Use watches or consul-template for hot reloads
- Back up KV with consul kv export
- Never store secrets in KV; use Vault
- Add ACLs in production clusters

## Capabilities

### kv-store
Read, write, list, and delete configuration keys in Consul KV

**Commands:**
- `consul kv put config/api/port 8080`
- `consul kv get config/api/port`
- `consul kv list config/`
- `consul kv delete config/api/port`

**Examples:**
- consul kv put config/api/feature-flags/retries 3
- consul kv get -recurse config/api
- consul kv put -flags=0 config/api/deploy "blue"

### consul-template
Render config files from Consul KV with consul-template

**Commands:**
- `consul-template -template "config.ctmpl:config.json" -once`
- `consul-template -template "config.ctmpl:config.json:reload.sh"`
- `consul watch -type keyprefix -prefix config/api env`
- `consul members`

**Examples:**
- consul-template -template "config.ctmpl:config.json" -once
- consul watch -type keyprefix -prefix config/api env
- consul members -detailed
