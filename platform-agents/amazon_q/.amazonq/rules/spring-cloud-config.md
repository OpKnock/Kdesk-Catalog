# Spring Cloud Config

Manages externalized configuration for Spring microservices through Config Server: retrieves merged properties per environment, encrypts secrets at rest, and signals clients to refresh without restart.

## Instructions

# Spring Cloud Config

Consumes centralized configuration from Spring Cloud Config Server.

## What this skill does

- Fetches resolved config for any app/profile/label from the server
- Encrypts and decrypts secrets through the /encrypt and /decrypt endpoints
- Triggers runtime refresh on clients via /actuator/refresh

## When to use

- Centralizing config for a microservice fleet
- Rotating encrypted passwords without redeploys
- Debugging why a client sees stale properties

## Real commands

```bash
# Resolved config for app, profile, label
curl -s localhost:8888/apps-service/dev | jq -r '.propertySources[0].source'
curl -s localhost:8888/apps-service/dev/master | jq '.name'

# Encrypt a secret with the server's key
curl -s -X POST http://localhost:8888/encrypt -d 'secretvalue' -H 'Content-Type: text/plain'

# Decrypt back
curl -s -X POST http://localhost:8888/decrypt -d 'AgB...encrypted...'

# Client picks up new values
curl -X POST http://localhost:8888/actuator/refresh -H 'Content-Type: application/json' -d '{}'
```

## Config in git

```yaml
# apps-service-dev.yml
db:
  password: '{cipher}AgB...'
```

## Testing

```bash
curl -s localhost:8888/apps-service/dev | jq -r '.propertySources[0].source["db.password"]'
curl -s -X POST http://localhost:8888/encrypt -d 'test' | tee enc.txt
curl -s -X POST http://localhost:8888/decrypt -d "$(cat enc.txt)"
```

## Best practices

- Store ciphertext with the {cipher} prefix in config files
- Scope encryption to the Config Server only; never share the key
- Version config files with the same tag as the services that use them

## Capabilities

### config-server-client
Fetches environment-specific properties, manages ciphertext via encrypt/decrypt endpoints, and broadcasts refresh events to clients

**Commands:**
- `curl -s localhost:8888/apps-service/dev | jq -r '.propertySources[0].source'`
- `curl -s localhost:8888/apps-service/dev/master | jq '.name'`
- `curl -X POST http://localhost:8888/actuator/refresh -H "Content-Type: application/json" -d "{}"`
- `curl -s -X POST http://localhost:8888/encrypt -d "secretvalue" -H "Content-Type: text/plain"`
- `curl -s -X POST http://localhost:8888/decrypt -d "AgB...encrypted..."`

**Examples:**
- curl -s localhost:8888/apps-service/dev | jq -r '.propertySources[0].source.db'
- curl -s localhost:8888/apps-service/dev/master | jq '.name'
- curl -s -X POST http://localhost:8888/encrypt -d 'dbpass'