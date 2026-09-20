# Railway

Deploy to Railway: login, init, link, deploy, variables, logs and project management with the railway CLI.

## Instructions

# Railway

Railway deploys apps with zero config: push code, it runs.

## What this skill does

- Logs in and links projects
- Deploys from the current directory
- Manages variables and runs commands in the environment

## When to use

- Heroku-style deploys without the lock-in
- Preview environments per PR

## Real commands

```bash
# Auth
railway login
railway init
railway link

# Deploy
railway up
railway deploy

# Variables
railway variables
railway variables --set FOO=bar
railway variables --delete FOO

# Run in project env
railway run npm run migrate
railway run python manage.py migrate

# Logs
railway logs
railway logs --deployment
```

## Best practices

- Keep secrets in variables, never in git
- Use railway up for quick deploys, railway deploy for pinned environments
- Run migrations via railway run before releases

## Capabilities

### railway-deployments
Deploy applications to Railway, manage environment variables and inspect deployments.

**Commands:**
- `railway login`
- `railway init`
- `railway up`
- `railway deploy`
- `railway variables`

**Examples:**
- railway up
- railway variables --set FOO=bar
- railway run npm run migrate
