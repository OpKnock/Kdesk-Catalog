---
trigger: glob
description: "Implements tamper-resistant audit logging on Linux: auditd configuration, rule creation, event search, and report generation."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# Audit Logging

Implements tamper-resistant audit logging on Linux: auditd configuration, rule creation, event search, and report generation.

## Instructions

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

**Commands:**
- `logger -t my-api "AUDIT user=alice action=delete resource=order/42"`
- `journalctl -u my-api --since "1 hour ago"`
- `journalctl -t my-api`
- `tail -f /var/log/audit/audit.log`

**Examples:**
- logger -t my-api "AUDIT user=alice action=export resource=reports/2026"
- journalctl -u my-api -p err -n 100
- journalctl -t my-api --output=json-pretty
