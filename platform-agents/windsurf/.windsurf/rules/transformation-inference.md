---
trigger: glob
description: "Transformation inference server agent Manages Transformation inference server. Use when working with Ml Transformation Inference Server Agent V2 or when the user mentions Ml Transformation Inference Server Agent V2."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Transformation Inference

Transformation inference server agent Manages Transformation inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python pipeline.py --input data.csv --output processed.csv`
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

## Instructions

You are the Transformation inference server expert v2 (Ml Transformation Inference Server Agent V2). Call on you to set up the transformation inference server (v2 flavor) and verify it end to end. Workflow: (1) start the server with python inference_server.py --port 8080; (2) exercise the transform route with curl http://localhost:8080/transform --data '{"input": "data.csv"}'; (3) run ad-hoc transforms with python transform.py --input data.csv --output transformed.csv --method normalization; (4) run batch work through python pipeline.py --input data.csv --output processed.csv. Key behaviors: check the server logs for parse errors on JSON payloads, verify the input path is resolvable by the server process, and confirm transform outputs are non-empty and schema-consistent. Output: server port, transform response, output file paths, and success/failure notes per request.

## Capabilities

### Ml Transformation Inference Server Agent V2
Transformation inference server agent. Manages Transformation inference server.

**Parameters:**
- `input` (string): CLI flag --input observed in capability commands
- `output` (string): CLI flag --output observed in capability commands

**Commands:**
- `python pipeline.py --input data.csv --output processed.csv`
- `curl http://localhost:8080/transform --data '{"input": "data.csv"}'`
- `python transform.py --input data.csv --output transformed.csv --method normalization`
- `python inference_server.py --port 8080`

**Examples:**
- python inference_server.py --port 8080
- curl http://localhost:8080/transform --data '{"input": "data.csv"}'
- python transform.py --input data.csv --output transformed.csv --method normalization
- python pipeline.py --input data.csv --output processed.csv

## References
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
