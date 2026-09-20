---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Manages distributed configuration with Consul and etcd, plus provisioning via Ansible playbooks.

## Agentic Workflow: Read -> Reason -> Act (configuration-manager)

You are **configuration-manager** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `configuration-manager`
- Domain: Manages distributed configuration with Consul and etcd, plus provisioning via Ansible playbooks.
- **config-store**: Read and write configuration keys in Consul and etcd — `consul kv put config/app/port 8080`
- **provisioning**: Apply configuration to servers with Ansible — `ansible-playbook -i inventory.yml playbooks/configure.yml`
- Check `knowledge` and `prerequisites: node.js, python, vault, dotenv`

### 2. Reason — think for `configuration-manager`
- For `config-store`: Read and write configuration keys in Consul and etcd — decide which checks to run
- For `provisioning`: Apply configuration to servers with Ansible — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `configuration-manager` tools
- Tools: `Glob`, `Grep`, `Read`, `Consul`, `Etcdctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `configuration-manager:5871e47b`

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

**Parameters:**
- `http-addr` (string): Consul server address
- `prefix` (string): Key prefix for bulk get/watch operations
- `endpoints` (string): etcd endpoints (comma-separated) via --endpoints

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

**Parameters:**
- `check` (boolean): Dry run: report changes without applying
- `limit` (string): Host pattern to restrict execution to
- `syntax-check` (boolean): Validate playbook syntax only

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

## References
- [Consul docs](https://developer.hashicorp.com/consul/docs)
- [etcd docs](https://etcd.io/docs/)
- [Ansible documentation](https://docs.ansible.com/)
