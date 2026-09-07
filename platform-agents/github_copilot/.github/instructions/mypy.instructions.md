---
applyTo: "**/*.py **/*.r **/*.sh **/*.{yaml,yml}"
---

Static type checking of Python code with mypy, including strict mode, incremental builds, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mypy src/`
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

# MyPy

Static type checker for Python. Finds type errors before runtime, on both typed and
untyped codebases.

## When to Use

- Verifying type safety of a Python application or library
- Enforcing strict typing on core modules while onboarding old code
- Checking that refactors did not break type contracts

## Real Commands

```bash
# Install
pip install mypy

# Basic check
mypy src/

# Strict mode (all checks on)
mypy --strict src/

# Check specific packages, ignore missing stubs
mypy --ignore-missing-imports app tests

# Target a specific Python version
mypy --python-version 3.11 --config-file mypy.ini .

# No caching for CI runs
mypy --no-incremental --cache-dir=/dev/null src/

# Show error codes to suppress selectively
mypy --show-error-codes src/
```

## Config (mypy.ini)

```ini
[mypy]
python_version = 3.11
strict = true
ignore_missing_imports = true
exclude = (venv|build)/

[mypy.plugins]
plugins = pydantic.mypy
```

## CI

```yaml
- name: Type check
  run: mypy src/ --no-incremental
```

## Best Practices

- Adopt `--strict` per-module via `# mypy: disable-error-code` only when needed
- Use `--show-error-codes` to address each code class once
- Disable incremental cache in CI for determinism
- Use `--exclude` for generated code instead of `--ignore-missing-imports` everywhere

## Capabilities

### type-check-python
Run mypy with configurable strictness, scopes, and output formats

**Parameters:**
- `strict` (boolean): Enable all strict mode flags (no untyped defs, disallow Any, etc.)
- `python-version` (string): Python version to type check against, e.g. 3.11
- `ignore-missing-imports` (boolean): Silence errors for packages without type stubs

**Commands:**
- `mypy src/`
- `mypy --strict src/`
- `mypy --ignore-missing-imports --no-incremental src/`
- `mypy --python-version 3.11 --config-file mypy.ini app/`
- `mypy --warn-unused-configs --check-untyped-defs src/`

**Examples:**
- mypy src tests
- mypy --strict --show-error-codes src/
- mypy --cache-dir=.mypy_cache --pretty src/

## References
- [mypy documentation](https://mypy.readthedocs.io/)
- [mypy strict mode](https://mypy.readthedocs.io/en/stable/command_line.html)
