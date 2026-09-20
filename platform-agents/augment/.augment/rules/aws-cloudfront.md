---
type: agent_requested
description: "Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing. Use when working with distribution lifecycle, invalidation, api or when the user mentions distribution lifecycle, invalidation, api."
---

Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws cloudfront create-distribution --origin-domain-name my-b`, `aws cloudfront create-invalidation --distribution-id E2EXAMP`
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

# AWS CloudFront

## What this skill does

Manages AWS CloudFront CDN distributions: creating distributions from S3/HTTP origins, updating cache behavior, invalidating edge caches, and verifying responses at the edge.

## When to use

- Serving a static site or API through a CDN
- Pushing a new deploy when TTLs are long (invalidation)
- Debugging stale content served from the edge

## Real commands

```bash
# Create a distribution
aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com

# List distributions
aws cloudfront list-distributions --query 'DistributionList.Items[].{Id:Id,DomainName:DomainName,Status:Status}' --output table

# Invalidate everything after a deploy
aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/*"

# Targeted invalidation
aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/index.html" "/assets/*"

# Verify edge response
curl -sI https://d111111abcdef8.cloudfront.net/index.html | grep -iE 'x-cache|age'
```

## Testing

- Check x-cache header: Hit-from-cloudfront vs RefreshHit/Miss
- Poll list-invalidations until status becomes Completed

## Best practices

- Invalidate narrow paths (/* only for emergencies)
- Version assets by filename to avoid invalidations entirely
- Use Origin Shield + default TTLs tuned to content type
- Get the ETag from get-distribution before update/delete

## Capabilities

### distribution-lifecycle
Create and manage CloudFront distributions.

**Parameters:**
- `origin_domain` (string): Origin domain name
- `distribution_id` (string): CloudFront distribution ID

**Commands:**
- `aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com`
- `aws cloudfront get-distribution --id E2EXAMPLE`
- `aws cloudfront list-distributions --query 'DistributionList.Items[].{Id:Id,DomainName:DomainName}'`
- `aws cloudfront update-distribution --id E2EXAMPLE --distribution-config file://config.json`
- `aws cloudfront delete-distribution --id E2EXAMPLE --if-match ETAG123`

**Examples:**
- aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com --default-root-object index.html
- aws cloudfront list-distributions --query 'DistributionList.Items[].{Id:Id,DomainName:DomainName,Status:Status}' --output table
- aws cloudfront get-distribution --id E2EXAMPLE | jq '.Distribution.DistributionConfig.DefaultCacheBehavior'

### invalidation
Invalidate cached objects at edge locations.

**Parameters:**
- `paths` (string): Object paths to invalidate
- `distribution_id` (string): Distribution ID

**Commands:**
- `aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/*"`
- `aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/index.html" "/assets/*"`
- `aws cloudfront list-invalidations --distribution-id E2EXAMPLE`
- `aws cloudfront get-invalidation --distribution-id E2EXAMPLE --id INV123`
- `curl -sI https://d111111abcdef8.cloudfront.net/index.html | grep -iE 'x-cache|age|via'`

**Examples:**
- aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/css/*" "/js/*"
- aws cloudfront list-invalidations --distribution-id E2EXAMPLE --max-items 5
- curl -sI https://d111111abcdef8.cloudfront.net/app.js | grep -i x-cache

## References
- [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)
- [AWS CLI cloudfront Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloudfront/index.html)