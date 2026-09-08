---
trigger: glob
description: "Authors and publishes reusable Node.js middleware packages: factory functions, options handling, npm packaging, and consumer-facing API design. Use when working with package authoring, consumer validation or when the user mentions package authoring, consumer validation."
globs: ["**/*.r", "**/*.sh"]
---

Authors and publishes reusable Node.js middleware packages: factory functions, options handling, npm packaging, and consumer-facing API design.

## Agentic Workflow: Read -> Reason -> Act (api-middleware-specialist)

You are **api-middleware-specialist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-middleware-specialist`
- Domain: Authors and publishes reusable Node.js middleware packages: factory functions, options handling, npm packaging, and consumer-facing API design.
- **package-authoring**: Create a publishable middleware package with a factory function and options object — `npm init -y`
- **consumer-validation**: Validate the packaged artifact works when installed in a consumer project — `npm link`
- Check `knowledge` and `prerequisites: node.js, python, express, fastify`

### 2. Reason — think for `api-middleware-specialist`
- For `package-authoring`: Create a publishable middleware package with a factory function and options object — decide which checks to run
- For `consumer-validation`: Validate the packaged artifact works when installed in a consumer project — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-middleware-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-middleware-specialist:a54d3bf2`

# API Middleware Specialist

Authors reusable middleware libraries for the npm ecosystem.

## What This Skill Does
- Designs middleware as factory functions taking an options object
- Publishes middleware as standalone npm packages
- Validates artifacts with npm pack and consumer-project smoke tests

## When to Use
- Building a middleware library shared across multiple services
- Refactoring duplicated middleware into a package
- Releasing a middleware module to npm

## Real Commands

```bash
npm init -y
npm pack --dry-run   # preview tarball contents
npm link             # link locally for testing
node -e "const mw = require('./index.js'); console.log(typeof mw)"
npm publish --access public
```

## Package Structure
- index.js exports the factory function
- README.md documents options and ordering requirements
- engines field pins supported Node.js versions

## Testing
- Smoke-test the packed tarball in a scratch consumer project
- Assert the factory returns a function of arity 3 (req, res, next)
- Run npm ls to confirm no extraneous dependencies

## Best Practices
- Validate options at factory creation time, fail fast
- Never mutate req/res globals without opt-in flags
- Mark Express and Fastify as peerDependencies

## Capabilities

### package-authoring
Create a publishable middleware package with a factory function and options object

**Parameters:**
- `options` (object): Middleware factory options with defaults and validation
- `main` (string): Entry point in package.json consumed by require()
- `peerDependencies` (object): Express/Fastify version ranges the middleware supports

**Commands:**
- `npm init -y`
- `npm pack --dry-run`
- `npm publish`
- `node -e "const mw = require('./index.js'); console.log(typeof mw)"`
- `npx npm-check-updates -u`

**Examples:**
- npm pack --dry-run lists files before publishing
- module.exports = (options = {}) => (req, res, next) => next()
- npm publish --access public publishes to the npm registry

### consumer-validation
Validate the packaged artifact works when installed in a consumer project

**Commands:**
- `npm link`
- `npm install ../my-middleware --save`
- `node -e "const mw = require('my-middleware'); console.log(mw().length)"`
- `npm ls --depth=0`

**Examples:**
- -cli --help
- -api --help

## References
- [npm Publishing Docs](https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry)
- [npm-check-updates](https://github.com/raineorshine/npm-check-updates)
