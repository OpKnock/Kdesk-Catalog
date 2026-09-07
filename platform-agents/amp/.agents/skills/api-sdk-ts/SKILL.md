---
name: "api-sdk-ts"
description: "Builds TypeScript SDKs: tsup bundling with ESM/CJS and d.ts, tsc type checking, typedoc API docs, and npm publishing flow. Use when working with ts build, ts docs or when the user mentions ts build, ts docs."
license: "MIT"
compatibility: "Requires openapi-generator, node.js, python, typescript."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(npm:*) Bash(npx:*)"
---

Builds TypeScript SDKs: tsup bundling with ESM/CJS and d.ts, tsc type checking, typedoc API docs, and npm publishing flow.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -D tsup typescript typedoc`, `npx typedoc src/index.ts --out docs`
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

# API SDK v2 - TypeScript

TypeScript SDK building.

## What This Skill Does
- Bundles ESM/CJS with d.ts output
- Type-checks and generates docs
- Publishes clean npm packages

## When to Use
- Building TS SDKs for distribution
- Maintaining type-safe clients
- Publishing to npm

## Real Commands

```bash
npm install -D tsup typescript typedoc
npx tsup src/index.ts --format cjs,esm --dts
npx tsc --noEmit
npx typedoc src/index.ts --out docs
```

## tsup Config

```ts
import { defineConfig } from 'tsup';
export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  clean: true,
  sourcemap: true
});
```

## Testing
- Run tsc --noEmit before release
- Verify dual-format require/import both work
- Check npm pack contents

## Best Practices
- Export types from index
- Set files in package.json
- Add exports map for ESM/CJS resolution

## Capabilities

### ts-build
Bundle a TypeScript SDK with tsup

**Parameters:**
- `entry` (string): Entry point file
- `formats` (string): cjs, esm, iife
- `outDir` (string): Output directory

**Commands:**
- `npm install -D tsup typescript typedoc`
- `npx tsup src/index.ts --format cjs,esm --dts`
- `npx tsc --noEmit`
- `npx tsup src/index.ts --format cjs,esm --dts --clean`
- `npm run build`

**Examples:**
- tsup --format cjs,esm emits dual-format bundles
- --dts generates type declarations
- tsc --noEmit type-checks the source

### ts-docs
Generate API documentation with typedoc

**Commands:**
- `npx typedoc src/index.ts --out docs`
- `npx typedoc --entryPointStrategy expand src --out docs`
- `npm pack --dry-run`
- `npm publish`

**Examples:**
- -cli --help
- -api --help

## References
- [tsup Docs](https://tsup.egoist.dev/)
- [TypeDoc Docs](https://typedoc.org/)
