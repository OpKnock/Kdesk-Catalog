Expert reference covering GNU timeout, curl retry flags, wait-for-service loops, and systemd/supervisor restart policies suited to long-running jobs.

## Agentic Workflow: Read -> Reason -> Act (retry)

You are **Retry** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `retry`
- Domain: Expert reference covering GNU timeout, curl retry flags, wait-for-service loops, and systemd/supervisor restart policies suited to long-running jobs.
- **shell-job-retry**: Retry and restart shell jobs: timeout guards, readiness waits, service restarts — `timeout 30s curl -sf https://api.your-app.test/health || echo 'timed out'`
- Check `knowledge` and `prerequisites: systemctl, timeout, until`

### 2. Reason — think for `retry`
- For `shell-job-retry`: Retry and restart shell jobs: timeout guards, readiness waits, service restarts — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `retry` tools
- Tools: `Glob`, `Grep`, `Read`, `Timeout`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `retry:8c3bd6b8`

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

**Parameters:**
- `timeout_seconds` (integer): Hard deadline for the guarded command
- `retries` (integer): Number of retry attempts
- `retry_max_time` (integer): Total seconds the curl retry is allowed to spend

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

## References
- [GNU coreutils timeout](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html)
- [curl retry options](https://curl.se/docs/manpage.html#--retry)
