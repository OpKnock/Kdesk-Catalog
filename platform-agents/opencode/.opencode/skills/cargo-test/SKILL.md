---
name: "cargo-test"
description: "Runs Rust test suites with cargo test, nextest, and coverage tools, including doctests and race condition checks. Use when working with cargo testing, nextest and coverage, concurrency and vet or when the user mentions cargo testing, nextest and coverage, concurrency and vet."
---

Runs Rust test suites with cargo test, nextest, and coverage tools, including doctests and race condition checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cargo test`, `cargo nextest run`
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

# cargo test

Test Rust code with unit, integration, and doc tests.

## What This Skill Does

- Runs the full test matrix (unit, integration, docs)
- Filters tests by name and shows captured output
- Measures coverage with tarpaulin or llvm-cov
- Speeds up CI with nextest sharding

## When to Use

- Verifying changes before merge
- Debugging a single failing test
- Enforcing coverage thresholds

## Real Commands

```bash
# Basics
cargo test
cargo test my_module::test_name
cargo test -- --nocapture
cargo test --release
cargo test --doc

# Nextest
cargo nextest run
cargo nextest run --partition count:2/2

# Coverage
cargo tarpaulin --out html
cargo llvm-cov --open

# Quality
cargo clippy --all-targets -- -D warnings
```

## Sample Test

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn parses_numbers() {
        assert_eq!("42".parse::<u32>().unwrap(), 42);
    }

    #[test]
    fn rejects_empty() {
        assert!("".parse::<u32>().is_err());
    }
}
```

## Best Practices

- Use #[test] + assert_eq!/assert! for unit tests
- Put integration tests in tests/ for public API coverage
- Run doctests in CI; they rot silently
- Gate coverage at 80%+ with tarpaulin thresholds
- Use nextest for fast feedback on large workspaces

## Capabilities

### cargo-testing
Run unit, integration, and doc tests.

**Parameters:**
- `filter` (string): Test name substring filter
- `nocapture` (boolean): Show println output from tests
- `threads` (number): Test thread count

**Commands:**
- `cargo test`
- `cargo test my_module::test_name`
- `cargo test -- --nocapture`
- `cargo test --release`
- `cargo test --doc`

**Examples:**
- cargo test
- cargo test my_module::test_name -- --nocapture
- cargo test -- --test-threads=8

### nextest-and-coverage
Faster parallel testing and coverage measurement.

**Parameters:**
- `outFormat` (string): Coverage format: html, xml, json
- `partition` (string): Test partition for sharding

**Commands:**
- `cargo nextest run`
- `cargo nextest run --partition count:2/2`
- `cargo tarpaulin --out html`
- `cargo llvm-cov --open`
- `cargo nextest run --fail-fast`

**Examples:**
- cargo nextest run
- cargo tarpaulin --out html
- cargo llvm-cov --open

### concurrency-and-vet
Race detection and lints for tests.

**Parameters:**
- `features` (string): Cargo features to enable
- `testThreads` (integer): Number of parallel test threads via --test-threads.

**Commands:**
- `cargo test -- --test-threads=1`
- `RUSTFLAGS='-C target-feature=+crt-static' cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --features integration`

**Examples:**
- cargo test -- --test-threads=1
- cargo clippy --all-targets -- -D warnings
- cargo test --features integration

## References
- [cargo test Reference](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [Nextest Documentation](https://nexte.st/)
- [cargo-tarpaulin](https://github.com/xd009642/tarpaulin)
