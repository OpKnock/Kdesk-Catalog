---
applyTo: "**/*.r **/*.sh **/*.{ts,tsx}"
---

Develops React applications with Vite: scaffolding, JSX, hooks, and production builds with strict TypeScript.

## Agentic Workflow: Read -> Reason -> Act (react)

You are **React** (frontend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `react`
- Domain: Develops React applications with Vite: scaffolding, JSX, hooks, and production builds with strict TypeScript.
- **vite**: Scaffold and run React apps on the Vite toolchain. — `npm create vite@latest my-app -- --template react-ts`
- **typescript-check**: Type-check and optimize React code. — `npx tsc --noEmit`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `react`
- For `vite`: Scaffold and run React apps on the Vite toolchain. — decide which checks to run
- For `typescript-check`: Type-check and optimize React code. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `react` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `react:b3eaa858`

# React

Build React applications on Vite with typed components and fast iteration.

## When to Use

- New SPAs where you own the full toolchain
- Migrating from legacy CRA tooling
- Component-heavy interactive UIs

## Scaffold

```bash
npm create vite@latest my-app -- --template react-ts
npm install
npm run dev
```

## Component basics

```tsx
type UserCardProps = { name: string; role: string; onSelect: (id: string) => void };

export function UserCard({ name, role, onSelect }: UserCardProps) {
  return (
    <button onClick={() => onSelect(name)}>
      <strong>{name}</strong> <span>{role}</span>
    </button>
  );
}
```

## Hooks discipline

- `useState` for local state, `useReducer` for complex transitions
- `useEffect` for subscriptions and sync with external systems only
- `useMemo`/`useCallback` only when profiling proves the need

```tsx
export function useDebounced<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}
```

## Type checking and build

```bash
npx tsc --noEmit
npm run build
npm run preview
```

## Best practices

- Type all props and state; avoid `any` at module boundaries.
- Colocate tests next to components: `UserCard.test.tsx`.
- Split code by feature folders with a `components/` shared dir.
- Use `import.meta.env` typed env variables, never string lookups.

## Testing

```bash
npx vitest run --coverage
```

Verify coverage before every release.

## Capabilities

### vite
Scaffold and run React apps on the Vite toolchain.

**Parameters:**
- `template` (string): react, react-ts, or vanilla-ts
- `port` (number): Dev server port
- `open` (string): Open browser on dev start

**Commands:**
- `npm create vite@latest my-app -- --template react-ts`
- `npm install`
- `npm run dev`
- `npm run build`
- `npm run preview`

**Examples:**
- npm create vite@latest admin -- --template react-ts --no-interactive
- npm run dev -- --port 5173 --open
- npm run build && npm run preview -- --port 4173

### typescript-check
Type-check and optimize React code.

**Parameters:**
- `mode` (string): Vite build mode for env configs
- `noEmit` (string): Type-check without emitting files
- `minify` (string): esbuild or terser minifier

**Commands:**
- `npx tsc --noEmit`
- `npm run build && npx tsc --noEmit`
- `npx vite build --mode production`
- `npm run preview`
- `npx eslint . --ext ts,tsx`

**Examples:**
- npx tsc --noEmit --strict
- npx vite build --minify esbuild
- npx tsc --noEmit && npm run build

## References
- [React Quick Start](https://react.dev/learn)
- [Vite Guide](https://vite.dev/guide/)
- [TypeScript with React](https://www.typescriptlang.org/docs/handbook/react-&-webpack.html)
