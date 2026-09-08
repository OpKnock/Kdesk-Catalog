---
type: agent_requested
description: "Manages local and system logging: journald, syslog, log rotation, logrotate policies, and real-time tailing on Linux hosts. Use when working with journald management, syslog and rotation, devops or when the user mentions journald management, syslog and rotation, devops."
---

Manages local and system logging: journald, syslog, log rotation, logrotate policies, and real-time tailing on Linux hosts.

## Agentic Workflow: Read -> Reason -> Act (logging-devops)

You are **logging-devops** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `logging-devops`
- Domain: Manages local and system logging: journald, syslog, log rotation, logrotate policies, and real-time tailing on Linux hosts.
- **journald-management**: Query, filter, and maintain the systemd journal. — `journalctl -u nginx --since '2 hours ago'`
- **syslog-and-rotation**: Configure rsyslog forwarding and logrotate policies. — `tail -f /var/log/syslog`
- Check `knowledge` and `prerequisites: journalctl, logger, logrotate, rsyslogd`

### 2. Reason — think for `logging-devops`
- For `journald-management`: Query, filter, and maintain the systemd journal. — decide which checks to run
- For `syslog-and-rotation`: Configure rsyslog forwarding and logrotate policies. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `logging-devops` tools
- Tools: `Glob`, `Grep`, `Read`, `Journalctl`, `Tail` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `logging-devops:31380d7f`

# Local Logging Operations

Manage logs on Linux hosts: journald, syslog, rotation, and live tailing.

## What This Skill Does

- Queries journald with unit/priority/time filters
- Watches live logs with journalctl -f and tail -f
- Configures logrotate for rotation, compression, and retention
- Routes syslog with rsyslog (local files, remote, filtering)
- Manages disk usage with journal vacuuming

## When to Use

- Debugging a service on a VM via its logs
- Disk fills up because logs never rotate
- Forwarding logs to a central server

## Real Commands

```bash
# journald
journalctl -u nginx --since '2 hours ago'
journalctl -p err --no-pager
journalctl -f -u kubelet
journalctl --disk-usage
journalctl --vacuum-size=200M
journalctl --vacuum-time=7d

# tailing
tail -f /var/log/syslog
tail -n 200 /var/log/nginx/error.log

# rotation
logrotate -d /etc/logrotate.d/nginx    # dry run
logrotate -f /etc/logrotate.conf       # force
logrotate -s /var/lib/logrotate/status /etc/logrotate.d/nginx

# syslog
rsyslogd -N1 -f /etc/rsyslog.conf
logger -t deploy -p user.notice 'release 1.2.0 shipped'
```

## logrotate Config

```
/var/log/nginx/*.log {
  daily
  rotate 14
  compress
  delaycompress
  missingok
  notifempty
  create 0640 www-data adm
  sharedscripts
  postrotate
    [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
  endscript
}
```

## Best Practices

- Test rotation with `logrotate -d` before enforcing
- Vacuum the journal proactively on busy hosts
- Centralize host logs via rsyslog/Logstash instead of SSH tailing
- Include timestamps and hostnames in forwarded syslog templates
- Monitor `/var/log` disk usage; rotation is not backup

## Capabilities

### journald-management
Query, filter, and maintain the systemd journal.

**Parameters:**
- `unit` (string): systemd unit name
- `priority` (string): Priority filter: err, warning, info, debug
- `since` (string): Time window, e.g. '1 hour ago'

**Commands:**
- `journalctl -u nginx --since '2 hours ago'`
- `journalctl -p err --no-pager`
- `journalctl -f`
- `journalctl --disk-usage`
- `journalctl --vacuum-size=200M`
- `journalctl _PID=$(pgrep nginx | head -1)`

**Examples:**
- journalctl -u nginx --since '2 hours ago'
- journalctl -p err --no-pager
- journalctl --vacuum-size=200M

### syslog-and-rotation
Configure rsyslog forwarding and logrotate policies.

**Parameters:**
- `config` (string): logrotate or rsyslog config path
- `file` (string): Log file to tail

**Commands:**
- `tail -f /var/log/syslog`
- `tail -n 200 /var/log/nginx/error.log`
- `logrotate -d /etc/logrotate.d/nginx`
- `logrotate -f /etc/logrotate.conf`
- `rsyslogd -N1 -f /etc/rsyslog.conf`
- `logger -t deploy -p user.notice 'release 1.2.0 shipped'`

**Examples:**
- logrotate -d /etc/logrotate.d/nginx
- rsyslogd -N1 -f /etc/rsyslog.conf
- tail -f /var/log/syslog

## References
- [journalctl Manual](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)
- [logrotate Manual](https://man7.org/linux/man-pages/man8/logrotate.8.html)
- [rsyslog Documentation](https://www.rsyslog.com/doc/)