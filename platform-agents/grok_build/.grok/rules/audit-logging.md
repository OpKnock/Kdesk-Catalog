Implements tamper-resistant audit logging on Linux: auditd configuration, rule creation, event search, and report generation.

## Agentic Workflow: Read -> Reason -> Act (audit-logging)

You are **Audit Logging** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `audit-logging`
- Domain: Implements tamper-resistant audit logging on Linux: auditd configuration, rule creation, event search, and report generation.
- **auditd**: Configure the Linux audit daemon and its rules. — `auditctl -w /etc/passwd -p wa -k password_changes`
- **search-report**: Search audit logs and produce summaries. — `ausearch -k password_changes -ts today`
- **app-logging**: Forward application audit events to syslog/journald. — `logger -t my-api "AUDIT user=alice action=delete resource=order/42"`
- Check `knowledge` and `prerequisites: auditctl, augenrules, aureport, ausearch`

### 2. Reason — think for `audit-logging`
- For `auditd`: Configure the Linux audit daemon and its rules. — decide which checks to run
- For `search-report`: Search audit logs and produce summaries. — decide which checks to run
- For `app-logging`: Forward application audit events to syslog/journald. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `audit-logging` tools
- Tools: `Glob`, `Grep`, `Read`, `Auditctl`, `Systemctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `audit-logging:d80dfe65`

# Audit Logging

## What this skill does

Implements tamper-resistant audit logging on Linux: auditd rules for sensitive files and syscalls, event search with ausearch, report generation with aureport, and application event forwarding via logger/journald.

## When to use

- Compliance (SOC2, PCI) requires immutable access logs
- Tracking who changed /etc/passwd or executed privileged commands
- Centralizing app security events for forensics

## Real commands

```bash
# Add a watch rule with a key
auditctl -w /etc/passwd -p wa -k password_changes

# List active rules
auditctl -l

# Syscall rules (record every execve)
auditctl -a always,exit -F arch=b64 -S execve -k exec_events

# Search events by key
ausearch -k password_changes -ts today -i

# Summary report
ureport -au --start today
```

Note: `ausearch -k password_changes -ts today -i` renders human-readable; `aureport -au` lists authentication events.

## App events

```bash
logger -t my-api "AUDIT user=alice action=delete resource=order/42"
journalctl -u my-api --since "1 hour ago"
```

## Testing

- Touch a watched file and confirm an event via ausearch
- Compare aureport totals against known activity

## Best practices

- Log who/what/when/result for every privileged action
- Ship audit.log to a remote SIEM; treat local logs as suspect
- Use rule keys consistently for fast search

## Capabilities

### auditd
Configure the Linux audit daemon and its rules.

**Parameters:**
- `watch_path` (string): File or directory to watch
- `permissions` (string): Permission filter: r, w, x, a
- `key` (string): Audit rule key (max 32 chars)

**Commands:**
- `auditctl -w /etc/passwd -p wa -k password_changes`
- `auditctl -l`
- `systemctl restart auditd`
- `auditctl -D`
- `augenrules --load`

**Examples:**
- auditctl -w /etc/shadow -p wa -k shadow_changes
- auditctl -a always,exit -F arch=b64 -S execve -k exec_events
- augenrules --check

### search-report
Search audit logs and produce summaries.

**Parameters:**
- `key` (string): Rule key to filter by
- `time_start` (string): Start time (-ts), e.g. today or 09:00
- `time_end` (string): End time (-te)

**Commands:**
- `ausearch -k password_changes -ts today`
- `ausearch -m USER_LOGIN -ts yesterday`
- `aureport -au --start today`
- `aureport -l --failed`
- `ausearch -k exec_events -i`

**Examples:**
- ausearch -k password_changes -i | tail -20
- aureport -au -ts 09:00 -te 17:00
- ausearch -m AVC -ts today | grep -c denied

### app-logging
Forward application audit events to syslog/journald.

**Parameters:**
- `tag` (string): Syslog tag (-t) for the application
- `message` (string): Audit event message

**Commands:**
- `logger -t my-api "AUDIT user=alice action=delete resource=order/42"`
- `journalctl -u my-api --since "1 hour ago"`
- `journalctl -t my-api`
- `tail -f /var/log/audit/audit.log`

**Examples:**
- logger -t my-api "AUDIT user=alice action=export resource=reports/2026"
- journalctl -u my-api -p err -n 100
- journalctl -t my-api --output=json-pretty

## References
- [auditd Manual](https://linux.die.net/man/8/auditd)
- [ausearch Manual](https://linux.die.net/man/8/ausearch)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)