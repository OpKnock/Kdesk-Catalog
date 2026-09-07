Firebase Remote Config: manage parameter values per environment, publish changes with conditions, and fetch config from the CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s 'https://firebaseremoteconfig.googleapis.com/v1/proj`
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

# Firebase Remote Config

## What this skill does

Remote Config changes app behavior without a release: parameters with per-condition values are served to clients with a template versioned server-side. This skill covers template inspection and publishing.

## When to use

- Rolling out UI experiments per audience
- Killing a feature remotely during incidents
- A/B testing parameter values

## Real commands

```bash
# List all parameters
curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.parameters | keys'

# Inspect one parameter and its conditions
curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.parameters.maintenance_mode'

# Current template version
curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.version'

# Client-side fetch and activate
node -e "const rc=require('firebase/remote-config');const app=initializeApp();rc.getRemoteConfig(app).then(c=>{console.log(c.value('welcome_message'));c.activate()})"
```

## Condition example

```json
"conditions": [{
  "name": "android_2_plus",
  "expression": "device.android_version >= 8"
}]
```

## Publishing safely

```bash
# Fetch template -> edit -> publish with If-Match etag to avoid conflicts
curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'If-Match: <etag>'
```

## Best practices

- Always give every parameter a sensible default in the client SDK.
- Use conditions sparingly; each adds complexity and cache misses.
- Publish during low-traffic windows; clients cache templates.
- Validate with the REST `validate` step before publishing.
- Version-stamp experiments so analytics can correlate results.

## Capabilities

### remote-config
List, get, and publish Remote Config parameters and templates.

**Parameters:**
- `parameter-key` (string): Remote Config parameter key
- `condition` (string): Condition like app_version or audience segment
- `default-value` (string): Fallback value when no condition matches

**Commands:**
- `curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.parameters | keys'`
- `curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.parameters.maintenance_mode'`
- `node -e "const rc=require('firebase/remote-config');const app=initializeApp();rc.getRemoteConfig(app).then(c=>{console.log(c.value('welcome_message'));c.activate()})"`
- `curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.version'`
- `curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'If-Match: <etag>' | jq '.parameters'`

**Examples:**
- curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.parameters | keys'
- curl -s 'https://firebaseremoteconfig.googleapis.com/v1/projects/$PROJECT_ID/remoteConfig' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.version'
- node -e "const rc=require('firebase/remote-config');const app=initializeApp();rc.getRemoteConfig(app).then(c=>{console.log(c.value('welcome_message'));c.activate()})"

## References
- [Remote Config REST API](https://firebase.google.com/docs/reference/rest/remote-config/)
- [Remote Config overview](https://firebase.google.com/docs/remote-config)