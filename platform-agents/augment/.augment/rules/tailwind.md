---
type: agent_requested
description: "Configures and builds utility-first CSS with Tailwind: content scanning, custom themes, and production optimization."
---

# Tailwind

Configures and builds utility-first CSS with Tailwind: content scanning, custom themes, and production optimization.

## Instructions

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