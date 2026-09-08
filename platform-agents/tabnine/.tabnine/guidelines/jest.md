Writes and runs JavaScript/TypeScript tests with Jest: unit tests, mocks, snapshots, and watch mode.

## Agentic Workflow: Read -> Reason -> Act (jest)

You are **jest** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `jest`
- Domain: Writes and runs JavaScript/TypeScript tests with Jest: unit tests, mocks, snapshots, and watch mode.
- **jest-running**: Run Jest suites with filters and watch mode. — `npx jest`
- **mocking**: Mock modules, timers, and fetch calls. — `npx jest --coverage --silent`
- **snapshots**: Create, update, and review snapshots. — `npx jest --updateSnapshot`
- Check `knowledge` and `prerequisites: global.fetch, jest.mock('./api, jest.usefaketimers, npx`

### 2. Reason — think for `jest`
- For `jest-running`: Run Jest suites with filters and watch mode. — decide which checks to run
- For `mocking`: Mock modules, timers, and fetch calls. — decide which checks to run
- For `snapshots`: Create, update, and review snapshots. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `jest` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Jest.mock('./api')` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `jest:bb1224b2`

# Jest

Unit and integration testing for JavaScript and TypeScript.

## What This Skill Does

- Runs test suites with filters and watch mode
- Writes assertions with rich matchers
- Mocks modules, timers, and network calls
- Maintains snapshot tests safely

## When to Use

- Adding tests to JS/TS services
- Debugging a failing unit test
- Regression protection for pure logic

## Real Commands

```bash
# Run
npx jest
npx jest src/order.test.js
npx jest -t "calculates total"
npx jest --watch
npx jest --ci --coverage

# Snapshots
npx jest --updateSnapshot
npx jest --ci --snapshotSummary

# Debug
npx jest --coverage --silent
```

## Sample Test

```js
test('calculates total with discount', () => {
  const order = new Order([{ price: 10, qty: 2 }, { price: 5, qty: 1 }]);
  expect(order.total(0.1)).toBeCloseTo(22.5);
});

test('applies discount once', () => {
  const order = new Order([{ price: 10, qty: 2 }]);
  const spy = jest.spyOn(order, 'discount');
  order.total(0.1);
  expect(spy).toHaveBeenCalledTimes(1);
});
```

## Best Practices

- Use toBeCloseTo for floats; never toBe on decimals
- Keep unit tests synchronous and fast
- Mock external APIs; test real behavior in integration
- Review snapshot diffs carefully in PRs
- Run --watch during development, --ci in pipelines

## Capabilities

### jest-running
Run Jest suites with filters and watch mode.

**Parameters:**
- `path` (string): Test file or directory
- `testNamePattern` (string): Test name filter (-t)
- `ci` (boolean): CI mode (no watch, deterministic)

**Commands:**
- `npx jest`
- `npx jest src/order.test.js`
- `npx jest -t "calculates total"`
- `npx jest --watch`
- `npx jest --ci --coverage`

**Examples:**
- npx jest src/order.test.js
- npx jest -t "calculates total"
- npx jest --watch

### mocking
Mock modules, timers, and fetch calls.

**Parameters:**
- `module` (string): Module to mock
- `restoreMocks` (boolean): Restore mocks between tests with --restoreMocks.

**Commands:**
- `npx jest --coverage --silent`
- `jest.mock('./api')`
- `jest.useFakeTimers()`
- `global.fetch = jest.fn()`
- `npx jest --restoreMocks`

**Examples:**
- jest.mock('./api')
- jest.useFakeTimers()
- global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({}) }))

### snapshots
Create, update, and review snapshots.

**Parameters:**
- `updateSnapshot` (boolean): Update snapshot files
- `ci` (boolean): CI mode with --ci --snapshotSummary output.

**Commands:**
- `npx jest --updateSnapshot`
- `npx jest --ci --snapshotSummary`
- `npx jest -t "renders" --updateSnapshot`
- `npx jest --watch --updateSnapshot`

**Examples:**
- npx jest --updateSnapshot
- npx jest --ci --snapshotSummary
- npx jest -t "renders" --updateSnapshot

## References
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Jest Snapshot Testing](https://jestjs.io/docs/snapshot-testing)