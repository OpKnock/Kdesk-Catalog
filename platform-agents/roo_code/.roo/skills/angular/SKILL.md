---
name: "angular"
description: "Builds, tests, and deploys Angular applications with the Angular CLI: components, signals, routing, and standalone APIs. Use when working with scaffold, build test, frontend or when the user mentions scaffold, build test, frontend."
license: "MIT"
compatibility: "Requires ng."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "frontend"}
allowed-tools: "Glob Grep Read Bash(ng:*)"
---

Builds, tests, and deploys Angular applications with the Angular CLI: components, signals, routing, and standalone APIs.

## Agentic Workflow: Read -> Reason -> Act (angular)

You are **angular** (frontend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `angular`
- Domain: Builds, tests, and deploys Angular applications with the Angular CLI: components, signals, routing, and standalone APIs.
- **scaffold**: Create Angular workspaces, components, and services. — `ng new my-app --style=scss --routing --ssr=false`
- **build-test**: Build, serve, test, and analyze Angular apps. — `ng serve --port 4200 --hmr`
- Check `knowledge` and `prerequisites: ng`

### 2. Reason — think for `angular`
- For `scaffold`: Create Angular workspaces, components, and services. — decide which checks to run
- For `build-test`: Build, serve, test, and analyze Angular apps. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `angular` tools
- Tools: `Glob`, `Grep`, `Read`, `Ng` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `angular:e2ce3cc6`

# Angular

Develop Angular apps with the Angular CLI and modern standalone APIs.

## When to Use

- Enterprise SPAs needing strong structure and DI
- Teams standardized on TypeScript and RxJS/signals
- Apps with complex forms and routing

## Create a workspace

```bash
ng new my-app --style=scss --routing --ssr=false
```

Prefer standalone components (default) - modules are only needed for legacy code.

## Generate code

```bash
ng generate component dashboard --standalone --inline-template --inline-style
ng generate service api/orders
ng generate guard auth/requires-login
ng add @angular/material
```

## Development loop

```bash
ng serve --port 4200 --hmr
ng test --watch=false --browsers=ChromeHeadless
ng lint --fix
ng build --configuration=production
```

## Signals instead of observables where possible

```typescript
export class CartComponent {
  items = signal<Item[]>([]);
  total = computed(() => this.items().reduce((s, i) => s + i.price, 0));
}
```

## Routing with lazy loading

```typescript
export const routes: Routes = [
  { path: 'checkout', loadComponent: () => import('./checkout/checkout.component').then(m => m.CheckoutComponent) },
  { path: '', loadChildren: () => import('./home/routes').then(m => m.routes) }
];
```

## Best practices

- Use OnPush change detection with signals.
- Keep components small; extract presentational vs. container roles.
- Run `ng build` with a strict TypeScript config in CI.
- Use `inject()` instead of constructor injection for readability.

## Testing

```bash
ng test --watch=false --code-coverage
```

Target 80%+ coverage on services and reducers, not templates.

## Capabilities

### scaffold
Create Angular workspaces, components, and services.

**Parameters:**
- `style` (string): CSS preprocessor: scss, sass, less, css
- `routing` (string): true/false to add the router
- `ssr` (string): true/false server-side rendering support

**Commands:**
- `ng new my-app --style=scss --routing --ssr=false`
- `ng generate component dashboard`
- `ng generate service api/orders`
- `ng add @angular/material`
- `ng generate component dashboard --standalone --inline-template --inline-style`

**Examples:**
- ng new store --style=scss --routing --ssr=false
- ng generate component checkout/payment --standalone
- ng generate service auth/token

### build-test
Build, serve, test, and analyze Angular apps.

**Parameters:**
- `configuration` (string): production, development, or custom config
- `watch` (string): true/false test watch mode
- `browsers` (string): Karma browser launcher, e.g. ChromeHeadless

**Commands:**
- `ng serve --port 4200 --hmr`
- `ng build --configuration=production`
- `ng test --watch=false --browsers=ChromeHeadless`
- `ng lint --fix`
- `ng build --configuration=production --stats-json`

**Examples:**
- ng serve --open
- ng test --watch=false --code-coverage
- ng build --configuration=staging --output-path dist/staging

## References
- [Angular CLI](https://angular.dev/tools/cli)
- [Angular Guide](https://angular.dev/guide/components)
- [Angular Router](https://angular.dev/guide/routing)
