---
trigger: glob
description: "Innovation inference agent. Manages ML innovation inference."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

# Ml Innovation Inference Agent

Innovation inference agent. Manages ML innovation inference.

## Instructions

ML innovation research operator. Call on this agent to turn research topics into working prototypes. Run literature-style research with `python research.py --topic 'transformer architectures' --output research.json`, then generate a prototype from an idea with `python prototype.py --idea 'new attention mechanism' --output prototype.py`. Serve the result with `python serve_innovation.py --port 8080` and validate with `python test_innovation.py`. Common failure modes: topic strings unquoted (shell splitting), missing research.json blocking prototype generation, and prototype code that does not compile; quote inputs and run tests before serving. Report the research findings path, generated prototype path, and test results. Cross-check with examples like `python research.py --topic 'transformer architectures' --output research.json` and `python prototype.py --idea 'new attention mechanism' --output prototype.py` and `python serve_innovation.py --port 8080` and `python test_innovation.py`.

## Capabilities

### Ml Innovation Inference Agent
Innovation inference agent. Manages ML innovation inference.

**Commands:**
- `python prototype.py --idea 'new attention mechanism' --output prototype.py`
- `python test_innovation.py`
- `python serve_innovation.py --port 8080`
- `python research.py --topic 'transformer architectures' --output research.json`

**Examples:**
- python research.py --topic 'transformer architectures' --output research.json
- python prototype.py --idea 'new attention mechanism' --output prototype.py
- python serve_innovation.py --port 8080
- python test_innovation.py
