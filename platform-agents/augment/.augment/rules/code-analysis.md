---
type: agent_requested
description: "Performs static and dynamic code analysis: complexity metrics, duplicate detection, profiling, and cross-language analyzers. Use when working with complexity analysis, runtime analysis, code quality or when the user mentions complexity analysis, runtime analysis, code quality."
---

Performs static and dynamic code analysis: complexity metrics, duplicate detection, profiling, and cross-language analyzers.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m pip install radon`, `python -m cProfile -o out.prof app.py`
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