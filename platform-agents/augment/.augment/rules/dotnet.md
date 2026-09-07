---
type: agent_requested
description: "Develops .NET backend services with the dotnet CLI: projects, EF Core migrations, tests, and publish workflows. Use when working with dotnet cli, dotnet ef, dotnet testing, backend or when the user mentions dotnet cli, dotnet ef, dotnet testing, backend."
---

Develops .NET backend services with the dotnet CLI: projects, EF Core migrations, tests, and publish workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `dotnet new webapi -n MyApi`, `dotnet ef migrations add InitialCreate`
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

# .NET

Backend services with the dotnet CLI and ASP.NET Core.

## When to Use

- REST APIs with ASP.NET Core minimal APIs or controllers
- Enterprise services needing strong typing and EF Core ORM
- Cross-platform console tools and workers
- gRPC services with the built-in gRPC stack

## Commands

```bash
# Create a Web API project
dotnet new webapi -n MyApi

# Add to a solution
dotnet new sln -n App
dotnet sln add src/MyApi/MyApi.csproj

# Build, run, and watch
dotnet build
dotnet run
dotnet watch run

# Publish
dotnet publish -c Release -o ./publish

# Add packages
dotnet add package Newtonsoft.Json

# EF Core migrations
dotnet ef migrations add InitialCreate
dotnet ef database update
dotnet ef migrations list

# Tests
dotnet test
dotnet test --filter "FullyQualifiedName~OrderTests"

# Format
dotnet format
dotnet format --verify-no-changes
```

## Minimal API Example

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();
```

## Best Practices

- Use minimal APIs for small services, controllers for larger teams
- Enable nullable reference types and treat warnings as errors in CI
- Use EF Core migrations for schema and dotnet ef database update in deploys
- Pin target frameworks and run dotnet format --verify-no-changes in CI
- Use appsettings per-environment config with user secrets in dev

## Capabilities

### dotnet-cli
Create, build, and run .NET projects.

**Parameters:**
- `template` (string): Template name: webapi, console, classlib
- `name` (string): Project or solution name

**Commands:**
- `dotnet new webapi -n MyApi`
- `dotnet run`
- `dotnet build`
- `dotnet watch run`
- `dotnet publish -c Release -o ./publish`

**Examples:**
- dotnet new sln -n App
- dotnet watch run --launch-profile https
- dotnet publish -c Release --self-contained -r win-x64

### dotnet-ef
Manage Entity Framework Core migrations and schema.

**Parameters:**
- `name` (string): Migration name
- `context` (string): DbContext type

**Commands:**
- `dotnet ef migrations add InitialCreate`
- `dotnet ef database update`
- `dotnet ef migrations remove`
- `dotnet ef migrations list`
- `dotnet ef dbcontext info`

**Examples:**
- dotnet ef migrations add AddUserIndex --context AppDbContext
- dotnet ef database update --no-build
- dotnet ef migrations script

### dotnet-testing
Run tests and format code.

**Parameters:**
- `filter` (string): Test filter expression
- `coverage` (boolean): Collect code coverage with Coverlet

**Commands:**
- `dotnet test`
- `dotnet test --filter TestCategory=Unit`
- `dotnet format`
- `dotnet add package Newtonsoft.Json`

**Examples:**
- dotnet test --logger "console;verbosity=detailed"
- dotnet format --verify-no-changes
- dotnet test -p:CollectCoverage=true

## References
- [.NET Docs](https://learn.microsoft.com/dotnet)
- [EF Core Docs](https://learn.microsoft.com/ef/core/)
- [ASP.NET Core Docs](https://learn.microsoft.com/aspnet/core)