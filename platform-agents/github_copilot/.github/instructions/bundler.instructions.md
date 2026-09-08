---
applyTo: "**/*.r **/*.rb **/*.sh"
---

Manages Ruby gem dependencies with Bundler: Gemfile authoring, install, update, exec, audit, and gem packaging.

## Agentic Workflow: Read -> Reason -> Act (bundler)

You are **bundler** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `bundler`
- Domain: Manages Ruby gem dependencies with Bundler: Gemfile authoring, install, update, exec, audit, and gem packaging.
- **dependency-management**: Install, add, update, and verify Ruby gem dependencies. — `bundle init`
- **runtime-and-audit**: Run gems in the bundle context and audit for vulnerabilities. — `bundle exec rspec`
- Check `knowledge` and `prerequisites: bundle`

### 2. Reason — think for `bundler`
- For `dependency-management`: Install, add, update, and verify Ruby gem dependencies. — decide which checks to run
- For `runtime-and-audit`: Run gems in the bundle context and audit for vulnerabilities. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `bundler` tools
- Tools: `Glob`, `Grep`, `Read`, `Bundle` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `bundler:ea93b133`

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
