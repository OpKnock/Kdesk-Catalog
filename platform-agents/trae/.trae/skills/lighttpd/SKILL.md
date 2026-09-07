---
name: "lighttpd"
description: "Configure and operate the lighttpd web server: config validation, foreground/daemon modes, module enablement, and simple virtual hosts. Use when working with lighttpd run, lighttpd modules, api or when the user mentions lighttpd run, lighttpd modules, api."
license: "MIT"
compatibility: "Requires lighttpd, lighttpd-enable-mod, systemctl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(lighttpd:*) Bash(lighttpd-enable-mod:*) Bash(systemctl:*)"
---

Configure and operate the lighttpd web server: config validation, foreground/daemon modes, module enablement, and simple virtual hosts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `lighttpd -f /etc/lighttpd/lighttpd.conf -t`, `lighttpd-enable-mod fastcgi`
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

# lighttpd

Configure and run the lighttpd web server.

## What this skill does

- Validates configuration files before applying.
- Runs lighttpd in daemon or foreground mode.
- Enables modules and virtual hosts.

## When to use

- Lightweight static file serving and reverse proxying.
- Embedded devices and low-memory VMs.
- Auditing or tuning existing lighttpd installs.

## Real commands

```bash
# Validate config
lighttpd -f /etc/lighttpd/lighttpd.conf -t

# Run in foreground (debug)
lighttpd -f /etc/lighttpd/lighttpd.conf -D

# Run via systemd
systemctl start lighttpd
systemctl reload lighttpd

# Version
lighttpd -v

# Enable modules (Debian/Ubuntu wrappers)
lighttpd-enable-mod fastcgi
lighttpd-enable-mod mod_compress
lighttpd-enable-mod mod_rewrite

# Test the server
curl -sI http://localhost/ | head -5
```

## Config example

```
server.document-root = "/var/www/html"
server.port = 80
server.username = "www-data"
server.groupname = "www-data"

server.modules += ("mod_compress")
compress.cache-dir = "/var/cache/lighttpd/compress/"
compress.filetype = ("text/plain", "text/html", "application/json")

server.modules += ("mod_fastcgi")
fastcgi.server = (
  "/api" => (( "host" => "127.0.0.1", "port" => 9000 ))
)
```

## Testing

```bash
lighttpd -f /etc/lighttpd/lighttpd.conf -t && echo "config OK"
```

## Best practices

- Always run -t before reload to avoid taking the site down.
- Run as a non-root user; bind low ports via capabilities or systemd.
- Check error.log for module loading failures after enabling modules.

## Capabilities

### lighttpd-run
Validate config and start lighttpd in various modes.

**Parameters:**
- `config` (string): lighttpd config file path.
- `foreground` (boolean): -D runs in foreground for debugging.

**Commands:**
- `lighttpd -f /etc/lighttpd/lighttpd.conf -t`
- `lighttpd -f /etc/lighttpd/lighttpd.conf -D`
- `systemctl start lighttpd`
- `systemctl reload lighttpd`
- `lighttpd -v`

**Examples:**
- lighttpd -f /etc/lighttpd/lighttpd.conf -t
- lighttpd -f /etc/lighttpd/lighttpd.conf -D
- systemctl reload lighttpd

### lighttpd-modules
Enable modules and configure virtual hosts.

**Parameters:**
- `module` (string): Module name to enable.

**Commands:**
- `lighttpd-enable-mod fastcgi`
- `lighttpd-enable-mod mod_rewrite`
- `lighttpd-enable-mod mod_compress`
- `curl -sI http://localhost/ | head -5`

**Examples:**
- lighttpd-enable-mod fastcgi
- lighttpd-enable-mod mod_compress
- curl -sI http://localhost/ | head -5

## References
- [lighttpd Documentation](https://redmine.lighttpd.net/projects/lighttpd/wiki)
- [lighttpd Configuration](https://redmine.lighttpd.net/projects/lighttpd/wiki/Docs_Configuration)
