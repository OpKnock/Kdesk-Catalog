---
applyTo: "**/*.r **/*.rs **/*.sh"
---

# Ldap

Query and administer OpenLDAP directories using ldapsearch, ldapadd, and ldapmodify to manage entries, apply LDIF-based changes, and perform authenticated binds.

## Instructions

# LDAP (OpenLDAP)

Query and administer LDAP directories with the OpenLDAP client tools.

## What this skill does

- Searches entries with ldapsearch (anonymous and bound).
- Adds/modifies/deletes entries via LDIF.
- Resets passwords with ldappasswd.

## When to use

- Integrating apps with corporate directory auth.
- Provisioning and auditing users/groups.
- Debugging bind and search filter issues.

## Real commands

```bash
# Authenticated search
ldapsearch -x -H ldap://localhost:389 \
  -D 'cn=admin,dc=myapp,dc=test' -w secret \
  -b 'dc=myapp,dc=test' '(uid=alice)'

# Minimal output, specific attributes
ldapsearch -x -LLL -b 'ou=people,dc=myapp,dc=test' \
  '(&(objectClass=inetOrgPerson)(mail=*@myapp.test))' cn mail

# Root DSE (capabilities)
ldapsearch -x -b 'dc=myapp,dc=test' '(objectClass=*)' -s base

# Add from LDIF
ldapadd -x -H ldap://localhost:389 \
  -D 'cn=admin,dc=myapp,dc=test' -w secret -f alice.ldif

# Modify from LDIF
ldapmodify -x -H ldap://localhost:389 \
  -D 'cn=admin,dc=myapp,dc=test' -w secret -f change.ldif

# Delete
ldapdelete -x -H ldap://localhost:389 \
  -D 'cn=admin,dc=myapp,dc=test' -w secret \
  'uid=bob,ou=people,dc=myapp,dc=test'

# Password reset
ldappasswd -x -H ldap://localhost:389 \
  -D 'cn=admin,dc=myapp,dc=test' -w secret -s newpass \
  'uid=alice,ou=people,dc=myapp,dc=test'
```

## alice.ldif example

```ldif
dn: uid=alice,ou=people,dc=myapp,dc=test
objectClass: inetOrgPerson
objectClass: posixAccount
cn: Alice Smith
sn: Smith
uid: alice
uidNumber: 1001
gidNumber: 100
homeDirectory: /home/alice
mail: alice@myapp.test
userPassword: {SSHA}encrypted-hash
```

## Testing

```bash
ldapsearch -x -b 'ou=people,dc=myapp,dc=test' '(uid=alice)' dn
```

## Best practices

- Use -LLL for scriptable output and -w for bind passwords only on trusted hosts.
- Never store plaintext userPassword in LDIF; use hashed values.
- Test filters with the smallest scope (ou=) before running on the full tree.

## Capabilities

### ldap-query
Search and read directory entries with ldapsearch.

**Commands:**
- `ldapsearch -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -b 'dc=myapp,dc=test' '(uid=alice)'`
- `ldapsearch -x -LLL -b 'ou=people,dc=myapp,dc=test' '(&(objectClass=inetOrgPerson)(mail=*@myapp.test))' cn mail`
- `ldapsearch -x -b 'dc=myapp,dc=test' '(objectClass=*)' -s base`
- `ldapsearch -x -H ldaps://localhost:636 -D 'cn=admin,dc=myapp,dc=test' -w secret -b 'dc=myapp,dc=test' '(cn=bob)'`

**Examples:**
- ldapsearch -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -b 'dc=myapp,dc=test' '(uid=alice)'
- ldapsearch -x -LLL -b 'ou=people,dc=myapp,dc=test' '(mail=*@myapp.test)' cn mail
- ldapsearch -x -b 'dc=myapp,dc=test' '(objectClass=*)' -s base

### ldap-write
Add, modify, and delete entries with LDIF files.

**Commands:**
- `ldapadd -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -f alice.ldif`
- `ldapmodify -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -f change.ldif`
- `ldapdelete -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret 'uid=bob,ou=people,dc=myapp,dc=test'`
- `ldappasswd -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -s newpass 'uid=alice,ou=people,dc=myapp,dc=test'`

**Examples:**
- ldapadd -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -f alice.ldif
- ldapmodify -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret -f change.ldif
- ldapdelete -x -H ldap://localhost:389 -D 'cn=admin,dc=myapp,dc=test' -w secret 'uid=bob,ou=people,dc=myapp,dc=test'
