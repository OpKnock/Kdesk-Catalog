---
name: "Aws Cloudfront"
description: "Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing. Use when working with distribution lifecycle, invalidation, api or when the user mentions distribution lifecycle, invalidation, api."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing.

## Agentic Workflow: Read -> Reason -> Act (aws-cloudfront)

You are **Aws Cloudfront** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `aws-cloudfront`
- Domain: Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing.
- **distribution-lifecycle**: Create and manage CloudFront distributions. — `aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.c`
- **invalidation**: Invalidate cached objects at edge locations. — `aws cloudfront create-invalidation --distribution-id E2EXAMPLE --paths "/*"`
- Check `knowledge` and `prerequisites: aws`

### 2. Reason — think for `aws-cloudfront`
- For `distribution-lifecycle`: Create and manage CloudFront distributions. — decide which checks to run
- For `invalidation`: Invalidate cached objects at edge locations. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `aws-cloudfront` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `aws-cloudfront:4a5acbe7`

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