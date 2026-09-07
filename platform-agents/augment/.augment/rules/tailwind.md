---
type: agent_requested
description: "Configures and builds utility-first CSS with Tailwind: content scanning, custom themes, and production optimization. Use when working with setup, build, frontend or when the user mentions setup, build, frontend."
---

Configures and builds utility-first CSS with Tailwind: content scanning, custom themes, and production optimization.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install -D tailwindcss @tailwindcss/cli`, `npx @tailwindcss/cli -i src/input.css -o dist/output.css`
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

# Tailwind CSS

Ship utility-first CSS with Tailwind CLI pipelines.

## When to Use

- Rapid UI iteration with utility classes
- Consistent design tokens across large teams
- Small CSS payloads with only used classes compiled

## Install and configure

```bash
npm install -D tailwindcss @tailwindcss/cli
npx @tailwindcss/cli init -p
```

## Input CSS

```css
@import "tailwindcss";
@theme {
  --color-brand: #4f46e5;
  --font-display: "Sora", sans-serif;
}
```

## Build and watch

```bash
npx @tailwindcss/cli -i src/input.css -o dist/output.css
npx @tailwindcss/cli -i src/input.css -o dist/output.css --watch
npx @tailwindcss/cli -i src/input.css -o dist/output.css --minify
```

## Content scanning

Tailwind v4 auto-detects sources; with a config file, keep content globs tight:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,tsx}'],
  theme: { extend: { colors: { brand: '#4f46e5' } } }
};
```

## Custom utilities

```css
@utility glass {
  backdrop-filter: blur(8px);
  background: rgb(255 255 255 / 0.8);
}
```

## Best practices

- Keep design tokens in `@theme`, not scattered hex values.
- Extract repeated markup into components, not custom classes.
- Verify output size: minified CSS should grow only with usage.
- Prefer responsive prefixes over media query duplication.

## Testing

```bash
npx @tailwindcss/cli -i src/input.css -o dist/output.css --minify
ls -la dist/output.css
```

Watch for unexpected bloat after adding libraries.

## Capabilities

### setup
Install and configure Tailwind CSS.

**Parameters:**
- `init` (string): Generate config with -p for postcss
- `ts` (string): Generate TypeScript config
- `content` (string): Glob patterns of files to scan for classes

**Commands:**
- `npm install -D tailwindcss @tailwindcss/cli`
- `npx @tailwindcss/cli init -p`
- `npx @tailwindcss/cli init --ts`
- `npm install -D @tailwindcss/vite`
- `npm install -D @tailwindcss/typography`

**Examples:**
- npm install -D tailwindcss @tailwindcss/vite
- npx @tailwindcss/cli init --ts
- npm install -D @tailwindcss/forms @tailwindcss/typography

### build
Compile Tailwind CSS for development and production.

**Parameters:**
- `input` (string): Input CSS file with @import tailwindcss
- `output` (string): Output CSS file path
- `minify` (string): Minify output for production

**Commands:**
- `npx @tailwindcss/cli -i src/input.css -o dist/output.css`
- `npx @tailwindcss/cli -i src/input.css -o dist/output.css --minify`
- `npx @tailwindcss/cli -i src/input.css -o dist/output.css --watch`
- `npx @tailwindcss/cli -i src/input.css -o dist/output.css --minify --watch`
- `npx tailwindcss -c tailwind.config.js -i src/input.css -o dist/output.css`

**Examples:**
- npx @tailwindcss/cli -i src/input.css -o dist/output.css --minify
- npx @tailwindcss/cli -i src/input.css -o dist/output.css --watch
- npx tailwindcss -c tailwind.config.js -i src/input.css -o dist/output.css --minify

## References
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Tailwind CLI](https://tailwindcss.com/docs/cli)
- [Tailwind with Vite](https://tailwindcss.com/docs/installation/using-vite)