---
type: agent_requested
description: "Runs SonarQube analysis via sonar-scanner CLI and manages quality gates, measures, and projects. Use when working with sonar scanner, code quality or when the user mentions sonar scanner, code quality."
---

Runs SonarQube analysis via sonar-scanner CLI and manages quality gates, measures, and projects.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sonar-scanner -Dsonar.projectKey=myapp -Dsonar.host.url=http`
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