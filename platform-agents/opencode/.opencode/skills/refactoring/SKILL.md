---
name: "refactoring"
description: "Guides safe refactoring: detecting duplication, measuring complexity, and validating with tests after each change. Use when working with refactoring workflow, code quality or when the user mentions refactoring workflow, code quality."
---

Guides safe refactoring: detecting duplication, measuring complexity, and validating with tests after each change.

## Agentic Workflow: Read -> Reason -> Act (refactoring)

You are **refactoring** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `refactoring`
- Domain: Guides safe refactoring: detecting duplication, measuring complexity, and validating with tests after each change.
- **refactoring-workflow**: Analyze, refactor, and verify code changes using duplication and dependency tools — `npx jscpd src/`
- Check `knowledge` and `prerequisites: git, npx, pytest, python`

### 2. Reason — think for `refactoring`
- For `refactoring-workflow`: Analyze, refactor, and verify code changes using duplication and dependency tools — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `refactoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `refactoring:147107b3`

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

**Parameters:**
- `min-lines` (integer): Minimum duplicate block length in lines for jscpd
- `circular` (boolean): Report circular dependencies with madge
- `extensions` (string): File extensions madge should analyze, e.g. ts,tsx,js

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

## References
- [Martin Fowler Refactoring](https://martinfowler.com/refactoring/)
- [Working Effectively with Legacy Code summary](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
