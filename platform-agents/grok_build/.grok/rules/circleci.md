Build, validate, and debug CircleCI pipelines with the circleci CLI, including orbs and local execution.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `circleci config validate`, `circleci orb publish orb.yml myorg/myorb@0.0.1`
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

# CircleCI

Build and validate CircleCI pipelines from the command line.

## When to Use

- Validating config before pushing
- Testing config changes locally with Docker
- Publishing and consuming orbs

## Install

```bash
curl -fLSs https://circle.ci/cli | bash
# macOS
brew install circleci
```

## Validate

```bash
circleci config validate
circleci config process .circleci/config.yml > processed.yml
```

## Config Example

```yaml
version: 2.1
orbs:
  go: circleci/go@1.7.3
jobs:
  build:
    docker:
      - image: cimg/go:1.22
    steps:
      - checkout
      - go/load-cache
      - run: go test ./...
      - go/save-cache
workflows:
  main:
    jobs:
      - build
```

## Local Execution

```bash
circleci local execute --job build
```

## Orbs

```bash
circleci orb validate my-orb.yml
circleci orb publish my-orb.yml myorg/api-orb@1.0.0
circleci orb list myorg
```

## Testing

```bash
circleci config validate .circleci/config.yml
circleci config pack .circleci/config | circleci config validate
```

## Best Practices

- Validate config in a pre-commit hook
- Pin orb versions in production
- Use local execute to test jobs that do not need private env vars
- Keep secrets in project or context env vars, never in config
- Process config to debug conditional logic and orbs

## Capabilities

### pipeline-validate
Validate, process, and inspect CircleCI config files

**Parameters:**
- `config_path` (string): Path to config.yml, default .circleci/config.yml

**Commands:**
- `circleci config validate`
- `circleci config validate .circleci/config.yml`
- `circleci config process .circleci/config.yml > processed.yml`
- `circleci config pack .circleci/config`

**Examples:**
- circleci config validate .circleci/config.yml
- circleci config process .circleci/config.yml | circleci config validate
- circleci config pack .circleci/config > .circleci/config.yml

### orbs-and-runs
Manage orbs and run jobs locally with the CircleCI CLI

**Parameters:**
- `job` (string): Job name to execute locally
- `orb_ref` (string): Orb reference like namespace/orb@version

**Commands:**
- `circleci orb publish orb.yml myorg/myorb@0.0.1`
- `circleci orb validate orb.yml`
- `circleci orb list myorg`
- `circleci local execute --job test`
- `circleci build --job test`

**Examples:**
- circleci orb validate my-orb.yml && circleci orb publish my-orb.yml myorg/api-orb@1.0.0
- circleci local execute --job build
- circleci orb list myorg | grep api

## References
- [CircleCI CLI Docs](https://circleci.com/docs/local-cli/)
- [CircleCI Config Docs](https://circleci.com/docs/configuration-reference/)