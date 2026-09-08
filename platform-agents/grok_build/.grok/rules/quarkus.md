Quarkus application development: CLI scaffolding, extensions, dev mode, testing and packaging.

## Agentic Workflow: Read -> Reason -> Act (quarkus)

You are **Quarkus** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `quarkus`
- Domain: Quarkus application development: CLI scaffolding, extensions, dev mode, testing and packaging.
- **quarkus-workflow**: Create, extend, run and test Quarkus apps with the quarkus CLI and Maven. — `quarkus create app hello-world`
- Check `knowledge` and `prerequisites: ./mvnw, quarkus`

### 2. Reason — think for `quarkus`
- For `quarkus-workflow`: Create, extend, run and test Quarkus apps with the quarkus CLI and Maven. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `quarkus` tools
- Tools: `Glob`, `Grep`, `Read`, `Quarkus`, `./mvnw` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `quarkus:4ef7d0de`

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