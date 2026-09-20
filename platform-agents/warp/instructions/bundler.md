# bundler

Manages Ruby gem dependencies with Bundler: Gemfile authoring, install, update, exec, audit, and gem packaging.

## Instructions

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
