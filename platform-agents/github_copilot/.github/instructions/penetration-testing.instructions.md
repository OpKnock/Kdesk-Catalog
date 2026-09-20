---
applyTo: "**/*.go **/*.r **/*.sh **/*.sql"
---

# penetration-testing

Runs authorized security assessments: reconnaissance with nmap, web scanning with nuclei/gobuster, and targeted exploitation checks.

## Instructions

# Penetration Testing

Authorized security assessments with a repeatable methodology.

## When to Use

- Scope-based security reviews of apps/infra
- Compliance-required periodic testing
- Verifying fixes after incidents

## Rules of engagement

Only scan systems you own or have written authorization for. Document scope, timing, and approved techniques before starting.

## Reconnaissance

```bash
nmap -sV -sC -p- -T4 target.example.com
nmap -sV -p 80,443,8080 10.0.0.0/24
```

## Web scanning

```bash
nuclei -u https://target.example.com -severity high,critical
gobuster dir -u http://target.example.com -w /usr/share/wordlists/dirb/common.txt
nikto -h http://target.example.com
```

## Injection checks

```bash
sqlmap -u 'http://target.example.com/item?id=1' --batch --dbs
```

## Reporting

- Every finding: severity, evidence (request/response), impact, remediation.
- Separate exploitable from informational.
- Re-test after fixes; close findings with evidence.

## Best practices

- Keep scan logs; they prove scope compliance.
- Rate-limit scans to avoid DoS of the target.
- Store findings in a tracker, never just a PDF.
- Coordinate with the defender team on timing.

## Testing

Validate scanner configuration against a lab target before production scoping.

## Capabilities

### recon
Discover hosts, ports, and services.

**Commands:**
- `nmap -sV -sC -p- -T4 target.example.com`
- `nmap -sV -p 80,443,8080 10.0.0.0/24`
- `nmap --script vulners -p 443 target.example.com`
- `whois localhost && dig localhost A +short`
- `nmap -sn 10.0.0.0/24`

**Examples:**
- nmap -sV -sC 10.0.1.5 -oN scan.txt
- nmap --top-ports 1000 -T4 target.example.com
- nmap -sV -p 3306,5432,6379 db.internal

### web
Scan web apps for vulnerabilities and content.

**Commands:**
- `nuclei -u http://localhost:8080 -severity high,critical`
- `gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirb/common.txt -t 40`
- `sqlmap -u 'http://localhost:8080/item?id=1' --batch --dbs`
- `nikto -h http://localhost:8080 -p 80`
- `ffuf -u http://localhost:8080/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301`

**Examples:**
- nuclei -u http://localhost:8080 -t http/exposures -o nuclei-results.txt
- gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
- sqlmap -u 'http://localhost:8080/item?id=1' --batch --technique=BEU --level=2
