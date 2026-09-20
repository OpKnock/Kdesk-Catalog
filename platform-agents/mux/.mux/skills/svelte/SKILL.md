---
name: "svelte"
description: "Builds reactive Svelte 5 apps with runes, SvelteKit routing, and the sv CLI: dev, check, and build workflows."
---

# svelte

Builds reactive Svelte 5 apps with runes, SvelteKit routing, and the sv CLI: dev, check, and build workflows.

## Instructions

# Svelte

Build reactive Svelte 5 apps with runes and SvelteKit.

## When to Use

- Small-to-medium apps wanting minimal framework weight
- Strong compile-time reactivity with tiny bundles
- Transitioning from React with a simpler mental model

## Scaffold

```bash
npx sv create my-app --template minimal --types ts
npm run dev
```

## Runes (Svelte 5)

```svelte
<script lang="ts">
  let count = $state(0);
  const doubled = $derived(count * 2);
  $effect(() => {
    console.log('count is', count);
  });
</script>

<button onclick={() => count++}>Count: {count}</button>
<p>Doubled: {doubled}</p>
```

## SvelteKit routing

```svelte
<!-- src/routes/+page.svelte -->
<h1>Home</h1>

<!-- src/routes/about/+page.svelte -->
<h1>About</h1>
```

```ts
// src/routes/+page.server.ts
export async function load({ fetch }) {
  const res = await fetch('/api/featured');
  return { featured: await res.json() };
}
```

## Check and build

```bash
npx svelte-check --tsconfig ./tsconfig.json --fail-on-warnings
npm run build
```

Choose an adapter via `npx sv add adapter-node` for Node deployment.

## Best practices

- Use runes consistently; avoid legacy `let x = reactive` patterns.
- Keep page server loads lean and streaming for slow APIs.
- Gate CI on svelte-check with --fail-on-warnings.
- Use `$derived` for anything computed from state.

## Testing

```bash
npm run check
npm run build
```

Run both before release; build failures here are usually adapter config.

## Capabilities

### sv-cli
Create and manage Svelte projects with the sv CLI.

**Commands:**
- `npx sv create my-app --template minimal --types ts`
- `npm run dev`
- `npx sv add tailwindcss`
- `npx sv add eslint`
- `npm run preview`

**Examples:**
- npx sv create blog --template demo --no-install
- npx sv add adapter-node
- npx sv add --check

### check-build
Type-check and build SvelteKit applications.

**Commands:**
- `npx svelte-check --tsconfig ./tsconfig.json`
- `npm run check`
- `npm run build`
- `npx svelte-kit sync`
- `npm run build && npx svelte-check`

**Examples:**
- npx svelte-check --tsconfig ./tsconfig.json --fail-on-warnings
- npx svelte-kit sync
- npm run check && npm run build
