Writes and runs BASH unit tests with Bats, covering assertions, setup/teardown, and CI-friendly TAP output.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bats test.bats`, `load 'test_helper/bats-support/load'`
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

# Bats

Unit testing for Bash and shell scripts.

## What This Skill Does

- Writes test files with @test blocks
- Uses run, assert_success, and assert_output
- Manages setup/teardown fixtures
- Produces TAP output for CI

## When to Use

- Testing shell scripts and CLI tools
- Regression tests for deploy and ops scripts
- CI for anything written in Bash

## Real Commands

```bash
# Run tests
bats test.bats
bats --tap tests/
bats -f 'parses' test.bats

# Run a Bats suite in CI
bats --tap tests/ | tee results.tap
```

## Sample Test File

```bash
#!/usr/bin/env bats

load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

setup() {
  export FOO="bar"
}

teardown() {
  rm -f /tmp/test-output
}

@test "greeting prints hello" {
  run ./greet.sh alice
  assert_success
  assert_output 'hello alice'
}

@test "greeting fails without args" {
  run ./greet.sh
  assert_failure
  assert_output --partial 'usage'
}
```

## Best Practices

- Keep tests deterministic: set env in setup, clean in teardown
- Use run to capture stdout/stderr/exit code
- Prefer assert_output --partial over exact matching
- Use tags and -f filters for targeted debugging
- Run the full suite in CI with --tap output

## Capabilities

### bats-testing
Author and run Bats test files with filters.

**Parameters:**
- `filter` (string): Run only tests matching the regex (-f)
- `tap` (boolean): TAP output format
- `dryRun` (boolean): Count and print tests without running (-c)

**Commands:**
- `bats test.bats`
- `bats -t test.bats`
- `bats --tap tests/`
- `bats -f 'parses' test.bats`
- `bats -c test.bats`

**Examples:**
- bats test.bats
- bats --tap tests/
- bats -f 'returns error' test.bats

### assertions-and-fixtures
Use bats-assert helpers and fixtures in tests.

**Parameters:**
- `command` (string): Command to run under `run`
- `expected` (string): Expected output for assertions

**Commands:**
- `load 'test_helper/bats-support/load'`
- `load 'test_helper/bats-assert/load'`
- `assert_success`
- `assert_output --partial 'error'`
- `run ./deploy.sh --dry-run`

**Examples:**
- assert_success
- assert_output --regexp 'deploying.*prod'
- run ./script.sh -h && assert_failure

## References
- [Bats Documentation](https://bats-core.readthedocs.io/)
- [bats-assert GitHub](https://github.com/bats-core/bats-assert)