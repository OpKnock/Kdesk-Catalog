---
trigger: glob
description: "Implements the State pattern in TypeScript with Vitest: state machines that swap behavior as state changes. Use when working with ts vitest, state or when the user mentions ts vitest, state."
globs: ["**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
---

Implements the State pattern in TypeScript with Vitest: state machines that swap behavior as state changes.

## Agentic Workflow: Read -> Reason -> Act (state)

You are **State** (patterns/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — patterns context for `state`
- Domain: Implements the State pattern in TypeScript with Vitest: state machines that swap behavior as state changes.
- **ts-vitest**: Implement and test state machine examples. — `npm init -y && npm install -D typescript vitest`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `state`
- For `ts-vitest`: Implement and test state machine examples. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `state` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `state:6324a440`

# State Pattern

Let an object change behavior when its state changes.

## When to Use

- Objects with many conditional state branches
- Workflows: draft -> review -> published
- Replacing huge switch/if chains

## Example (TypeScript)

```typescript
interface DocumentState {
  publish(doc: Document): void;
  label(): string;
}

class DraftState implements DocumentState {
  label() { return 'draft'; }
  publish(doc: Document) { doc.setState(new ReviewState()); }
}

class ReviewState implements DocumentState {
  label() { return 'review'; }
  publish(doc: Document) { throw new Error('Needs approval'); }
}

class Document {
  private state: DocumentState = new DraftState();
  setState(s: DocumentState) { this.state = s; }
  publish() { this.state.publish(this); }
  status() { return this.state.label(); }
}
```

## Test

```typescript
import { describe, it, expect } from 'vitest';

describe('Document workflow', () => {
  it('draft publishes to review', () => {
    const doc = new Document();
    doc.publish();
    expect(doc.status()).toBe('review');
  });

  it('review refuses direct publish', () => {
    const doc = new Document();
    doc.publish();
    expect(() => doc.publish()).toThrow('Needs approval');
  });
});
```

```bash
npx tsc --noEmit --strict state.ts
npx vitest run tests/state.test.ts
```

## Best practices

- States hold transitions; the context holds data.
- Encode illegal transitions as explicit errors.
- Consider a state machine library for complex flows.
- Test every transition and every illegal transition.

## Testing

Cover all legal transitions plus each invalid one.

## Capabilities

### ts-vitest
Implement and test state machine examples.

**Parameters:**
- `t` (string): Test name filter
- `coverage` (string): Coverage collection
- `strict` (string): Strict TypeScript check

**Commands:**
- `npm init -y && npm install -D typescript vitest`
- `npx tsc --noEmit --strict state.ts`
- `npx vitest run tests/state.test.ts`
- `npx vitest run --coverage`
- `npx vitest run tests/state.test.ts -t 'draft'`

**Examples:**
- npx vitest run tests/state.test.ts
- npx tsc --noEmit --strict state.ts machine.ts
- npx vitest run -t 'publish'

## References
- [Refactoring Guru: State](https://refactoring.guru/design-patterns/state)
- [Vitest](https://vitest.dev/guide/)
