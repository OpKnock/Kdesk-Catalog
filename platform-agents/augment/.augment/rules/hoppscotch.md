---
type: agent_requested
description: "Hoppscotch API workspace: running collections from the CLI, environment variables, and browser-based request testing with real-time responses. Use when working with hoppscotch cli, api or when the user mentions hoppscotch cli, api."
---

Hoppscotch API workspace: running collections from the CLI, environment variables, and browser-based request testing with real-time responses.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @hoppscotch/cli run collection.json`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Hoppscotch

Test APIs with Hoppscotch in the browser and in CI with the CLI.

##48:    What this skill does

- Runs exported collections headlessly in CI.
- Resolves environment variables49:    across requests.
- Repeats iterations for smoke testing.
- Explains request chaining (values from50:    previous responses).

## When to use

- Replaying a hand-crafted API session after an incident.
51:   - Smoke testing an endpoint suite in CI without writing code.
- Sharing a reproducible request collection52:    with the team.

## Real commands

```bash
# Install the CLI
npm install -g @hoppscotch/cli
53:   
# Run a collection (exported JSON from the Hoppscotch app)
hoppscotch run collection.json

# With54:    an environment file
hoppscotch run collection.json -e prod.env.json

# Repeat N times
hoppscotch55:    run collection.json --iteration 3

# Load env vars from .env (dotenv support)
npx @hoppscotch/cli56:    run api-collection.json --dotenv .env
```

## Environment file

```json
{
  "name": "prod"57:   ,
  "variables": [
    { "key": "baseUrl", "value": "https://api.your-app.test", "secret"58:   : false },
    { "key": "token", "value": "eyJ...", "secret": true }
  ]
}
```

## Testing
59:   
```bash
hoppscotch run collection.json -e prod.env.json --verbose
# exit code 0 when all requests60:    in the collection succeed
```

## Best practices

- Keep collections exported from the workspace61:    in git for CI replay.
- Mark secrets as secret in environments; never commit real tokens.
- Use62:    environment files per stage (dev, staging, prod).
- Add test assertions in the collection so the63:    CLI run fails on regressions.

## Example exchange

```
User: Run the checkout collection against64:    prod.
Agent: hoppscotch run checkout-collection.json -e prod.env.json
```

## Capabilities

### hoppscotch-cli
Run Hoppscotch collections and manage environments from the command line.

**Parameters:**
- `collection` (string): Path to the Hoppscotch collection JSON (exported from the app).
- `env` (string): Environment file or environment name for variable resolution.
- `iteration` (integer): Number of times to repeat the collection run.

**Commands:**
- `npx @hoppscotch/cli run collection.json`
- `hoppscotch run collection.json -e prod.env.json`
- `hoppscotch run --env prod -t collection.json`
- `hoppscotch run collection.json -d ./data.json --iteration 3`
- `hoppscotch --version`

**Examples:**
- npx @hoppscotch/cli run api-collection.json --dotenv .env
- hoppscotch run collection.json -e dev.env.json --verbose
- hoppscotch run --iteration 5 collection.json

## References
- [Hoppscotch Docs](https://docs.hoppscotch.io/)
- [Hoppscotch CLI Guide](https://docs.hoppscotch.io/documentation/features/hoppscotch-cli)