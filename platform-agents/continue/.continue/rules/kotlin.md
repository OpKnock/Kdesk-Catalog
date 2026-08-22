---
name: "Kotlin"
description: "Develops Android apps with Kotlin and Gradle: builds, tests, linting, and ktlint formatting checks."
globs: ["**/*.java", "**/*.json", "**/*.kt", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Kotlin

Develops Android apps with Kotlin and Gradle: builds, tests, linting, and ktlint formatting checks.

## Instructions

# Kotlin (Android)

Build Android apps with Kotlin and the Gradle toolchain.

## When to Use

- Android application development
- Kotlin multiplatform and JVM libraries
- Enforcing code style across Kotlin sources

## Wrapper first

```bash
gradle wrapper --gradle-version 8.10
```

Commit the wrapper; teams should never rely on a local Gradle install.

## Core tasks

```bash
./gradlew assembleDebug
./gradlew testDebugUnitTest
./gradlew lint
```

`lint` runs Android Lint - treat warnings as errors in CI with `warningsAsErrors`.

## Testing

```bash
./gradlew testDebugUnitTest --tests 'com.example.orders.*'
```

Use Robolectric for JVM unit tests and instrumented tests for UI flows.

## ktlint gates

```bash
ktlint 'src/**/*.kt'
ktlint -F 'src/**/*.kt'
```

Run `ktlint -F` locally, plain `ktlint` in CI.

## Kotlin scripts

```bash
kotlinc -script build-data.kts
```

## Best practices

- Pin Gradle and Kotlin plugin versions in the wrapper.
- Keep unit tests JVM-fast; only critical flows instrumented.
- Use the Android Kotlin style guide consistently.
- Cache Gradle deps in CI to cut build time.

## Testing

```bash
./gradlew build && ktlint 'src/**/*.kt'
```

Both must pass before merge.

## Capabilities

### gradle
Build and test Android/Kotlin projects with Gradle.

**Commands:**
- `gradle wrapper --gradle-version 8.10`
- `./gradlew build`
- `./gradlew testDebugUnitTest`
- `./gradlew assembleDebug`
- `./gradlew --status`

**Examples:**
- ./gradlew build --daemon --offline
- ./gradlew testReleaseUnitTest --tests 'com.example.api.*'
- ./gradlew assembleRelease --stacktrace

### kotlin-tools
Format, lint, and run Kotlin scripts.

**Commands:**
- `ktlint 'src/**/*.kt'`
- `ktlint -F 'src/**/*.kt'`
- `kotlinc -script build-data.kts`
- `kotlinc -version`
- `java -jar ktlint.jar --reporter=json,output=ktlint-report.json`

**Examples:**
- ktlint --code-style=official 'src/**/*.kt'
- kotlinc -script stats.kts -- data.csv
- ktlint -F --editorconfig=.editorconfig 'src/**/*.kt'