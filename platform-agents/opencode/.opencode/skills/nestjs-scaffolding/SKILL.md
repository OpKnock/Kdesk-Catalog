---
name: "nestjs-scaffolding"
description: "Scaffolds NestJS projects and generates modules, controllers, services, guards, and interceptors using the Nest CLI. Structures applications with dependency injection and modular architecture. Use when working with nestjs scaffolding, api or when the user mentions nestjs scaffolding, api."
---

Scaffolds NestJS projects and generates modules, controllers, services, guards, and interceptors using the Nest CLI. Structures applications with dependency injection and modular architecture.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nest new my-app --package-manager npm`
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
