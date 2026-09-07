---
applyTo: "**/*.r **/*.rs **/*.sh **/*.sql"
---

Deploy and tune a Web Application Firewall with ModSecurity and OWASP CRS, block OWASP Top 10 attacks, and reduce false positives.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -d --name crs -p 80:80 -p 443:443 -e PARANOIA=1 -`, `nginx -t`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# WAF Implementation

Put a web application firewall in front of HTTP traffic to detect and block OWASP Top 10 attacks while keeping legitimate users flowing.

## When to Use

- Public-facing apps that accept untrusted input (forms, uploads, APIs)
- Defense-in-depth alongside runtime protections, not as a replacement
- Compliance requirements that demand a WAF (PCI-DSS often expects one)
- Rate spikes from botnets and automated attack scanners

## Deployment Model

1. Proxy mode: the WAF sits in front of origin, terminates or forwards TLS, and inspects requests and responses.
2. Inline vs tap: inline blocks; tap (DetectionOnly) only logs. Start in DetectionOnly.
3. Out-of-band updates: never reload rules mid-traffic without testing; reload only after config validation (nginx -t).

## Rule Tuning Loop

1. Run DetectionOnly for 1-2 weeks; collect audit log matches.
2. Rank rule IDs by frequency; group by application route.
3. For each misfire, either allowlist the exact payload pattern or disable the rule via SecRuleUpdateActionById for the affected path only.
4. Promote to blocking per-paranoia-level, starting with PARANOIA=1.
5. Re-run regression traffic after every change.

## Logging and Alerts

- Keep audit logs: full request, matched rule IDs, and the payload snippet.
- Ship WAF logs to the SIEM; alert on repeated 403s from one source IP.
- Correlate WAF events with origin access logs to catch bypasses.

## Common Pitfalls

- Default rule set without tuning produces customer-breaking false positives.
- Blocking on content-encoding issues (gzip) instead of decoding first.
- Forgetting WebSocket and file-upload endpoints, which bypass classic CRS checks.
- No test for bypass: always replay the payloads against the live origin.

## Verification Checklist

- SQLi payload returns 403 and appears in audit log
- XSS payload in query string returns 403
- Legitimate login flow still works
- WAF outage falls open or closed deliberately, with a documented decision
- Rules updated from a pinned CRS version, not latest floating tag

## Capabilities

### Deploy ModSecurity with OWASP CRS
Start an OWASP CRS-enabled ModSecurity container in front of your app and verify it proxies traffic and loads rules.

**Parameters:**
- `PARANOIA` (integer): CRS paranoia level (1-4); higher levels block more but create more false positives.
- `BLOCKING_PARANOIA` (integer): Paranoia level at which traffic is actually blocked.

**Commands:**
- `docker run -d --name crs -p 80:80 -p 443:443 -e PARANOIA=1 -e BLOCKING_PARANOIA=1 owasp/modsecurity-crs:nginx`
- `docker exec -it crs bash`
- `docker logs crs | grep -i 'ModSecurity'`
- `docker stop crs && docker rm crs`

**Examples:**
- docker run -d --name crs -p 80:80 -p 443:443 -e PARANOIA=1 -e BLOCKING_PARANOIA=1 owasp/modsecurity-crs:nginx
- docker logs crs | grep -i 'ModSecurity'

### Configure and reload WAF rules
Check nginx config, reload the WAF, and test that attack payloads are detected and blocked.

**Parameters:**
- `target URL` (string): Origin behind the WAF to test, e.g. http://localhost.
- `log path` (string): Location of the ModSecurity audit log inside the container.

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost/login --data 'user=admin&pass=1%27%20OR%20%271%27%3D%271'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`
- `docker exec -it crs cat /var/log/modsec_audit.log | tail -50`

**Examples:**
- curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost/login --data 'user=admin&pass=1%27%20OR%20%271%27%3D%271'
- docker exec -it crs cat /var/log/modsec_audit.log | tail -50

### Tune rules and reduce false positives
Run in DetectionOnly mode, analyze audit log matches, and disable or adjust the rules that misfire on legitimate traffic.

**Parameters:**
- `rule id` (integer): CRS rule ID to pass or block (e.g. 949110 for inbound anomalies).
- `mode` (string): SecRuleEngine mode: On, DetectionOnly, Off.

**Commands:**
- `sed -i 's/SecRuleEngine On/SecRuleEngine DetectionOnly/' /etc/modsecurity.d/modsecurity.conf`
- `grep -E 'id "9|rule_id' /var/log/modsec_audit.log | sort | uniq -c | sort -rn`
- `sed -i 's/#SecRuleUpdateActionById/SecRuleUpdateActionById 949110:pass/' /etc/modsecurity.d/crs-setup.conf`
- `nginx -t && nginx -s reload`

**Examples:**
- grep -E 'id "9|rule_id' /var/log/modsec_audit.log | sort | uniq -c | sort -rn
- sed -i 's/#SecRuleUpdateActionById/SecRuleUpdateActionById 949110:pass/' /etc/modsecurity.d/crs-setup.conf

## References
- [](https://github.com/owasp-modsecurity/ModSecurity)
- [](https://github.com/coreruleset/coreruleset)
- [](https://coreruleset.org/docs/)
- [](https://github.com/owasp-modsecurity/ModSecurity/wiki/Reference-Manual)
