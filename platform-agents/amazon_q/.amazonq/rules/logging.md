System and application logging basics: tail/grep log files, journald queries, syslog emission, and kernel message checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tail -n 200 /var/log/nginx/access.log`, `journalctl -u myapp --since yesterday`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Logging (Basics)

Inspect and manage system and application logs on Linux.

## What this skill does

- Tails and greps application log files.
- Queries journald with filters and live following.
- Emits syslog messages and reads kernel logs.

## When to use

- First-line debugging of app failures.
- Auditing what a service logged over time.
- Emitting structured alerts into syslog from scripts.

## Real commands

```bash
# Tail application logs
tail -n 200 /var/log/nginx/access.log
tail -f /var/log/nginx/access.log

# Filter errors
grep -i 'error\|exception' /var/log/app/app.log | tail -50
grep -c 'ERROR' /var/log/app/app.log

# journald: service logs since yesterday
journalctl -u myapp --since yesterday

# journald: follow live
journalctl -u myapp -f

# journald: errors this boot
journalctl -p err -b

# Emit a syslog message
logger -p user.err 'disk usage over 90%' -t cron-check

# Kernel messages
dmesg --level=err,warn | tail -20
```

## Testing

```bash
logger -p user.notice 'test message' && journalctl -t  -n 1
```

## Best practices

- Log to stderr/stdout in apps; let journald/systemd collect it.
- Use logger -t tags so scripts are greppable.
- Rotate large files; journalctl --vacuum-size to bound journal disk use.

## Capabilities

### file-logs
Tail, filter, and analyze application log files.

**Parameters:**
- `file` (string): Log file path.
- `pattern` (string): Grep pattern.
- `lines` (integer): Number of tail lines.

**Commands:**
- `tail -n 200 /var/log/nginx/access.log`
- `tail -f /var/log/nginx/access.log`
- `grep -i 'error\|exception' /var/log/app/app.log | tail -50`
- `grep -c 'ERROR' /var/log/app/app.log`

**Examples:**
- tail -f /var/log/nginx/access.log
- grep -i 'error\|exception' /var/log/app/app.log | tail -50
- grep -c 'ERROR' /var/log/app/app.log

### journald-syslog
Query journald and emit syslog messages.

**Parameters:**
- `unit` (string): systemd unit name.
- `priority` (string): Log priority: err, warn, info.
- `since` (string): Time window, e.g. yesterday, 1 hour ago.

**Commands:**
- `journalctl -u myapp --since yesterday`
- `journalctl -u myapp -f`
- `journalctl -p err -b`
- `logger -p user.err 'disk usage over 90%' -t cron-check`
- `dmesg --level=err,warn | tail -20`

**Examples:**
- journalctl -u myapp --since yesterday
- journalctl -p err -b
- logger -p user.err 'disk usage over 90%' -t cron-check

## References
- [journalctl man page](https://man7.org/linux/man-pages/man1/journalctl.1.html)
- [rsyslog documentation](https://www.rsyslog.com/doc/)