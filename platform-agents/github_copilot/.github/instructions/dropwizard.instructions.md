---
applyTo: "**/*.java **/*.r **/*.sh **/*.sql **/*.{yaml,yml}"
---

# Dropwizard

Operates Dropwizard services: validates config, runs DB migrations, and checks healthchecks and metrics on the admin port from the fat jar.

## Instructions

# Dropwizard

## What this skill does

Dropwizard bundles Jetty, Jersey, Jackson, and Dropwizard Metrics into one fat jar. The CLI supports `server`, `check`, and `db` commands; the admin port (8081 by default) exposes healthchecks, metrics, and threads.

## When to use

- Starting or stopping a Dropwizard service
- Pre-deploy config validation and DB migration
- Investigating unhealthy services via the admin endpoints

## Real commands

```bash
# Validate config, then run
java -jar app.jar check config.yml
java -jar app.jar server config.yml

# Run or verify DB migrations
java -jar app.jar db migrate config.yml
java -jar app.jar db status config.yml

# Healthchecks and metrics on the admin port
curl -s localhost:8081/healthcheck | jq '.deadlocks, .database'
curl -s localhost:8081/metrics | jq '.meters'
curl -s localhost:8081/threads | head -50
```

## config.yml example

```yaml
server:
  applicationConnectors:
    - type: http
      port: 8080
  adminConnectors:
    - type: http
      port: 8081
database:
  driverClass: org.postgresql.Driver
  user: app
  password: secret
  url: jdbc:postgresql://db:5432/app
logging:
  level: INFO
```

## Healthcheck example

```java
import com.codahale.metrics.health.HealthCheck;

public class DatabaseHealthCheck extends HealthCheck {
    @Override
    protected Result check() {
        return db.isValid(2) ? Result.healthy() : Result.unhealthy("db unreachable");
    }
}
```

## Testing

```bash
# Gate deploys on healthcheck output
curl -sf localhost:8081/healthcheck | jq -e 'all(.; .healthy == true)'
```

## Best practices

- Always run `check` before `server` in CI.
- Use `db status` to confirm migration drift before rollout.
- Poll /healthcheck (not /metrics) for load balancer health.
- Set adminConnectors to a private network or firewall it.

## Capabilities

### dropwizard-server
Start, validate, migrate, and monitor a Dropwizard application from its fat jar.

**Commands:**
- `java -jar app.jar server config.yml`
- `java -jar app.jar check config.yml`
- `java -jar app.jar db migrate config.yml`
- `curl -s localhost:8081/healthcheck | jq`
- `curl -s localhost:8081/metrics | jq '.meters."com.example.orders.api"'`
- `curl -s localhost:8081/threads | head -50`

**Examples:**
- java -jar app.jar check config.yml && java -jar app.jar server config.yml
- curl -s localhost:8081/healthcheck | jq '.deadlocks, .database'
- java -jar app.jar db migrate config.yml --migrations migrations.xml
