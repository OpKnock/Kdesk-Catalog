---
name: "apache-httpd"
description: "Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads. Use when working with config management, vhost and auth, api or when the user mentions config management, vhost and auth, api."
license: "MIT"
compatibility: "Requires apachectl, htpasswd, httpd. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(apachectl:*) Bash(curl:*) Bash(htpasswd:*) Bash(httpd:*)"
---

Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads.

## Agentic Workflow: Read -> Reason -> Act (apache-httpd)

You are **Apache Httpd** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `apache-httpd`
- Domain: Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads.
- **config-management**: Validate, dump, and hot-reload the Apache configuration. — `apachectl -t`
- **vhost-and-auth**: Configure virtual hosts and protect directories with htpasswd. — `htpasswd -c /etc/httpd/conf/.htpasswd alice`
- Check `knowledge` and `prerequisites: apachectl, htpasswd, httpd`

### 2. Reason — think for `apache-httpd`
- For `config-management`: Validate, dump, and hot-reload the Apache configuration. — decide which checks to run
- For `vhost-and-auth`: Configure virtual hosts and protect directories with htpasswd. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `apache-httpd` tools
- Tools: `Glob`, `Grep`, `Read`, `Apachectl`, `Httpd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `apache-httpd:462b2819`

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
