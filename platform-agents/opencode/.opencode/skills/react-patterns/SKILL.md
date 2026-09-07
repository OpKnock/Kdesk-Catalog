---
name: "react-patterns"
description: "Applies production React architecture patterns: composition, state management, Storybook, and code quality gates for component libraries. Use when working with storybook, code quality, frontend or when the user mentions storybook, code quality, frontend."
---

Applies production React architecture patterns: composition, state management, Storybook, and code quality gates for component libraries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx storybook@latest init --type react-vite`, `npx eslint src --ext .ts,.tsx --max-warnings 0`
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

# React Patterns

Architect maintainable React codebases with proven patterns and gates.

## When to Use

- Growing component libraries used by multiple teams
- Refactors of tangled prop drilling and effects
- Introducing testing and visual review into a React codebase

## Composition over props drilling

```tsx
type CardProps = { title: string; children: React.ReactNode };

export function Card({ title, children }: CardProps) {
  return <section className="card">{title && <h2>{title}</h2>}{children}</section>;
}
```

## State management tiers

- Local UI state: `useState`/`useReducer`
- Server state: TanStack Query
- Cross-cutting global state: Zustand or Context + reducer

```bash
npm install @tanstack/react-query zustand
```

## Storybook as the component contract

```bash
npx storybook@latest init --type react-vite
npm run build-storybook
```

Add a11y addon and Chromatic for visual regression on every PR.

## Code quality gates

```bash
npx eslint src --ext .ts,.tsx --max-warnings 0
```

```json
{
  "extends": ["eslint:recommended", "plugin:react-hooks/recommended"],
  "rules": { "react-hooks/rules-of-hooks": "error" }
}
```

## Best practices

- Keep effects minimal; derive state during render where possible.
- Export memoized callbacks only when profiling shows a need.
- Every shared component gets a Storybook story and a unit test.
- Review dependency upgrades quarterly with npm outdated.

## Testing

```bash
npx vitest run --coverage
```

Run unit + storybook interaction tests before visual review.

## Capabilities

### storybook
Build and maintain a component library with Storybook.

**Parameters:**
- `type` (string): react-vite, react-webpack5, or framework preset
- `project-token` (string): Chromatic visual regression token
- `addon` (string): Storybook addon package to install

**Commands:**
- `npx storybook@latest init --type react-vite`
- `npx storybook@latest add @storybook/addon-a11y`
- `npm run storybook`
- `npm run build-storybook`
- `npx chromatic --project-token $CHROMATIC_TOKEN --auto-accept-changes`

**Examples:**
- npx storybook@latest init --type react-vite --no-dev
- npm run build-storybook -- --quiet
- npx chromatic --exit-zero-on-changes

### code-quality
Enforce React patterns with ESLint and dependency hygiene.

**Parameters:**
- `max-warnings` (number): CI gate on warnings
- `rule` (string): Inline rule override
- `ext` (string): File extensions to lint

**Commands:**
- `npx eslint src --ext .ts,.tsx --max-warnings 0`
- `npx eslint src --fix`
- `npm install -D eslint-plugin-react-hooks eslint-plugin-react-refresh`
- `npx npm-check-updates -u`
- `npm outdated`

**Examples:**
- npx eslint src --max-warnings 0 --rule 'react-hooks/rules-of-hooks:error'
- npx npm-check-updates -u && npm install
- npx eslint src/components --fix

## References
- [React Docs](https://react.dev/learn)
- [Storybook](https://storybook.js.org/docs)
- [React Hooks rules](https://react.dev/reference/rules)
