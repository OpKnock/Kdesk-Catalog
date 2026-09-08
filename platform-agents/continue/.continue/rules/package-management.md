---
name: "package-management"
description: "Manages dependencies across ecosystems: npm/pnpm/yarn, pip/uv, cargo, and go modules \u2014 install, update, audit, and CI strategies. Use when working with js package managers, python and system, devtools or when the user mentions js package managers, python and system, devtools."
globs: ["**/*.go", "**/*.java", "**/*.py", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

Manages dependencies across ecosystems: npm/pnpm/yarn, pip/uv, cargo, and go modules — install, update, audit, and CI strategies.

## Agentic Workflow: Read -> Reason -> Act (package-management)

You are **package-management** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `package-management`
- Domain: Manages dependencies across ecosystems: npm/pnpm/yarn, pip/uv, cargo, and go modules — install, update, audit, and CI strategies.
- **js-package-managers**: Install and audit JavaScript dependencies with npm/pnpm/yarn. — `npm install`
- **python-and-system**: Manage Python, Rust, and Go dependencies. — `pip install -r requirements.txt`
- Check `knowledge` and `prerequisites: cargo, npm, pip, pip-audit`

### 2. Reason — think for `package-management`
- For `js-package-managers`: Install and audit JavaScript dependencies with npm/pnpm/yarn. — decide which checks to run
- For `python-and-system`: Manage Python, Rust, and Go dependencies. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `package-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Pnpm` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `package-management:4a7f48d6`

# Cross-Ecosystem Package Management

Install, update, and audit dependencies across languages.

## What This Skill Does

- Manages JS deps (npm/pnpm/yarn) with lockfiles
- Manages Python deps (pip/uv) and virtualenvs
- Manages Rust (cargo) and Go modules
- Audits all ecosystems for vulnerabilities
- Advises on lockfile and CI strategies

## When to Use

- Setting up dependency management for a project
- Responding to vulnerability advisories
- Standardizing package manager workflows

## Real Commands

```bash
# JavaScript
npm install
npm ci                          # clean lockfile install
npm audit --audit-level=high
npm outdated
pnpm dlx create-vite@latest myapp
yarn upgrade-interactive

# Python
python -m venv .venv
pip install -r requirements.txt
pip-audit -r requirements.txt
uv pip install -e ".[dev]"

# Rust / Go
cargo add serde --features derive
cargo audit
cargo update
go mod tidy
go get -u ./...
```

## Best Practices

- Commit lockfiles and use npm ci / pnpm install --frozen-lockfile in CI
- Run audits on every merge (npm audit, pip-audit, cargo audit)
- Prefer one package manager per repo; do not mix
- Pin direct deps, let transitive resolve from lockfile
- Use uv for speed on large Python projects
- Add `dependabot` or Renovate for automated update PRs

## Capabilities

### js-package-managers
Install and audit JavaScript dependencies with npm/pnpm/yarn.

**Parameters:**
- `package` (string): Package name
- `audit-level` (string): Audit severity threshold

**Commands:**
- `npm install`
- `npm ci`
- `npm audit --audit-level=high`
- `npm outdated`
- `pnpm dlx create-vite@latest myapp`
- `yarn upgrade-interactive`

**Examples:**
- npm ci
- npm audit --audit-level=high
- pnpm dlx create-vite@latest myapp

### python-and-system
Manage Python, Rust, and Go dependencies.

**Parameters:**
- `file` (string): Requirements/manifest file
- `crate` (string): Crate name for cargo add

**Commands:**
- `pip install -r requirements.txt`
- `pip-audit -r requirements.txt`
- `uv pip install -r pyproject.toml`
- `cargo add serde --features derive`
- `cargo audit`
- `go mod tidy`
- `go get -u ./...`

**Examples:**
- pip-audit -r requirements.txt
- cargo audit
- go mod tidy

## References
- [npm CLI](https://docs.npmjs.com/cli/)
- [pip-audit](https://github.com/pypa/pip-audit)
- [cargo-audit](https://rustsec.org/)
- [uv](https://docs.astral.sh/uv/)