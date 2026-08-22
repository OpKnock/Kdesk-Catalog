---
name: "logging-devops"
description: "Manages local and system logging: journald, syslog, log rotation, logrotate policies, and real-time tailing on Linux hosts."
---

# logging-devops

Manages local and system logging: journald, syslog, log rotation, logrotate policies, and real-time tailing on Linux hosts.

## Instructions

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
