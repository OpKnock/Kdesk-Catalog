---
trigger: glob
description: "Start, inspect, and stop test containers. JUnit integration with it handling Java. Node.js integration with it package. and services."
globs: ["**/*.go", "**/*.java", "**/*.r", "**/*.sh", "**/*.sql"]
---

# testcontainers

Start, inspect, and stop test containers. JUnit integration with it handling Java. Node.js integration with it package. and services.

## Instructions

# Testcontainers

Run real dependencies in tests with throwaway containers.

## What This Skill Does

- Starts databases, brokers, and services per test suite
- Manages lifecycle automatically (start, wait, stop)
- Maps random ports to avoid conflicts
- Works with Java, Node, Go, and .NET test runners

## When to Use

- Integration tests that need a real Postgres/Redis
- Testing against real message brokers
- Replacing in-memory mocks with actual services

## Real Commands

```bash
# Inspect running test containers
docker ps --filter name=testcontainer
docker logs $(docker ps -q --filter name=testcontainer-postgres)

# Java
mvn test -Dtest=OrderRepositoryIT
mvn verify
./gradlew test --tests "*ContainerTest"

# Node
npm test
npx jest --runInBand tests/db.test.js
```

## Java Example

```java
@Testcontainers
class OrderRepositoryIT {
  @Container
  static PostgreSQLContainer<?> postgres =
      new PostgreSQLContainer<>("postgres:16");

  @Test
  void persistsOrder() {
    // dataSource points at postgres.getJdbcUrl()
  }
}
```

## Best Practices

- Scope containers to the suite, not each test
- Use wait strategies (healthcheck) before asserting
- Cap parallel containers to avoid resource exhaustion
- Clean up images after CI runs
- Keep container versions pinned to match production

## Capabilities

### container-lifecycle
Start, inspect, and stop test containers.

**Commands:**
- `docker ps --filter name=testcontainer`
- `docker logs $(docker ps -q --filter name=testcontainer-postgres)`
- `docker network ls`
- `docker image prune -f`
- `mvn test -Dtest=PostgresContainerTest`

**Examples:**
- docker logs $(docker ps -q --filter name=testcontainer-postgres)
- docker ps --filter name=testcontainer
- mvn test -Dtest=PostgresContainerTest

### testcontainers-java
JUnit integration with Testcontainers for Java.

**Commands:**
- `mvn test -Dtest=OrderRepositoryIT`
- `mvn verify`
- `./gradlew test --tests "*ContainerTest"`
- `mvn test -Dcontainers.maxNumberOfContainers=4`

**Examples:**
- mvn test -Dtest=OrderRepositoryIT
- ./gradlew test --tests "*ContainerTest"
- mvn verify

### testcontainers-node
Node.js integration with testcontainers package.

**Commands:**
- `npm test`
- `npx jest --runInBand tests/db.test.js`
- `node --test tests/containers.test.js`
- `docker stats --no-stream $(docker ps -q --filter name=testcontainer)`

**Examples:**
- npm test
- npx jest --runInBand tests/db.test.js
- docker stats --no-stream $(docker ps -q --filter name=testcontainer)
