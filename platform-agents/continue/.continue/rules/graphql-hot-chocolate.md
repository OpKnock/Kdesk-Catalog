---
name: "Graphql Hot Chocolate"
description: "GraphQL in .NET with Hot Chocolate: build schemas from C# types, run the server, and use Banana Cake Pop for testing. Use when working with hotchocolate development, api or when the user mentions hotchocolate development, api."
globs: ["**/*.cs", "**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

GraphQL in .NET with Hot Chocolate: build schemas from C# types, run the server, and use Banana Cake Pop for testing.

## Agentic Workflow: Read -> Reason -> Act (graphql-hot-chocolate)

You are **Graphql Hot Chocolate** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `graphql-hot-chocolate`
- Domain: GraphQL in .NET with Hot Chocolate: build schemas from C# types, run the server, and use Banana Cake Pop for testing.
- **hotchocolate-development**: Scaffold Hot Chocolate servers, add packages, and run queries. — `dotnet add package HotChocolate.AspNetCore`
- Check `knowledge` and `prerequisites: dotnet`

### 2. Reason — think for `graphql-hot-chocolate`
- For `hotchocolate-development`: Scaffold Hot Chocolate servers, add packages, and run queries. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `graphql-hot-chocolate` tools
- Tools: `Glob`, `Grep`, `Read`, `Dotnet`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `graphql-hot-chocolate:de54e49f`

# GraphQL Hot Chocolate

## What this skill does

Hot Chocolate is the .NET GraphQL server from ChilliCream. It supports code-first (C# classes become schema types), schema-first (SDL), and a rich middleware pipeline.

## When to use

- Adding GraphQL to ASP.NET Core services
- .NET teams wanting strong typing end to end
- Reusing EF Core entities in the graph

## Real commands

```bash
# Add the package and run
 dotnet add package HotChocolate.AspNetCore
dotnet run

# Build and test
dotnet build --no-restore
 dotnet test

# Query the endpoint
curl -s -X POST http://localhost:5000/graphql -H 'Content-Type: application/json' -d '{"query":"{ books { title } }"}' | jq
```

## Program.cs example

```csharp
using HotChocolate;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddGraphQLServer().AddQueryType<Query>();

var app = builder.Build();
app.MapGraphQL();
app.Run();

public record Book(string Title, string Author);

public class Query
{
    public Book GetBook() => new("C# in Depth", "Jon Skeet");
}
```

## Testing

```bash
# Export the schema SDL
curl -s -X POST http://localhost:5000/graphql -H 'Content-Type: application/json' -d '{"query":"{ __schema { queryType { name } } }"}' | jq '.data'
```

## Best practices

- Prefer code-first for .NET services; it keeps types in sync.
- Use `[GraphQLName]` attributes for API naming conventions.
- Register resolvers via `[Service]` injection, not globals.
- Enable persisted operations for production caching.
- Use Banana Cake Pop for exploratory queries in dev.

## Capabilities

### hotchocolate-development
Scaffold Hot Chocolate servers, add packages, and run queries.

**Parameters:**
- `package` (string): Hot Chocolate package name
- `endpoint` (string): GraphQL endpoint path
- `schema-export` (string): Output path for schema SDL

**Commands:**
- `dotnet add package HotChocolate.AspNetCore`
- `dotnet run`
- `dotnet build --no-restore`
- `curl -s -X POST http://localhost:5000/graphql -H 'Content-Type: application/json' -d '{"query":"{ books { title } }"}' | jq`
- `dotnet test`

**Examples:**
- dotnet add package HotChocolate.AspNetCore && dotnet run
- curl -s -X POST http://localhost:5000/graphql -H 'Content-Type: application/json' -d '{"query":"{ books { title } }"}' | jq
- dotnet build --no-restore

## References
- [Hot Chocolate docs](https://chillicream.com/docs/hotchocolate)
- [Banana Cake Pop](https://chillicream.com/docs/bananacakepop)