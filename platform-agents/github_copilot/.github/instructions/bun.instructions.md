---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx}"
---

# Bun

Develops and runs JavaScript/TypeScript backend services with the Bun runtime, bundler, test runner, and package manager.

## Instructions

# Bun

Backend development with the Bun runtime and toolchain.

## When to Use

- Running TypeScript server code without a separate compile step
- Building APIs with Bun.serve, Hono, or Elysia
- Packaging services as single-file executables with bun compile
- Fast installs and task running where npm is slow

## Commands

```bash
# Scaffold a new project
bun init

# Install dependencies from package.json
bun install

# Add a dependency
bun add hono
bun add -d typescript

# Run a script or TS file directly
bun run dev
bun run src/server.ts

# Test runner
bun test
bun test --coverage

# Benchmark
bun bench

# Lint and format
bun lint
bun fmt --check

# Compile to a standalone binary
bun compile --outfile app server.ts
```

## HTTP Server

```typescript
// server.ts
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response(`Hello ${new URL(req.url).pathname}`);
  },
});
console.log(`Listening on ${server.url}`);
```

## Best Practices

- Use bunx instead of npx for one-off tools
- Run bun --bun to force Bun over node when scripts call node
- Put shared types in a single tsconfig with strict mode
- Use bun test --coverage in CI to enforce thresholds
- Compile production binaries with bun compile --minify for smaller artifacts
- Pin bun.lock in version control for reproducible installs

## Capabilities

### bun-runtime
Initialize projects, run scripts, and compile executables with Bun.

**Commands:**
- `bun init`
- `bun install`
- `bun run dev`
- `bun run build`
- `bun compile --outfile app server.ts`

**Examples:**
- bun init -y
- bun run src/server.ts --port 3000
- bun compile --minify --outfile api main.ts

### bun-testing
Run unit tests, benchmarks, and linting.

**Commands:**
- `bun test`
- `bun test --coverage`
- `bun bench`
- `bun lint`
- `bun fmt --check`

**Examples:**
- bun test test/unit/*.test.ts
- bun bench bench/parse.bench.ts
- bun test --coverage --coverage-reporter=text
