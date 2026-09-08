---
name: "gradle-test"
description: "Runs JVM test suites with Gradle, including test filtering, caching, parallel execution, and reports. Use when working with gradle testing, parallel and cache, reports and coverage or when the user mentions gradle testing, parallel and cache, reports and coverage."
type: knowledge
triggers: ["gradle-test", "gradle-testing", "parallel-and-cache", "reports-and-coverage"]
---

Runs JVM test suites with Gradle, including test filtering, caching, parallel execution, and reports.

## Agentic Workflow: Read -> Reason -> Act (gradle-test)

You are **gradle-test** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `gradle-test`
- Domain: Runs JVM test suites with Gradle, including test filtering, caching, parallel execution, and reports.
- **gradle-testing**: Run Gradle test tasks with filters. — `./gradlew test`
- **parallel-and-cache**: Speed up builds with parallelism and caching. — `./gradlew test --parallel`
- **reports-and-coverage**: Generate test reports and coverage with JaCoCo. — `./gradlew test jacocoTestReport`
- Check `knowledge` and `prerequisites: ./gradlew`

### 2. Reason — think for `gradle-test`
- For `gradle-testing`: Run Gradle test tasks with filters. — decide which checks to run
- For `parallel-and-cache`: Speed up builds with parallelism and caching. — decide which checks to run
- For `reports-and-coverage`: Generate test reports and coverage with JaCoCo. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gradle-test` tools
- Tools: `Glob`, `Grep`, `Read`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gradle-test:21c37cee`

# Gradle Test

Run and optimize JVM tests with the Gradle build tool.

## What This Skill Does

- Executes test tasks with class/method filters
- Parallelizes and caches test execution
- Generates JaCoCo coverage reports and gates
- Watches files for continuous testing

## When to Use

- Running the full suite in CI
- Debugging a specific test class
- Speeding up a slow build

## Real Commands

```bash
# Run all
./gradlew test

# Filtered
./gradlew test --tests "com.example.OrderServiceTest"
./gradlew test --tests "*Service*"

# Speed
./gradlew test --parallel --build-cache
./gradlew test --continuous

# Fresh and verbose
./gradlew cleanTest test
./gradlew test --rerun-tasks

# Coverage
./gradlew test jacocoTestReport
./gradlew test jacocoTestCoverageVerification
```

## Test Config (build.gradle)

```groovy
test {
    useJUnitPlatform()
    maxParallelForks = 4
    testLogging {
        events "passed", "skipped", "failed"
    }
}
jacocoTestCoverageVerification {
    violationRules {
        rule { limit { minimum = 0.8 } }
    }
}
```

## Best Practices

- Use --tests patterns for targeted reruns
- Run with --build-cache in CI
- Gate on JaCoCo minimum coverage
- Use --continuous locally for TDD
- Keep unit tests free of external services

## Capabilities

### gradle-testing
Run Gradle test tasks with filters.

**Parameters:**
- `tests` (string): Test class/method pattern
- `rerunTasks` (boolean): Ignore up-to-date cache
- `info` (boolean): Verbose logging

**Commands:**
- `./gradlew test`
- `./gradlew test --tests "com.example.OrderServiceTest"`
- `./gradlew test --tests "*Service*"`
- `./gradlew test --rerun-tasks`
- `./gradlew test --info`

**Examples:**
- ./gradlew test
- ./gradlew test --tests "com.example.OrderServiceTest"
- ./gradlew test --tests "*Service*" --rerun-tasks

### parallel-and-cache
Speed up builds with parallelism and caching.

**Parameters:**
- `maxWorkers` (number): Worker limit
- `buildCache` (boolean): Enable build cache

**Commands:**
- `./gradlew test --parallel`
- `./gradlew test --max-workers=4`
- `./gradlew test --build-cache`
- `./gradlew test --continuous`
- `./gradlew test --watch-fs`

**Examples:**
- ./gradlew test --parallel
- ./gradlew test --build-cache
- ./gradlew test --continuous

### reports-and-coverage
Generate test reports and coverage with JaCoCo.

**Parameters:**
- `report` (string): Report task, e.g. jacocoTestReport
- `tests` (string): Test name filter pattern, e.g. *Service* for --tests.

**Commands:**
- `./gradlew test jacocoTestReport`
- `./gradlew test --tests "*Service*" jacocoTestCoverageVerification`
- `./gradlew test --console=plain`
- `./gradlew cleanTest test`

**Examples:**
- ./gradlew test jacocoTestReport
- ./gradlew cleanTest test
- ./gradlew test --console=plain

## References
- [Gradle Java Testing](https://docs.gradle.org/current/userguide/java_testing.html)
- [Gradle Test Filtering](https://docs.gradle.org/current/userguide/java_testing.html#test_filtering)
- [JaCoCo Gradle Plugin](https://docs.gradle.org/current/userguide/jacoco_plugin.html)
