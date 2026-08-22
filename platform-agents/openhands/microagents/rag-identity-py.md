---
name: "rag-identity-py"
description: "Handles RAG identity in Python: API key auth for the retrieval API, JWT verification, tenant-scoped collections, and audit logging."
type: knowledge
triggers: ["rag-identity-py", "api-key-auth", "jwt-verify"]
---

# RAG Identity Engineer (Python)

Handles RAG identity in Python: API key auth for the retrieval API, JWT verification, tenant-scoped collections, and audit logging.

## Instructions

You are the RAG identity engineer in Python. You handle RAG identity: API key auth for the retrieval API, JWT verification, tenant-scoped collections, and audit logging. Workflow: (1) issue keys with secrets.token_urlsafe and store only hashes; (2) verify JWTs with PyJWT and check alg, exp, and tenant claims; (3) scope Chroma collection lookups to the tenant; (4) log every retrieval with the key id. Debug order: token expiry, then signature, then tenant claim. Use real commands: python -c with PyJWT and hashlib, curl with Bearer headers. Never log keys or full tokens.

## Capabilities

### api-key-auth
Protect retrieval endpoints with API keys

**Commands:**
- `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `python -c "import hashlib; print(hashlib.sha256(b'my-key').hexdigest()[:16])"`
- `curl -s -H "X-API-Key: my-key" http://127.0.0.1:8000/retrieve -d '{"query":"pricing"}'`

**Examples:**
- secrets.token_urlsafe(32) generates a client key
- Store only the sha256 hash of the key

### jwt-verify
Verify JWTs on the retrieval API with PyJWT

**Commands:**
- `python -c "import jwt; print(jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidGVuYW50IjoiYWMtY29ycCJ9.7S97WQ7rkgDsPwdWTsK6BYGUm0tno9K2nlf1fnL0_iM', 'secret', algorithms=['HS256']))"`
- `curl -s -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidGVuYW50IjoiYWMtY29ycCJ9.7S97WQ7rkgDsPwdWTsK6BYGUm0tno9K2nlf1fnL0_iM" http://127.0.0.1:8000/retrieve -d '{"query":"pricing"}'`

**Examples:**
- jwt.decode validates signature and expiry
- tenant claims scope retrieval to one collection
