---
name: "Nikto"
description: "Web server vulnerability scanning with Nikto: fingerprinting servers, finding misconfigurations, and producing reports."
globs: ["**/*.html", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Nikto

Web server vulnerability scanning with Nikto: fingerprinting servers, finding misconfigurations, and producing reports.

## Instructions

# Nikto

Open-source web server scanner that checks for dangerous files, outdated software,
and server misconfigurations.

## When to Use

- Quick reconnaissance of a web server before deeper testing
- Checking for default files (backups, admin pages) on a host
- Verifying a host is patched after a CVE advisory

## Real Commands

```bash
# Update the vulnerability database first
nikto -update

# Basic HTTPS scan
nikto -h https://example.com

# Specific port with SSL
nikto -h 10.0.0.5 -p 8443 -ssl

# HTML report
nikto -h example.com -o report.html -Format html

# Reduced false positives: only interesting file checks
nikto -h example.com -Tuning 123

# Polite scanning with delay
nikto -h example.com -Pause 2 -evasion 1
```

## Tuning Codes

- `1` Interesting files, `2` Misconfiguration, `3` Information disclosure
- `4` Injection, `6` Remote file retrieval

```bash
# Only interesting files + misconfig + info disclosure
nikto -h target -Tuning 123
```

## Best Practices

- Run `nikto -update` before each engagement
- Combine with Nmap: `nmap -sV -p80,443 target` first to narrow the port list
- Use `-Pause` for production hosts to avoid load
- Nikto finds low-hanging fruit only; pair with OWASP ZAP for full testing

## Example Response

Returns matched items like 'Server: nginx/1.18.0 may be vulnerable' with OSVDB IDs,
then the agent recommends upgrading or confirming the config.

## Capabilities

### web-vuln-scan
Run Nikto scans against web servers with tuning, auth, and report options

**Commands:**
- `nikto -h http://localhost:8080`
- `nikto -h 192.168.1.10 -p 8443 -ssl`
- `nikto -h localhost -o report.html -Format html`
- `nikto -h localhost -Tuning 1234 -Pause 2`
- `nikto -h localhost -useragent "Mozilla/5.0" -evasion 1`

**Examples:**
- nikto -h http://localhost:8080 -ssl -port 443
- nikto -h intranet.example.com -id admin:password
- nikto -h localhost -o results.csv -Format csv