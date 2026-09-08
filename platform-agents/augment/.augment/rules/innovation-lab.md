---
type: agent_requested
description: "Runs rapid prototyping experiments: quick scaffolds, local servers, and disposable environments to validate ideas fast. Use when working with prototype, experiment or when the user mentions prototype, experiment."
---

Runs rapid prototyping experiments: quick scaffolds, local servers, and disposable environments to validate ideas fast.

## Agentic Workflow: Read -> Reason -> Act (innovation-lab)

You are **innovation-lab** (strategy) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — strategy context for `innovation-lab`
- Domain: Runs rapid prototyping experiments: quick scaffolds, local servers, and disposable environments to validate ideas fast.
- **prototype**: Spin up throwaway prototypes in minutes. — `npm create vite@latest idea -- --template react-ts`
- **experiment**: Track experiments and measure results. — `jupyter lab --port 8888 --no-browser`
- Check `knowledge` and `prerequisites: figma, notion, slack, github`

### 2. Reason — think for `innovation-lab`
- For `prototype`: Spin up throwaway prototypes in minutes. — decide which checks to run
- For `experiment`: Track experiments and measure results. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `innovation-lab` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Jupyter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `innovation-lab:35bc3ec1`

# Innovation Lab

Validate ideas with the cheapest possible experiment.

## When to Use

- Evaluating a new framework, library, or pattern
- Building a demo for stakeholders
- Testing a hypothesis with data

## Fast scaffolds

```bash
npm create vite@latest idea -- --template react-ts
python -m http.server 8000
```

Match the scaffold to the question: static HTML for copy, Vite for UI interaction, FastAPI for API behavior.

## Disposable dependencies

```bash
docker compose up -d redis postgres
```

Use containers for deps so teardown is `docker compose down -v`.

## Data experiments

```bash
jupyter lab --port 8888 --no-browser
jupyter nbconvert --to notebook --execute experiment.ipynb --output executed.ipynb
```

Executed notebooks are the experiment record.

## Keep a history

```bash
git tag experiment/2026-08-cache-vs-nocache
git log --oneline --graph -15
```

## Rules for prototypes

- Timebox: one day max; the goal is a decision, not production code.
- Document the decision: what changed your mind?
- Kill or promote: delete the spike or re-build properly.
- Never let a prototype accumulate production load.

## Testing

```bash
python -m pytest tests/ -q
npm run build
```

Even a spike should compile and pass its unit checks before the review.

## Capabilities

### prototype
Spin up throwaway prototypes in minutes.

**Parameters:**
- `port` (number): Local server port
- `directory` (string): Directory to serve
- `template` (string): Scaffold template

**Commands:**
- `npm create vite@latest idea -- --template react-ts`
- `python -m http.server 8000`
- `python -m venv .venv && .venv/Scripts/pip install fastapi uvicorn`
- `docker compose up -d redis`
- `npm create astro@latest -- --template minimal`

**Examples:**
- python -m http.server 8000 --directory public
- npm create vite@latest idea -- --template vanilla-ts
- docker compose up -d postgres redis

### experiment
Track experiments and measure results.

**Parameters:**
- `notebook` (string): Jupyter notebook path
- `tag` (string): Git tag for the experiment
- `execute` (string): Execute notebooks headlessly

**Commands:**
- `jupyter lab --port 8888 --no-browser`
- `jupyter nbconvert --to notebook --execute experiment.ipynb --output executed.ipynb`
- `git tag experiment/2026-08-cache-vs-nocache`
- `git log --oneline --graph -15`
- `pip install pytest && python -m pytest tests/ -q`

**Examples:**
- jupyter nbconvert --to script --output exp experiment.ipynb
- git tag -a experiment/v1 -m 'cache-vs-nocache baseline'
- python -m pytest tests/ -q --tb=short

## References
- [Vite](https://vite.dev/guide/)
- [Jupyter](https://jupyter.org/documentation)
- [FastAPI](https://fastapi.tiangolo.com/)