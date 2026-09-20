---
name: "bundler"
description: "Manages Ruby gem dependencies with Bundler: Gemfile authoring, install, update, exec, audit, and gem packaging. Use when working with dependency management, runtime and audit, devtools or when the user mentions dependency management, runtime and audit, devtools."
license: "MIT"
compatibility: "Requires bundle."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devtools"}
allowed-tools: "Glob Grep Read Bash(bundle:*)"
---

Manages Ruby gem dependencies with Bundler: Gemfile authoring, install, update, exec, audit, and gem packaging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bundle init`, `bundle exec rspec`
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

# Bundler for Ruby

Manage Ruby gem dependencies deterministically with Bundler.

## What This Skill Does

- Author Gemfile and resolve Gemfile.lock
- Installs gems into the bundle path
- Updates and reports outdated gems
- Runs commands inside the bundle context (bundle exec)
- Audits dependencies for vulnerabilities
- Builds new gem skeletons

## When to Use

- Any Ruby project with dependencies
- Upgrading a Rails app's gem set
- CI: install from lockfile deterministically

## Real Commands

```bash
# Project setup
bundle init
bundle add rails --version '~> 7.1'
bundle add rspec --group test
bundle install --jobs 4
bundle config set path vendor/bundle

# Maintenance
bundle update --all
bundle outdated
bundle check
bundle lock --add-platform x86_64-linux

# Runtime
bundle exec rspec
bundle exec rake db:migrate
bundle exec rubocop

# Security
bundle audit check --update
bundle audit fix --patch

# Packaging
bundle gem my_gem
```

## Best Practices

- Commit Gemfile.lock for apps (not for gems)
- Use groups: development/test/production separation
- Run bundle audit in CI to fail on vulnerable deps
- Use `bundle exec` to avoid version conflicts
- Add platforms to the lockfile for multi-OS teams

## Capabilities

### dependency-management
Install, add, update, and verify Ruby gem dependencies.

**Parameters:**
- `gem` (string): Gem name
- `version` (string): Version constraint
- `group` (string): Gem group, e.g. test, development

**Commands:**
- `bundle init`
- `bundle install --jobs 4`
- `bundle add rails --version '~> 7.1'`
- `bundle update --all`
- `bundle outdated`
- `bundle check`
- `bundle config set path vendor/bundle`

**Examples:**
- bundle install --jobs 4
- bundle add rspec --group test
- bundle outdated

### runtime-and-audit
Run gems in the bundle context and audit for vulnerabilities.

**Parameters:**
- `command` (string): Command to run in bundle context
- `platform` (string): Platform to add to lockfile

**Commands:**
- `bundle exec rspec`
- `bundle exec rake db:migrate`
- `bundle audit check --update`
- `bundle exec rubocop`
- `bundle lock --add-platform x86_64-linux`
- `bundle clean --force`

**Examples:**
- bundle exec rspec
- bundle audit check --update
- bundle lock --add-platform x86_64-linux

## References
- [Bundler Documentation](https://bundler.io/docs.html)
- [bundle-audit](https://github.com/rubysec/bundler-audit)
