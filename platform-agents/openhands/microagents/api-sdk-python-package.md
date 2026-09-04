---
name: "api-sdk-python-package"
description: "Builds Python SDKs: pyproject.toml configuration, python -m build, editable installs, twine checks, and PyPI publishing."
type: knowledge
triggers: ["api-sdk-python-package", "python-package", "package-metadata"]
---

# Api Sdk Python Package

Builds Python SDKs: pyproject.toml configuration, python -m build, editable installs, twine checks, and PyPI publishing.

## Instructions

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
