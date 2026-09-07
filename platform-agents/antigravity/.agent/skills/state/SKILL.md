---
name: "state"
description: "Implements the State pattern in TypeScript with Vitest: state machines that swap behavior as state changes. Use when working with ts vitest, state or when the user mentions ts vitest, state."
license: "MIT"
compatibility: "Requires npm, npx."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "patterns"}
allowed-tools: "Glob Grep Read Bash(npm:*) Bash(npx:*)"
---

Implements the State pattern in TypeScript with Vitest: state machines that swap behavior as state changes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm init -y && npm install -D typescript vitest`
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
