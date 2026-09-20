---
trigger: glob
description: "Runs JVM test suites with Gradle, including test filtering, caching, parallel execution, and reports."
globs: ["**/*.r", "**/*.sh"]
---

# gradle-test

Runs JVM test suites with Gradle, including test filtering, caching, parallel execution, and reports.

## Instructions

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

**Commands:**
- `./gradlew test jacocoTestReport`
- `./gradlew test --tests "*Service*" jacocoTestCoverageVerification`
- `./gradlew test --console=plain`
- `./gradlew cleanTest test`

**Examples:**
- ./gradlew test jacocoTestReport
- ./gradlew cleanTest test
- ./gradlew test --console=plain
