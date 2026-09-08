---
applyTo: "**/*.py **/*.r **/*.sh"
---

Sorts Python imports with isort: config profiles, black compatibility, section handling, and CI checks.

## Agentic Workflow: Read -> Reason -> Act (isort)

You are **isort** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `isort`
- Domain: Sorts Python imports with isort: config profiles, black compatibility, section handling, and CI checks.
- **isort-sort**: Sort imports with control over profiles. — `isort src/`
- **isort-config**: Configure import sections and settings. — `isort --version`
- Check `knowledge` and `prerequisites: isort`

### 2. Reason — think for `isort`
- For `isort-sort`: Sort imports with control over profiles. — decide which checks to run
- For `isort-config`: Configure import sections and settings. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `isort` tools
- Tools: `Glob`, `Grep`, `Read`, `Isort` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `isort:bcd4d0d5`

# isort

Sort Python imports consistently.

## When to Use

- Enforcing import ordering across a Python codebase
- Pairing with black for a full formatting story
- Grouping stdlib, third-party, and first-party imports
- CI gates that catch import drift

## Commands

```bash
# Sort a directory
isort src/

# Check only
isort --check-only src/

# Show diff
isort --diff src/

# Black-compatible profile
isort --profile black src/
```

## Config Example

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 100
skip = ["migrations", "venv"]
known_first_party = ["myapp"]
```

## Import Order

```python
# stdlib first
import os
import sys

# third-party
import requests

# first-party
from myapp import utils
```

## Best Practices

- Use profile = black so black and isort agree
- Add known_first_party for your own packages
- Run isort --check-only in CI, sort in pre-commit
- Keep sections: stdlib, third-party, first-party
- Skip generated files and migrations
- Run isort before black for stable results

## Capabilities

### isort-sort
Sort imports with control over profiles.

**Parameters:**
- `paths` (string): Files or directories
- `profile` (string): black, django, google
- `check-only` (boolean): Check without writing

**Commands:**
- `isort src/`
- `isort --check-only src/`
- `isort --diff src/`
- `isort --profile black src/`
- `isort file1.py file2.py`

**Examples:**
- isort --check-only --diff src/
- isort --profile black --line-length 100 src/
- isort --skip venv --skip migrations src/

### isort-config
Configure import sections and settings.

**Parameters:**
- `settings-path` (string): Config file path
- `profile` (string): Sorting profile: black, django

**Commands:**
- `isort --version`
- `isort --settings-path pyproject.toml src/`
- `isort --show-config`
- `isort --resolve-all-configs src/`

**Examples:**
- isort --show-config | grep -A5 profile
- python -m isort src/

## References
- [isort Docs](https://pycqa.github.io/isort/)
- [isort on GitHub](https://github.com/PyCQA/isort)
