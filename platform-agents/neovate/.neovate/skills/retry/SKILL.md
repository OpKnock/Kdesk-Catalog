---
name: "retry"
description: "Expert reference covering GNU timeout, curl retry flags, wait-for-service loops, and systemd/supervisor restart policies suited to long-running jobs."
---

# Retry

Expert reference covering GNU timeout, curl retry flags, wait-for-service loops, and systemd/supervisor restart policies suited to long-running jobs.

## Instructions

# Retry (shell & process level)

Expert skill for retrying shell commands, jobs, and services.

## What this skill does

- Wraps flaky commands in GNU timeout so they cannot hang forever
- Retries failed curl downloads with total-time budgets
- Waits for dependencies and restarts services with systemd/supervisor

## When to use

- Init scripts and cron jobs hitting briefly-unavailable services
- CI steps that flake on network timeouts
- Container start scripts waiting for databases

## Real commands

```bash
# Hard deadline: kill after 30s
timeout 30s curl -sf https://api.your-app.test/health || echo 'timed out'

# Retry 3x within 60s total
curl --retry 3 --retry-max-time 60 --fail https://api.your-app.test/data -o data.json

# Wait until a port accepts connections
until nc -z db 5432; do sleep 2; done

# Rerun only failed CI jobs
gh run rerun 1234567890 --failed

# systemd restart policy (edit then set Restart=on-failure, RestartSec=5)
systemctl edit myservice
```

## systemd unit fragment

```ini
[Service]
Restart=on-failure
RestartSec=5
StartLimitBurst=10
```

## Testing

```bash
# Simulate a slow start, then prove the readiness loop works
for i in $(seq 1 10); do curl -sf http://localhost:8080/ready && break; sleep 3; done
```

## Best practices

- Always pair retries with an overall timeout, or a hung job never dies
- Prefer --retry-connrefused so refused connections are retried too
- For services, use the platform restart policy instead of shell loops

## Capabilities

### shell-job-retry
Retry and restart shell jobs: timeout guards, readiness waits, service restarts

**Commands:**
- `timeout 30s curl -sf https://api.your-app.test/health || echo 'timed out'`
- `curl --retry 3 --retry-max-time 60 --fail https://api.your-app.test/data -o data.json`
- `until nc -z db 5432; do sleep 2; done`
- `gh run rerun 1234567890 --failed`
- `systemctl edit myservice`

**Examples:**
- timeout 30s curl -sf https://api.your-app.test/health && echo up || echo down
- for i in $(seq 1 10); do curl -sf http://localhost:8080/ready && break; sleep 3; done
- systemctl restart myservice && systemctl status myservice --no-pager
