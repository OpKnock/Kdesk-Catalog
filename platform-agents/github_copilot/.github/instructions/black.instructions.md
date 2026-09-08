---
applyTo: "**/*.py **/*.r **/*.sh"
---

Formats Python code with Black: deterministic formatting, config control, diff previews, and CI enforcement.

## Agentic Workflow: Read -> Reason -> Act (black)

You are **black** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `black`
- Domain: Formats Python code with Black: deterministic formatting, config control, diff previews, and CI enforcement.
- **black-format**: Format Python files and preview changes. — `black --safe src/`
- **black-config**: Configure Black per project. — `black --version`
- Check `knowledge` and `prerequisites: black`

### 2. Reason — think for `black`
- For `black-format`: Format Python files and preview changes. — decide which checks to run
- For `black-config`: Configure Black per project. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `black` tools
- Tools: `Glob`, `Grep`, `Read`, `Black` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `black:deac8220`

# Black

The uncompromising Python formatter.

## When to Use

- Enforcing one consistent style across a Python codebase
- Ending format debates (Black has no style options)
- Pre-commit and CI format gates
- Pairing with isort for import ordering

## Commands

```bash
# Format a directory
black src/

# Check without modifying
black --check src/

# Show the diff only
black --diff src/

# Line length control
black --line-length 100 src/

# Exclude paths
black --exclude "/(\.venv|node_modules|migrations)/" src/

# Specific files
black file1.py file2.py
```

## Config Example

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ["py312"]
extend-exclude = """
/(migrations|\.venv)/
"""
```

## Best Practices

- Use --check --diff in CI; format on pre-commit
- Keep Black config in pyproject.toml, not CLI flags
- Pair with isort --profile black for compatible sorting
- Run Black on everything including tests
- Pin the Black version to avoid churn between releases
- Never mix hand-formatted code with Black-formatted code

## Capabilities

### black-format
Format Python files and preview changes.

**Parameters:**
- `paths` (string): Files or directories
- `line-length` (integer): Line length (default 88)
- `check` (boolean): Check without writing

**Commands:**
- `black --safe src/`
- `black --check src/`
- `black --diff src/`
- `black file1.py file2.py`
- `black --line-length 100 src/`

**Examples:**
- black --check --diff src/
- black --line-length 88 --target-version py312 src/
- black --fast src/

### black-config
Configure Black per project.

**Parameters:**
- `exclude` (string): Regex of files to exclude
- `config` (string): pyproject.toml or setup.cfg path

**Commands:**
- `black --version`
- `black --help | grep line-length`
- `black --exclude "/(\\.venv|node_modules)/" src/`
- `black --include "\\.pyi?$" src/`

**Examples:**
- black --exclude "/migrations/" src/
- python -m black src/

## References
- [Black Docs](https://black.readthedocs.io)
- [Black on GitHub](https://github.com/psf/black)
