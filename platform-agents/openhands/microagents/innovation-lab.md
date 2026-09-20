---
name: "innovation-lab"
description: "Runs rapid prototyping experiments: quick scaffolds, local servers, and disposable environments to validate ideas fast."
type: knowledge
triggers: ["innovation-lab", "prototype", "experiment"]
---

# innovation-lab

Runs rapid prototyping experiments: quick scaffolds, local servers, and disposable environments to validate ideas fast.

## Instructions

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
