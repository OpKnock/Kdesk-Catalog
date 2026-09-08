Migrates and evolves API caching layers — moving between cache stores, adding CDN edge caching, and consolidating invalidation.

## Agentic Workflow: Read -> Reason -> Act (api-cache-migration)

You are **Api Cache Migration** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-cache-migration`
- Domain: Migrates and evolves API caching layers — moving between cache stores, adding CDN edge caching, and consolidating invalidation.
- **cache-migration**: Migrate cache stores (e.g. in-memory to Redis) with data export/import and key renames — `redis-cli --scan --pattern 'legacy:*' > keys.txt`
- **cdn-integration**: Wire a CDN (CloudFront or edge cache) in front of the API with purge operations — `aws cloudfront create-invalidation --distribution-id E12345 --paths '/api/*'`
- Check `knowledge` and `prerequisites: redis, node.js, python`

### 2. Reason — think for `api-cache-migration`
- For `cache-migration`: Migrate cache stores (e.g. in-memory to Redis) with data export/import and key renames — decide which checks to run
- For `cdn-integration`: Wire a CDN (CloudFront or edge cache) in front of the API with purge operations — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-cache-migration` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Aws` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-cache-migration:71e00df5`

# API Cache (Migration & Edge)

Evolves existing caching setups: migrating stores, adding edge layers, and consolidating invalidation.

## When to Use
- Moving from in-memory to distributed cache
- Adding a CDN in front of the API
- Consolidating fragmented cache namespaces
- Replacing TTL-only invalidation with event-driven

## Real Commands

```bash
# List keys before migration
redis-cli --scan --pattern 'legacy:*' > keys.txt

# Rename namespace
redis-cli --scan --pattern 'legacy:*' | while read k; do redis-cli RENAME $k api:$k; done

# Pipe-import a dump
redis-cli --pipe < dump.txt

# CDN purge
aws cloudfront create-invalidation --distribution-id E12345 --paths '/api/*'

# Varnish ban
varnishadm ban 'req.url ~ ^/api/products'
```

## Migration Checklist
1. Export current keys with TTLs (`redis-cli --scan` + `redis-cli TTL`)
2. Stand up the new store in parallel
3. Flip readers, keep writers dual-write
4. Verify `redis-cli DBSIZE` matches
5. Purge CDN paths on cutover

## Testing
Compare hit ratios and p95 latency before and after each migration step.

## Best Practices
- One invalidation path per resource
- Version cache keys on schema changes
- Run migrations during low-traffic windows

## Capabilities

### cache-migration
Migrate cache stores (e.g. in-memory to Redis) with data export/import and key renames

**Parameters:**
- `srcPattern` (string): Key pattern for the old cache namespace
- `dstPrefix` (string): Prefix for the new namespace

**Commands:**
- `redis-cli --scan --pattern 'legacy:*' > keys.txt`
- `redis-cli --pipe < dump.txt`
- `redis-cli RENAME legacy:users:42 api:users:42`
- `redis-cli --scan --pattern 'legacy:*' | xargs -I{} redis-cli RENAME {} api:{}`
- `redis-cli DBSIZE`

**Examples:**
- redis-cli --scan --pattern 'legacy:*' | while read k; do redis-cli RENAME $k api:$k; done
- redis-cli --pipe < dump.txt && redis-cli DBSIZE
- redis-cli --scan --pattern 'api:*' | xargs redis-cli DEL

### cdn-integration
Wire a CDN (CloudFront or edge cache) in front of the API with purge operations

**Parameters:**
- `distributionId` (string): CloudFront distribution ID
- `paths` (string): Paths to purge

**Commands:**
- `aws cloudfront create-invalidation --distribution-id E12345 --paths '/api/*'`
- `aws cloudfront get-cache-policy --id 658327ea-f89d-4fab-a63d-7e88639e58f6`
- `aws cloudfront list-distributions --query 'DistributionList.Items[?DefaultCacheBehaviour.TargetOriginId==`api`].Id'`
- `varnishadm ban 'req.url ~ ^/api/products'`
- `curl -s -X PURGE http://edge/api/products -o /dev/null -w '%{http_code}'`

**Examples:**
- aws cloudfront create-invalidation --distribution-id E12345 --paths '/api/products/*'
- varnishadm ban 'req.url ~ ^/api/orders'
- curl -s -X PURGE http://edge/api/products -o /dev/null -w '%{http_code}'

## References
- [Redis Migration Guide](https://redis.io/docs/latest/operate/oss_and_stack/management/)
- [AWS CloudFront Docs](https://docs.aws.amazon.com/cloudfront/)
- [Varnish Bans](https://varnish-cache.org/docs/trunk/users-guide/purging.html)
