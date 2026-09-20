---
name: "email-delivery-engineer"
description: "Troubleshoots email delivery: SPF/DKIM/DMARC verification, SMTP testing with swaks, Postfix queue management, and deliverability audits."
---

# email-delivery-engineer

Troubleshoots email delivery: SPF/DKIM/DMARC verification, SMTP testing with swaks, Postfix queue management, and deliverability audits.

## Instructions

# Email Delivery Engineering

Diagnose and fix email deliverability: auth records, SMTP paths, and queues.

## What This Skill Does

- Verifies SPF/DKIM/DMARC DNS records
- Tests SMTP delivery with swaks (auth, TLS, content)
- Manages the Postfix queue (inspect, flush, delete)
- Validates DKIM signatures locally
- Audits headers for auth results

## When to Use

- Emails landing in spam or bouncing
- Setting up a new sending domain
- Investigating queue buildup or deferred mail

## Real Commands

```bash
# DNS auth records
dig +short TXT example.com | grep -i spf
dig +short TXT selector._domainkey.example.com
dig +short TXT _dmarc.example.com
dig +short MX example.com

# DKIM verification
opendkim-testkey -d example.com -s default -vvv

# SMTP path testing
swaks --to user@example.com --server smtp.example.com   --from alerts@example.com --body 'test message'
swaks --to user@example.com --tls --auth LOGIN   --auth-user apikey --auth-password secret --server smtp.example.com

# Postfix queue
postqueue -p
postqueue -f              # flush
postsuper -d ALL          # delete all (careful)
mailq | tail -5
postconf -d myhostname
```

## Deliverability Checklist

1. SPF covers all senders (no hardfail conflicts)
2. DKIM signs with a valid selector
3. DMARC policy published with monitoring (p=none first)
4. MX/MTA accepts and forwards correctly
5. Spam score and content header audits pass

## Best Practices

- Read auth-results headers in the test mailbox after swaks
- Keep DMARC at p=quarantine after two weeks of p=none
- Monitor bounces via the queue, not just the inbox
- Use TLS everywhere: port 587 submission, STARTTLS relay
- Rotate DKIM keys on a schedule and re-test

## Capabilities

### authentication-diagnostics
Verify SPF, DKIM, and DMARC records for a domain.

**Commands:**
- `dig +short TXT localhost | grep spf`
- `dig +short TXT selector._domainkey.example.com`
- `dig +short TXT _dmarc.example.com`
- `opendkim-testkey -d localhost -s default -vvv`
- `spfquery -sender=jane@localhost -ip=203.0.113.9`
- `dig +short MX localhost`

**Examples:**
- dig +short TXT localhost | grep spf
- dig +short TXT _dmarc.example.com
- opendkim-testkey -d localhost -s default -vvv

### smtp-and-queue
Test SMTP paths and manage the Postfix queue.

**Commands:**
- `swaks --to user@localhost --server smtp.example.com --from alerts@localhost`
- `swaks --to user@localhost --tls --auth LOGIN --auth-user apikey --auth-password secret`
- `postqueue -p`
- `postqueue -f`
- `postsuper -d ALL`
- `mailq | tail -5`

**Examples:**
- swaks --to user@localhost --server smtp.example.com
- postqueue -p
- postsuper -d ALL
