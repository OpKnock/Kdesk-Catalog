Builds Python SDKs: pyproject.toml configuration, python -m build, editable installs, twine checks, and PyPI publishing.

## Agentic Workflow: Read -> Reason -> Act (api-sdk-python-package)

You are **Api Sdk Python Package** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-sdk-python-package`
- Domain: Builds Python SDKs: pyproject.toml configuration, python -m build, editable installs, twine checks, and PyPI publishing.
- **python-package**: Package a Python SDK with build and setuptools — `pip install build twine`
- **package-metadata**: Configure pyproject.toml metadata — `python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d[`
- Check `knowledge` and `prerequisites: openapi-generator, node.js, python`

### 2. Reason — think for `api-sdk-python-package`
- For `python-package`: Package a Python SDK with build and setuptools — decide which checks to run
- For `package-metadata`: Configure pyproject.toml metadata — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sdk-python-package` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Twine` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sdk-python-package:1b6ca7bd`

# API SDK v3 - Python

Python SDK packaging.

## What This Skill Does
- Configures pyproject.toml
- Builds sdist and wheels
- Publishes to PyPI with twine

## When to Use
- Building Python clients
- Distributing SDKs to internal users
- Open-source SDK releases

## Real Commands

```bash
pip install build twine
python -m build
pip install -e .
twine check dist/*
twine upload dist/*
```

## pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "my-sdk"
version = "1.0.0"
description = "Client SDK for My API"
```

## Testing
- Install from the built wheel in a venv
- Verify import works after install
- Check twine metadata before upload

## Best Practices
- Test on test.pypi.org first
- Pin dependency ranges loosely
- Keep the package importable and typed

## Capabilities

### python-package
Package a Python SDK with build and setuptools

**Parameters:**
- `dist` (string): Distribution files glob
- `repository` (string): PyPI repository URL
- `token` (string): PyPI API token

**Commands:**
- `pip install build twine`
- `python -m build`
- `pip install -e .`
- `twine check dist/*`
- `twine upload dist/*`

**Examples:**
- python -m build creates sdist and wheel
- pip install -e . installs in editable mode
- twine check validates package metadata

### package-metadata
Configure pyproject.toml metadata

**Commands:**
- `python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['name'], d['project']['version'])"`
- `pip show my-sdk`
- `python -c "import my_sdk; print(my_sdk.__version__)"`

**Examples:**
- -cli --help
- -api --help

## References
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Twine Docs](https://twine.readthedocs.io/en/stable/)
