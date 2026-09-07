---
name: "ansible-lint"
description: "Lints Ansible playbooks and roles with ansible-lint: best-practice rules, YAML validation, and CI integration. Use when working with ansible lint cli, ansible lint config, code quality or when the user mentions ansible lint cli, ansible lint config, code quality."
license: "MIT"
compatibility: "Requires ansible-lint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(ansible-lint:*)"
---

Lints Ansible playbooks and roles with ansible-lint: best-practice rules, YAML validation, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ansible-lint playbooks/`, `ansible-lint --generate-ignore-file`
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

# ansible-lint

Lint Ansible playbooks and roles.

## When to Use

- Enforcing best practices across playbook repositories
- Catching YAML, module, and FQCN mistakes before runs
- CI gating on infrastructure-as-code changes
- Keeping roles consistent across the codebase

## Commands

```bash
# Lint a directory
ansible-lint playbooks/

# Verbose
ansible-lint playbook.yml -v

# Exclude directories
ansible-lint --exclude=roles/vendor/

# Custom rules dir
ansible-lint -r custom-rules.yml playbook.yml

# Skip a rule
ansible-lint playbook.yml --skip-list fqcn-builtins

# List rules and tags
ansible-lint --list-rules
ansible-lint --list-tags

# Auto-fix
ansible-lint --fix playbook.yml
```

## Config Example

```yaml
# .ansible-lint
exclude_paths:
  - .cache
  - roles/vendor
skip_list:
  - yaml[line-length]
warn_list:
  - experimental
```

## Best Practices

- Run ansible-lint in CI on every MR
- Use FQCNs for all modules (ansible.builtin.*)
- Add no-changed-when to every command task
- Keep line length within the yaml rule default
- Auto-fix with --fix, then review the diff
- Treat new violations as blockers; manage legacy ones via skip_list

## Capabilities

### ansible-lint-cli
Run ansible-lint with rule and config control.

**Parameters:**
- `paths` (string): Files or directories to lint
- `skip-list` (string): Comma-separated rule ids to skip
- `verbose` (boolean): Verbose output

**Commands:**
- `ansible-lint playbooks/`
- `ansible-lint playbook.yml -v`
- `ansible-lint --exclude=roles/vendor/`
- `ansible-lint -r custom-rules.yml playbook.yml`
- `ansible-lint --offline`

**Examples:**
- ansible-lint -p playbooks/
- ansible-lint playbook.yml --skip-list fqcn-builtins
- ansible-lint --list-tags

### ansible-lint-config
Manage config and rule selection.

**Parameters:**
- `config` (string): Config file path
- `fix` (boolean): Auto-fix issues

**Commands:**
- `ansible-lint --generate-ignore-file`
- `ansible-lint --list-rules`
- `ansible-lint --config .ansible-lint`
- `ansible-lint --fix playbook.yml`

**Examples:**
- ansible-lint --list-rules | grep -i "no-changed-when"
- ansible-lint --fix

## References
- [ansible-lint Docs](https://ansible.readthedocs.io/projects/lint/)
- [Ansible Docs](https://docs.ansible.com/)
