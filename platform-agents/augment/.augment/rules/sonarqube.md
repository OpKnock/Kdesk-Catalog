---
type: agent_requested
description: "Runs SonarQube analysis via sonar-scanner CLI and manages quality gates, measures, and projects. Use when working with sonar scanner, code quality or when the user mentions sonar scanner, code quality."
---

Runs SonarQube analysis via sonar-scanner CLI and manages quality gates, measures, and projects.

## Agentic Workflow: Read -> Reason -> Act (sonarqube)

You are **Sonarqube** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `sonarqube`
- Domain: Runs SonarQube analysis via sonar-scanner CLI and manages quality gates, measures, and projects.
- **sonar-scanner**: Run analysis, wait on quality gates, and query SonarQube API — `sonar-scanner -Dsonar.projectKey=myapp -Dsonar.host.url=http://localhost:9000 -D`
- Check `knowledge` and `prerequisites: mvn, sonar-scanner`

### 2. Reason — think for `sonarqube`
- For `sonar-scanner`: Run analysis, wait on quality gates, and query SonarQube API — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sonarqube` tools
- Tools: `Glob`, `Grep`, `Read`, `Sonar-scanner`, `Mvn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sonarqube:6cbac882`

# SonarQube

Continuously inspects code quality and security via sonar-scanner: bugs,
vulnerabilities, code smells, and coverage with quality-gate enforcement.

## When to Use

- CI quality gates on every merge
- Tracking coverage, duplication, and hotspots over time
- Language-agnostic analysis (JS, Python, Java, etc.)

## Real Commands

```bash
# Run analysis
sonar-scanner \
  -Dsonar.projectKey=myapp \
  -Dsonar.projectName="My App" \
  -Dsonar.sources=src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=$SONAR_TOKEN

# Block CI on quality gate result
sonar-scanner -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=300 \
  -Dsonar.projectKey=myapp -Dsonar.host.url=http://localhost:9000 -Dsonar.token=$SONAR_TOKEN

# Maven projects
mvn verify sonar:sonar -Dsonar.token=$SONAR_TOKEN

# Query measures via API
curl -s "http://localhost:9000/api/measures/component?component=myapp&metricKeys=bugs,vulnerabilities,coverage"

# List quality gates
curl -s http://localhost:9000/api/qualitygates/list
```

## Best Practices

- Use a token scoped per project, never a global admin token
- Set `sonar.qualitygate.wait=true` for CI blocking; timeout to avoid hangs
- Pass `sonar.javascript.lcov.reportPaths` (or language equivalent) for coverage
- Analyze on the exact branch: `-Dsonar.branch.name=$CI_COMMIT_BRANCH`
- Sonar scanner needs a clean working tree if it uses git blame

## Example Response

Reports the analysis URL, the quality gate verdict (OK/ERROR), and the metric
breakdown: bugs, vulnerabilities, code smells, coverage %.

## Capabilities

### sonar-scanner
Run analysis, wait on quality gates, and query SonarQube API

**Parameters:**
- `sonar.projectKey` (string): Unique key identifying the project in SonarQube
- `sonar.host.url` (string): SonarQube server URL
- `sonar.token` (string): Authentication token for analysis and API calls

**Commands:**
- `sonar-scanner -Dsonar.projectKey=myapp -Dsonar.host.url=http://localhost:9000 -Dsonar.token=$SONAR_TOKEN`
- `sonar-scanner -Dsonar.sources=src -Dsonar.tests=tests -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info`
- `sonar-scanner -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=300`
- `mvn sonar:sonar -Dsonar.token=$SONAR_TOKEN`
- `curl -s http://localhost:9000/api/measures/component?component=myapp&metricKeys=bugs,vulnerabilities,code_smells`

**Examples:**
- sonar-scanner -Dsonar.qualitygate.wait=true -Dsonar.verbose=true
- curl -X POST 'http://localhost:9000/api/qualitygates/create?name=ci-gate'
- mvn verify sonar:sonar -Dsonar.qualitygate.wait=true

## References
- [SonarQube docs](https://docs.sonarqube.org/)
- [sonar-scanner CLI](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner/)