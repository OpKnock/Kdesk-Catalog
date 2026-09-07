---
name: "quarkus"
description: "Quarkus application development: CLI scaffolding, extensions, dev mode, testing and packaging. Use when working with quarkus workflow, api or when the user mentions quarkus workflow, api."
license: "MIT"
compatibility: "Requires ./mvnw, quarkus."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(./mvnw:*) Bash(quarkus:*)"
---

Quarkus application development: CLI scaffolding, extensions, dev mode, testing and packaging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `quarkus create app hello-world`
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

# Quarkus

Quarkus is a Kubernetes-native Java stack with fast startup, low RSS, and developer joy.

## What this skill does

- Scaffolds apps with the quarkus CLI
- Adds extensions for REST, persistence, messaging
- Runs dev mode and builds artifacts

## When to use

- New Java microservices
- Serverless/native deployments

## Real commands

```bash
# Create
quarkus create app hello-world
quarkus create app -P io.quarkus.platform:quarkus-bom:3.10.0 hello

# Dev mode
quarkus dev
quarkus dev --port 8081

# Extensions
quarkus ext add resteasy-reactive,resteasy-reactive-jackson
quarkus ext add hibernate-orm-panache,postgresql-client

# Build and test
quarkus build
./mvnw test
quarkus build --native
```

## REST endpoint

```java
@Path("/hello")
public class HelloResource {
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() { return "Hello Quarkus"; }
}
```

## application.properties

```properties
quarkus.http.port=8080
quarkus.datasource.db-kind=postgresql
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/app
```

## Best practices

- Use dev mode's continuous testing
- Profile and size before native builds
- Pin the BOM version in CI

## Capabilities

### quarkus-workflow
Create, extend, run and test Quarkus apps with the quarkus CLI and Maven.

**Parameters:**
- `extensions` (array): Extensions to add via quarkus ext add
- `port` (integer): Dev mode port
- `package_type` (string): fast-jar, uber-jar or native

**Commands:**
- `quarkus create app hello-world`
- `quarkus dev`
- `quarkus ext add resteasy-reactive,resteasy-reactive-jackson`
- `quarkus build`
- `./mvnw test`

**Examples:**
- quarkus create app -P io.quarkus.platform:quarkus-bom:3.10.0 hello
- quarkus dev --port 8081
- quarkus build --native

## References
- [Quarkus Guides](https://quarkus.io/guides/)
- [Quarkus CLI](https://quarkus.io/guides/cli-tooling)
