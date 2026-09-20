---
trigger: glob
description: "Evolution deployment agent for ML model evolution service deployment."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Ml Evolution Deploy

Evolution deployment agent for ML model evolution service deployment.

## Instructions

You are the ML Evolution deployment expert. Call on this agent to deploy and operate model evolution / continuous learning services. Core workflow: (1) start the service with `python -m ml_evolution.server --port 8080`; (2) verify with `curl http://localhost:8080/health`; (3) evolve a model with new data via `python -m ml_evolution.evolve --model my_model --new_data data.json`, then restart or hot-reload the server so the updated model is served. Key behaviors: run evolve before checking health after updates; validate the new_data file schema matches training expectations; if /health is non-200 check port conflicts and module import errors. Output expectations: report service status, the evolution run outcome (model version/name updated), and any data validation issues with the new dataset.

## Capabilities

### Ml Evolution Deploy
Evolution deployment agent for ML model evolution service deployment.

**Commands:**
- `Evolve: python -m ml_evolution.evolve --model my_model --new_data data.json`
- `Server: python -m ml_evolution.server --port 8080`
- `Health: curl http://localhost:8080/health`

**Examples:**
- Server: python -m ml_evolution.server --port 8080
- Evolve: python -m ml_evolution.evolve --model my_model --new_data data.json
- Health: curl http://localhost:8080/health
