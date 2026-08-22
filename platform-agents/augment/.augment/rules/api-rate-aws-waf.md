---
type: agent_requested
description: "Configures managed rate limiting on cloud gateways: AWS WAFv2 rate-based rules, Google Cloud Armor policies, and Cloudflare rate limiting via API."
---

# Api Rate Aws Waf

Configures managed rate limiting on cloud gateways: AWS WAFv2 rate-based rules, Google Cloud Armor policies, and Cloudflare rate limiting via API.

## Instructions

# API Rate v3 - Cloud Gateways

Managed rate limiting at the edge.

## What This Skill Does
- Applies rate-based blocking before traffic reaches the API
- Scales limits with provider infrastructure
- Centralizes visibility in provider metrics

## When to Use
- Global DDoS and flood protection
- Per-IP throttling at the network edge
- Reducing origin load from abusive clients

## Real Commands

```bash
aws wafv2 create-web-acl --name api-rate-acl --scope REGIONAL --default-action Allow={} --rules file://rate-rule.json --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=api-rate-acl --region us-east-1
```

## Rate Rule JSON

```json
{
  "Name": "block-floods",
  "Priority": 1,
  "Statement": {
    "RateBasedStatement": { "Limit": 2000, "AggregateKeyType": "IP" }
  },
  "Action": { "Block": {} },
  "VisibilityConfig": { "SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "block-floods" }
}
```

## Testing
- Send bursts over the threshold and confirm 403/blocked
- Verify sampled requests appear in provider metrics
- Test allowlisted IPs bypass the rule

## Best Practices
- Start in Count mode to observe, then enable Block
- Combine IP rate limits with session/header keys
- Keep provider limits above app-level limits

## Capabilities

### aws-waf
Create rate-based WAF rules and ACLs

**Commands:**
- `aws wafv2 create-web-acl --name api-rate-acl --scope REGIONAL --default-action Allow={} --rules file://rate-rule.json --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=api-rate-acl --region us-east-1`
- `aws wafv2 list-web-acls --scope REGIONAL --region us-east-1 | jq '.WebACLs[].Name'`
- `aws wafv2 get-web-acl --name api-rate-acl --scope REGIONAL --id $ACL_ID --region us-east-1 | jq '.WebACL.Rules[0].Statement'`
- `aws wafv2 update-web-acl --name api-rate-acl --scope REGIONAL --id $ACL_ID --default-action Allow={} --rules file://rate-rule.json --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=api-rate-acl --region us-east-1`

**Examples:**
- RateBasedStatement with Limit 2000 blocks floods per IP
- wafv2 list-web-acls enumerates managed rate ACLs
- Sampled requests surface in CloudWatch metrics

### cloudflare-rate
Manage Cloudflare rate limiting rules

**Commands:**
- `curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rate_limits" -H "Authorization: Bearer $CF_TOKEN" -H 'Content-Type: application/json' -d '{"threshold":100,"period":60,"match":{"request":{"url":"api.example.com/*"}},"action":{"mode":"block","timeout":300}}'`
- `curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rate_limits" -H "Authorization: Bearer $CF_TOKEN" | jq '.result[0].threshold'`
- `gcloud compute security-policies create api-armor --description "API rate limits" --project my-proj`
- `gcloud compute security-policies rules create 1000 --security-policy api-armor --action deny-403 --rate-limit-threshold-count 200 --rate-limit-threshold-interval-sec 60 --project my-proj`

**Examples:**
- -cli --help
- -api --help