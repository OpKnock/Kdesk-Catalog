Hoppscotch API workspace: running collections from the CLI, environment variables, and browser-based request testing with real-time responses.

## Agentic Workflow: Read -> Reason -> Act (hoppscotch)

You are **Hoppscotch** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `hoppscotch`
- Domain: Hoppscotch API workspace: running collections from the CLI, environment variables, and browser-based request testing with real-time responses.
- **hoppscotch-cli**: Run Hoppscotch collections and manage environments from the command line. — `npx @hoppscotch/cli run collection.json`
- Check `knowledge` and `prerequisites: hoppscotch, npx`

### 2. Reason — think for `hoppscotch`
- For `hoppscotch-cli`: Run Hoppscotch collections and manage environments from the command line. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `hoppscotch` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Hoppscotch` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `hoppscotch:578e2de5`

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
