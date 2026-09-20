---
type: agent_requested
description: "Develops Android apps with Kotlin and Gradle: builds, tests, linting, and ktlint formatting checks. Use when working with gradle, kotlin tools or when the user mentions gradle, kotlin tools."
---

Develops Android apps with Kotlin and Gradle: builds, tests, linting, and ktlint formatting checks.

## Agentic Workflow: Read -> Reason -> Act (kotlin)

You are **Kotlin** (mobile/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — mobile context for `kotlin`
- Domain: Develops Android apps with Kotlin and Gradle: builds, tests, linting, and ktlint formatting checks.
- **gradle**: Build and test Android/Kotlin projects with Gradle. — `gradle wrapper --gradle-version 8.10`
- **kotlin-tools**: Format, lint, and run Kotlin scripts. — `ktlint 'src/**/*.kt'`
- Check `knowledge` and `prerequisites: ./gradlew, gradle, java, kotlinc`

### 2. Reason — think for `kotlin`
- For `gradle`: Build and test Android/Kotlin projects with Gradle. — decide which checks to run
- For `kotlin-tools`: Format, lint, and run Kotlin scripts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kotlin` tools
- Tools: `Glob`, `Grep`, `Read`, `Gradle`, `./gradlew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kotlin:a5701562`

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

**Parameters:**
- `task` (string): Gradle task like assembleDebug, test, lint
- `tests` (string): Test class filter with --tests
- `stacktrace` (string): Full stack traces on failure

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

**Parameters:**
- `glob` (string): Kotlin file glob
- `format` (string): Auto-fix with -F
- `code-style` (string): official or android code style

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

## References
- [Kotlin Docs](https://kotlinlang.org/docs/home.html)
- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)
- [ktlint](https://github.com/pinterest/ktlint)