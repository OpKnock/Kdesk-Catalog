---
trigger: glob
description: "Static type checking with TypeScript: strictness, incremental builds, and monorepo project references. Use when working with tsc checking, code quality or when the user mentions tsc checking, code quality."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{ts,tsx}", "**/*.{yaml,yml}"]
---

Static type checking with TypeScript: strictness, incremental builds, and monorepo project references.

## Agentic Workflow: Read -> Reason -> Act (type-checking)

You are **type-checking** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `type-checking`
- Domain: Static type checking with TypeScript: strictness, incremental builds, and monorepo project references.
- **tsc-checking**: Type-check TypeScript projects with configurable strictness and outputs — `tsc --noEmit`
- Check `knowledge` and `prerequisites: tsc`

### 2. Reason — think for `type-checking`
- For `tsc-checking`: Type-check TypeScript projects with configurable strictness and outputs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `type-checking` tools
- Tools: `Glob`, `Grep`, `Read`, `Tsc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `type-checking:3da49e41`

# Type Checking

Runs the TypeScript compiler in no-emit mode to validate types across the project,
with strictness tuned per codebase.

## When to Use

- Pre-merge type gate in CI
- Verifying a refactor didn't break type contracts
- Onboarding strict mode incrementally

## Real Commands

```bash
# Basic check
npx tsc --noEmit

# Strict + unused checks
npx tsc --noEmit --strict --noUnusedLocals --noUnusedParameters

# Fast re-checks with incremental cache
npx tsc --noEmit --incremental --tsBuildInfoFile node_modules/.cache/tsbuildinfo

# CI-friendly output
npx tsc -p tsconfig.json --pretty false

# Vue SFC projects
npx vue-tsc --noEmit

# Monorepo with project references
npx tsc --build
```

## CI

```yaml
- name: Type check
  run: npx tsc --noEmit --pretty false
```

## Strict-mode rollout

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

## Best Practices

- Enforce `strict` in new projects; migrate old ones package by package
- Use `--incremental` locally, disable or persist cache in CI
- Add `skipLibCheck: true` to avoid slow .d.ts checking
- Fail CI on any error: `tsc --noEmit --pretty false` exit code is 1 on errors

## Example Response

Reports each error as `path(file):line:col - TSxxxx: message`, grouped by file,
plus the total error count and suggestions for fixing each category.

## Capabilities

### tsc-checking
Type-check TypeScript projects with configurable strictness and outputs

**Parameters:**
- `noEmit` (boolean): Type-check without emitting files
- `project` (string): Path to tsconfig.json to use
- `strict` (boolean): Enable all strict type-checking options

**Commands:**
- `tsc --noEmit`
- `tsc -p tsconfig.json --pretty false`
- `tsc --noEmit --strict --noUnusedLocals`
- `tsc --noEmit --incremental --tsBuildInfoFile .cache/tsconfig.tsbuildinfo`
- `tsc --noEmit --project tsconfig.build.json`

**Examples:**
- npx vue-tsc --noEmit
- tsc --noEmit --composite false
- tsc --build --force

## References
- [TypeScript compiler options](https://www.typescriptlang.org/tsconfig)
- [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/)
