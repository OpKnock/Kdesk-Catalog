---
name: "api-input-validation-engineer"
description: "Secures API endpoints with schema validation (Joi/Zod/Pydantic), sanitization, and injection prevention."
globs: ["**/*.html", "**/*.json", "**/*.py", "**/*.r", "**/*.rs", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# api-input-validation-engineer

Secures API endpoints with schema validation (Joi/Zod/Pydantic), sanitization, and injection prevention.

## Instructions

# API Input Validation Engineer

Validates and sanitizes all API input to prevent injection, type confusion, and XSS.

## When to Use
- Securing public endpoints
- Preventing SQL/command injection
- Enforcing data integrity

## Real Commands

```bash
# Zod
npm install zod
node -e "const {z}=require('zod');const r=z.object({email:z.string().email()}).safeParse({email:'nope'});console.log(r.error.issues)"

# Joi
npm install joi
node -e "const J=require('joi');const r=J.object({id:J.number().integer().min(1)}).validate({id:0});console.log(r.error.message)"

# Pydantic
pip install pydantic

# Scanners
zap-baseline.py -t http://localhost:3000/api -r zap-report.html
sqlmap -u 'http://localhost:3000/api/users?id=1' --batch
```

## Validation Layers
- Schema: types, formats, ranges
- Sanitize: strip control chars and scripts
- Query: parameterized statements only

## Testing
Probe with `' OR 1=1`, `<script>`, oversized payloads, and wrong types.

## Best Practices
- Validate at the boundary, never trust clients
- Fail fast with 422 + details
- Never put user input in raw SQL

## Capabilities

### schema-validation
Validate request bodies, query params, and headers with typed schemas

**Commands:**
- `npm install zod`
- `node -e "const {z}=require('zod');const s=z.object({email:z.string().email(),age:z.number().min(0).max(120)});console.log(s.safeParse({email:'a@b.com',age:30}))"`
- `npm install joi`
- `node -e "const J=require('joi');const r=J.object({email:J.string().email()}).validate({email:'bad'});console.log(r.error)"`
- `pip install pydantic && python -c "from pydantic import BaseModel, EmailStr; m=type('U',(BaseModel,),{'__annotations__':{'email':EmailStr}}); print(m(email='a@b.com'))"`

**Examples:**
- node -e "const {z}=require('zod');const r=z.object({email:z.string().email()}).safeParse({email:'nope'});console.log(r.success?'ok':r.error.issues)"
- node -e "const J=require('joi');const r=J.object({id:J.number().integer().min(1)}).validate({id:0});console.log(r.error.message)"
- pip install pydantic && python -c "from pydantic import BaseModel, EmailStr; c=type('U',(BaseModel,),{'__annotations__':{'email':EmailStr}}); print(c(email='x@y.z'))"

### injection-testing
Verify injection resistance with automated scanners and manual probes

**Commands:**
- `zap-baseline.py -t http://localhost:3000/api -r zap-report.html`
- `zap-full-scan.py -t http://localhost:3000/api -J zap.json`
- `curl -s 'http://localhost:3000/api/users?id=1%20OR%201%3D1' -o /dev/null -w '%{http_code}'`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"demo-scriptalert(1)demo-script"}' -w '\n%{http_code}'`
- `python -m pip install sqlmap && sqlmap -u 'http://localhost:3000/api/users?id=1' --batch --crawl 2`

**Examples:**
- zap-baseline.py -t http://localhost:3000/api -r zap-report.html && start zap-report.html
- curl -s 'http://localhost:3000/api/users?id=1%20OR%201%3D1' -o /dev/null -w '%{http_code}\n'
- sqlmap -u 'http://localhost:3000/api/users?id=1' --batch