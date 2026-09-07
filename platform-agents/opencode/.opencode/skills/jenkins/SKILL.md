---
name: "jenkins"
description: "Administers Jenkins: pipeline-as-code with Jenkinsfile, job management via CLI, plugin installs, and credential handling. Use when working with pipeline as code, system administration, devops or when the user mentions pipeline as code, system administration, devops."
---

Administers Jenkins: pipeline-as-code with Jenkinsfile, job management via CLI, plugin installs, and credential handling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `jenkins-jobs update --job 'ci-deploy' jenkins_jobs.ini`, `java -jar jenkins-cli.jar -s http://localhost:8080/ install-`
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

# Jenkins Administration

Operate Jenkins: pipeline-as-code, jobs, plugins, and credentials.

## What This Skill Does

- Writes declarative Jenkinsfile pipelines (stages, steps, post)
- Runs, monitors, and reads console output of builds via CLI
- Installs plugins and manages credentials
- Reloads configuration and restarts safely
- Boots a local Jenkins for testing (java -jar jenkins.war)

## When to Use

- Migrating jobs to Jenkinsfile pipeline-as-code
- Debugging a failing build from CLI without UI access
- Admin tasks: plugins, credentials, reloads

## Real Commands

```bash
# Local dev instance
java -jar jenkins.war --httpPort=8080 --enable-fresh-install

# CLI operations (auth via token)
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$(cat ~/.jenkins_token) list-jobs
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:$(cat ~/.jenkins_token) build ci-deploy -p BRANCH=main
java -jar jenkins-cli.jar -s http://localhost:8080/ console ci-deploy 12
java -jar jenkins-cli.jar -s http://localhost:8080/ create-job newjob < config.xml

# Admin
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin kubernetes git -restart
java -jar jenkins-cli.jar -s http://localhost:8080/ reload-configuration
java -jar jenkins-cli.jar -s http://localhost:8080/ get-credentials-as-xml system::system::jenkins mycred
```

## Declarative Pipeline

```groovy
pipeline {
  agent any
  stages {
    stage('Build') { steps { sh 'npm ci && npm run build' } }
    stage('Test')  { steps { sh 'npm test' } }
  }
  post {
    failure { slackSend color: 'danger', message: "Build failed ${env.BUILD_URL}" }
  }
}
```

## Best Practices

- Store everything as Jenkinsfile in the repo (pipeline-as-code)
- Use credential IDs referenced by name, never secrets inline
- Add `options { timeout(time: 30, unit: 'MINUTES') }` to every pipeline
- Prefer agent pod templates (kubernetes plugin) over static slaves
- Back up $JENKINS_HOME and pin plugin versions

## Capabilities

### pipeline-as-code
Write and run declarative Jenkinsfile pipelines.

**Parameters:**
- `url` (string): Jenkins base URL
- `job` (string): Job name
- `build-number` (integer): Build number for console

**Commands:**
- `jenkins-jobs update --job 'ci-deploy' jenkins_jobs.ini`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ build ci-deploy`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ console ci-deploy 12`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ list-jobs`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ create-job test < config.xml`

**Examples:**
- java -jar jenkins-cli.jar -s http://localhost:8080/ build ci-deploy -p BRANCH=main
- java -jar jenkins-cli.jar -s http://localhost:8080/ list-jobs
- java -jar jenkins-cli.jar -s http://localhost:8080/ console ci-deploy 12

### system-administration
Manage plugins, credentials, and reload configuration.

**Parameters:**
- `plugin` (string): Plugin name to install
- `credential-id` (string): Credential ID

**Commands:**
- `java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin kubernetes git -restart`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ reload-configuration`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ get-credentials-as-xml system::system::jenkins mycred`
- `java -jar jenkins-cli.jar -s http://localhost:8080/ restart`
- `java -jar jenkins.war --httpPort=8080`

**Examples:**
- java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin kubernetes -restart
- java -jar jenkins-cli.jar -s http://localhost:8080/ reload-configuration
- java -jar jenkins.war --httpPort=8080

## References
- [Jenkins User Handbook](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins CLI](https://www.jenkins.io/doc/book/managing/cli/)
