---
name: "configuration-manager"
description: "Manages distributed configuration with Consul and etcd, plus provisioning via Ansible playbooks."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# configuration-manager

Manages distributed configuration with Consul and etcd, plus provisioning via Ansible playbooks.

## Instructions

# Configuration Manager

Centralizes runtime configuration in distributed key-value stores and automates
server provisioning with Ansible.

## When to Use

- Storing app config that must change without redeploys
- Rolling out the same config across a fleet
- Managing secrets-adjacent config via encrypted stores

## Real Commands

```bash
# Consul KV
consul kv put config/app/port 8080
consul kv get config/app/port
consul kv delete config/app/port
consul kv export -http-addr=localhost:8500 > config-backup.json

# etcd
etcdctl put /config/app/log_level info
etcdctl get /config/app --prefix
etcdctl watch /config/app --prefix

# Ansible provisioning
ansible-inventory -i inventory.yml --list
ansible all -i inventory.yml -m ping
ansible-playbook -i inventory.yml playbooks/configure.yml --syntax-check
ansible-playbook -i inventory.yml playbooks/configure.yml --check
ansible-playbook -i inventory.yml playbooks/configure.yml
```

## Playbook Example

```yaml
- hosts: web
  become: true
  vars:
    app_port: 8080
  tasks:
    - name: Write app config
      copy:
        content: "port={{ app_port }}"
        dest: /etc/app/config
```

## Best Practices

- Use `--check` before applying playbooks to fleets
- Store non-secret config in KV; secrets in Vault with KV access control
- Version config exports alongside releases
- Prefix keys by environment: `config/prod/app/...`
- Pin Ansible collections in requirements.yml

## Example Response

Returns config read/write results, a diff of what an Ansible run would change
(--check output), and the applied summary after execution.

## Capabilities

### config-store
Read and write configuration keys in Consul and etcd

**Commands:**
- `consul kv put config/app/port 8080`
- `consul kv get config/app/port`
- `consul kv delete config/app/port`
- `etcdctl put /config/app/database.url postgres://app@db:5432/app`
- `etcdctl get /config/app --prefix`

**Examples:**
- consul kv export -http-addr=consul.service.consul:8500 > config.json
- etcdctl watch /config/app --prefix
- ansible-inventory -i inventory.yml --list | jq '.all.hosts'

### provisioning
Apply configuration to servers with Ansible

**Commands:**
- `ansible-playbook -i inventory.yml playbooks/configure.yml`
- `ansible all -i inventory.yml -m ping`
- `ansible-playbook --syntax-check playbooks/configure.yml`
- `ansible-galaxy install geerlingguy.nginx`
- `ansible-playbook -i inventory.yml playbooks/configure.yml --check`

**Examples:**
- ansible-playbook -i inventory.yml playbooks/deploy.yml -l web
- ansible all -i inventory.yml -m setup -a 'filter=ansible_os_family'
- ansible-playbook playbooks/update.yml --limit 'staging'