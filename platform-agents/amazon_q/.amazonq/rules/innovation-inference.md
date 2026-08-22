# Innovation Inference

Innovation inference server agent Manages Innovation inference server.

## Instructions

Innovation inference server operator (v2). Call on this agent to serve innovation prototypes as a hosted inference endpoint. Launch with `python inference_server.py --port 8080`, then request an idea generation with `curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'`. Backfill context with `python research.py --topic 'transformer architectures' --output research.json` and `python prototype.py --idea 'new attention mechanism' --output prototype.py`. Common failure modes: port 8080 already bound, missing research artifacts, and payload schema mismatch; check the port and artifact files before restarting. Report the innovate response, research/prototype artifact paths, and server status. Cross-check with examples like `python inference_server.py --port 8080` and `curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'` and `python research.py --topic 'transformer architectures' --output research.json` and `python prototype.py --idea 'new attention mechanism' --output prototype.py`.

## Capabilities

### Ml Innovation Inference Server Agent V2
Innovation inference server agent. Manages Innovation inference server.

**Commands:**
- `python prototype.py --idea 'new attention mechanism' --output prototype.py`
- `python research.py --topic 'transformer architectures' --output research.json`
- `curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'`
- `python inference_server.py --port 8080`

**Examples:**
- python inference_server.py --port 8080
- curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'
- python research.py --topic 'transformer architectures' --output research.json
- python prototype.py --idea 'new attention mechanism' --output prototype.py