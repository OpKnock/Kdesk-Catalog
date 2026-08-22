---
type: agent_requested
description: "Detects and responds to threats at runtime with Falco, Tracee, auditd, and strace: suspicious syscalls, containers, and process behavior."
---

# runtime-protection

Detects and responds to threats at runtime with Falco, Tracee, auditd, and strace: suspicious syscalls, containers, and process behavior.

## Instructions

# Runtime Protection

Detect malicious behavior while it happens.

## When to Use

- Container escape and privilege escalation detection
- Suspicious process behavior monitoring
- Forensics after an incident

## Falco

```bash
falcoctl install falco
falco -r /etc/falco/falco_rules.yaml
```

Rule example - terminal in container:

```yaml
- rule: Terminal shell in container
  desc: A shell was spawned in a container
  condition: container.id != host and proc.name = bash
  output: shell spawned in container (proc=%proc.name container=%container.id)
  priority: WARNING
```

## Tracee

```bash
tracee-ebpf --events execve,openat
```

## Syscall tracing

```bash
strace -f -e trace=execve,openat -o trace.log ./app
```

## Kernel audit

```bash
auditctl -a always,exit -F arch=b64 -S execve -k exec-log
auditctl -l
ausearch -k exec-log -ts recent
```

## Alert pipeline

Falco events -> priority threshold -> pager. Wire outputs to a SIEM or message queue.

## Best practices

- Tune rules to the workload to avoid alert fatigue.
- Ship the event stream off-host immediately.
- Test rules with real attack simulations (e.g., kubectl exec).
- Keep Falco/Tracee versions pinned and updated.

## Testing

Simulate a known-bad action (shell in container) and verify the rule fires within seconds.

## Capabilities

### falco
Run Falco threat detection and manage rules.

**Commands:**
- `falco --version`
- `falcoctl install falco`
- `falco -r /etc/falco/falco_rules.yaml -e /dev/null`
- `falco --json --output '{"event":"%evt.type","proc":"%proc.name"}'`
- `falcoctl artifact list --type rules`

**Examples:**
- falco -r my-rules.yaml | head -20
- falcoctl artifact install falco_rules:2.0
- falco --version && falco -h | head -20

### syscall
Trace and audit syscall activity.

**Commands:**
- `strace -f -e trace=execve,openat -o trace.log ./app`
- `strace -p 1234 -f -e trace=network`
- `auditctl -a always,exit -F arch=b64 -S execve -k exec-log`
- `auditctl -l`
- `ausearch -k exec-log -ts recent | head -30`

**Examples:**
- strace -f -e trace=openat ./app 2>&1 | grep ENOENT | head
- auditctl -a always,exit -F arch=b64 -S socket -k net-conn
- ausearch -k net-conn -i | head -20