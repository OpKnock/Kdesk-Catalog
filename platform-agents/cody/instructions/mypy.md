Static type checking of Python code with mypy, including strict mode, incremental builds, and CI integration.

## Agentic Workflow: Read -> Reason -> Act (mypy)

You are **mypy** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `mypy`
- Domain: Static type checking of Python code with mypy, including strict mode, incremental builds, and CI integration.
- **type-check-python**: Run mypy with configurable strictness, scopes, and output formats — `mypy src/`
- Check `knowledge` and `prerequisites: mypy`

### 2. Reason — think for `mypy`
- For `type-check-python`: Run mypy with configurable strictness, scopes, and output formats — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mypy` tools
- Tools: `Glob`, `Grep`, `Read`, `Mypy` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mypy:838f6537`

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
