---
name: "edge-deployment"
description: "Deploys static and serverless content to the edge with CloudFront + S3: syncs assets, creates and invalidates distributions, and updates Lambda@Edge functions. Use when working with cloudfront edge, api or when the user mentions cloudfront edge, api."
type: knowledge
triggers: ["edge-deployment", "cloudfront-edge"]
---

Deploys static and serverless content to the edge with CloudFront + S3: syncs assets, creates and invalidates distributions, and updates Lambda@Edge functions.

## Agentic Workflow: Read -> Reason -> Act (edge-deployment)

You are **Edge Deployment** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `edge-deployment`
- Domain: Deploys static and serverless content to the edge with CloudFront + S3: syncs assets, creates and invalidates distributions, and updates Lambda@Edge functions.
- **cloudfront-edge**: Manage S3-backed CloudFront distributions and edge invalidations for static deployments. — `aws s3 sync ./public s3://my-bucket --delete`
- Check `knowledge` and `prerequisites: aws`

### 2. Reason — think for `edge-deployment`
- For `cloudfront-edge`: Manage S3-backed CloudFront distributions and edge invalidations for static deployments. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `edge-deployment` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `edge-deployment:0dba79a8`

# Edge Deployment

## What this skill does

Edge deployment pushes content to CDN and edge-compute locations so users hit nearby POPs. The typical stack: S3 for storage, CloudFront for distribution, Lambda@Edge for request-time logic.

## When to use

- Shipping a static site or SPA globally

- Invalidating cached content after a release

- Adding edge request/response headers without a server

## Real commands

```bash
# Sync assets to S3 (delete stale files)
aws s3 sync ./public s3://my-bucket --delete

# Find your distributions
aws cloudfront list-distributions --query 'DistributionList.Items[].{id:Id,domain:DomainName}'

# Inspect cache behaviors and origins
aws cloudfront get-distribution --id E1234567890ABC | jq '.Distribution.DistributionConfig.CacheBehaviors'

# Invalidate after deploy
aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths '/*'

# Verify the object reached the edge
curl -sI https://d1abc2def3g4h5.cloudfront.net/ | grep -iE 'x-cache|etag'
```

## Deploy script example

```bash
set -euo pipefail
aws s3 sync ./public s3://my-bucket --delete --cache-control "max-age=300"
INV=$(aws cloudfront create-invalidation --distribution-id $DIST_ID --paths '/*' --query Invalidation.Id --output text)
aws cloudfront wait invalidation-completed --distribution-id $DIST_ID --id $INV
```

## Testing

```bash
# Confirm the invalidation finished before traffic check
aws cloudfront get-invalidation --distribution-id E1234567890ABC --id $INV | jq '.Invalidation.Status'
```

## Best practices

- Cache hashed assets (immutable) for a year; cache HTML for minutes.

- Use Origin Access Control (OAC) so only CloudFront reads the bucket.

- Invalidate only the paths that changed; `/*` costs more and thrashes the cache.

- Test with `?cache-bust` query params instead of invalidating in dev.

## Capabilities

### cloudfront-edge
Manage S3-backed CloudFront distributions and edge invalidations for static deployments.

**Parameters:**
- `distribution-id` (string): CloudFront distribution id to invalidate or inspect
- `bucket` (string): S3 bucket serving the edge content
- `paths` (array): Object paths to invalidate, e.g. /* or /assets/*

**Commands:**
- `aws s3 sync ./public s3://my-bucket --delete`
- `aws cloudfront list-distributions --query 'DistributionList.Items[].{id:Id,domain:DomainName}'`
- `aws cloudfront get-distribution --id E1234567890ABC`
- `aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths '/*'`
- `aws s3api head-object --bucket my-bucket --key index.html`

**Examples:**
- aws s3 sync ./public s3://my-bucket --delete && aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths '/*'
- aws cloudfront list-distributions --query 'DistributionList.Items[].{id:Id,domain:DomainName}' | jq
- curl -s https://d1abc2def3g4h5.cloudfront.net/ | head -5

## References
- [CloudFront with S3](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [Lambda@Edge](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-at-edge.html)
