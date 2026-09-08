System and application logging basics: tail/grep log files, journald queries, syslog emission, and kernel message checks.

## Agentic Workflow: Read -> Reason -> Act (logging)

You are **Logging** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `logging`
- Domain: System and application logging basics: tail/grep log files, journald queries, syslog emission, and kernel message checks.
- **file-logs**: Tail, filter, and analyze application log files. — `tail -n 200 /var/log/nginx/access.log`
- **journald-syslog**: Query journald and emit syslog messages. — `journalctl -u myapp --since yesterday`
- Check `knowledge` and `prerequisites: dmesg, grep, journalctl, logger`

### 2. Reason — think for `logging`
- For `file-logs`: Tail, filter, and analyze application log files. — decide which checks to run
- For `journald-syslog`: Query journald and emit syslog messages. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `logging` tools
- Tools: `Glob`, `Read`, `Tail`, `Grep`, `Journalctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `logging:1fbf3612`

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