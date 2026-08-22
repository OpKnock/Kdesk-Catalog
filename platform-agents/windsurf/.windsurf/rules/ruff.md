---
trigger: glob
description: "Ultra-fast Python linter and formatter: runs hundreds of rules at once and fixes files in place."
globs: ["**/*.py", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{yaml,yml}"]
---

# ruff

Ultra-fast Python linter and formatter: runs hundreds of rules at once and fixes files in place.

## Instructions

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
