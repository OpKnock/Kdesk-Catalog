---
name: "gradle-dependency-scan"
description: "Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins."
type: knowledge
triggers: ["gradle-dependency-scan", "gradle-scan", "dependency-analysis"]
---

# Gradle Dependency Scan

Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins.

## Instructions

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

**Commands:**
- `gradle dependencyInsight --dependency log4j-core`
- `gradle dependencies --configuration compileClasspath`
- `gradle dependencyInsight --dependency jackson --configuration runtimeClasspath`
- `gradle -q dependencies > deps.txt`

**Examples:**
- gradle dependencyInsight --dependency spring-web
- gradle dependencies --write-verification-metadata sha256
