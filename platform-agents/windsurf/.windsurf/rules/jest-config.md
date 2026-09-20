---
trigger: glob
description: "Configures Jest for JS/TS projects: presets, coverage thresholds, module mappers, reporters, and watch plugins. Use when working with jest initialization, config options, coverage and reporters, testing or when the user mentions jest initialization, config options, coverage and reporters, testing."
globs: ["**/*.r", "**/*.sh"]
---

Configures Jest for JS/TS projects: presets, coverage thresholds, module mappers, reporters, and watch plugins.

## Agentic Workflow: Read -> Reason -> Act (jest-config)

You are **jest-config** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `jest-config`
- Domain: Configures Jest for JS/TS projects: presets, coverage thresholds, module mappers, reporters, and watch plugins.
- **jest-initialization**: Initialize and inspect Jest configuration. — `npx jest --init`
- **config-options**: Configure environments, mappers, and transforms. — `npx jest --env=jsdom`
- **coverage-and-reporters**: Coverage thresholds and custom reporters. — `npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `jest-config`
- For `jest-initialization`: Initialize and inspect Jest configuration. — decide which checks to run
- For `config-options`: Configure environments, mappers, and transforms. — decide which checks to run
- For `coverage-and-reporters`: Coverage thresholds and custom reporters. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `jest-config` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `jest-config:df955c33`

# Jest Configuration

Tune Jest for your project's testing needs.

## What This Skill Does

- Initializes and validates Jest configs
- Sets environments, transforms, and module mappers
- Configures coverage thresholds and reporters
- Optimizes watch mode and caching

## When to Use

- Setting up Jest for a new project
- Migrating tests between environments
- Enforcing coverage policies

## Real Commands

```bash
# Init and inspect
npx jest --init
npx jest --showConfig
npx jest --listTests

# Runtime config flags
npx jest --env=jsdom
npx jest --testMatch='**/*.test.ts'
npx jest --moduleNameMapper='{"^@/(.*)$":"<rootDir>/src/$1"}'

# Coverage
npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
npx jest --coverageReporters=lcov,text-summary

# Reporters
npx jest --reporters=default --reporters=jest-junit
```

## jest.config.js

```js
module.exports = {
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  coverageThreshold: {
    global: { lines: 80, statements: 80, branches: 70, functions: 80 }
  }
};
```

## Best Practices

- Keep config in code (jest.config.js) for reviewability
- Use setupFilesAfterEnv for global mocks
- Set thresholds that fail the build on regression
- Cache mappers/transforms to keep suites fast
- Document non-obvious moduleNameMapper aliases

## Capabilities

### jest-initialization
Initialize and inspect Jest configuration.

**Parameters:**
- `showConfig` (boolean): Print resolved config
- `debug` (boolean): Print config debugging info

**Commands:**
- `npx jest --init`
- `npx jest --showConfig`
- `npx jest --listTests`
- `npx jest --clearCache`
- `npx jest --debug`

**Examples:**
- npx jest --init
- npx jest --showConfig
- npx jest --listTests

### config-options
Configure environments, mappers, and transforms.

**Parameters:**
- `env` (string): Test environment: node, jsdom
- `testMatch` (array): Test file patterns
- `moduleNameMapper` (object): Module alias mapping

**Commands:**
- `npx jest --env=jsdom`
- `npx jest --testMatch='**/*.test.ts'`
- `npx jest --testPathIgnorePatterns=/node_modules/`
- `npx jest --moduleNameMapper='{"^@/(.*)$":"demo-rootdir/src/$1"}'`
- `npx jest --coverage`

**Examples:**
- npx jest --env=jsdom
- npx jest --testMatch='**/*.test.ts'
- npx jest --moduleNameMapper='{"^@/(.*)$":"demo-rootdir/src/$1"}'

### coverage-and-reporters
Coverage thresholds and custom reporters.

**Parameters:**
- `coverageThreshold` (object): Global or per-file thresholds
- `coverageReporters` (array): Report formats: lcov, html, text

**Commands:**
- `npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'`
- `npx jest --coverageReporters=lcov,text-summary`
- `npx jest --reporters=default --reporters=jest-junit`
- `npx jest --coverageDirectory=coverage`

**Examples:**
- npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
- npx jest --coverageReporters=lcov,text-summary
- npx jest --reporters=default --reporters=jest-junit

## References
- [Jest Configuration](https://jestjs.io/docs/configuration)
- [Jest CLI Options](https://jestjs.io/docs/cli)
