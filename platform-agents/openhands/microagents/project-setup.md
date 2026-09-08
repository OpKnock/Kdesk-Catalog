---
name: "project-setup"
description: "Bootstraps new projects: git init, scaffolds (create-vite, cargo new, cookiecutter), venvs, repo creation, and CI skeleton. Use when working with scaffolding, repo and hygiene, devtools or when the user mentions scaffolding, repo and hygiene, devtools."
type: knowledge
triggers: ["project-setup", "scaffolding", "repo-and-hygiene"]
---

Bootstraps new projects: git init, scaffolds (create-vite, cargo new, cookiecutter), venvs, repo creation, and CI skeleton.

## Agentic Workflow: Read -> Reason -> Act (project-setup)

You are **project-setup** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `project-setup`
- Domain: Bootstraps new projects: git init, scaffolds (create-vite, cargo new, cookiecutter), venvs, repo creation, and CI skeleton.
- **scaffolding**: Scaffold projects with ecosystem-standard generators. — `npx create-vite@latest frontend --template react-ts`
- **repo-and-hygiene**: Create repos and set up baseline project hygiene. — `git init -b main`
- Check `knowledge` and `prerequisites: cargo, cookiecutter, echo, git`

### 2. Reason — think for `project-setup`
- For `scaffolding`: Scaffold projects with ecosystem-standard generators. — decide which checks to run
- For `repo-and-hygiene`: Create repos and set up baseline project hygiene. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `project-setup` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `project-setup:27bbc19f`

# Project Bootstrapping

Scaffold new repositories quickly with correct structure and tooling.

## What This Skill Does

- Scaffolds apps with framework generators (Vite, cargo new, cookiecutter)
- Initializes git and creates GitHub repos
- Sets up virtualenvs and module paths
- Adds baseline hygiene: .gitignore, lint, CI skeleton
- Makes the first commit

## When to Use

- Starting any new project
- Standardizing project creation across teams
- Setting up CI + repo in one flow

## Real Commands

```bash
# Scaffold
npx create-vite@latest frontend --template react-ts
cargo new my-service --bin
cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
python -m venv .venv
go mod init github.com/acme/service

# Clone-based (no git history)
npx degit user/repo my-clone

# Repo setup
git init -b main
gh repo create myorg/myapp --private --source=. --push
git add -A
git commit -m 'chore: scaffold project'
```

## Baseline Hygiene Checklist

- .gitignore (node_modules, .env, dist, __pycache__)
- License + README
- Lint config (eslint/ruff)
- CI workflow skeleton
- Lockfile committed

## Best Practices

- Use --template flags over manual file creation
- Create the repo with --source=. --push to avoid re-clone
- Commit the scaffold immediately to keep diffs reviewable
- Add CI in the same PR as the scaffold
- Choose generator templates that match team standards

## Capabilities

### scaffolding
Scaffold projects with ecosystem-standard generators.

**Parameters:**
- `name` (string): Project name
- `template` (string): Scaffold template

**Commands:**
- `npx create-vite@latest frontend --template react-ts`
- `cargo new my-service --bin`
- `cookiecutter gh:audreyfeldroy/cookiecutter-pypackage`
- `python -m venv .venv`
- `go mod init github.com/acme/service`
- `npx degit user/repo my-clone`

**Examples:**
- npx create-vite@latest frontend --template react-ts
- cargo new my-service --bin
- cookiecutter gh:audreyfeldroy/cookiecutter-pypackage

### repo-and-hygiene
Create repos and set up baseline project hygiene.

**Parameters:**
- `org` (string): GitHub org for repo creation
- `repo-name` (string): Repository name

**Commands:**
- `git init -b main`
- `gh repo create myorg/myapp --private --source=. --push`
- `git commit -m 'chore: initial commit'`
- `npx eslint --init`
- `echo 'node_modules/' > .gitignore`
- `git add -A && git commit -m 'chore: scaffold'`

**Examples:**
- gh repo create myorg/myapp --private --source=. --push
- git init -b main
- echo 'node_modules/' > .gitignore

## References
- [create-vite](https://vite.dev/guide/)
- [gh repo create](https://cli.github.com/manual/gh_repo_create)
- [Cookiecutter](https://cookiecutter.readthedocs.io/)
