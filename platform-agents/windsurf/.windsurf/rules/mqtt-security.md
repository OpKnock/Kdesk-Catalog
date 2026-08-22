---
trigger: glob
description: "Secure MQTT deployments: TLS listeners, client certificates, username/password auth, and broker ACLs."
globs: ["**/*.r", "**/*.sh"]
---

# Mqtt Security

Secure MQTT deployments: TLS listeners, client certificates, username/password auth, and broker ACLs.

## Instructions

# MQTT Security

MQTT is plaintext by default; securing it means TLS on the wire plus authentication and authorization at the broker.

## What this skill does

- Generates CA/server/client certificates with openssl
- Configures mosquitto listeners, passwords and ACLs
- Verifies the secured channel end-to-end

## When to use

- Exposing a broker beyond localhost
- Meeting compliance requirements for message transport
- Restricting which clients can pub/sub on which topics

## Real commands

```bash
# CA certificate
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=myca"

# Server cert signed by CA
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=broker.example.com"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# User passwords
mosquitto_passwd -b /etc/mosquitto/passwd alice secret123

# Test the TLS listener
openssl s_client -connect localhost:8883 -cafile ca.crt

# Mutual TLS pub/sub
mosquitto_pub -h localhost -p 8883 --cafile ca.crt --cert client.crt --key client.key -t secure/topic -m hi
mosquitto_sub -h localhost -p 8883 --cafile ca.crt --cert client.crt --key client.key -t secure/topic -v
```

## mosquitto.conf

```conf
listener 8883
allow_anonymous false
password_file /etc/mosquitto/passwd
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
cafile /etc/mosquitto/certs/ca.crt
require_certificate true
acl_file /etc/mosquitto/acl
```

## ACL file

```
user alice
topic readwrite sensors/#
```

## Best practices

- `require_certificate true` for mutual TLS where possible
- Never allow anonymous in production
- Restart and test after every config change (`mosquitto -c conf -v`)

## Capabilities

### mqtt-security-config
Generate certificates, configure mosquitto TLS/auth/ACL settings and verify secured connections.

**Commands:**
- `openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=myca"`
- `mosquitto_passwd -b /etc/mosquitto/passwd alice secret123`
- `openssl s_client -connect localhost:8883 -cafile ca.crt`
- `mosquitto_pub -h localhost -p 8883 --cafile ca.crt --cert client.crt --key client.key -t secure/topic -m hi`
- `mosquitto_sub -h localhost -p 8883 --cafile ca.crt --cert client.crt --key client.key -t secure/topic -v`

**Examples:**
- mosquitto_pub -h localhost -p 8883 --cafile ca.crt -t test -m hi -u alice -P secret123
- openssl s_client -connect localhost:8883 -showcerts -cafile ca.crt
- mosquitto -c /etc/mosquitto/mosquitto.conf -v
