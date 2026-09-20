# Timeout

Bound shell commands with GNU it and related tools.

## Instructions

# GNU timeout

Hand-crafted skill for bounding command execution with coreutils timeout.

## What this skill does

- Kills long-running commands after a deadline
- Sends SIGKILL after a grace period with -k
- Wraps flaky network commands so scripts cannot hang

## When to use

- Cron jobs that occasionally hang
- CI steps stuck on network waits
- Any script that must finish in a bounded time

## Real commands

```bash
# Kill after 30s; exit status 124 on timeout
timeout 30s sleep 60
echo $?

# Grace: TERM, then KILL after 5s more
timeout -k 5 30s docker pull busybox

# Network probe that cannot hang
timeout 10s ping -c 20 8.8.8.8

# curl's own bound
curl --max-time 10 -s https://example.com

# Python equivalent
python -c 'import signal; signal.alarm(5); print("alarm set")'
```

## Exit statuses

- 124: the command was killed by the timeout
- 125: timeout itself failed
- 126/127: command could not be run/found

## Script pattern

```bash
if timeout 30s ./deploy.sh; then
  echo "deploy finished"
else
  echo "deploy timed out"
fi
```

## Testing

```bash
timeout 2s sleep 10; echo "exit: $?"   # expect 124
timeout 5s curl -sf https://example.com && echo ok
```

## Best practices

- Check exit code 124 explicitly to distinguish timeouts from failures
- Add -k only when the process ignores TERM
- Combine with retry loops: bounded attempts, bounded runtime

## Capabilities

### timeout-guard
Bound shell commands with GNU timeout and related tools

**Commands:**
- `timeout 30s sleep 60`
- `timeout -k 5 30s docker pull busybox`
- `timeout 10s ping -c 20 8.8.8.8`
- `curl --max-time 10 -s http://localhost:8080`
- `python -c 'import signal; signal.alarm(5); print("alarm set")'`

**Examples:**
- timeout 30s sleep 60; echo $?
- timeout -k 5 30s docker pull busybox
- timeout 10s ping -c 20 8.8.8.8
