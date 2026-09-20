---
type: agent_requested
description: "gRPC services and clients in C# with Grpc.Net.Client, Grpc.Tools proto codegen, and dotnet CLI project scaffolding. Use when working with csharp grpc, api or when the user mentions csharp grpc, api."
---

gRPC services and clients in C# with Grpc.Net.Client, Grpc.Tools proto codegen, and dotnet CLI project scaffolding.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `dotnet new grpc -o GrpcGreeter`
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

# gRPC C#

Build gRPC services and clients in .NET with Grpc.Net.Client and Grpc.Tools.

## What this skill does

- Scaffolds gRPC service and client projects with the dotnet CLI.
- Generates C# code from proto files at build time via Grpc.Tools.
- Calls unary, streaming, and server-streaming RPCs from client apps.
- Configures channels, deadlines, and interceptors.

## When to use

- A .NET backend needs internal RPC communication.
- Porting an existing proto contract into a C# microservice.
- Adding gRPC health checks to an ASP.NET Core service.

## Real commands

```bash
# Scaffold a service
dotnet new grpc -o GrpcGreeter
cd GrpcGreeter

# Client-side packages
dotnet add package Grpc.Net.Client
dotnet add package Google.Protobuf
dotnet add package Grpc.Tools

# Build and run
dotnet build
dotnet run
```

## csproj proto codegen

```xml
<ItemGroup>
  <Protobuf Include="Protos\greet.proto" GrpcServices="Server" />
  <Protobuf Include="Protos\greet.proto" GrpcServices="Client" />
</ItemGroup>
```

## Client call

```csharp
using var channel = GrpcChannel.ForAddress("https://localhost:5001");
var client = new Greeter.GreeterClient(channel);
var reply = await client.SayHelloAsync(new HelloRequest { Name = "Ada" });
Console.WriteLine(reply.Message);
```

## Testing

```bash
dotnet test
dotnet run --project GrpcGreeter &
curl -s http://localhost:5001/greet/ada  # if grpc-gateway endpoint exposed
```

## Best practices

- Use one shared GrpcChannel per service, not one per call.
- Set deadlines: `client.SayHelloAsync(req, deadline: DateTime.UtcNow.AddSeconds(5))`.
- Enable HTTP/2 cleartext on dev: `AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true)`.
- Keep protos in a shared class library so client and server reference the same contract.

## Example exchange

```
User: The client can't reach the local gRPC server over plain HTTP.
Agent: Enable unencrypted HTTP/2 support in the client, or run the server over HTTPS.
```

## Capabilities

### csharp-grpc
Scaffold .NET gRPC projects, generate code from proto files, and call services with Grpc.Net.Client.

**Parameters:**
- `project` (string): Project or solution path to build/run.
- `package` (string): NuGet package to add (Grpc.Net.Client, Grpc.Tools, Grpc.AspNetCore).
- `proto_file` (string): Proto file referenced in the csproj for codegen.

**Commands:**
- `dotnet new grpc -o GrpcGreeter`
- `dotnet add package Grpc.Net.Client`
- `dotnet add package Google.Protobuf`
- `dotnet add package Grpc.Tools`
- `dotnet run --project GrpcGreeter`

**Examples:**
- dotnet build GrpcGreeter && dotnet run --project GrpcGreeter
- dotnet add package Grpc.AspNetCore
- dotnet add GrpcGreeterClient reference GrpcGreeter

## References
- [gRPC C# Docs](https://grpc.io/docs/languages/csharp/)
- [gRPC on ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/grpc/)