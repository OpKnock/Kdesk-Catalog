Runs Java test suites with Maven Surefire and Failsafe, including test filters, parallel execution, and reports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn test`, `mvn verify`
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

**Parameters:**
- `test` (string): Test class or method pattern
- `quiet` (boolean): Quiet output (-q)
- `failIfNoSpecifiedTests` (boolean): Fail when -Dtest matches nothing

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

**Parameters:**
- `itTest` (string): Integration test pattern
- `skipITs` (boolean): Skip integration tests

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

**Parameters:**
- `parallel` (string): Parallel mode: classes, methods
- `threadCount` (number): Threads for parallel execution

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

## References
- [Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
- [Maven Failsafe Plugin](https://maven.apache.org/surefire/maven-failsafe-plugin/)
- [Maven CLI Reference](https://maven.apache.org/ref/3.9.0/mvn/index.html)