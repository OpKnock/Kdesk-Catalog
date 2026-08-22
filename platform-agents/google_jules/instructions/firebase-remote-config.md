# Firebase Remote Config

Firebase Remote Config: manage parameter values per environment, publish changes with conditions, and fetch config from the CLI.

## Instructions

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
