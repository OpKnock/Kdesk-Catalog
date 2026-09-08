---
name: "toml"
description: "Query, validate, and format TOML configuration files using tomlq, yq, Python's stdlib tomllib, and taplo. Reads Cargo.toml and pyproject.toml values, enforces consistent formatting in CI, and parses TOML safely without external dependencies. Use when working with toml tooling, api or when the user mentions toml tooling, api."
---

Query, validate, and format TOML configuration files using tomlq, yq, Python's stdlib tomllib, and taplo. Reads Cargo.toml and pyproject.toml values, enforces consistent formatting in CI, and parses TOML safely without external dependencies.

## Agentic Workflow: Read -> Reason -> Act (toml)

You are **Toml** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `toml`
- Domain: Query, validate, and format TOML configuration files using tomlq, yq, Python's stdlib tomllib, and taplo. Reads Cargo.toml and pyproject.toml values, enforces consistent formatting in CI, and parses T
- **toml-tooling**: Query, validate, and format TOML files — `tomlq -r '.package.name' Cargo.toml`
- Check `knowledge` and `prerequisites: python, taplo, tomlq`

### 2. Reason — think for `toml`
- For `toml-tooling`: Query, validate, and format TOML files — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `toml` tools
- Tools: `Glob`, `Grep`, `Read`, `Tomlq`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `toml:169e3cbf`

# TOML

Hand-crafted skill for reading and editing TOML configuration files.

## What this skill does

- Queries TOML with tomlq and yq's toml parser
- Reads config with Python's stdlib tomllib
- Formats and lints with taplo

## When to use

- Cargo.toml or pyproject.toml config questions
- Editing .toml configs in CI scripts
- Enforcing consistent formatting on TOML files

## Real commands

```bash
# Query values
tomlq -r '.package.name' Cargo.toml
tomlq -r '.package.version' Cargo.toml

# yq handles toml with -p toml
yq -p toml '.tool.pytest.ini_options' pyproject.toml
yq -p toml '.dependencies.rocket' Cargo.toml

# Python stdlib (3.11+)
python -c "import tomllib; print(tomllib.load(open('Cargo.toml','rb'))['package']['name'])"
python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['dependencies'])"

# Format and lint
taplo fmt Cargo.toml
taplo lint Cargo.toml
taplo fmt --check .   # CI gate
```

## TOML basics

```toml
[package]
name = "demo"
version = "0.1.0"

[dependencies]
rocket = "0.5.1"
```

## Testing

```bash
tomlq -r '.package.name' Cargo.toml
python -c "import tomllib; tomllib.load(open('pyproject.toml','rb')); print('valid')"
```

## Best practices

- Prefer tomllib (read-only) over toml package for safety
- Use yq -p toml to pipe TOML into other jq-style processing
- Run taplo fmt --check in CI to keep formatting consistent

## Capabilities

### toml-tooling
Query, validate, and format TOML files

**Parameters:**
- `file` (string): TOML file to query or format
- `expression` (string): jq-style path like .package.name
- `format` (boolean): taplo fmt or --check

**Commands:**
- `tomlq -r '.package.name' Cargo.toml`
- `yq -p toml '.tool.pytest.ini_options' pyproject.toml`
- `python -c "import tomllib; print(tomllib.load(open('Cargo.toml','rb'))['package']['name'])"`
- `taplo fmt Cargo.toml`
- `taplo lint Cargo.toml`

**Examples:**
- tomlq -r '.package.version' Cargo.toml
- yq -p toml '.dependencies.rocket' Cargo.toml
- python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['dependencies'])"

## References
- [TOML spec v1.0](https://toml.io/en/v1.0.0)
- [taplo CLI](https://taplo.tamasfe.dev/cli/introduction.html)
