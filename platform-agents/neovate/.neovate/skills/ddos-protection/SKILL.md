---
name: "ddos-protection"
description: "Mitigates DDoS attacks: rate limiting, firewall rules, CDN shielding, and attack simulation."
---

# ddos-protection

Mitigates DDoS attacks: rate limiting, firewall rules, CDN shielding, and attack simulation.

## Instructions

# DDoS Protection

Defends services against volumetric and application-layer attacks: edge shielding,
rate limits, and firewall rules.

## When to Use

- During an active attack
- Hardening before launch (prep)
- Validating that mitigation configs actually work

## Real Commands

```bash
# Edge: enable proxy/CDN shielding and rate limits
# (via Cloudflare API)
curl -s -X POST 'https://api.cloudflare.com/client/v4/zones/$ZONE/rate_limits' \
  -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' \
  -d '{"match": {"request": {"url": "*"}}, "threshold": 100, "period": 60, "action": {"mode": "simulate"}}'

# Host: connection limit at the firewall
sudo iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 100 -j DROP

# Nginx rate limit
sudo nginx -t && sudo nginx -s reload

# Validate: simulate traffic
sudo ab -n 10000 -c 100 https://app.example.com/

# Capture evidence
sudo tcpdump -i eth0 -c 5000 -w /tmp/ddos.pcap
```

## Nginx Rate Limit Config

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=20r/s;
server {
  location /api/ {
    limit_req zone=api burst=40 nodelay;
  }
}
```

## Best Practices

- Put a CDN/edge in front; never expose origin IPs
- Rate limit per IP and per user (auth token)
- Use `simulate` actions first, then enforce
- Keep origin whitelisted to the CDN only
- Have a runbook: edge rules + firewall + emergency scaling

## Example Response

During an attack: identifies the traffic signature from pcap, applies edge + host
mitigations, and verifies origin pressure drops.

## Capabilities

### ddos-mitigation
Configure rate limits, firewall rules, and verify mitigation

**Commands:**
- `iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 100 -j DROP`
- `nginx -t && nginx -s reload`
- `ab -n 10000 -c 100 http://localhost:8080/`
- `tcpdump -i eth0 -c 5000 -w /tmp/ddos.pcap`
- `curl -s -X POST 'https://api.cloudflare.com/client/v4/zones/$ZONE/rate_limits' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{"match":{"request":{"url":"*"}}}'`

**Examples:**
- iptables -L -n -v | head -30
- wrk -t8 -c500 -d60s http://localhost:8080/ --latency
- ufw limit ssh comment 'rate limit ssh'
