---
applyTo: "**/*.r **/*.sh"
---

Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `apachectl -t`, `htpasswd -c /etc/httpd/conf/.htpasswd alice`
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

# Apache HTTP Server

## What this skill does

Administers Apache httpd: validating configs before reload, inspecting virtual hosts and modules, configuring reverse proxies and SSL, and protecting paths with htpasswd basic auth.

## When to use

- A config change must be validated before a reload
- Setting up a virtual host for a new site
- Password-protecting an internal path

## Real commands

```bash
# Validate config
apachectl -t

# Dump vhost summary
apachectl -S

# Check loaded modules
httpd -t -D DUMP_MODULES | grep -E "ssl|proxy"

# Graceful reload
apachectl graceful

# htpasswd management
htpasswd -c /etc/httpd/conf/.htpasswd alice
htpasswd -b /etc/httpd/conf/.htpasswd bob bobpass
apachectl -t && apachectl graceful
```

## Vhost example

```apache
<VirtualHost *:443>
  ServerName api.your-app.test
  SSLEngine on
  SSLCertificateFile /etc/pki/tls/certs/api.crt
  SSLCertificateKeyFile /etc/pki/tls/private/api.key
  ProxyPass /api/ http://backend:8080/api/
  ErrorLog logs/api-error.log
  CustomLog logs/api-access.log combined
</VirtualHost>
```

## Basic auth block

```apache
<Location /admin>
  AuthType Basic
  AuthName "Admin"
  AuthUserFile /etc/httpd/conf/.htpasswd
  Require valid-user
</Location>
```

## Testing

- Always run `apachectl -t` before `graceful`
- Test auth with curl -u and confirm 401 without credentials

## Best practices

- Prefer graceful over restart to avoid dropping connections
- Use bcrypt (htpasswd -B) for password files
- Check apachectl -S after adding vhosts for name collisions

## Capabilities

### config-management
Validate, dump, and hot-reload the Apache configuration.

**Parameters:**
- `config_file` (string): Alternate config file via -f
- `module` (string): Module name to check via DUMP_MODULES

**Commands:**
- `apachectl -t`
- `apachectl -S`
- `httpd -V`
- `apachectl graceful`
- `apachectl configtest`

**Examples:**
- apachectl -t && apachectl graceful
- apachectl -S | grep -E "port|vhost"
- httpd -t -D DUMP_MODULES | grep ssl

### vhost-and-auth
Configure virtual hosts and protect directories with htpasswd.

**Parameters:**
- `file` (string): htpasswd file path
- `user` (string): Username to add/remove
- `bcrypt` (boolean): -B enables bcrypt hashing

**Commands:**
- `htpasswd -c /etc/httpd/conf/.htpasswd alice`
- `htpasswd -b /etc/httpd/conf/.htpasswd bob bobpass`
- `htpasswd -D /etc/httpd/conf/.htpasswd bob`
- `htpasswd -nB alice`
- `curl -u alice:pass -I http://localhost/private/`

**Examples:**
- htpasswd -c .htpasswd admin && apachectl -t && apachectl graceful
- curl -I -u alice:secret http://localhost/private/
- htpasswd -bB /etc/httpd/conf/.htpasswd deploy deploypass

## References
- [Apache httpd Docs](https://httpd.apache.org/docs/2.4/)
- [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)
- [Apache Invocation](https://httpd.apache.org/docs/2.4/invoking.html)
