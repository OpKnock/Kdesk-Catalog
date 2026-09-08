---
name: "api-error-express-middleware"
description: "Implements error handling middleware for Express and FastAPI: centralized handlers, logging, and consistent responses. Use when working with express middleware, fastapi handlers or when the user mentions express middleware, fastapi handlers."
license: "MIT"
compatibility: "Requires node.js, python, openapi, postman. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(npm:*) Bash(pip:*) Bash(python:*)"
---

Implements error handling middleware for Express and FastAPI: centralized handlers, logging, and consistent responses.

## Agentic Workflow: Read -> Reason -> Act (api-error-express-middleware)

You are **Api Error Express Middleware** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-error-express-middleware`
- Domain: Implements error handling middleware for Express and FastAPI: centralized handlers, logging, and consistent responses.
- **express-middleware**: Add centralized error middleware to Express APIs — `npm install http-errors`
- **fastapi-handlers**: Register exception handlers in FastAPI with consistent bodies — `pip install fastapi`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-error-express-middleware`
- For `express-middleware`: Add centralized error middleware to Express APIs — decide which checks to run
- For `fastapi-handlers`: Register exception handlers in FastAPI with consistent bodies — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-error-express-middleware` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-error-express-middleware:41e8fb8e`

# API Error (Implementation)

Implements centralized error handling in Node and Python APIs.

## When to Use
- Errors returned ad hoc from handlers
- Stack traces leaking in responses
- Adding structured error logging

## Real Commands

```bash
# Express
npm install http-errors express-async-errors
node -e "const h=require('http-errors');const e=h(422,'bad input');console.log(e.status)"

# FastAPI
python -c "from fastapi import HTTPException;print(HTTPException(status_code=422,detail={'code':'VALIDATION_1001'}))"

# Probe
curl -s http://localhost:3000/api/boom -w '\n%{http_code}'
```

## Middleware Shape

```js
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({
    code: err.code || 'INTERNAL',
    title: err.message,
    status: err.status || 500,
    instance: req.originalUrl
  });
});
```

## Testing
Assert every route returns the same error body shape.

## Best Practices
- Log the stack, never expose it
- Map unknown errors to 500 with INTERNAL code

## Capabilities

### express-middleware
Add centralized error middleware to Express APIs

**Parameters:**
- `status` (string): HTTP status
- `code` (string): Error code

**Commands:**
- `npm install http-errors`
- `node -e "const h=require('http-errors');const e=h(404,'missing');console.log(e.status,e.message)"`
- `npm install express-async-errors`
- `node -e "require('express-async-errors');console.log('async handlers patched')"`
- `curl -s http://localhost:3000/api/boom -w '\n%{http_code}'`

**Examples:**
- node -e "const h=require('http-errors');const e=h(422,'bad input',{code:'VALIDATION_1001'});console.log(e.status,e.expose)"
- curl -s http://localhost:3000/api/boom -w '\n%{http_code}'
- npm install http-errors express-async-errors

### fastapi-handlers
Register exception handlers in FastAPI with consistent bodies

**Parameters:**
- `status` (string): HTTP status code
- `detail` (string): Error detail

**Commands:**
- `pip install fastapi`
- `python -c "from fastapi import FastAPI,HTTPException;print(HTTPException(status_code=404,detail='missing'))"`
- `python -c "import uvicorn;print('uvicorn ok')"`
- `curl -s http://localhost:8000/api/missing -w '\n%{http_code}'`
- `python -c "from fastapi.responses import JSONResponse;r=JSONResponse({'detail':'x'},status_code=400);print(r.status_code)"`

**Examples:**
- python -c "from fastapi import HTTPException;print(HTTPException(status_code=422,detail={'code':'VALIDATION_1001'}))"
- curl -s http://localhost:8000/api/missing -w '\n%{http_code}'
- python -c "from fastapi.responses import JSONResponse;print(JSONResponse({'detail':'x'},400).status_code)"

## References
- [Express Error Handling](https://expressjs.com/en/guide/error-handling.html)
- [FastAPI Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
