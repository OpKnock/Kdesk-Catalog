---
name: "asyncapi-security"
description: "Defines and validates authentication mechanisms for event-driven APIs including API keys, OAuth2 flows, OpenID Connect, and mutual TLS across message brokers and generated client code. Use when working with security schemes, oauth broker, tls mtls, api or when the user mentions security schemes, oauth broker, tls mtls, api."
type: knowledge
triggers: ["asyncapi-security", "security-schemes", "oauth-broker", "tls-mtls"]
---

Defines and validates authentication mechanisms for event-driven APIs including API keys, OAuth2 flows, OpenID Connect, and mutual TLS across message brokers and generated client code.

## Agentic Workflow: Read -> Reason -> Act (asyncapi-security)

You are **Asyncapi Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `asyncapi-security`
- Domain: Defines and validates authentication mechanisms for event-driven APIs including API keys, OAuth2 flows, OpenID Connect, and mutual TLS across message brokers and generated client code.
- **security-schemes**: Author AsyncAPI securitySchemes and validate documents. — `npx @asyncapi/cli validate asyncapi.yaml`
- **oauth-broker**: Obtain OAuth2 tokens and connect to broker operations secured with OAuth2/OpenID Connect. — `curl -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_creden`
- **tls-mtls**: Validate and test TLS/mTLS security schemes for broker endpoints. — `echo | openssl s_client -connect kafka.your-app.test:9093 -showcerts 2>/dev/null`
- Check `knowledge` and `prerequisites: kafka-topics, mosquitto_pub, npx, openssl`

### 2. Reason — think for `asyncapi-security`
- For `security-schemes`: Author AsyncAPI securitySchemes and validate documents. — decide which checks to run
- For `oauth-broker`: Obtain OAuth2 tokens and connect to broker operations secured with OAuth2/OpenID Connect. — decide which checks to run
- For `tls-mtls`: Validate and test TLS/mTLS security schemes for broker endpoints. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `asyncapi-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `asyncapi-security:5cbba702`

# AsyncAPI Security

## What this skill does

Models and enforces AsyncAPI security schemes (apiKey, OAuth2, OpenID Connect, mutual TLS) in documents, generated clients, and broker connections.

## When to use

- A spec must declare how channels are authenticated
- Connecting generated clients to OAuth2-secured brokers
- Validating mTLS handshakes to Kafka/MQTT endpoints

## Real commands

```bash
# Validate the security schemes in a document
npx @asyncapi/cli validate asyncapi.yaml

# Get a client-credentials token
curl -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api-consumer -d client_secret=secret -d scope=kafka:read

# Introspect the token
curl -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN | jq '.active'

# mTLS check to the broker
openssl s_client -connect kafka.your-app.test:9093 -cert client.crt -key client.key -CAfile ca.crt < /dev/null 2>&1 | grep 'Verify return code'
```

## Spec example

```yaml
components:
  securitySchemes:
    oauth:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://auth.your-app.test/oauth2/token
          scopes:
            kafka:read: Read access
    mtls:
      type: mutualTLS
channels:
  orders:
    address: orders
    security:
      - oauth: [kafka:read]
```

## Testing

- Validate documents in CI with the AsyncAPI CLI
- Test broker auth with kafka-topics --command-config

## Best practices

- Apply security at both the document and broker level
- Rotate client credentials; never embed secrets in specs
- Use scope-based authorization, not shared topics

## Capabilities

### security-schemes
Author AsyncAPI securitySchemes and validate documents.

**Parameters:**
- `file` (string): AsyncAPI document to validate
- `ruleset` (string): Custom lint ruleset

**Commands:**
- `npx @asyncapi/cli validate asyncapi.yaml`
- `npx @asyncapi/cli lint asyncapi.yaml`
- `npx @asyncapi/cli validate https://raw.githubusercontent.com/asyncapi/spec/master/examples/streetlights.yml`
- `npx @asyncapi/cli --version`

**Examples:**
- npx @asyncapi/cli validate asyncapi.yaml
- npx @asyncapi/cli lint --ruleset security-rules.json asyncapi.yaml
- npx @asyncapi/cli validate asyncapi.yaml && echo valid

### oauth-broker
Obtain OAuth2 tokens and connect to broker operations secured with OAuth2/OpenID Connect.

**Parameters:**
- `token_url` (string): OAuth2 token endpoint URL
- `client_id` (string): OAuth2 client identifier
- `scope` (string): Requested OAuth2 scopes

**Commands:**
- `curl -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api-consumer -d client_secret=secret -d scope=kafka:read`
- `curl -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN`
- `kafka-topics --bootstrap-server kafka.your-app.test:9093 --command-config client-oauth.properties --list`
- `mosquitto_pub -h mqtt.your-app.test -p 8883 -u client --pw $TOKEN -t orders/created -m '{"id":1}' --cafile ca.crt`

**Examples:**
- TOKEN=$(curl -s -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api-consumer -d client_secret=secret -d scope=kafka:read | jq -r .access_token) && echo $TOKEN
- curl -s -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN | jq '.active'
- mosquitto_pub -h mqtt.your-app.test -p 8883 -u client --pw $TOKEN -t orders/created -m hello

### tls-mtls
Validate and test TLS/mTLS security schemes for broker endpoints.

**Parameters:**
- `broker_host` (string): Broker host:port
- `cafile` (string): CA certificate path
- `client_cert` (string): Client certificate for mTLS

**Commands:**
- `echo | openssl s_client -connect kafka.your-app.test:9093 -showcerts 2>/dev/null | openssl x509 -noout -subject -issuer`
- `echo | openssl s_client -connect kafka.your-app.test:9093 -cert client.crt -key client.key -CAfile ca.crt 2>&1 | grep -E 'Verify|Protocol'`
- `kafka-topics --bootstrap-server kafka.your-app.test:9093 --command-config client-mtls.properties --list`
- `openssl verify -CAfile ca.crt client.crt`

**Examples:**
- openssl s_client -connect kafka.your-app.test:9093 -showcerts < /dev/null | openssl x509 -noout -dates
- openssl s_client -connect kafka.your-app.test:9093 -cert client.crt -key client.key -CAfile ca.crt < /dev/null 2>&1 | grep 'Verify return code'
- kafka-topics --bootstrap-server kafka.your-app.test:9093 --command-config client-mtls.properties --describe --topic orders

## References
- [AsyncAPI Security Schemes](https://www.asyncapi.com/docs/reference/specification/v3.0.0#security-scheme-object)
- [AsyncAPI Security Best Practices](https://www.asyncapi.com/docs/guides/security)
- [OAuth 2.0 Spec](https://www.rfc-editor.org/rfc/rfc6749)
