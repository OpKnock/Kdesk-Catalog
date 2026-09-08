---
trigger: glob
description: "Scaffolds NestJS projects and generates modules, controllers, services, guards, and interceptors using the Nest CLI. Structures applications with dependency injection and modular architecture. Use when working with nestjs scaffolding, api or when the user mentions nestjs scaffolding, api."
globs: ["**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
---

Scaffolds NestJS projects and generates modules, controllers, services, guards, and interceptors using the Nest CLI. Structures applications with dependency injection and modular architecture.

## Agentic Workflow: Read -> Reason -> Act (nestjs-scaffolding)

You are **Nestjs Scaffolding** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nestjs-scaffolding`
- Domain: Scaffolds NestJS projects and generates modules, controllers, services, guards, and interceptors using the Nest CLI. Structures applications with dependency injection and modular architecture.
- **nestjs-scaffolding**: Scaffold NestJS projects and generate modules, controllers, services and guards with the Nest CLI. — `nest new my-app --package-manager npm`
- Check `knowledge` and `prerequisites: nest, npm`

### 2. Reason — think for `nestjs-scaffolding`
- For `nestjs-scaffolding`: Scaffold NestJS projects and generate modules, controllers, services and guards with the Nest CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nestjs-scaffolding` tools
- Tools: `Glob`, `Grep`, `Read`, `Nest`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nestjs-scaffolding:afdef314`

# NestJS

NestJS is a progressive Node.js framework with TypeScript, dependency injection and a modular architecture.

## What this skill does

- Scaffolds projects and generates components with the CLI
- Structures modules, controllers and providers
- Adds guards, interceptors and validation

## When to use

- TypeScript backend services with structure
- Teams that want conventions and DI

## Real commands

```bash
# New project
nest new my-app --package-manager npm

# Generate components
nest g module auth
nest g controller users
nest g service users
nest g guard roles --flat

# Develop
npm run start:dev
npm run lint
```

## Minimal controller

```typescript
@Controller('users')
export class UsersController {
  constructor(private readonly users: UsersService) {}
  @Get(':id')
  findOne(@Param('id') id: string) { return this.users.findOne(id); }
}
```

## Module wiring

```typescript
@Module({
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}
```

## Best practices

- One module per domain feature
- Use guards for auth, pipes for validation
- Run `npm run lint` and `npm run build` before commit

## Capabilities

### nestjs-scaffolding
Scaffold NestJS projects and generate modules, controllers, services and guards with the Nest CLI.

**Parameters:**
- `package_manager` (string): npm, yarn or pnpm
- `name` (string): Component name for code generation
- `flat` (boolean): Skip the subdirectory when generating

**Commands:**
- `nest new my-app --package-manager npm`
- `nest g module auth`
- `nest g controller users`
- `nest g service users`
- `npm run start:dev`

**Examples:**
- nest g guard roles --flat
- nest g interceptor logging --flat
- npm run lint

## References
- [NestJS Documentation](https://docs.nestjs.com/)
- [Nest CLI Reference](https://docs.nestjs.com/cli/usages)
