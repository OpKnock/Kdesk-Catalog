---
name: "gradle-dependency-scan"
description: "Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins. Use when working with gradle scan, dependency analysis, code quality or when the user mentions gradle scan, dependency analysis, code quality."
license: "MIT"
compatibility: "Requires gradle."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(gradle:*)"
---

Scans Gradle dependencies for vulnerabilities and licenses with OWASP dependency-check and Gradle plugins.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gradle dependencyCheckAnalyze`, `gradle dependencyInsight --dependency log4j-core`
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
