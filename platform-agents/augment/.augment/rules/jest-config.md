---
type: agent_requested
description: "Configures Jest for JS/TS projects: presets, coverage thresholds, module mappers, reporters, and watch plugins."
---

# jest-config

Configures Jest for JS/TS projects: presets, coverage thresholds, module mappers, reporters, and watch plugins.

## Instructions

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

**Commands:**
- `npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'`
- `npx jest --coverageReporters=lcov,text-summary`
- `npx jest --reporters=default --reporters=jest-junit`
- `npx jest --coverageDirectory=coverage`

**Examples:**
- npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
- npx jest --coverageReporters=lcov,text-summary
- npx jest --reporters=default --reporters=jest-junit