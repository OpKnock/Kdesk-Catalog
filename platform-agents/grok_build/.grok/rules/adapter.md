Implements the Adapter pattern in TypeScript: converting interfaces between incompatible systems with minimal coupling.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx tsc --strict --outDir dist adapter.ts`
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