# Helidon

Oracle Helidon microservices: helidon init project scaffolding, Maven builds, running SE/NT applications, and live reload development.

## Instructions

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
