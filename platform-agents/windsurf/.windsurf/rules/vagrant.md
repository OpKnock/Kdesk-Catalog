---
trigger: glob
description: "Manages reproducible virtual machines with Vagrant: boxes, providers, provisioning, snapshots, and multi-machine environments."
globs: ["**/*.r", "**/*.rb", "**/*.sh"]
---

# vagrant

Manages reproducible virtual machines with Vagrant: boxes, providers, provisioning, snapshots, and multi-machine environments.

## Instructions

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
