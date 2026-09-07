---
applyTo: "**/*.py **/*.r **/*.sh"
---

Lints Python with flake8 (pyflakes + pycodestyle + mccabe): style, complexity, and bug checks with plugins and configs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `flake8 src/`, `pip install flake8-bugbear`
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

# Flake8

Python style and logic linting.

## When to Use

- Enforcing PEP 8 style consistently
- Catching unused imports, undefined names (pyflakes)
- Complexity budgets with mccabe
- Fast CI linting with minimal config

## Commands

```bash
# Basic
flake8 src/

# Tuning
flake8 src/ --max-line-length 100
flake8 src/ --max-complexity 10

# Selection and stats
flake8 --select E,F,W src/
flake8 --statistics src/
flake8 --count src/

# Ignore codes
flake8 --extend-ignore E203,W503 src/

# Plugins
pip install flake8-bugbear flake8-docstrings
flake8 --select B,D src/
```

## Config Example

```toml
# setup.cfg
[flake8]
max-line-length = 100
max-complexity = 12
extend-ignore = E203,W503
exclude = .git,__pycache__,migrations
```

## Best Practices

- Pair with black: ignore E203/W503 which conflict with black
- Keep the complexity threshold low (10-12)
- Use pyflakes code F catches for real bugs
- Add bugbear plugin for common footguns
- Run flake8 --statistics in CI for trend tracking
- Exclude generated and vendored directories

## Capabilities

### flake8-lint
Run flake8 checks with configuration.

**Parameters:**
- `paths` (string): Files or directories
- `max-line-length` (integer): Line length limit
- `max-complexity` (integer): Complexity threshold

**Commands:**
- `flake8 src/`
- `flake8 src/main.py --max-line-length 100`
- `flake8 --max-complexity 10 src/`
- `flake8 --extend-ignore E203,W503 src/`
- `flake8 --count src/`

**Examples:**
- flake8 --statistics src/
- flake8 --select E,F,W src/
- flake8 --show-source src/

### flake8-plugins
Extend flake8 with plugins.

**Parameters:**
- `select` (string): Comma-separated codes to run
- `plugin` (string): PyPI plugin package, e.g. flake8-bugbear

**Commands:**
- `pip install flake8-bugbear`
- `pip install flake8-docstrings`
- `pip install flake8-annotations`
- `flake8 --version`

**Examples:**
- pip install flake8-print flake8-builtins
- flake8 --select B,D,ANN src/

## References
- [Flake8 Docs](https://flake8.pycqa.org)
- [Pycodestyle Docs](https://pycodestyle.pycqa.org)
- [Pyflakes Docs](https://github.com/PyCQA/pyflakes)
