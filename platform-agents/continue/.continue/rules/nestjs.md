---
name: "nestjs"
description: "Builds structured Node.js services with NestJS: modules, controllers, providers, CLI scaffolding, and testing. Use when working with nestjs cli, nestjs testing, backend or when the user mentions nestjs cli, nestjs testing, backend."
globs: ["**/*.r", "**/*.scala", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

Builds structured Node.js services with NestJS: modules, controllers, providers, CLI scaffolding, and testing.

## Agentic Workflow: Read -> Reason -> Act (nestjs)

You are **nestjs** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `nestjs`
- Domain: Builds structured Node.js services with NestJS: modules, controllers, providers, CLI scaffolding, and testing.
- **nestjs-cli**: Scaffold modules, controllers, and services. — `npx @nestjs/cli new myapp`
- **nestjs-testing**: Run unit and e2e tests. — `npm test`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `nestjs`
- For `nestjs-cli`: Scaffold modules, controllers, and services. — decide which checks to run
- For `nestjs-testing`: Run unit and e2e tests. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nestjs` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nestjs:38c6b4c9`

# NestJS

Structured Node.js framework for scalable services.

## When to Use

- Services needing clear module boundaries and dependency injection
- Teams that want opinionated structure and conventions
- APIs combining REST, GraphQL, WebSockets, and microservices
- Enterprise Node.js with built-in testing support

## Commands

```bash
# New app
npx @nestjs/cli new myapp

# Scaffolding
npx nest generate module orders
npx nest generate controller orders
npx nest generate service orders
npx nest generate pipe validation

# Run
npm run start:dev
npm run start -- --watch

# Tests
npm test
npm run test:e2e
```

## Module Example

```typescript
// orders.module.ts
@Module({
  imports: [DatabaseModule],
  controllers: [OrdersController],
  providers: [OrdersService],
})
export class OrdersModule {}
```

```typescript
// orders.controller.ts
@Controller("orders")
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

  @Get(":id")
  findOne(@Param("id") id: string) {
    return this.ordersService.findOne(id);
  }
}
```

## Best Practices

- One resource per module with clear imports/exports
- Use guards for auth and pipes for validation at boundaries
- Keep services free of HTTP concerns
- Write unit tests with jest mocks for providers
- Run e2e tests against a real test database in CI
- Follow the nest CLI naming for consistency

## Capabilities

### nestjs-cli
Scaffold modules, controllers, and services.

**Parameters:**
- `name` (string): Element name
- `type` (string): module, controller, service, pipe, guard

**Commands:**
- `npx @nestjs/cli new myapp`
- `npx nest generate module orders`
- `npx nest generate controller orders`
- `npx nest generate service orders`
- `npm run start:dev`

**Examples:**
- npx nest g resource users --no-spec
- npx nest generate pipe validation
- npm run start -- --watch

### nestjs-testing
Run unit and e2e tests.

**Parameters:**
- `testPathPattern` (string): Test name pattern
- `e2e` (boolean): Run the end-to-end suite

**Commands:**
- `npm test`
- `npm run test:e2e`
- `npm run test -- --testPathPattern="orders"`
- `npm run test -- --coverage`

**Examples:**
- npm run test:e2e -- --runInBand
- npm run test -- --watch

## References
- [NestJS Docs](https://docs.nestjs.com)
- [NestJS CLI Reference](https://docs.nestjs.com/cli/overview)