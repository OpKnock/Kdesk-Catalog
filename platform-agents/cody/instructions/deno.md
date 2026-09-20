# Deno

Builds secure TypeScript services with the Deno runtime using built-in permissions, std library, test runner, and compilation.

## Instructions

# Deno

Secure TypeScript runtime with built-in tooling.

## When to Use

- TypeScript-first services without npm toolchain overhead
- Edge functions and serverless workloads on Deno Deploy
- Scripts that need explicit permission grants (network, fs)
- Single-file tools distributed as compiled binaries

## Commands

```bash
# Scaffold
deno init

# Run with explicit permissions
deno run --allow-net main.ts
deno run --allow-net --allow-read=./data main.ts

# Type-check without running
deno check main.ts

# Formatting and linting
deno fmt
deno fmt --check
deno lint

# Testing
deno test
deno test --coverage

# Benchmark
deno bench

# Compile to a standalone binary
deno compile --allow-net -o app main.ts

# Task runner from deno.json
deno task dev
```

## Server Example

```typescript
Deno.serve((req) => {
  const url = new URL(req.url);
  return new Response(`Hello ${url.pathname}`);
});
```

## Best Practices

- Grant the narrowest permissions: prefer --allow-net=host:port over full access
- Put scripts and deps in deno.json; use deno task for commands
- Check imports with deno check --all before pushing
- Pin import versions; Deno supports npm: specifiers for interop
- Use deno compile in CI to ship native binaries

## Capabilities

### deno-runtime
Scaffold, run, and compile Deno projects.

**Commands:**
- `deno init`
- `deno run main.ts`
- `deno run --allow-net --allow-env main.ts`
- `deno check main.ts`
- `deno compile --allow-net -o app main.ts`

**Examples:**
- deno run --allow-net --allow-read=./data main.ts
- deno compile --target x86_64-unknown-linux-gnu -o app main.ts
- deno check --all src/

### deno-quality
Format, lint, and test Deno code.

**Commands:**
- `deno fmt`
- `deno fmt --check`
- `deno lint`
- `deno test`
- `deno test --coverage`

**Examples:**
- deno fmt --check src/
- deno lint --rules-exclude=no-explicit-any
- deno test test/ --coverage=coverage
