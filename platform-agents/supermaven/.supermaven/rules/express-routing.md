# Express Routing

Build REST APIs with Express: scaffold projects, run the dev server, add middleware, and test routes with supertest.

## Instructions

# Express v2

## What this skill does

Express is the classic Node.js web framework. This skill covers modern Express practice: generators, middleware chains (morgan, cors, helmet), JSON APIs, and route testing with supertest.

## When to use

- Scaffolding a new REST service quickly
- Adding logging, CORS, and security headers to an existing app
- Writing integration tests for routes

## Real commands

```bash
# Scaffold
npx express-generator --view=ejs myapp
cd myapp && npm install

# Run (with dev reload)
npm start
npx nodemon src/app.js

# Common middleware
gnpm install express morgan cors helmet

# Test
npm test
```

## Route + middleware example

```javascript
const express = require('express')
const app = express()

app.use(express.json())
app.use(require('morgan')('combined'))
app.use(require('helmet')())

app.get('/api/orders/:id', (req, res, next) => {
  try {
    const order = db.find(req.params.id)
    if (!order) {
      const err = new Error('Not found')
      err.status = 404
      throw err
    }
    res.json(order)
  } catch (e) {
    next(e)
  }
})

app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message })
})

app.listen(3000)
```

## Testing with supertest

```javascript
const request = require('supertest')
const app = require('../src/app')

test('returns 404 for missing order', async () => {
  const res = await request(app).get('/api/orders/999')
  expect(res.status).toBe(404)
})
```

## Best practices

- Put `app` in its own module so supertest can import it without listening.
- Order middleware correctly: security headers -> logging -> json -> routes.
- Use the four-arg error handler; never send stacks to clients.
- Prefer `express.json()` over body-parser directly.
- Pin `engines` in package.json to the Node version in prod.

## Capabilities

### express-routing
Scaffold, run, extend, and test Express applications.

**Commands:**
- `npx express-generator --view=ejs myapp`
- `npm install express morgan cors helmet`
- `npm start`
- `npm run dev`
- `npx nodemon src/app.js`
- `npm test`

**Examples:**
- npx express-generator --view=ejs myapp && cd myapp && npm install && npm start
- npm install express morgan cors helmet && npm run dev
- curl -s localhost:3000/api/orders | jq