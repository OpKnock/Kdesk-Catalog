---
name: "pci"
description: "Test network segmentation, TLS strength, and scan coverage handling it scopes. and logs.'. Use when working with pci controls, compliance or when the user mentions pci controls, compliance."
type: knowledge
triggers: ["pci", "pci-controls"]
---

Test network segmentation, TLS strength, and scan coverage handling it scopes. and logs.'

## Agentic Workflow: Read -> Reason -> Act (pci)

You are **Pci** (compliance/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — compliance context for `pci`
- Domain: Test network segmentation, TLS strength, and scan coverage handling it scopes. and logs.'
- **pci-controls**: Test network segmentation, TLS strength, and scan coverage for PCI scopes — `nmap -sT -sV -p 443 --script ssl-enum-ciphers payment.example.com`
- Check `knowledge` and `prerequisites: nikto, nmap, sslscan`

### 2. Reason — think for `pci`
- For `pci-controls`: Test network segmentation, TLS strength, and scan coverage for PCI scopes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pci` tools
- Tools: `Glob`, `Grep`, `Read`, `Nmap`, `Sslscan` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pci:fbc08093`

# PCI DSS

Payment Card Industry Data Security Standard compliance checks for cardholder data
environments (CDE).

## When to Use

- Validating TLS and cipher strength on payment endpoints
- Verifying network segmentation between CDE and non-CDE
- Confirming no PAN data is stored unencrypted
- Preparing for ASV scans (Requirement 11)

## Real Commands

```bash
# TLS strength on the payment endpoint
nmap -sT -sV -p 443 --script ssl-enum-ciphers payment.example.com
sslscan payment.example.com

# Web-level checks
nikto -h payment.example.com -p 443 -ssl

# PAN data leakage check in code
rg -i "card_number|pan|cvv|track[12]" src/ --glob '!*.test.*'

# Segmentation: try reaching DB ports from the DMZ
nmap -p 3306,5432,1521 --open 10.0.0.0/24

# Verify cert subject
curl -k -v https://payment.example.com/ 2>&1 | grep -i subject:
```

## Core Requirement Checks

- Req 3: no full PAN at rest; masked displays only
- Req 4: TLS 1.2+ with strong ciphers
- Req 7: least-privilege access to cardholder data
- Req 8: MFA, unique IDs, password policies
- Req 10: audit logs with 12-month retention
- Req 11: quarterly ASV scans + penetration testing

## Best Practices

- Isolate the CDE with strict firewall rules; test from every segment
- Disable TLS 1.0/1.1 and weak ciphers (3DES, RC4)
- Never log PAN; tokenize or truncate
- Document compensating controls for anything non-compliant
- Keep scanning scoped: scan only in-scope assets you own

## Example Response

Returns cipher/TLS verdicts, open-port findings across segments, PAN-location hits
in code, and a requirement-by-requirement status with fix steps.

## Capabilities

### pci-controls
Test network segmentation, TLS strength, and scan coverage for PCI scopes

**Parameters:**
- `script` (string): nmap NSE script to run, e.g. ssl-enum-ciphers
- `open` (boolean): Report only open ports
- `ssl` (boolean): Force TLS mode in nikto

**Commands:**
- `nmap -sT -sV -p 443 --script ssl-enum-ciphers payment.example.com`
- `sslscan payment.example.com`
- `nikto -h payment.example.com -p 443 -ssl`
- `curl -k -v http://localhost:8080/ 2>&1 | grep -i 'subject:'`
- `nmap -sS -p 1-65535 --open 10.0.0.0/24 -oX segment-scan.xml`

**Examples:**
- nmap -p 1521,3306,5432 --open 10.0.0.0/24
- curl -s -o /dev/null -w '%{ssl_version} %{http_version}\n' http://localhost:8080
- rg -i "card|pan|track2|cvv" src/ --glob '!*.test.*'

## References
- [PCI DSS official](https://www.pcisecuritystandards.org/)
- [PCI DSS v4 requirements](https://www.pcisecuritystandards.org/document_library/?category=PCI%20DSS)
