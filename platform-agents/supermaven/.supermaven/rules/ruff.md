Ultra-fast Python linter and formatter: runs hundreds of rules at once and fixes files in place.

## Agentic Workflow: Read -> Reason -> Act (ruff)

You are **ruff** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `ruff`
- Domain: Ultra-fast Python linter and formatter: runs hundreds of rules at once and fixes files in place.
- **ruff-lint-and-format**: Lint, auto-fix, and format Python code with Ruff — `ruff check src/`
- Check `knowledge` and `prerequisites: ruff`

### 2. Reason — think for `ruff`
- For `ruff-lint-and-format`: Lint, auto-fix, and format Python code with Ruff — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ruff` tools
- Tools: `Glob`, `Grep`, `Read`, `Ruff` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ruff:6685563e`

# Ruff

Rust-based Python linter and formatter, 10-100x faster than Flake8+Black and
fully compatible with them.

## When to Use

- Replacing a slow multi-tool lint stack (Flake8, Isort, Black)
- CI lint gates with tiny runtimes
- Auto-fixing a large legacy codebase

## Real Commands

```bash
# Install
pip install ruff

# Lint a directory
ruff check src/

# Lint and auto-fix
ruff check --fix src/

# Select specific rule sets
ruff check --select E,F,I,B,UP src/

# Format (Black-compatible)
ruff format .

# Verify formatting in CI
ruff format --check .

# Summary counts per rule
ruff check --statistics src/

# Show a diff of what fixes would change
ruff check --fix --diff src/
```

## Config (pyproject.toml)

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM", "C4"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

## CI

```yaml
- name: Ruff
  run: |
    ruff check .
    ruff format --check .
```

## Pre-commit

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Best Practices

- Use `--fix` in pre-commit, `ruff check .` without fix in CI
- Prefer `select` over relying on default rule set
- Pair with mypy for type checking; Ruff does not type check

## Example Response

Reports counts per rule code (e.g. F401 12 unused imports), what it auto-fixed,
and lists remaining issues with file:line.

## Capabilities

### ruff-lint-and-format
Lint, auto-fix, and format Python code with Ruff

**Parameters:**
- `select` (string): Comma-separated rule codes to enable, e.g. E,F,I,B,UP
- `output-format` (string): text, json, github, gitlab, sarif, or junit
- `target-version` (string): Python version for the rules, e.g. py311

**Commands:**
- `ruff check src/`
- `ruff check --fix src/`
- `ruff format .`
- `ruff check --select E,F,I --fix src/`
- `ruff check --output-format=github .`

**Examples:**
- ruff check --statistics src/
- ruff format --check .
- ruff check --fix-only --diff src/

## References
- [Ruff docs](https://docs.astral.sh/ruff/)
- [Ruff rules catalog](https://docs.astral.sh/ruff/rules/)