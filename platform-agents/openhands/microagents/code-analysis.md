---
name: "code-analysis"
description: "Performs static and dynamic code analysis: complexity metrics, duplicate detection, profiling, and cross-language analyzers. Use when working with complexity analysis, runtime analysis, code quality or when the user mentions complexity analysis, runtime analysis, code quality."
type: knowledge
triggers: ["code-analysis", "complexity-analysis", "runtime-analysis"]
---

Performs static and dynamic code analysis: complexity metrics, duplicate detection, profiling, and cross-language analyzers.

## Agentic Workflow: Read -> Reason -> Act (code-analysis)

You are **code-analysis** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `code-analysis`
- Domain: Performs static and dynamic code analysis: complexity metrics, duplicate detection, profiling, and cross-language analyzers.
- **complexity-analysis**: Measure code complexity and duplication. — `python -m pip install radon`
- **runtime-analysis**: Profile CPU, memory, and hot paths. — `python -m cProfile -o out.prof app.py`
- Check `knowledge` and `prerequisites: node, pprof, python, radon`

### 2. Reason — think for `code-analysis`
- For `complexity-analysis`: Measure code complexity and duplication. — decide which checks to run
- For `runtime-analysis`: Profile CPU, memory, and hot paths. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `code-analysis` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Radon` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `code-analysis:910cc73c`

# Code Analysis

Analyze code quality and runtime behavior.

## When to Use

- Finding dead code and overly complex modules
- Profiling hot paths before optimization
- Measuring maintainability index in CI
- Comparing refactors with before/after metrics

## Static Analysis

```bash
# Cyclomatic complexity
pip install radon
radon cc src/ -s -a

# Maintainability index
radon mi src/ -s

# Dead code
pip install vulture
vulture src/ --min-confidence 100
```

## Runtime Profiling

```bash
# Python
python -m cProfile -o out.prof app.py
python -m cProfile -s cumtime app.py | head -30

# Node
node --cpu-prof --cpu-prof-dir=./prof app.js
node --heap-prof --heap-prof-dir=./prof app.js

# Go
go test -cpuprofile=cpu.out ./...
pprof -top cpu.out
pprof -web cpu.out
```

## Best Practices

- Set complexity budgets per module and enforce in CI
- Profile with realistic workloads, not synthetic ones
- Check both CPU and heap profiles for leaks
- Measure before/after every refactor
- Focus on the top 5 hot functions, not everything
- Combine with tests to ensure behavior is unchanged

## Capabilities

### complexity-analysis
Measure code complexity and duplication.

**Parameters:**
- `path` (string): Source directory
- `threshold` (integer): Complexity threshold

**Commands:**
- `python -m pip install radon`
- `radon cc src/ -s`
- `radon mi src/ -s`
- `python -m pip install vulture`
- `vulture src/`

**Examples:**
- radon cc src/ -s -a
- radon mi src/ -s -j
- vulture src/ --min-confidence 100

### runtime-analysis
Profile CPU, memory, and hot paths.

**Parameters:**
- `profile-file` (string): Profiler output path
- `method` (string): cpu or heap profiling

**Commands:**
- `python -m cProfile -o out.prof app.py`
- `python -m pstats`
- `node --cpu-prof --cpu-prof-dir=./prof app.js`
- `go test -cpuprofile=cpu.out ./...`
- `pprof -top cpu.out`

**Examples:**
- python -m cProfile -s cumtime app.py | head -30
- node --heap-prof --heap-prof-dir=./prof app.js
- pprof -web cpu.out

## References
- [Radon Docs](https://radon.readthedocs.io)
- [Vulture Docs](https://github.com/jendrikseipp/vulture)
- [pprof Docs](https://github.com/google/pprof)
