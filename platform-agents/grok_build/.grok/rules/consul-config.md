Manage API configuration and service discovery with HashiCorp Consul: KV store, watches, and env-consul templates.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `consul kv put config/api/port 8080`, `consul-template -template "config.ctmpl:config.json" -once`
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

**Parameters:**
- `key` (string): KV key path such as config/api/port
- `value` (string): Value to store

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

**Parameters:**
- `template_file` (string): Go template path mapping such as config.ctmpl:config.json

**Commands:**
- `consul-template -template "config.ctmpl:config.json" -once`
- `consul-template -template "config.ctmpl:config.json:reload.sh"`
- `consul watch -type keyprefix -prefix config/api env`
- `consul members`

**Examples:**
- consul-template -template "config.ctmpl:config.json" -once
- consul watch -type keyprefix -prefix config/api env
- consul members -detailed

## References
- [Consul KV Docs](https://developer.hashicorp.com/consul/docs/dynamic-app-config/kv)
- [consul-template Docs](https://developer.hashicorp.com/consul/tutorials/get-started/consul-template)