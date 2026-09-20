# Kerberos

Authenticate and administer Kerberos: kinit/klist sessions, keytab management with kadmin, and troubleshooting ticket errors.

## Instructions

# Kerberos

Authenticate and administer MIT Kerberos realms.

## What this skill does

- Obtains and manages TGT/ticket sessions with kinit/klist/kdestroy.
- Creates principals and keytabs with kadmin.
- Troubleshoots ticket expiry and preauth errors.

## When to use

- SSO authentication for Hadoop, NFS, or LDAP.
- Service principals for hosts and daemons.
- Debugging kinit failures (KDC unreachable, clock skew, preauth).

## Real commands

```bash
# Obtain a ticket (prompts for password)
kinit alice@STAGING.MYAPP.TEST

# Ticket with explicit lifetime
kinit -l 10h alice@STAGING.MYAPP.TEST

# List active tickets
klist
klist -f    # with flags (A=preauth, F=forwardable)

# Keytab tickets
klist -kt /etc/krb5.keytab

# Destroy the ticket cache
kdestroy

# Admin: create a user principal
kadmin -p admin/admin@STAGING.MYAPP.TEST \
  -q "addprinc -pw s3cret bob@STAGING.MYAPP.TEST"

# Admin: add service principal to a keytab
kadmin -p admin/admin@STAGING.MYAPP.TEST \
  -q "ktadd -k /etc/krb5.keytab host/web-01.staging.myapp.test@STAGING.MYAPP.TEST"

# List principals
kadmin -p admin/admin@STAGING.MYAPP.TEST -q "listprincs"
```

## krb5.conf example

```ini
[libdefaults]
  default_realm = STAGING.MYAPP.TEST
  dns_lookup_realm = false
  dns_lookup_kdc = false
  ticket_lifetime = 24h
[realms]
  STAGING.MYAPP.TEST = {
    kdc = kdc1.staging.myapp.test
    admin_server = kdc1.staging.myapp.test
  }
[domain_realm]
  .staging.myapp.test = STAGING.MYAPP.TEST
```

## Testing

```bash
# Verify the service ticket works
kvno host/web-01.staging.myapp.test@STAGING.MYAPP.TEST
```

## Best practices

- Never embed passwords in scripts; use keytabs with restricted principals.
- Keep the clock in sync; skew > 5 minutes breaks preauth.
- Use -l and -r lifetimes matching service requirements; renew with kinit -R.

## Capabilities

### session-mgmt
Obtain, list, and destroy Kerberos tickets.

**Commands:**
- `kinit alice@STAGING.MYAPP.TEST`
- `kinit -l 10h alice@STAGING.MYAPP.TEST`
- `klist`
- `klist -f`
- `kdestroy`

**Examples:**
- kinit alice@STAGING.MYAPP.TEST
- klist -f
- kdestroy

### admin-ops
Create principals and manage keytabs with kadmin.

**Commands:**
- `kadmin -p admin/admin@STAGING.MYAPP.TEST -q "addprinc -pw s3cret bob@STAGING.MYAPP.TEST"`
- `kadmin -p admin/admin@STAGING.MYAPP.TEST -q "ktadd -k /etc/krb5.keytab host/web-01.staging.myapp.test@STAGING.MYAPP.TEST"`
- `kadmin -p admin/admin@STAGING.MYAPP.TEST -q "listprincs"`
- `kadmin -p admin/admin@STAGING.MYAPP.TEST -q "delprinc bob@STAGING.MYAPP.TEST"`
- `klist -kt /etc/krb5.keytab`

**Examples:**
- kadmin -p admin/admin@STAGING.MYAPP.TEST -q "addprinc -pw s3cret bob@STAGING.MYAPP.TEST"
- kadmin -p admin/admin@STAGING.MYAPP.TEST -q "ktadd -k /etc/krb5.keytab host/web-01.staging.myapp.test@STAGING.MYAPP.TEST"
- klist -kt /etc/krb5.keytab