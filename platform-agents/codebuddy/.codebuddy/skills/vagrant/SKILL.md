---
name: "vagrant"
description: "Manages reproducible virtual machines with Vagrant: boxes, providers, provisioning, snapshots, and multi-machine environments. Use when working with vm lifecycle, provisioning and snapshots, devops or when the user mentions vm lifecycle, provisioning and snapshots, devops."
license: "MIT"
compatibility: "Requires vagrant."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(vagrant:*)"
---

Manages reproducible virtual machines with Vagrant: boxes, providers, provisioning, snapshots, and multi-machine environments.

## Agentic Workflow: Read -> Reason -> Act (vagrant)

You are **vagrant** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `vagrant`
- Domain: Manages reproducible virtual machines with Vagrant: boxes, providers, provisioning, snapshots, and multi-machine environments.
- **vm-lifecycle**: Initialize, boot, and manage VMs from a Vagrantfile. — `vagrant init hashicorp/bionic64`
- **provisioning-and-snapshots**: Provision VMs, reload configs, and snapshot state. — `vagrant provision`
- Check `knowledge` and `prerequisites: vagrant`

### 2. Reason — think for `vagrant`
- For `vm-lifecycle`: Initialize, boot, and manage VMs from a Vagrantfile. — decide which checks to run
- For `provisioning-and-snapshots`: Provision VMs, reload configs, and snapshot state. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vagrant` tools
- Tools: `Glob`, `Grep`, `Read`, `Vagrant` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vagrant:e2964406`

# Vagrant Virtual Machines

Create reproducible dev VMs with a Vagrantfile: boxes, providers, provisioning, snapshots.

## What This Skill Does

- Boots VMs from public/private boxes (VirtualBox, VMware, Hyper-V)
- Provisions with shell, Ansible, or Docker provisioners
- Manages snapshots for repeatable test states
- Supports multi-machine environments (app + db VMs)
- Tears down cleanly with destroy

## When to Use

- Reproducible local dev environments
- Testing provisioning scripts safely
- Legacy app environments needing exact OS versions

## Real Commands

```bash
# Lifecycle
vagrant init hashicorp/bionic64
vagrant up
vagrant ssh
vagrant status
vagrant halt
vagrant destroy -f

# Provisioning
vagrant provision
vagrant reload --provision
vagrant up --provision

# Snapshots and boxes
vagrant snapshot save baseline
vagrant snapshot list
vagrant snapshot restore baseline
vagrant box list
vagrant box update
```

## Vagrantfile Sketch

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y docker.io
  SHELL
end
```

## Best Practices

- Pin box versions to avoid drift: `config.vm.box_version`
- Use snapshot save/restore for pre/post test states
- Prefer shell/Ansible provisioners over manual SSH config
- Keep Vagrantfiles in git for environment parity
- Use `vagrant destroy -f` in CI cleanup

## Capabilities

### vm-lifecycle
Initialize, boot, and manage VMs from a Vagrantfile.

**Parameters:**
- `box` (string): Box name, e.g. hashicorp/bionic64
- `machine` (string): Machine name in multi-machine Vagrantfiles

**Commands:**
- `vagrant init hashicorp/bionic64`
- `vagrant up`
- `vagrant ssh`
- `vagrant status`
- `vagrant halt`
- `vagrant destroy -f`

**Examples:**
- vagrant init hashicorp/bionic64
- vagrant up
- vagrant ssh

### provisioning-and-snapshots
Provision VMs, reload configs, and snapshot state.

**Parameters:**
- `snapshot` (string): Snapshot name
- `box` (string): Box to query

**Commands:**
- `vagrant provision`
- `vagrant reload --provision`
- `vagrant snapshot save baseline`
- `vagrant snapshot list`
- `vagrant snapshot restore baseline`
- `vagrant box list`

**Examples:**
- vagrant provision
- vagrant snapshot save baseline
- vagrant snapshot restore baseline

## References
- [Vagrant Documentation](https://developer.hashicorp.com/vagrant/docs)
- [Vagrant Provisioning](https://developer.hashicorp.com/vagrant/docs/provisioning)
- [HashiCorp Vagrant Catalog](https://app.vagrantup.com/boxes/search)
