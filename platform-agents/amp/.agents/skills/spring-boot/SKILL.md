---
name: "spring-boot"
description: "Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs filtered test suites."
---

# Spring Boot

Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs filtered test suites.

## Instructions

# Spring Boot

Hand-crafted skill for the Spring Boot application lifecycle with Maven.

## What this skill does

- Generates Maven projects from start.spring.io with selected starters
- Runs the app in dev mode and probes actuator endpoints
- Packages an executable jar and runs the test suite

## When to use

- Starting or onboarding a Spring Boot service
- Local development loop: run, hit actuator, iterate
- Building a release artifact for deployment

## Real commands

```bash
# Scaffold a Maven project with web + actuator on Java 21
curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip && unzip -q demo.zip -d demo

# Dev run
./mvnw spring-boot:run

# Actuator health
curl -s localhost:8080/actuator/health

# Tests
./mvnw test
./mvnw test -Dtest=HelloControllerTest

# Package and run the jar
./mvnw package -DskipTests && java -jar target/demo-0.0.1-SNAPSHOT.jar
```

## application.yaml

```yaml
server:
  port: 8080
spring:
  application:
    name: demo
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

## Testing

```bash
./mvnw spring-boot:run &
curl -s localhost:8080/actuator/health | jq .status
./mvnw test
```

## Best practices

- Use the mvnw wrapper so builds are reproducible
- Expose only safe actuator endpoints in production
- Prefer the packaged jar over spring-boot:run in prod

## Capabilities

### spring-boot-lifecycle
Manages the Spring Boot application lifecycle with Maven. Generates projects from start.spring.io, runs in dev mode with spring-boot:run, probes actuator endpoints, packages executable JARs, and runs filtered test suites.

**Commands:**
- `curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip`
- `./mvnw spring-boot:run`
- `curl -s localhost:8080/actuator/health`
- `./mvnw test`
- `./mvnw test -Dtest=HelloControllerTest`
- `./mvnw package -DskipTests`
- `java -jar target/demo-0.0.1-SNAPSHOT.jar`

**Examples:**
- curl -s https://start.spring.io/starter.zip -d type=maven-project -d dependencies=web,actuator -d javaVersion=21 -o demo.zip
- ./mvnw spring-boot:run
- curl -s localhost:8080/actuator/health
- ./mvnw test
- ./mvnw package -DskipTests && java -jar target/demo-0.0.1-SNAPSHOT.jar
