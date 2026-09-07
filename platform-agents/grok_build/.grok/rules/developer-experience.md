Improves DX: unified dev commands, parallel task runners, instant feedback loops, and consistent tooling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm pkg set scripts.dev="vite" scripts.lint="eslint . --max-`
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

# Developer Experience

Makes local development fast and consistent: unified scripts, parallel runners,
instant checks, and low-friction setup.

## When to Use

- A repo where devs run 5 different command sequences
- Slow feedback loops blocking iteration
- New-hire onboarding friction

## Real Commands

```bash
# One command to rule them all
sudo npm pkg set scripts.dev="vite" scripts.check="npm-run-all --parallel lint typecheck"
sudo npm pkg set scripts.test="vitest run" scripts.dx="npm run check && npm run dev"

# Run web + api together
sudo npx concurrently -k -n web,api -c blue,green "npm run dev:web" "npm run dev:api"

# Parallel checks
sudo npm-run-all --parallel lint typecheck test

# Affected-only in monorepos
sudo npx nx affected -t test --base=origin/main

# One-time env setup
sudo npx playwright install --with-deps
```

## Recommended Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "check": "npm-run-all --parallel lint typecheck",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

## Best Practices

- Provide `dev`, `build`, `check`, `test` in every package
- Prefer `--parallel` for independent checks
- Add a CONTRIBUTING quick-start with one command
- Automate dependency setup (playwright install, husky init)
- Keep cold-start dev time under 10 seconds if possible

## Example Response

Standardizes the repo scripts, wires parallel runners, and verifies the whole
dev loop works from a fresh clone.

## Capabilities

### dx-tooling
Standardize scripts and run tasks in parallel for faster feedback

**Parameters:**
- `parallel` (boolean): Run tasks in parallel (npm-run-all)
- `names` (string): concurrently -n: task names for prefixes
- `with-deps` (boolean): Install browser dependencies for Playwright

**Commands:**
- `npm pkg set scripts.dev="vite" scripts.lint="eslint . --max-warnings 0"`
- `npx concurrently -k -n web,api -c blue,green "npm run dev:web" "npm run dev:api"`
- `npm-run-all --parallel lint typecheck test`
- `npx nx affected -t test --base=origin/main`
- `npx playwright install --with-deps`

**Examples:**
- npx concurrently "npm run dev" "npm run storybook"
- npm run check && npm run dev
- npx nx run-many -t build --skip-nx-cache

## References
- [npm-run-all docs](https://github.com/mysticatea/npm-run-all)
- [concurrently docs](https://github.com/open-cli-tools/concurrently)
- [Nx developer experience](https://nx.dev/features/explore-graph)