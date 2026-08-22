---
name: "express"
description: "Builds Node.js HTTP APIs with Express: routing, middleware, error handling, validation, and production hardening."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
alwaysApply: false
---

# express

Builds Node.js HTTP APIs with Express: routing, middleware, error handling, validation, and production hardening.

## Instructions

# Express

Minimal web framework for Node.js.

## When to Use

- REST APIs and web apps with simple routing needs
- Microservices where a lightweight runtime is preferred
- SPA backends serving JSON and static files

## Commands

```bash
# Scaffold
npm init -y
npm install express
npx express-generator myapp

# Run
node server.js
node --watch server.js

# Common middleware
npm install helmet cors express-rate-limit morgan
npm install compression

# Testing
npm install --save-dev supertest
```

## App Example

```javascript
const express = require("express");
const app = express();

app.use(express.json());
app.use(require("helmet")());

app.get("/health", (req, res) => res.json({ ok: true }));

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: "internal" });
});

app.listen(3000);
```

## Best Practices

- Put helmet, cors, and json body parsing before routes
- Validate request input; never trust req.body blindly
- Centralize error handling in one error middleware
- Use async wrapper or try/catch for promises in handlers
- Run npm audit in CI and pin production dependencies
- Serve behind a reverse proxy with trust proxy enabled when needed

## Capabilities

### express-app
Scaffold and run Express applications.

**Commands:**
- `npm init -y`
- `npm install express`
- `npx express-generator myapp`
- `node server.js`
- `npm start`

**Examples:**
- npx express-generator --view=ejs myapp
- node --watch server.js
- npm run dev

### express-middleware
Add routing, validation, and error middleware.

**Commands:**
- `npm install helmet cors express-rate-limit`
- `npm install morgan`
- `npm install --save-dev supertest`
- `npm audit fix`

**Examples:**
- npm install express-validator joi
- npm install compression
- npm audit --audit-level=high