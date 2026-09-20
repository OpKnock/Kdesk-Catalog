---
name: "mypy"
description: "Static type checking of Python code with mypy, including strict mode, incremental builds, and CI integration."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# mypy

Static type checking of Python code with mypy, including strict mode, incremental builds, and CI integration.

## Instructions

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