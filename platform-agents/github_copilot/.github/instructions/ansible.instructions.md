---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# ansible

Automates infrastructure with Ansible: ad-hoc commands, playbooks, roles, and vault secrets.

## Instructions

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
