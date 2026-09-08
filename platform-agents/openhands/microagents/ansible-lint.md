---
name: "ansible-lint"
description: "Lints Ansible playbooks and roles with ansible-lint: best-practice rules, YAML validation, and CI integration. Use when working with ansible lint cli, ansible lint config, code quality or when the user mentions ansible lint cli, ansible lint config, code quality."
type: knowledge
triggers: ["ansible-lint", "ansible-lint-cli", "ansible-lint-config"]
---

Lints Ansible playbooks and roles with ansible-lint: best-practice rules, YAML validation, and CI integration.

## Agentic Workflow: Read -> Reason -> Act (ansible-lint)

You are **Ansible Lint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `ansible-lint`
- Domain: Lints Ansible playbooks and roles with ansible-lint: best-practice rules, YAML validation, and CI integration.
- **ansible-lint-cli**: Run ansible-lint with rule and config control. — `ansible-lint playbooks/`
- **ansible-lint-config**: Manage config and rule selection. — `ansible-lint --generate-ignore-file`
- Check `knowledge` and `prerequisites: ansible-lint`

### 2. Reason — think for `ansible-lint`
- For `ansible-lint-cli`: Run ansible-lint with rule and config control. — decide which checks to run
- For `ansible-lint-config`: Manage config and rule selection. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ansible-lint` tools
- Tools: `Glob`, `Grep`, `Read`, `Ansible-lint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ansible-lint:f7dd7087`

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
