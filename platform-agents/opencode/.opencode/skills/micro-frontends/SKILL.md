---
name: "micro-frontends"
description: "Architects micro-frontend platforms with single-spa, Module Federation, and Nx workspaces: composition, sharing, and independent deploys. Use when working with single spa, nx or when the user mentions single spa, nx."
---

Architects micro-frontend platforms with single-spa, Module Federation, and Nx workspaces: composition, sharing, and independent deploys.

## Agentic Workflow: Read -> Reason -> Act (micro-frontends)

You are **micro-frontends** (frontend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `micro-frontends`
- Domain: Architects micro-frontend platforms with single-spa, Module Federation, and Nx workspaces: composition, sharing, and independent deploys.
- **single-spa**: Build and register micro-frontend applications. — `npx create-single-spa --moduleType root-config`
- **nx**: Manage monorepo builds and dependencies with Nx. — `npx nx graph`
- Check `knowledge` and `prerequisites: node.js, react, webpack, single-spa`

### 2. Reason — think for `micro-frontends`
- For `single-spa`: Build and register micro-frontend applications. — decide which checks to run
- For `nx`: Manage monorepo builds and dependencies with Nx. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `micro-frontends` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `micro-frontends:9f84a812`

# Micro-Frontends

Compose independent frontend apps into one product.

## When to Use

- Multiple teams shipping one web product independently
- Migrating a monolith UI in slices
- Sharing a shell, auth, and navigation

## single-spa composition

```bash
npx create-single-spa --moduleType root-config
npx create-single-spa --moduleType app-parcel --framework react
```

Root config registers apps with lifecycle functions (bootstrap/mount/unmount).

## Module Federation sharing

```js
// webpack config of shell
new ModuleFederationPlugin({
  name: 'shell',
  remotes: { orders: 'orders@http://localhost:9001/remoteEntry.js' },
  shared: { react: { singleton: true } }
});
```

Singletons prevent duplicate React instances - version them carefully.

## Nx monorepo management

```bash
npx nx graph
npx nx run-many --target=test --all
npx nx affected:build --base=main
```

Only rebuild what changed using `affected`.

## Contracts between apps

- Shared props: user, locale, navigation state.
- Routing: each app owns its routes; the shell owns top-level segments.
- Styling: design tokens via shared packages, not global CSS.
- Events: pub/sub on window or a shared bus, versioned payloads.

## Best practices

- Version and document the integration contract.
- Every app deploys independently; no release trains.
- Shared UI in a versioned package, not duplicated code.
- E2E the shell + key apps in a single smoke suite.

## Testing

```bash
npx nx affected:test --base=origin/main
```

Run integration smoke tests across the composed shell weekly.

## Capabilities

### single-spa
Build and register micro-frontend applications.

**Parameters:**
- `moduleType` (string): root-config, app-parcel, or utility-module
- `framework` (string): react, vue, angular, svelte for the parcel
- `port` (number): Serve port for the app

**Commands:**
- `npx create-single-spa --moduleType root-config`
- `npx create-single-spa --moduleType app-parcel`
- `npm run build -- --watch`
- `npx serve -s dist -l 9000`
- `npm run importmap`

**Examples:**
- npx create-single-spa --moduleType app-parcel --framework react
- npx create-single-spa --moduleType root-config --dir root
- npm run build && npx serve -s dist -l 8080

### nx
Manage monorepo builds and dependencies with Nx.

**Parameters:**
- `target` (string): build, test, lint target
- `base` (string): Git base for affected computation
- `project` (string): Project name like shell or orders

**Commands:**
- `npx nx graph`
- `npx nx run shell:build --configuration=production`
- `npx nx affected:build --base=main`
- `npx nx run-many --target=test --all`
- `npx nx migrate latest`

**Examples:**
- npx nx affected:test --base=origin/main
- npx nx build shell --with-deps
- npx nx run-many --target=lint --parallel=3

## References
- [single-spa Docs](https://single-spa.js.org/docs/getting-started-overview)
- [Module Federation](https://webpack.js.org/concepts/module-federation/)
- [Nx Docs](https://nx.dev/)
