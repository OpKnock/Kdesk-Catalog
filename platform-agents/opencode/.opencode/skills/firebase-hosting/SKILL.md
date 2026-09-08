---
name: "firebase-hosting"
description: "Firebase Hosting: deploy sites, configure rewrites and headers, preview builds locally, and manage multiple sites per project. Use when working with hosting deploy, api or when the user mentions hosting deploy, api."
---

Firebase Hosting: deploy sites, configure rewrites and headers, preview builds locally, and manage multiple sites per project.

## Agentic Workflow: Read -> Reason -> Act (firebase-hosting)

You are **Firebase Hosting** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `firebase-hosting`
- Domain: Firebase Hosting: deploy sites, configure rewrites and headers, preview builds locally, and manage multiple sites per project.
- **hosting-deploy**: Deploy, preview, and configure Firebase Hosting sites. — `firebase init hosting`
- Check `knowledge` and `prerequisites: firebase`

### 2. Reason — think for `firebase-hosting`
- For `hosting-deploy`: Deploy, preview, and configure Firebase Hosting sites. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `firebase-hosting` tools
- Tools: `Glob`, `Grep`, `Read`, `Firebase` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `firebase-hosting:19096767`

# Firebase Hosting

## What this skill does

Firebase Hosting serves static sites and SPAs on a global CDN with one-command deploys, preview channels for every PR, and configurable rewrites and headers.

## When to use

- Shipping a static site or SPA
- Giving stakeholders a preview URL per PR
- Adding redirects, rewrites, or security headers

## Real commands

```bash
# Scaffold
firebase init hosting

# Deploy to the live channel
firebase hosting:deploy --only hosting

# Preview channels
firebase hosting:channel:deploy staging
firebase hosting:channel:deploy preview-123 --expires 7d
firebase hosting:channel:list

# Local preview
firebase serve --only hosting
```

## firebase.json hosting example

```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*"],
    "rewrites": [
      {"source": "**", "destination": "/index.html"},
      {"source": "/api/**", "function": "api"}
    ],
    "headers": [
      {"source": "/assets/**", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}
    ]
  }
}
```

## Testing

```bash
# Deploy a channel and curl it
firebase hosting:channel:deploy preview-123 --expires 7d
curl -sI https://preview-123-project.web.app | grep -i 'x-cache'
```

## Best practices

- Always preview on a channel before deploying to the live site.
- Cache hashed assets immutably; HTML without cache headers.
- Use rewrites for SPA fallback and functions for dynamic routes.
- Set `_` predeploy build step in CI so the site is always fresh.
- Pin `headers` per asset type, not per file.

## Capabilities

### hosting-deploy
Deploy, preview, and configure Firebase Hosting sites.

**Parameters:**
- `channel` (string): Preview channel name like staging
- `expires` (string): Channel expiry like 7d
- `site` (string): Hosting site id

**Commands:**
- `firebase init hosting`
- `firebase hosting:channel:deploy staging`
- `firebase hosting:deploy --only hosting`
- `firebase hosting:channel:deploy preview-123 --expires 7d`
- `firebase hosting:channel:list`
- `firebase serve --only hosting`

**Examples:**
- firebase init hosting && firebase hosting:channel:deploy staging
- firebase hosting:channel:deploy preview-123 --expires 7d
- firebase hosting:deploy --only hosting

## References
- [Firebase Hosting docs](https://firebase.google.com/docs/hosting)
- [Hosting full config](https://firebase.google.com/docs/hosting/full-config)
