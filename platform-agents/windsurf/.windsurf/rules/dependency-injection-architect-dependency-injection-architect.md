---
trigger: glob
description: "Designs dependency injection: container configuration, provider patterns, and scoping across frameworks. Use when working with di patterns or when the user mentions di patterns."
globs: ["**/*.r", "**/*.sh"]
---

Designs dependency injection: container configuration, provider patterns, and scoping across frameworks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx nest new app --package-manager npm`
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

# Dependency Injection Architect

Designs clean DI architectures: containers, provider scopes, factory providers,
and testability.

## When to Use

- Choosing container/framework setup for a new service
- Refactoring service classes toward DI
- Fixing scope misuse (singleton capturing request-scoped deps)

## Real Commands

```bash
# NestJS
sudo npx nest new app --package-manager npm
sudo npx nest g resource users
sudo npx nest g provider database
sudo npm run build && node dist/main.js

# Spring Boot
mvn spring-boot:run -Dspring-boot.run.profiles=dev
# Inspect the bean graph
curl -s localhost:8080/actuator/beans | jq '.contexts.application.beans | keys'

# .NET
sudo dotnet add package Microsoft.Extensions.DependencyInjection
sudo dotnet run --project src/App --environment Production
```

## Scoping Rules

- Singleton: shared state, stateless services
- Request/transient: per-call state
- Never inject request-scoped into singleton (captive dependency)

## Service Registration Example (NestJS)

```ts
@Module({
  providers: [
    DatabaseService,
    {
      provide: 'CONFIG',
      useFactory: (env: EnvService) => env.getConfig(),
      inject: [EnvService],
    },
  ],
})
export class AppModule {}
```

## Best Practices

- Depend on abstractions (interfaces), not concretions
- Register in composition root only
- Use factory providers for async/conditional dependencies
- Keep scopes explicit and consistent
- Test with real containers plus mocks for external IO

## Example Response

Diagrams the dependency graph, identifies scope violations (captive
dependencies), and refactors the registrations with tests.

## Capabilities

### di-patterns
Set up DI containers and providers in NestJS, Spring, and .NET

**Parameters:**
- `package-manager` (string): Package manager for nest new
- `profiles` (string): Spring profiles to activate
- `project` (string): dotnet project file for run

**Commands:**
- `npx nest new app --package-manager npm`
- `npx nest g resource users`
- `mvn spring-boot:run -Dspring-boot.run.profiles=dev`
- `dotnet add package Microsoft.Extensions.DependencyInjection`
- `npm run build && node dist/main.js`

**Examples:**
- npx nest g provider database
- curl -s localhost:8080/actuator/beans | jq '.contexts.application.beans | keys'
- dotnet run --project src/App --environment Production

## References
- [NestJS providers docs](https://docs.nestjs.com/fundamentals/custom-providers)
- [Spring dependency injection](https://docs.spring.io/spring-framework/reference/core/beans.html)
- [Microsoft DI docs](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
