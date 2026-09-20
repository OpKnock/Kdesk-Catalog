---
type: agent_requested
description: "Automates infrastructure with Ansible: ad-hoc commands, playbooks, roles, and vault secrets. Use when working with ansible playbooks, devops or when the user mentions ansible playbooks, devops."
---

Automates infrastructure with Ansible: ad-hoc commands, playbooks, roles, and vault secrets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ansible all -i inventory.yml -m ping`
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

# Ansible

Configuration management and automation: idempotent playbooks, roles, ad-hoc
commands, and encrypted secrets.

## When to Use

- Provisioning/configuring servers at scale
- Repeating multi-step setup idempotently
- Rolling out config changes with validation

## Real Commands

```bash
# Connectivity
sudo ansible all -i inventory.yml -m ping

# Ad-hoc
sudo ansible all -i inventory.yml -m command -a 'uptime'
sudo ansible web -i inventory.yml -m apt -a 'name=nginx state=latest' -b

# Playbooks
sudo ansible-playbook --syntax-check playbooks/deploy.yml
sudo ansible-playbook -i inventory.yml playbooks/deploy.yml --check --diff
sudo ansible-playbook -i inventory.yml playbooks/deploy.yml

# Scoped runs
sudo ansible-playbook -i inventory.yml playbooks/deploy.yml --limit web --tags nginx

# Roles
sudo ansible-galaxy init roles/webserver
sudo ansible-galaxy install geerlingguy.nginx -p roles/

# Secrets
sudo ansible-vault create secrets.yml
sudo ansible-vault encrypt secrets.yml
sudo ansible-playbook -i inventory.yml playbooks/deploy.yml --ask-vault-pass
```

## Playbook Example

```yaml
- hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: latest
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: true
```

## Best Practices

- Always run `--check --diff` before applying to production
- Keep playbooks idempotent (state=..., not shell)
- Use `--limit` and tags for targeted rollouts
- Encrypt secrets with ansible-vault; never plaintext
- Version inventories as code, per environment

## Example Response

For a rollout: syntax-checks, dry-runs with --check --diff, applies to the target
hosts, and reports changed/ok/failed per host.

## Capabilities

### ansible-playbooks
Run ad-hoc tasks and playbooks across inventories

**Parameters:**
- `inventory` (string): Inventory file or directory (-i)
- `check` (boolean): Dry-run: report changes without applying
- `tags` (string): Run only tasks with these tags

**Commands:**
- `ansible all -i inventory.yml -m ping`
- `ansible-playbook -i inventory.yml playbooks/deploy.yml`
- `ansible-playbook --syntax-check playbooks/deploy.yml`
- `ansible-playbook -i inventory.yml playbooks/deploy.yml --check --diff`
- `ansible-galaxy init roles/webserver`

**Examples:**
- ansible all -i inventory.yml -m command -a 'uptime'
- ansible-playbook -i inventory.yml playbooks/deploy.yml --limit web --tags nginx
- ansible-vault encrypt secrets.yml

## References
- [Ansible docs](https://docs.ansible.com/ansible/latest/index.html)
- [Ansible Galaxy](https://galaxy.ansible.com/)