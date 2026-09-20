---
type: agent_requested
description: "Automates server configuration with Ansible: inventory, playbooks, roles, and ad-hoc modules across fleets."
---

# ansible-infrastructure

Automates server configuration with Ansible: inventory, playbooks, roles, and ad-hoc modules across fleets.

## Instructions

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