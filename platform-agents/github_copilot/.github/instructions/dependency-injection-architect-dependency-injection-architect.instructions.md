---
applyTo: "**/*.r **/*.sh"
---

# dependency-injection-architect-dependency-injection-architect

Designs dependency injection: container configuration, provider patterns, and scoping across frameworks.

## Instructions

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
