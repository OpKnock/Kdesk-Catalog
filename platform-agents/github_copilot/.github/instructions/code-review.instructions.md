---
applyTo: "**/*.r **/*.sh"
---

Performs systematic code reviews: diff analysis, security checks, test coverage review, and actionable feedback.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git diff HEAD~1`, `gitleaks detect`
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

# Code Review

Review code effectively and systematically.

## When to Use

- Before merging any non-trivial change
- Auditing a commit range for security issues
- Giving feedback that improves the codebase
- Catching secrets and risky patterns early

## Review Checklist

1. Understand the change intent (commit message, issue)
2. Diff analysis: logic, edge cases, error paths
3. Style and consistency with the codebase
4. Tests: do they cover the change and the failure modes?
5. Security: secrets, injection, authz, input validation
6. Performance: N+1, blocking I/O, memory leaks

## Commands

```bash
# Diff analysis
git diff HEAD~1
git diff --stat HEAD~1
git diff --check
git log --oneline -10

# Secret scanning
gitleaks detect
trufflehog filesystem .
git log -p --all -S "password"

# History search for leaked material
git log -S "BEGIN RSA PRIVATE KEY" --all
```

## Best Practices

- Review the diff, not the whole file, unless asked
- Ask questions over commands; suggest over demand
- Separate blocking issues from nits clearly
- Verify claims: run the tests, not just read them
- Check that secrets are never committed (gitleaks in CI)
- Approve only when tests pass and concerns are resolved

## Capabilities

### diff-review
Analyze diffs and changed files.

**Parameters:**
- `range` (string): Commit range
- `path` (string): Path filter

**Commands:**
- `git diff HEAD~1`
- `git diff --stat HEAD~1`
- `git diff --check`
- `git log --oneline -10`
- `git show HEAD`

**Examples:**
- git diff HEAD~3..HEAD -- src/
- git diff --check HEAD~1
- git diff -U20 HEAD~1 | less

### security-review
Scan for secrets and vulnerable patterns.

**Parameters:**
- `scope` (string): Files or history to scan
- `range` (string): Commit range to scan

**Commands:**
- `gitleaks detect`
- `gitleaks detect --source .`
- `trufflehog filesystem .`
- `grep -rnE "api[_-]?key\s*=\s*[^[:space:]]{4,}" . --include="*.js" --include="*.ts"`
- `git log -p --all -S "password"`

**Examples:**
- gitleaks detect --log-opts="-20"
- trufflehog git --branch main
- git log -S "BEGIN RSA PRIVATE KEY" --all

## References
- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Gitleaks Docs](https://github.com/gitleaks/gitleaks)
