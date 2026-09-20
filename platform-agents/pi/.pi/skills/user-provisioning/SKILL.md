---
name: "user-provisioning"
description: "Manages user and group lifecycle via SCIM 2.0 APIs. Creates, reads, updates, and deactivates users, manages group memberships, filters with SCIM syntax, and integrates with identity providers like Okta and Azure AD."
---

# User Provisioning

Manages user and group lifecycle via SCIM 2.0 APIs. Creates, reads, updates, and deactivates users, manages group memberships, filters with SCIM syntax, and integrates with identity providers like Okta and Azure AD.

## Instructions

# User Provisioning

Hand-crafted skill for SCIM 2.0 user provisioning.

## What this skill does

- Creates, reads, updates, and deletes users via SCIM
- Manages group membership for access control
- Supports the deactivation lifecycle (active flag)
- Lists and filters users with SCIM filter syntax

## When to use

- Wiring IdP-to-app provisioning (Okta, Azure AD)
- Building an internal directory sync client
- Auditing what a SCIM provider stores

## Real commands

```bash
# Create a user
curl -s -X POST "http://localhost:8080/scim/v2/Users" -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d "{\"schemas\":[\"urn:ietf:params:scim:schemas:core:2.0:User\"],\"userName\":\"jdoe@company.test\",\"active\":true,\"name\":{\"givenName\":\"Jane\",\"familyName\":\"Doe\"}}" | jq

# Deactivate (never delete)
curl -s -X PATCH "http://localhost:8080/scim/v2/Users/123" -H "Content-Type: application/json" -d "{\"schemas\":[\"urn:ietf:params:scim:api:messages:2.0:PatchOp\"],\"Operations\":[{\"op\":\"replace\",\"path\":\"active\",\"value\":false}]}" | jq

# Filter users
curl -s "http://localhost:8080/scim/v2/Users?filter=userName+eq+%22jdoe%40company.test%22&startIndex=1&count=10" -H "Authorization: Bearer TOKEN" | jq

# Group with members
curl -s -X POST "http://localhost:8080/scim/v2/Groups" -H "Content-Type: application/json" -d "{\"schemas\":[\"urn:ietf:params:scim:schemas:core:2.0:Group\"],\"displayName\":\"eng\",\"members\":[{\"value\":\"123\"}]}" | jq

# Delete (terminal)
curl -s -X DELETE "http://localhost:8080/scim/v2/Users/123" -H "Authorization: Bearer TOKEN" -o /dev/null -w "%{http_code}"
```

## Lifecycle

- create -> active=true
- suspend/deprovision -> active=false
- delete only for forgotten-account cleanup

## Testing

```bash
curl -s "http://localhost:8080/scim/v2/Users?filter=userName+eq+%22jdoe%40company.test%22" -H "Authorization: Bearer TOKEN" | jq ".totalResults"
curl -s "http://localhost:8080/scim/v2/ServiceProviderConfig" -H "Authorization: Bearer TOKEN" | jq
```

## Best practices

- Deactivate instead of delete for compliance history
- URL-encode filters; use startIndex/count for pagination
- Test against ServiceProviderConfig before CRUD

## Capabilities

### scim-lifecycle
Manage user and group lifecycle over SCIM 2.0

**Commands:**
- `curl -s -X POST "http://localhost:8080/scim/v2/Users" -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d "{\"schemas\":[\"urn:ietf:params:scim:schemas:core:2.0:User\"],\"userName\":\"jdoe@company.test\",\"active\":true,\"name\":{\"givenName\":\"Jane\",\"familyName\":\"Doe\"}}" | jq`
- `curl -s -X PATCH "http://localhost:8080/scim/v2/Users/123" -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d "{\"schemas\":[\"urn:ietf:params:scim:api:messages:2.0:PatchOp\"],\"Operations\":[{\"op\":\"replace\",\"path\":\"active\",\"value\":false}]}" | jq`
- `curl -s "http://localhost:8080/scim/v2/Users?filter=userName+eq+%22jdoe%40company.test%22&startIndex=1&count=10" -H "Authorization: Bearer TOKEN" | jq`
- `curl -s -X POST "http://localhost:8080/scim/v2/Groups" -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d "{\"schemas\":[\"urn:ietf:params:scim:schemas:core:2.0:Group\"],\"displayName\":\"eng\",\"members\":[{\"value\":\"123\"}]}" | jq`
- `curl -s -X DELETE "http://localhost:8080/scim/v2/Users/123" -H "Authorization: Bearer TOKEN" -o /dev/null -w "%{http_code}"`

**Examples:**
- curl -s "http://localhost:8080/scim/v2/Users?filter=userName+eq+%22jdoe%40company.test%22" -H "Authorization: Bearer TOKEN" | jq
- curl -s -X PATCH "http://localhost:8080/scim/v2/Users/123" -H "Content-Type: application/json" -d "{\"Operations\":[{\"op\":\"replace\",\"value\":{\"active\":true}}]}" | jq
- curl -s -X POST "http://localhost:8080/scim/v2/Groups" -H "Content-Type: application/json" -d "{\"displayName\":\"eng\"}" | jq
