Oracle Helidon microservices: helidon init project scaffolding, Maven builds, running SE/NT applications, and live reload development.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helidon init --flavor se --archetype quickstart --project-na`
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

# Helidon

Build microservices with Oracle Helidon SE and MP.

## What this skill does

- Scaffolds projects with the helidon CLI.
- Builds runnable jars with Maven.
- Runs SE (functional style) and MP (MicroProfile) apps.
- Uses dev-mode live reload for fast iteration.

## When to use

- A JVM team wants a lightweight microservice framework with native-image support.
- Migrating a JAX-RS app to MicroProfile (Helidon MP).
- Building low-footprint services for containers.

## Real commands

```bash
# Scaffold a Helidon SE project
helidon init --flavor se --archetype quickstart --project-name myapp
cd myapp

# Build and run
mvn package
java -jar target/myapp.jar

# Or run without packaging
mvn exec:java

# Dev mode with live reload
mvn helidon:dev

# Check the greeting endpoint
curl http://localhost:8080/greet
```

## Helidon SE skeleton

```java
public static void main(String[] args) {
    WebServer server = WebServer.builder()
        .port(8080)
        .addRouting(Routing.builder()
            .get("/greet", (req, res) -> res.send("Hello World"))
            .build())
        .build();
    server.start();
}
```

## Testing

```bash
curl -s http://localhost:8080/greet
curl -s http://localhost:8080/greet/World
```

## Best practices

- Use `helidon:dev` during development; package only for deploy.
- For native images, run `mvn package -Pnative-image` and test startup.
- Keep port 8080 configurable via `server.port` in application.yaml.
- Prefer SE for greenfield functional apps, MP for MicroProfile-compatible stacks.

## Example exchange

```
User: Create a new Helidon SE quickstart project called cart.
Agent: helidon init --flavor se --archetype quickstart --project-name cart && cd cart && mvn package
```

## Capabilities

### helidon-lifecycle
Scaffold, build, and run Helidon SE and Helidon MP applications.

**Parameters:**
- `flavor` (string): se (functional) or mp (MicroProfile) flavor.
- `archetype` (string): quickstart, database, or oci archetype.
- `project_name` (string): Generated project directory name.

**Commands:**
- `helidon init --flavor se --archetype quickstart --project-name myapp`
- `mvn package`
- `java -jar target/myapp.jar`
- `mvn exec:java`
- `curl http://localhost:8080/greet`

**Examples:**
- helidon init --flavor mp --archetype quickstart --project-name mymp
- mvn package && java -jar target/myapp.jar
- mvn -DskipTests package

## References
- [Helidon Docs](https://helidon.io/docs/latest/)
- [Helidon CLI](https://helidon.io/docs/latest/about/cli)