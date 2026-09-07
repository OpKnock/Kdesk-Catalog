---
name: "black"
description: "Formats Python code with Black: deterministic formatting, config control, diff previews, and CI enforcement. Use when working with black format, black config, code quality or when the user mentions black format, black config, code quality."
license: "MIT"
compatibility: "Requires black."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(black:*)"
---

Formats Python code with Black: deterministic formatting, config control, diff previews, and CI enforcement.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `black --safe src/`, `black --version`
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
