---
applyTo: "**/*.go **/*.json **/*.py **/*.r **/*.sh"
---

# refactoring

Guides safe refactoring: detecting duplication, measuring complexity, and validating with tests after each change.

## Instructions

# Refactoring

Improves code structure without changing behavior, using tests as a safety net
and tooling to find hot spots.

## When to Use

- Removing duplicated code before adding a feature
- Breaking apart god classes and long functions
- Reducing circular dependencies

## Real Commands

```bash
# Find duplicated blocks
npx jscpd --min-lines 8 --min-tokens 40 src/

# Find circular imports
npx madge --circular --extensions ts src/

# List modules with too many dependencies
npx madge --json src/ | jq 'to_entries | map(select(.value|length>10))'

# Verify the tree still compiles
python -m compileall -q src/

# Confirm tests still pass
pytest -q

# Review rename scope with move detection
git diff -M --stat
```

## Safe Refactoring Workflow

1. **Baseline**: run the full test suite and note failures (must be green)
2. **Characterize**: if no tests exist, write characterization tests first
3. **Small steps**: extract a function, run tests, commit - repeat
4. **Verify**: compare behavior before/after with tests and a quick smoke run
5. **Cleanup**: remove dead code detected by the compiler/type-checker

## Anti-Patterns

- Refactoring and adding features in the same commit
- Renaming public APIs without updating all call sites
- 'Big-bang' rewrites without characterization tests

## Example Response

Maps the duplication clusters and circular dependencies found by jscpd/madge, then
proposes an order of refactorings with the test command to run after each step.

## Capabilities

### refactoring-workflow
Analyze, refactor, and verify code changes using duplication and dependency tools

**Commands:**
- `npx jscpd src/`
- `npx madge --circular src/`
- `git diff -M --stat`
- `python -m compileall src/`
- `pytest -q --cov=src`

**Examples:**
- npx jscpd --min-lines 10 --min-tokens 50 src/
- npx madge --circular --extensions ts src/
- git diff --word-diff main...HEAD
