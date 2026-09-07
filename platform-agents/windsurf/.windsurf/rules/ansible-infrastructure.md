---
trigger: glob
description: "Automates server configuration with Ansible: inventory, playbooks, roles, and ad-hoc modules across fleets. Use when working with playbooks, ad hoc, infrastructure or when the user mentions playbooks, ad hoc, infrastructure."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Automates server configuration with Ansible: inventory, playbooks, roles, and ad-hoc modules across fleets.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ansible-playbook -i inventory/prod.ini site.yml`, `ansible all -m ping -i inventory/prod.ini`
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

Automate server provisioning and configuration with Ansible.

## When to Use

- Bootstrapping and configuring VM fleets
- Enforcing service state (installed, running, enabled)
- Reproducible multi-environment deploys

## Inventory

```ini
[web]
web-1 ansible_host=10.0.1.11
web-2 ansible_host=10.0.1.12

[db]
db-1 ansible_host=10.0.2.21

[all:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/deploy_key
```

## Playbook structure

```yaml
- name: Configure web servers
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Restart nginx on config change
      service:
        name: nginx
        state: restarted
      notify: reload nginx
  handlers:
    - name: reload nginx
      service: { name: nginx, state: reloaded }
```

## Run safely

```bash
ansible-playbook -i inventory/prod.ini site.yml --check --diff
ansible-playbook site.yml --tags deploy
```

Always run `--check --diff` first on an unknown codebase.

## Ad-hoc operations

```bash
ansible all -m ping -i inventory/prod.ini
ansible web -m service -a 'name=nginx state=restarted' -b
```

## Roles

```bash
ansible-galaxy init roles/nginx
ansible-galaxy install -r requirements.yml
```

## Best practices

- Idempotent tasks: each run converges to the same state.
- Keep secrets in ansible-vault, never in vars files.
- Use handlers for restart-on-change, never restart unconditionally.
- Run check mode in CI on every PR.

## Testing

```bash
ansible-lint site.yml
ansible-playbook site.yml --syntax-check
```

Gate merges on both.

## Capabilities

### playbooks
Write and run Ansible playbooks against inventories.

**Parameters:**
- `inventory` (string): Inventory file or directory
- `tags` (string): Comma-separated tags to run
- `limit` (string): Host pattern subset to target

**Commands:**
- `ansible-playbook -i inventory/prod.ini site.yml`
- `ansible-playbook site.yml --tags deploy`
- `ansible-playbook site.yml --check --diff`
- `ansible-playbook site.yml --limit web --start-at-task 'nginx: restart'`
- `ansible-playbook site.yml -e env=staging`

**Examples:**
- ansible-playbook -i inventory/prod.ini site.yml --check
- ansible-playbook site.yml --tags nginx,deploy --diff
- ansible-playbook site.yml --limit 'web:!web-3'

### ad-hoc
Run one-off modules across hosts without a playbook.

**Parameters:**
- `module` (string): Module like service, apt, ping, shell
- `args` (string): Module arguments as key=value string
- `become` (string): Elevate privileges with -b

**Commands:**
- `ansible all -m ping -i inventory/prod.ini`
- `ansible web -m service -a 'name=nginx state=restarted' -b`
- `ansible db -m shell -a 'df -h /data'`
- `ansible all -m apt -a 'name=unattended-upgrades state=present' -b`
- `ansible all -m gather_facts --limit web`

**Examples:**
- ansible web -m service -a 'name=nginx state=started' -b --become-user=root
- ansible all -m ping --one-line
- ansible db -m command -a 'free -m'

## References
- [Ansible Docs](https://docs.ansible.com/ansible/latest/index.html)
- [Ansible CLI](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html)
- [Ansible Galaxy](https://galaxy.ansible.com/)
