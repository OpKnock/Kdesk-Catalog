---
name: "type-checking"
description: "Static type checking with TypeScript: strictness, incremental builds, and monorepo project references. Use when working with tsc checking, code quality or when the user mentions tsc checking, code quality."
license: "MIT"
compatibility: "Requires tsc."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(tsc:*)"
---

Static type checking with TypeScript: strictness, incremental builds, and monorepo project references.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tsc --noEmit`
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
