---
type: agent_requested
description: "Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins. Use when working with gradle scan, dependency analysis, code quality or when the user mentions gradle scan, dependency analysis, code quality."
---

Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins.

## Agentic Workflow: Read -> Reason -> Act (gradle-dependency-scan)

You are **Gradle Dependency Scan** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `gradle-dependency-scan`
- Domain: Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins.
- **gradle-scan**: Run vulnerability scans on Gradle projects. — `gradle dependencyCheckAnalyze`
- **dependency-analysis**: Inspect dependency trees and updates. — `gradle dependencyInsight --dependency log4j-core`
- Check `knowledge` and `prerequisites: gradle`

### 2. Reason — think for `gradle-dependency-scan`
- For `gradle-scan`: Run vulnerability scans on Gradle projects. — decide which checks to run
- For `dependency-analysis`: Inspect dependency trees and updates. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gradle-dependency-scan` tools
- Tools: `Glob`, `Grep`, `Read`, `Gradle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gradle-dependency-scan:2dc73d10`

# Gradle Dependency Scan

Find vulnerable and outdated Gradle dependencies.

## When to Use

- Before releases and in CI on every change
- Tracking CVE exposure in transitive dependencies
- License compliance checks
- Keeping the dependency tree understandable

## Setup

```groovy
// build.gradle
plugins {
  id "org.owasp.dependencycheck" version "10.0.0"
}
dependencyCheck {
  failBuildOnCVSS = 7
  suppressionFiles = ["dependency-check-suppressions.xml"]
}
```

## Commands

```bash
# Analyze the project
gradle dependencyCheckAnalyze

# Update the NVD database
gradle dependencyCheckUpdate

# Aggregate across subprojects
gradle dependencyCheckAggregate

# Inspect the tree
gradle dependencies
gradle dependencies --configuration runtimeClasspath

# Find a specific dependency path
gradle dependencyInsight --dependency log4j-core

# Preview updates
gradle dependencyUpdates
```

## Best Practices

- Fail the build on CVSS >= 7 in CI
- Run scans on every commit, not just releases
- Review suppression files; never blanket-suppress
- Pin plugin versions and update the NVD feed regularly
- Use dependencyInsight to trace transitive paths
- Enable dependency verification metadata in security-sensitive repos

## Capabilities

### gradle-scan
Run vulnerability scans on Gradle projects.

**Parameters:**
- `failBuildOnCVSS` (number): CVSS threshold to fail build
- `format` (string): Report format: html, json, sarif

**Commands:**
- `gradle dependencyCheckAnalyze`
- `gradle dependencyCheckUpdate`
- `gradle dependencyCheckAggregate`
- `gradle dependencies`
- `gradle dependencyUpdates`

**Examples:**
- gradle dependencyCheckAnalyze --scan
- gradle dependencyCheckAggregate -DfailBuildOnCVSS=7
- gradle dependencies --configuration runtimeClasspath

### dependency-analysis
Inspect dependency trees and updates.

**Parameters:**
- `dependency` (string): Dependency coordinate to inspect
- `configuration` (string): Gradle configuration to inspect

**Commands:**
- `gradle dependencyInsight --dependency log4j-core`
- `gradle dependencies --configuration compileClasspath`
- `gradle dependencyInsight --dependency jackson --configuration runtimeClasspath`
- `gradle -q dependencies > deps.txt`

**Examples:**
- gradle dependencyInsight --dependency spring-web
- gradle dependencies --write-verification-metadata sha256

## References
- [OWASP Dependency-Check](https://jeremylong.github.io/DependencyCheck/)
- [Gradle Dependency Verification](https://docs.gradle.org/current/userguide/dependency_verification.html)