# Configuration Management

Manage API server and service configuration with Ansible playbooks, roles, and config validation commands.

## Instructions

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

**Commands:**
- `ansible-galaxy init api-config-role`
- `ansible-galaxy role install geerlingguy.nginx`
- `ansible-config dump | grep -i timeout`
- `ansible -i inventory.ini all -m ping`

**Examples:**
- ansible-galaxy init api-config-role
- ansible -i inventory.ini web -m copy -a "src=nginx.conf dest=/etc/nginx/nginx.conf backup=yes"
- ansible -i inventory.ini web -m template -a "src=app.conf.j2 dest=/etc/app/config.json mode=0644"