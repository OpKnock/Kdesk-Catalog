---
trigger: glob
description: "Implements the Adapter pattern in TypeScript: converting interfaces between incompatible systems with minimal coupling. Use when working with typescript, adapter or when the user mentions typescript, adapter."
globs: ["**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
---

Implements the Adapter pattern in TypeScript: converting interfaces between incompatible systems with minimal coupling.

## Agentic Workflow: Read -> Reason -> Act (adapter)

You are **Adapter** (patterns/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — patterns context for `adapter`
- Domain: Implements the Adapter pattern in TypeScript: converting interfaces between incompatible systems with minimal coupling.
- **typescript**: Implement and test Adapter pattern examples. — `npx tsc --strict --outDir dist adapter.ts`
- Check `knowledge` and `prerequisites: node, npm, npx`

### 2. Reason — think for `adapter`
- For `typescript`: Implement and test Adapter pattern examples. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `adapter` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `adapter:86391bdb`

# Adapter Pattern

Let incompatible interfaces collaborate without rewriting them.

## When to Use

- Wrapping a third-party SDK behind your own contract
- Bridging legacy systems with new APIs
- Keeping domain code independent of vendor types

## Example (TypeScript)

```typescript
interface PaymentGateway {
  charge(amountCents: number): Promise<string>;
}

class StripeSDK {
  createCharge(opts: { amount: number; currency: string }): Promise<{ id: string }> {
    return Promise.resolve({ id: 'ch_' + Math.random() });
  }
}

class StripeAdapter implements PaymentGateway {
  constructor(private sdk: StripeSDK) {}
  charge(amountCents: number): Promise<string> {
    return this.sdk.createCharge({ amount: amountCents, currency: 'usd' }).then(c => c.id);
  }
}
```

## Test

```typescript
import { test } from 'node:test';
import assert from 'node:assert';

test('adapter maps currency and amounts', async () => {
  const gateway: PaymentGateway = new StripeAdapter(new StripeSDK());
  const id = await gateway.charge(199);
  assert.match(id, /^ch_/);
});
```

```bash
npx tsc --strict --outDir dist adapter.ts adapter.test.ts
node --test dist/*.test.js
```

## Variants

- Object adapter: composition (shown above).
- Class adapter: multiple inheritance (language-limited).
- Prefer object adapters - testable and flexible.

## Best practices

- Keep the adapter thin: translate, don't add business logic.
- Program against your interface, never the SDK directly.
- Unit test the adapter with a fake SDK.
- Name adapters by source: StripeAdapter, LegacyOrderAdapter.

## Testing

Test that all interface methods translate correctly, including error paths.

## Capabilities

### typescript
Implement and test Adapter pattern examples.

**Parameters:**
- `strict` (string): Enable strict type checking
- `outDir` (string): Compile output directory
- `watch` (string): Rebuild on change

**Commands:**
- `npx tsc --strict --outDir dist adapter.ts`
- `node --test dist/adapter.test.js`
- `npm init -y && npm install --save-dev typescript @types/node`
- `npx tsc --watch`
- `node dist/main.js`

**Examples:**
- npx tsc --strict adapter.ts main.ts --outDir dist
- node --test dist/*.test.js
- npx tsc --noEmit --strict adapter.ts

## References
- [Refactoring Guru: Adapter](https://refactoring.guru/design-patterns/adapter)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
