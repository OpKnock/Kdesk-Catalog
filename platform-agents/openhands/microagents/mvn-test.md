---
name: "mvn-test"
description: "Runs Java test suites with Maven Surefire and Failsafe, including test filters, parallel execution, and reports."
type: knowledge
triggers: ["mvn-test", "surefire-tests", "failsafe-integration", "parallel-and-reports"]
---

# mvn-test

Runs Java test suites with Maven Surefire and Failsafe, including test filters, parallel execution, and reports.

## Instructions

# Maven Test

Run Java tests with Surefire and Failsafe.

## What This Skill Does

- Runs unit tests with class/method filters
- Runs integration tests in the verify phase
- Parallelizes test execution
- Generates reports and coverage

## When to Use

- Running the suite in CI
- Debugging a specific failing test
- Enforcing quality gates

## Real Commands

```bash
# Unit tests
mvn test
mvn test -Dtest=OrderServiceTest
mvn test -Dtest=OrderServiceTest#testTotal
mvn test -Dtest=*ServiceTest -Dsurefire.failIfNoSpecifiedTests=false

# Integration tests
mvn verify
mvn verify -Dit.test=OrderIT
mvn failsafe:integration-test failsafe:verify

# Parallel and reports
mvn test -Dparallel=classes -DthreadCount=4
mvn surefire-report:report
mvn clean test
```

## Pom Configuration

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.2.5</version>
  <configuration>
    <parallel>classes</parallel>
    <threadCount>4</threadCount>
  </configuration>
</plugin>
```

## Best Practices

- Name integration tests *IT for Failsafe
- Use -Dtest for fast targeted loops
- Run mvn verify in CI to include integration tests
- Set failIfNoSpecifiedTests=false to avoid false failures
- Publish surefire reports as CI artifacts

## Capabilities

### surefire-tests
Run unit tests with Maven Surefire.

**Commands:**
- `mvn test`
- `mvn test -Dtest=OrderServiceTest`
- `mvn test -Dtest=OrderServiceTest#testTotal`
- `mvn -q test`
- `mvn test -Dtest=*ServiceTest -Dsurefire.failIfNoSpecifiedTests=false`

**Examples:**
- mvn test
- mvn test -Dtest=OrderServiceTest
- mvn test -Dtest=*ServiceTest -Dsurefire.failIfNoSpecifiedTests=false

### failsafe-integration
Run integration tests with Maven Failsafe.

**Commands:**
- `mvn verify`
- `mvn verify -Dit.test=OrderIT`
- `mvn verify -DskipITs=false`
- `mvn verify -Dit.test=*IT -Dfailsafe.failIfNoSpecifiedTests=false`
- `mvn failsafe:integration-test failsafe:verify`

**Examples:**
- mvn verify
- mvn verify -Dit.test=OrderIT
- mvn failsafe:integration-test failsafe:verify

### parallel-and-reports
Parallel tests, coverage, and reports.

**Commands:**
- `mvn test -Dparallel=classes -DthreadCount=4`
- `mvn test -Djacoco=true verify jacoco:report`
- `mvn surefire-report:report`
- `mvn test -DskipTests=false -Dsurefire.printSummary=true`
- `mvn clean test`

**Examples:**
- mvn test -Dparallel=classes -DthreadCount=4
- mvn surefire-report:report
- mvn clean test
