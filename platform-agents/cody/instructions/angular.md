# angular

Builds, tests, and deploys Angular applications with the Angular CLI: components, signals, routing, and standalone APIs.

## Instructions

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
