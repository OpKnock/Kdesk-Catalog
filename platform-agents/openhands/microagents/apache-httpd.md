---
name: "apache-httpd"
description: "Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads."
type: knowledge
triggers: ["apache-httpd", "config-management", "vhost-and-auth"]
---

# Apache Httpd

Administers Apache HTTP Server: config validation, virtual hosts, module inspection, htpasswd basic auth, and graceful reloads.

## Instructions

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
