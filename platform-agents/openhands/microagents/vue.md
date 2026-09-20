---
name: "vue"
description: "Builds Vue 3 applications with the create-vue toolchain: SFCs, Pinia state, vue-router, and vue-tsc type checking."
type: knowledge
triggers: ["vue", "scaffold", "typecheck-test"]
---

# vue

Builds Vue 3 applications with the create-vue toolchain: SFCs, Pinia state, vue-router, and vue-tsc type checking.

## Instructions

# Vue

Build Vue 3 applications with the official create-vue toolchain.

## When to Use

- New SPAs with Composition API and SFCs
- Teams wanting granular reactivity without a build-API lock-in
- Progressive adoption: Vue drops into existing HTML projects too

## Scaffold

```bash
npm create vue@latest my-app -- --typescript --router --pinia --eslint
npm run dev
```

## Composition API basics

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

const count = ref(0);
const doubled = computed(() => count.value * 2);
</script>

<template>
  <button @click="count++">{{ count }} / {{ doubled }}</button>
</template>
```

## Pinia store

```typescript
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  state: () => ({ items: [] as string[] }),
  actions: { add(sku: string) { this.items.push(sku); } },
  getters: { size: (s) => s.items.length }
});
```

## Type-checking SFCs

```bash
npx vue-tsc --noEmit
npm run build
```

vue-tsc validates template expressions against prop/ref types.

## Routing

```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/products/:id', component: ProductDetail, props: true },
  { path: '/checkout', component: Checkout, meta: { requiresAuth: true } }
];
```

## Best practices

- Use `<script setup lang="ts">` everywhere.
- Keep stores feature-scoped; avoid one global mega-store.
- Gate CI on vue-tsc --noEmit and npm run lint.
- Prefer computed over watchers for derived values.

## Testing

```bash
npm run test
npx vitest run --coverage
```

Test stores and composables; keep coverage above 80% for critical logic.

## Capabilities

### scaffold
Create Vue 3 projects and add libraries.

**Commands:**
- `npm create vue@latest my-app -- --typescript --router --pinia --eslint`
- `npm install`
- `npm run dev`
- `npm run build`
- `npm run lint`

**Examples:**
- npm create vue@latest store -- --typescript --router --pinia --eslint --vitest
- npm run dev -- --port 5173
- npm run build

### typecheck-test
Type-check, test, and analyze Vue components.

**Commands:**
- `npx vue-tsc --noEmit`
- `npm run test`
- `npx vitest run --coverage`
- `npm run lint -- --fix`
- `npm run build && npx vue-tsc --noEmit`

**Examples:**
- npx vue-tsc --noEmit --strict
- npx vitest run tests/unit/cart.spec.ts
- npm run lint -- --fix
