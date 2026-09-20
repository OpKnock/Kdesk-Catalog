# security-audit

Performs end-to-end host and network security audits with Lynis, ssh-audit, and nmap, producing hardening recommendations.

## Instructions

# Security Audit

Systematic host and network security auditing with hardening evidence.

## What This Skill Does

- Runs Lynis hardening audits with CIS-style scoring
- Audits SSH daemon configuration with ssh-audit
- Scans open ports and service versions with nmap
- Produces actionable hardening checklists

## When to Use

- Pre-production host hardening review
- Investigating unusual listening services
- Compliance evidence collection

## Real Commands

```bash
# Host audit
lynis audit system
lynis audit system --quick
lynis audit system --auditor "Security Team"
lynis audit policies

# SSH audit
ssh-audit 10.0.0.5
ssh-audit --level=info 10.0.0.5

# Network scan
nmap -sV -sC 10.0.0.5
nmap -p- --min-rate 1000 10.0.0.5
```

## Hardening Checklist

- Disable password SSH auth; enforce key-only access
- Update packages; enable automatic security updates
- Close unused ports and restrict with firewall rules
- Enable auditd and system accounting
- Harden kernel params (sysctl) per CIS guidance

## Best Practices

- Run audits on clean images before patching to measure drift
- Re-run after every major upgrade and compare hardening index
- Automate weekly lynis --quick in cron and ship logs to central storage
- Verify findings manually before applying changes
- Keep the audit log as compliance evidence

## Capabilities

### lynis-system-audit
Run Lynis hardening audits on Linux/macOS hosts.

**Commands:**
- `lynis audit system`
- `lynis audit system --quick`
- `lynis audit system --auditor "Security Team"`
- `lynis audit system --log-file /var/log/lynis-report.log`
- `lynis show commands`

**Examples:**
- lynis audit system --quick
- lynis audit system --auditor "Ops"
- lynis show commands

### network-and-service-scan
Scan services and SSH configurations for weaknesses.

**Commands:**
- `ssh-audit 10.0.0.5`
- `ssh-audit --level=info 10.0.0.5`
- `nmap -sV -sC 10.0.0.5`
- `nmap -p- --min-rate 1000 10.0.0.5`
- `lynis audit policies`

**Examples:**
- ssh-audit 10.0.0.5
- nmap -sV -sC 10.0.0.5
- lynis audit policies
