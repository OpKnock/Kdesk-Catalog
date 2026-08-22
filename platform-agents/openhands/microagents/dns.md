---
name: "dns"
description: "Diagnoses and manages DNS: dig lookups, zone transfers, MX/TXT checks, and propagation verification."
type: knowledge
triggers: ["dns", "dig", "troubleshoot"]
---

# Dns

Diagnoses and manages DNS: dig lookups, zone transfers, MX/TXT checks, and propagation verification.

## Instructions

# DNS

Diagnose DNS configuration with dig and friends.

## When to Use

- New domain or subdomain not resolving
- Email delivery failures (MX/SPF/DMARC)
- Verifying propagation after a cutover

## Basic lookups

```bash
dig example.com A
dig example.com MX
dig example.com TXT
dig @8.8.8.8 example.com A +short
```

## Follow the chain

```bash
dig example.com +trace
```

Use +trace to find where the chain breaks: root -> TLD -> authoritative.

## Propagation check

Compare independent resolvers:

```bash
dig @8.8.8.8 example.com A +short
dig @1.1.1.1 example.com A +short
dig @208.67.222.222 example.com A +short
```

Mismatches mean caching - wait out the TTL or bump it for the cutover.

## Email records

```bash
dig example.com MX
dig example.com TXT   # SPF + DMARC
```

```txt
dig _dmarc.example.com TXT +short
```

## DNSSEC verification

```bash
dig example.com +dnssec +multi | grep RRSIG
delv @9.9.9.9 example.com A
```

## Best practices

- Set TTL low (300s) before migration, restore after.
- Keep SPF below the 10-lookup limit.
- Always query authoritative server directly when debugging propagation.
- Record DNS changes in the change log with before/after dig output.

## Testing

Run the lookup matrix (A, MX, TXT, NS, SOA) on every environment after DNS changes.

## Capabilities

### dig
Query DNS records with dig for full detail.

**Commands:**
- `dig localhost A`
- `dig localhost MX`
- `dig localhost TXT`
- `dig @8.8.8.8 localhost A +short`
- `dig localhost +trace`

**Examples:**
- dig www.example.com A +short
- dig localhost ANY +noall +answer
- dig @1.1.1.1 _dmarc.example.com TXT

### troubleshoot
Cross-check records and test propagation across resolvers.

**Commands:**
- `dig @8.8.8.8 localhost A +short && dig @1.1.1.1 localhost A +short`
- `host -t CNAME www.example.com`
- `nslookup -type=MX localhost`
- `dig localhost +dnssec`
- `delv @9.9.9.9 localhost A`

**Examples:**
- dig @208.67.222.222 localhost A +short
- dig localhost +dnssec +multi | grep -E 'RRSIG|flags'
- nslookup -type=SOA localhost
