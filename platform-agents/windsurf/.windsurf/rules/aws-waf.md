---
trigger: glob
description: "Creates and manages web ACLs with IP sets and rate-based rules, associates them with Application Load Balancers, API Gateway stages, and CloudFront distributions, and inspects sampled requests. Use when working with web acl, rules ipset, associate, api or when the user mentions web acl, rules ipset, associate, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Creates and manages web ACLs with IP sets and rate-based rules, associates them with Application Load Balancers, API Gateway stages, and CloudFront distributions, and inspects sampled requests.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws wafv2 list-web-acls --scope REGIONAL`, `aws wafv2 create-ip-set --name blocked-ips --scope REGIONAL `
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

# AWS WAF

## What this skill does

Manages AWS WAF web ACLs: creating ACLs and rule groups, blocking IP sets, rate-based rules, associating with ALB/API Gateway/CloudFront, and inspecting sampled requests.

## When to use

- Blocking abusive IPs or bot traffic
- Rate-limiting an API at the edge
- Meeting compliance with managed rules (OWASP CRS)

## Real commands

```bash
# Create a web ACL
aws wafv2 create-web-acl --name my-acl --scope REGIONAL --default-action Allow={} --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl

# Create and update an IP set
aws wafv2 create-ip-set --name blocked-ips --scope REGIONAL --ip-address-version IPV4 --addresses 203.0.113.0/24
aws wafv2 update-ip-set --name blocked-ips --scope REGIONAL --id acl123 --addresses 203.0.113.0/24 198.51.100.0/24 --lock-token TOKEN123

# Attach rules from a JSON file
aws wafv2 update-web-acl --name my-acl --scope REGIONAL --id acl123 --default-action Allow={} --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl --rules file://rules.json

# Associate with an ALB
aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:111122223333:regional/webacl/my-acl/acl123 --resource-arn <alb-arn>

# See blocked IPs under a rate rule
aws wafv2 get-rate-based-statement-managed-keys --scope REGIONAL --web-acl-name my-acl --web-acl-id acl123
```

## Rules JSON fragment

```json
{"Name": "block-abuse", "Priority": 1, "Statement": {"IPSetReferenceStatement": {"ARN": "arn:aws:wafv2:...:ipset/blocked-ips/acl123"}}, "Action": {"Block": {}}, "VisibilityConfig": {"SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "block-abuse"}}
```

## Testing

- Curl the endpoint from an IP in the blocked set and expect 403
- Use sampled requests via CloudWatch Logs to verify decisions

## Best practices

- Start in Count mode, review logs, then switch to Block
- Use managed rule groups (AWSManagedRulesCommonRuleSet) first
- Scope ACLs to specific resources, not everything

## Capabilities

### web-acl
Create and inspect WAF web ACLs.

**Parameters:**
- `scope` (string): REGIONAL or CLOUDFRONT
- `acl_name` (string): Web ACL name

**Commands:**
- `aws wafv2 list-web-acls --scope REGIONAL`
- `aws wafv2 create-web-acl --name my-acl --scope REGIONAL --default-action Allow={} --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl`
- `aws wafv2 get-web-acl --name my-acl --scope REGIONAL --id acl123`
- `aws wafv2 delete-web-acl --name my-acl --scope REGIONAL --id acl123 --lock-token TOKEN123`
- `aws wafv2 list-web-acls --scope CLOUDFRONT`

**Examples:**
- aws wafv2 list-web-acls --scope REGIONAL --query 'WebACLs[].{name:Name,id:Id}'
- aws wafv2 create-web-acl --name my-acl --scope REGIONAL --default-action Allow={} --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl --rules file://rules.json
- aws wafv2 get-web-acl --name my-acl --scope REGIONAL --id acl123 | jq '.WebACL.Rules[].Name'

### rules-ipset
Add rules and IP sets to web ACLs.

**Parameters:**
- `ip_set_name` (string): IP set name
- `addresses` (string): CIDR addresses
- `rules_file` (string): JSON rules file

**Commands:**
- `aws wafv2 create-ip-set --name blocked-ips --scope REGIONAL --ip-address-version IPV4 --addresses 203.0.113.0/24`
- `aws wafv2 get-ip-set --name blocked-ips --scope REGIONAL --id ipset123`
- `aws wafv2 update-web-acl --name my-acl --scope REGIONAL --id acl123 --default-action Allow={} --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl --rules file://rules.json`
- `aws wafv2 list-ip-sets --scope REGIONAL`
- `aws wafv2 get-rate-based-statement-managed-keys --scope REGIONAL --web-acl-name my-acl --web-acl-id acl123`

**Examples:**
- aws wafv2 create-ip-set --name blocked-ips --scope REGIONAL --ip-address-version IPV4 --addresses 203.0.113.0/24 198.51.100.0/24
- aws wafv2 update-ip-set --name blocked-ips --scope REGIONAL --id acl123 --addresses 203.0.113.0/24 --lock-token TOKEN123
- aws wafv2 get-rate-based-statement-managed-keys --scope REGIONAL --web-acl-name my-acl --web-acl-id acl123 | jq '.ManagedKeysIPV4'

### associate
Associate web ACLs with protected resources.

**Parameters:**
- `resource_arn` (string): ARN of the protected resource
- `web_acl_arn` (string): Web ACL ARN

**Commands:**
- `aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:111122223333:regional/webacl/my-acl/acl123 --resource-arn arn:aws:elasticloadbalancing:us-east-1:111122223333:loadbalancer/app/api/abc`
- `aws wafv2 disassociate-web-acl --resource-arn arn:aws:apigateway:us-east-1::/restapis/abc123xyz/stages/prod`
- `aws wafv2 get-web-acl-for-resource --resource-arn arn:aws:apigateway:us-east-1::/restapis/abc123xyz/stages/prod`
- `aws wafv2 list-resources-for-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:111122223333:regional/webacl/my-acl/acl123`

**Examples:**
- aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:111122223333:regional/webacl/my-acl/acl123 --resource-arn arn:aws:elasticloadbalancing:us-east-1:111122223333:loadbalancer/app/api/abc
- aws wafv2 get-web-acl-for-resource --resource-arn arn:aws:apigateway:us-east-1::/restapis/abc123xyz/stages/prod
- aws wafv2 list-resources-for-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:111122223333:regional/webacl/my-acl/acl123

## References
- [WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
- [AWS CLI wafv2 Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/wafv2/index.html)
