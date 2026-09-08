Migrates API documentation: Swagger 2.0 to OpenAPI 3, doc site restructuring, and versioned docs with changelogs.

## Agentic Workflow: Read -> Reason -> Act (api-doc-spec-migration)

You are **Api Doc Spec Migration** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-doc-spec-migration`
- Domain: Migrates API documentation: Swagger 2.0 to OpenAPI 3, doc site restructuring, and versioned docs with changelogs.
- **spec-migration**: Convert and upgrade OpenAPI specs between versions — `npx swagger2openapi swagger.yaml -o openapi3.yaml`
- **doc-versioning**: Publish versioned documentation sites with changelogs — `mkdir -p docs/v1 docs/v2`
- Check `knowledge` and `prerequisites: swagger-cli, redoc-cli, openapi-generator`

### 2. Reason — think for `api-doc-spec-migration`
- For `spec-migration`: Convert and upgrade OpenAPI specs between versions — decide which checks to run
- For `doc-versioning`: Publish versioned documentation sites with changelogs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-doc-spec-migration` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Redocly` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-doc-spec-migration:69aa5225`

# API Doc (Migration & Versioning)

Upgrades and restructures API documentation across spec versions.

## When to Use
- Swagger 2.0 to OpenAPI 3.0 migration
- Docs out of sync with multiple versions
- Reorganizing a docs site

## Real Commands

```bash
# Convert spec
npx swagger2openapi -y swagger.yaml > openapi3.yaml
swagger-cli validate openapi3.yaml

# Lint migrated spec
npx @stoplight/spectral-cli lint --extends spectral:oas openapi3.yaml

# Versioned docs
mkdir -p docs/v1 docs/v2
redocly build-docs docs/v2/openapi.yaml -o public/v2/index.html

# Changelog discipline
git tag v2.0.0 && git push origin v2.0.0
```

## Migration Checklist
1. Convert with swagger2openapi
2. Fix `$ref` and discriminator changes
3. Validate and lint
4. Diff old vs new rendered docs

## Testing
Render both versions and walk every example link.

## Best Practices
- Never edit docs by hand; regenerate from spec
- Keep one changelog entry per breaking change

## Capabilities

### spec-migration
Convert and upgrade OpenAPI specs between versions

**Parameters:**
- `input` (string): Source spec file
- `output` (string): Target spec file

**Commands:**
- `npx swagger2openapi swagger.yaml -o openapi3.yaml`
- `npx swagger2openapi -y swagger.yaml > openapi3.yaml`
- `redocly bundle openapi3.yaml -o bundled.yaml`
- `swagger-cli validate openapi3.yaml`
- `npx @stoplight/spectral-cli lint --extends spectral:oas openapi3.yaml`

**Examples:**
- npx swagger2openapi -y swagger.yaml > openapi3.yaml && swagger-cli validate openapi3.yaml
- redocly bundle openapi3.yaml -o bundled.yaml
- npx @stoplight/spectral-cli lint --extends spectral:oas openapi3.yaml

### doc-versioning
Publish versioned documentation sites with changelogs

**Parameters:**
- `version` (string): API version
- `spec` (string): Spec path per version

**Commands:**
- `mkdir -p docs/v1 docs/v2`
- `redocly build-docs docs/v2/openapi.yaml -o public/v2/index.html`
- `node -e "const fs=require('fs');fs.writeFileSync('docs/CHANGELOG.md','# Changelog\n\n## v2.0.0\n- Breaking: renamed /items to /products\n')"`
- `git tag v2.0.0 && git push origin v2.0.0`
- `node -e "console.log(new Date().toISOString())"`

**Examples:**
- redocly build-docs docs/v2/openapi.yaml -o public/v2/index.html
- node -e "const fs=require('fs');fs.writeFileSync('docs/CHANGELOG.md','# Changelog\n\n## v2.0.0\n- Breaking: renamed /items to /products\n')"
- git tag v2.0.0 && git push origin v2.0.0

## References
- [swagger2openapi](https://github.com/Mermade/oas-kit)
- [Redocly Build Docs](https://redocly.com/docs/cli/commands/build-docs/)