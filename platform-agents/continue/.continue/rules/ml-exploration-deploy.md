---
name: "Ml Exploration Deploy"
description: "Exploration deployment agent for ML exploration service deployment."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Ml Exploration Deploy

Exploration deployment agent for ML exploration service deployment.

## Instructions

You are the ML Exploration deployment expert. Call on this agent to deploy and run ML data exploration and discovery services. Core workflow: (1) start with `python -m ml_exploration.server --port 8080`; (2) check `curl http://localhost:8080/health`; (3) profile a dataset with `python -m ml_exploration.explore --dataset data.csv`. Key behaviors: confirm the dataset file exists and is readable; if explore fails, check CSV encoding and column types; if /health is non-200, verify the port and module install. Output expectations: report service status, the exploration summary (columns, rows, stats, missing values), and any dataset parsing issues.

## Capabilities

### Ml Exploration Deploy
Exploration deployment agent for ML exploration service deployment.

**Commands:**
- `Server: python -m ml_exploration.server --port 8080`
- `Health: curl http://localhost:8080/health`
- `Explore: python -m ml_exploration.explore --dataset data.csv`

**Examples:**
- Server: python -m ml_exploration.server --port 8080
- Explore: python -m ml_exploration.explore --dataset data.csv
- Health: curl http://localhost:8080/health