---
type: agent_requested
description: "Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing."
---

# Aws Cloudfront

Manages AWS CloudFront distributions: creation, cache invalidation, origin configuration, and edge behavior testing.

## Instructions

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