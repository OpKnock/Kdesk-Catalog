---
type: agent_requested
description: "Manage API server and service configuration with Ansible playbooks, roles, and config validation commands. Use when working with ansible playbooks, roles and config, api or when the user mentions ansible playbooks, roles and config, api."
---

Manage API server and service configuration with Ansible playbooks, roles, and config validation commands.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ansible --version`, `ansible-galaxy init api-config-role`
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

# Configuration Management

Manage API configuration across servers with Ansible.

## When to Use

- Rolling out API config changes to fleets of servers
- Templating per-environment config from a single source
- Enforcing drift-free, idempotent configuration

## Setup

```bash
pip install ansible
ansible --version
```

## Inventory

```ini
[web]
api01.example.com
api02.example.com

[web:vars]
ansible_user=deploy
api_port=8080
```

## Playbook

```yaml
---
- name: Configure API servers
  hosts: web
  become: yes
  tasks:
    - name: Deploy config from template
      ansible.builtin.template:
        src: app.conf.j2
        dest: /etc/api/config.json
        mode: "0644"
      notify: restart api
  handlers:
    - name: restart api
      ansible.builtin.systemd:
        name: api
        state: restarted
```

## Run

```bash
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-playbook -i inventory.ini site.yml --check
ansible-playbook -i inventory.ini site.yml
```

## Roles

```bash
ansible-galaxy init api-config-role
ansible-galaxy role install geerlingguy.nginx
```

## Testing

```bash
ansible -i inventory.ini all -m ping
ansible -i inventory.ini web -m copy -a "src=nginx.conf dest=/etc/nginx/nginx.conf backup=yes" --check
```

## Best Practices

- Always run --check and --syntax-check before real runs
- Keep secrets in ansible-vault, never plain text
- Use handlers to restart services only on change
- Make tasks idempotent and declarative
- Store inventory and playbooks in version control

## Capabilities

### ansible-playbooks
Write and run Ansible playbooks to deploy and configure API services

**Parameters:**
- `inventory` (string): Path to inventory file such as inventory.ini
- `playbook` (string): Path to the playbook yaml file
- `extra_vars` (string): Extra variables in key=value form via -e

**Commands:**
- `ansible --version`
- `ansible-playbook -i inventory.ini site.yml --check`
- `ansible-playbook -i inventory.ini site.yml --syntax-check`
- `ansible-playbook -i inventory.ini site.yml -l web`

**Examples:**
- ansible-playbook -i inventory.ini site.yml --syntax-check
- ansible-playbook -i inventory.ini site.yml --check --diff
- ansible-playbook -i inventory.ini site.yml -e "api_port=8081"

### roles-and-config
Create reusable roles and manage templated configuration files

**Parameters:**
- `role_name` (string): Name of the role to scaffold
- `template` (string): Jinja2 template path

**Commands:**
- `ansible-galaxy init api-config-role`
- `ansible-galaxy role install geerlingguy.nginx`
- `ansible-config dump | grep -i timeout`
- `ansible -i inventory.ini all -m ping`

**Examples:**
- ansible-galaxy init api-config-role
- ansible -i inventory.ini web -m copy -a "src=nginx.conf dest=/etc/nginx/nginx.conf backup=yes"
- ansible -i inventory.ini web -m template -a "src=app.conf.j2 dest=/etc/app/config.json mode=0644"

## References
- [Ansible Documentation](https://docs.ansible.com/ansible/latest/)
- [Ansible Galaxy](https://galaxy.ansible.com/)