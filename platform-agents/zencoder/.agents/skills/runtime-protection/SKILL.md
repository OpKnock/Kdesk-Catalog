---
name: "runtime-protection"
description: "Detects and responds to threats at runtime with Falco, Tracee, auditd, and strace: suspicious syscalls, containers, and process behavior. Use when working with falco, syscall or when the user mentions falco, syscall."
license: "MIT"
compatibility: "Requires openrasp, contrast-security, falco, sysdig, aqua."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(auditctl:*) Bash(ausearch:*) Bash(falco:*) Bash(falcoctl:*) Bash(strace:*)"
---

Detects and responds to threats at runtime with Falco, Tracee, auditd, and strace: suspicious syscalls, containers, and process behavior.

## Agentic Workflow: Read -> Reason -> Act (runtime-protection)

You are **runtime-protection** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `runtime-protection`
- Domain: Detects and responds to threats at runtime with Falco, Tracee, auditd, and strace: suspicious syscalls, containers, and process behavior.
- **falco**: Run Falco threat detection and manage rules. — `falco --version`
- **syscall**: Trace and audit syscall activity. — `strace -f -e trace=execve,openat -o trace.log ./app`
- Check `knowledge` and `prerequisites: openrasp, contrast-security, falco, sysdig`

### 2. Reason — think for `runtime-protection`
- For `falco`: Run Falco threat detection and manage rules. — decide which checks to run
- For `syscall`: Trace and audit syscall activity. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `runtime-protection` tools
- Tools: `Glob`, `Grep`, `Read`, `Falco`, `Falcoctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `runtime-protection:d2b79741`

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

**Parameters:**
- `rules` (string): Rules file path
- `json` (string): JSON output mode
- `output` (string): Output template

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

**Parameters:**
- `syscall` (string): Syscalls to trace
- `key` (string): Audit rule key
- `pid` (number): Process id to attach

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

## References
- [Falco Docs](https://falco.org/docs/)
- [Tracee](https://github.com/aquasecurity/tracee)
- [auditd](https://man7.org/linux/man-pages/man8/auditctl.8.html)
