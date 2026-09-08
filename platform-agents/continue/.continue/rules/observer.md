---
name: "Observer"
description: "Implements the Observer pattern in Node.js: event-driven notifications with EventEmitter and node --test suites. Use when working with node, observer or when the user mentions node, observer."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Implements the Observer pattern in Node.js: event-driven notifications with EventEmitter and node --test suites.

## Agentic Workflow: Read -> Reason -> Act (observer)

You are **Observer** (patterns/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — patterns context for `observer`
- Domain: Implements the Observer pattern in Node.js: event-driven notifications with EventEmitter and node --test suites.
- **node**: Implement and test observer examples. — `node --test tests/`
- Check `knowledge` and `prerequisites: node`

### 2. Reason — think for `observer`
- For `node`: Implement and test observer examples. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `observer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `observer:785fe1f7`

# Observer Pattern

Notify many subscribers when state changes.

## When to Use

- UI updates on data changes
- Event-driven architectures
- Decoupling producers from consumers

## Example (Node.js)

```js
import { EventEmitter } from 'node:events';

class StockTracker extends EventEmitter {
  setPrice(symbol, price) {
    this.emit('price', { symbol, price });
  }
}

const tracker = new StockTracker();
tracker.on('price', ({ symbol, price }) => console.log(`${symbol}: $${price}`));
tracker.setPrice('ACME', 42.5);
```

## Test

```js
import { test } from 'node:test';
import assert from 'node:assert';

test('notifies subscribers on price change', () => {
  const tracker = new StockTracker();
  const seen = [];
  tracker.on('price', (p) => seen.push(p));
  tracker.setPrice('ACME', 42.5);
  assert.deepEqual(seen, [{ symbol: 'ACME', price: 42.5 }]);
});
```

```bash
node --test tests/
```

## Best practices

- Emit events with payload objects, not positional args.
- Use 'error' events for error propagation.
- Clean up listeners to prevent leaks (`off()`).
- Name events as past-tense facts: 'priceChanged'.

## Testing

Verify delivery order, payload shape, and listener cleanup.

## Capabilities

### node
Implement and test observer examples.

**Parameters:**
- `test-name-pattern` (string): Filter tests by name
- `watch` (string): Watch mode
- `file` (string): Test file path

**Commands:**
- `node --test tests/`
- `node --test tests/observer.test.mjs`
- `node --test --test-name-pattern 'stock' tests/`
- `node -e "const {EventEmitter}=require('events'); const e=new EventEmitter(); e.on('x',()=>console.log('fired')); e.emit('x');"`
- `node --test --watch tests/`

**Examples:**
- node --test tests/observer.test.mjs -v
- node --test-name-pattern 'notify' tests/
- node -e "const {EventEmitter}=require('events'); const e=new EventEmitter(); console.log(e.listenerCount('x'))"

## References
- [Refactoring Guru: Observer](https://refactoring.guru/design-patterns/observer)
- [Node.js EventEmitter](https://nodejs.org/api/events.html)
- [node --test runner](https://nodejs.org/api/test.html)