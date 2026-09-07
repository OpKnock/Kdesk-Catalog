Jenkins pipeline operations: triggering builds via jenkins-cli and curl, running Groovy scripts, listing jobs, and checking build status.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `java -jar jenkins-cli.jar -s http://localhost:8080 list-jobs`
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

# Jenkins Pipeline

Drive Jenkins from the terminal.

## What this skill does
47:   
- Lists jobs and triggers builds with parameters.
- Watches build results and console output.
- Runs48:    ad-hoc Groovy against the Jenkins instance.
- Fetches build artifacts from the API.

## When to49:    use

- Triggering CI from a script or another pipeline.
- Checking why a build failed without opening50:    the UI.
- Auditing installed plugins or job configs.

## Real commands

```bash
# List jobs
51:   java -jar jenkins-cli.jar -s http://localhost:8080 list-jobs

# Trigger a build and wait for result
52:   java -jar jenkins-cli.jar -s http://localhost:8080 build MyJob -s -v

# Trigger with curl (token auth)
53:   curl -X POST -u admin:token http://localhost:8080/job/MyJob/build

# Parameterized build
curl -u54:    admin:token -X POST 'http://localhost:8080/job/MyJob/buildWithParameters?TARGET=staging'

# Build55:    result
curl -u admin:token http://localhost:8080/job/MyJob/lastBuild/api/json | jq '.result, .duration'
56:   
# Groovy script (count plugins)
java -jar jenkins-cli.jar -s http://localhost:8080 groovy = 'println57:    Jenkins.instance.pluginManager.plugins.size()'

# Console output
java -jar jenkins-cli.jar -s http://localhost:808058:    console MyJob 42
```

## Polling loop

```bash
while :; do
  R=$(curl -s -u admin:token http://localhost:8080/job/MyJob/lastBuild/api/json59:    | jq -r .result)
  [ "$R" != "null" ] && break
  sleep 5
done
echo "build finished: $R"
60:   ```

## Testing

```bash
curl -s -u admin:token http://localhost:8080/api/json | jq '.jobs[].name'
61:   ```

## Best practices

- Prefer jenkins-cli for interactive work, curl for CI scripting.
- Use62:    API tokens, never raw passwords, in scripts.
- Poll api/json on the queued item, not the build, to63:    avoid missing builds.
- Pin jenkins-cli.jar version to the server version.

## Example exchange
64:   
```
User: Trigger a staging deploy build and wait for it.
Agent: curl -u admin:token -X POST 'http://localhost:8080/job/deploy/buildWithParameters?TARGET=staging'
65:          then poll lastBuild/api/json until .result != null
```

## Capabilities

### jenkins-cli
Trigger, monitor, and script Jenkins jobs from the terminal.

**Parameters:**
- `job` (string): Jenkins job name.
- `build_number` (integer): Build number to inspect.
- `params` (string): Build parameters as key=value pairs.

**Commands:**
- `java -jar jenkins-cli.jar -s http://localhost:8080 list-jobs`
- `java -jar jenkins-cli.jar -s http://localhost:8080 build MyJob -s -v`
- `curl -X POST -u admin:token http://localhost:8080/job/MyJob/build`
- `curl -u admin:token http://localhost:8080/job/MyJob/lastBuild/api/json | jq '.result, .duration'`
- `java -jar jenkins-cli.jar -s http://localhost:8080 groovy = 'println Jenkins.instance.pluginManager.plugins.size()'`

**Examples:**
- curl -u admin:token -X POST 'http://localhost:8080/job/MyJob/buildWithParameters?TARGET=staging'
- curl -s 'http://localhost:8080/job/MyJob/lastSuccessfulBuild/artifact/report.json' | jq .
- java -jar jenkins-cli.jar -s http://localhost:8080 console MyJob 42

## References
- [Jenkins CLI Docs](https://www.jenkins.io/doc/book/managing/cli/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)