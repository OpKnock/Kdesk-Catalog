---
type: agent_requested
description: "Scans Maven projects for known vulnerable dependencies using the OWASP Dependency-Check Maven plugin."
---

# Maven Dependency Scan

Scans Maven projects for known vulnerable dependencies using the OWASP Dependency-Check Maven plugin.

## Instructions

# Maven Dependency Scan

Uses OWASP Dependency-Check to identify known vulnerabilities (CVE) in every direct
and transitive Maven dependency.

## When to Use

- Scanning a Maven project before release
- Enforcing a CVSS threshold gate in CI
- Checking a dependency tree for CVEs after a version bump

## Real Commands

```bash
# Basic scan (writes report to target/dependency-check-report.html)
mvn org.owasp:dependency-check-maven:check

# Fail the build on CVSS >= 7, all report formats
mvn dependency-check:check -DfailBuildOnCVSS=7 -Dformat=ALL

# Update the local NVD cache only (no scan)
mvn dependency-check:update-only -DnvdApiKey=$NVD_API_KEY

# Aggregate across all modules of a multi-module build
mvn dependency-check:aggregate -Dformat=JSON -DoutputDirectory=target/dc

# With suppression file for known false positives
mvn dependency-check:check -DsuppressionFiles=suppressions.xml
```

## Suppressions Example (suppressions.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress>
    <notes>Only affects Windows builds</notes>
    <packageUrl regex="true">^pkg:maven/.*</packageUrl>
    <cve>CVE-2023-99999</cve>
  </suppress>
</suppressions>
```

## Best Practices

- Export an NVD API key (`-DnvdApiKey`) to avoid rate-limit failures
- Start with `-DfailBuildOnCVSS=11` to baseline, then tighten to 7
- Keep suppressions file reviewed and commented
- Cache reports (`-DoutputDirectory=target/dc`) for auditing

## Example Response

A scan that finds a vulnerable log4j transitive dep reports the exact package
coordinates, the CVE ID, CVSS score, and the affected version range, then the agent
recommends the upgraded version.

## Capabilities

### dependency-check
Run OWASP Dependency-Check against Maven projects and fail builds on high-CVSS findings

**Commands:**
- `mvn org.owasp:dependency-check-maven:check`
- `mvn dependency-check:check -DfailBuildOnCVSS=7 -Dformat=ALL`
- `mvn dependency-check:update-only`
- `mvn dependency-check:aggregate -Dformat=JSON`
- `mvn dependency-check:check -DnvdApiKey=$NVD_API_KEY -DsuppressionFiles=suppressions.xml`

**Examples:**
- mvn org.owasp:dependency-check-maven:check -Dformat=HTML
- mvn dependency-check:aggregate -Dformat=ALL -DoutputDirectory=target/dc
- mvn verify -Ddependency-check.failBuildOnCVSS=8