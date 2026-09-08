---
name: "asyncapi-java"
description: "Generates Java Spring Boot projects and POJO models from AsyncAPI documents, then builds, runs, and tests them with Maven. Use when working with spring generation, java models, api or when the user mentions spring generation, java models, api."
---

Generates Java Spring Boot projects and POJO models from AsyncAPI documents, then builds, runs, and tests them with Maven.

## Agentic Workflow: Read -> Reason -> Act (asyncapi-java)

You are **Asyncapi Java** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `asyncapi-java`
- Domain: Generates Java Spring Boot projects and POJO models from AsyncAPI documents, then builds, runs, and tests them with Maven.
- **spring-generation**: Generate a Spring Boot async API project from a spec. — `npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./genera`
- **java-models**: Generate Java POJOs from the spec schema with Modelina. — `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/main/java -`
- Check `knowledge` and `prerequisites: java, mvn, npx`

### 2. Reason — think for `asyncapi-java`
- For `spring-generation`: Generate a Spring Boot async API project from a spec. — decide which checks to run
- For `java-models`: Generate Java POJOs from the spec schema with Modelina. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `asyncapi-java` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Cd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `asyncapi-java:0df6f96c`

# AsyncAPI Java

## What this skill does

Generates Java/Spring Boot applications from AsyncAPI documents with the java-spring-template, generates POJOs with Modelina, and builds/runs/tests with Maven.

## When to use

- Bootstrapping a Spring Boot event consumer/producer from a spec
- Keeping Java payload classes in sync with message schemas
- Moving an existing JMS/Kafka app onto spec-driven generation

## Real commands

```bash
# Generate a Spring Boot project
npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./generated

# Build and run
cd generated
./mvnw clean package
./mvnw spring-boot:run

# Generate POJOs
npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/main/java --language Java --packageName com.example.orders
mvn compile

# Verify health
curl -s http://localhost:8080/actuator/health
```

## Generated structure

- src/main/java/.../handler/ - message listeners
- src/main/resources/application.yml - broker connection
- POJOs in the package you pass with Modelina

## Testing

- ./mvnw test runs generated unit tests
- Publish a message to the broker and assert the handler logs it

## Best practices

- Override broker settings via Spring profiles
- Regenerate and diff in CI
- Use Testcontainers Kafka for hermetic integration tests

## Capabilities

### spring-generation
Generate a Spring Boot async API project from a spec.

**Parameters:**
- `output` (string): Output directory for the generated project
- `param` (string): Template params, e.g. server=kafka

**Commands:**
- `npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./generated`
- `cd generated && ./mvnw clean package`
- `cd generated && ./mvnw spring-boot:run`
- `curl -s http://localhost:8080/actuator/health`
- `java -jar target/asyncapi-spring-0.0.1-SNAPSHOT.jar`

**Examples:**
- npx @asyncapi/generator asyncapi.yaml @asyncapi/java-spring-template -o ./generated --force-write
- cd generated && ./mvnw test
- cd generated && java -jar target/asyncapi-spring-0.0.1-SNAPSHOT.jar

### java-models
Generate Java POJOs from the spec schema with Modelina.

**Parameters:**
- `package_name` (string): Java package for generated models
- `type_mapping` (string): Custom type mapping, e.g. string=UUID

**Commands:**
- `npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/main/java --language Java`
- `mvn compile`
- `mvn test`
- `mvn package -DskipTests`

**Examples:**
- npx @asyncapi/modelina generate --input asyncapi.yaml --output ./src/main/java --language Java --packageName com.example.orders
- mvn package
- mvn dependency:tree | grep kafka

## References
- [Java Spring Template](https://github.com/asyncapi/java-spring-template)
- [Modelina Java](https://www.asyncapi.com/docs/tools/modelina/languages/Java)
- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
