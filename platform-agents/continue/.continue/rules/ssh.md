---
name: "ssh"
description: "Connects to remote hosts with ssh: config files, port forwarding, tunnels, keys, jump hosts, and verbose troubleshooting."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# ssh

Connects to remote hosts with ssh: config files, port forwarding, tunnels, keys, jump hosts, and verbose troubleshooting.

## Instructions

# SSH Connections

Connect and tunnel to remote hosts securely.

## What This Skill Does

- Connects with keys, ports, and command execution
- Configures per-host options in ~/.ssh/config
- Forwards local/remote ports and SOCKS proxies
- Uses jump hosts and agent forwarding
- Troubleshoots with verbose output

## When to Use

- Any remote shell access
- Exposing local services through tunnels
- Multi-hop bastion environments

## Real Commands

```bash
# Basic connections
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -t user@host 'sudo systemctl status nginx'
ssh -J jumpuser@bastion user@target

# Tunnels
ssh -L 8080:localhost:80 user@host          # local forward
ssh -L 3306:db.internal:3306 user@bastion   # through bastion
ssh -R 3000:localhost:3000 user@host        # remote forward
ssh -D 1080 -N user@host                    # SOCKS proxy
ssh -o ExitOnForwardFailure=yes -L 8080:localhost:80 user@host

# Debug
ssh -vvv user@host
```

## ~/.ssh/config

```
Host prod
  HostName 10.0.0.5
  User deploy
  IdentityFile ~/.ssh/id_ed25519
  ServerAliveInterval 30
```

## Best Practices

- Use config aliases over long flag lists
- Prefer -J for bastions; forward agent only when needed
- Add ExitOnForwardFailure to fail fast on tunnels
- Use -N for tunnels with no shell
- Verify fingerprints (ssh-keygen -F) before first connect

## Capabilities

### connections
Connect with keys, ports, and options.

**Commands:**
- `ssh user@host`
- `ssh -p 2222 user@host`
- `ssh -i ~/.ssh/id_ed25519 user@host`
- `ssh -t user@host 'sudo systemctl status nginx'`
- `ssh -J jumpuser@bastion user@target`
- `ssh -N -L 5432:localhost:5432 user@dbhost`

**Examples:**
- ssh -i ~/.ssh/id_ed25519 user@host
- ssh -t user@host 'sudo systemctl status nginx'
- ssh -J jumpuser@bastion user@target

### tunnels-and-forwarding
Forward ports, set up SOCKS proxies, and tunnel traffic.

**Commands:**
- `ssh -L 8080:localhost:80 user@host`
- `ssh -R 3000:localhost:3000 user@host`
- `ssh -D 1080 -N user@host`
- `ssh -L 3306:db.internal:3306 user@bastion`
- `ssh -o ExitOnForwardFailure=yes -L 8080:localhost:80 user@host`
- `ssh -vvv user@host`

**Examples:**
- ssh -L 3306:db.internal:3306 user@bastion
- ssh -D 1080 -N user@host
- ssh -vvv user@host