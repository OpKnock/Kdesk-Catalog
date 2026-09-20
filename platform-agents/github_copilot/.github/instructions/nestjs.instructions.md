---
applyTo: "**/*.r **/*.scala **/*.sh **/*.{ts,tsx}"
---

Builds structured Node.js services with NestJS: modules, controllers, providers, CLI scaffolding, and testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @nestjs/cli new myapp`, `npm test`
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
