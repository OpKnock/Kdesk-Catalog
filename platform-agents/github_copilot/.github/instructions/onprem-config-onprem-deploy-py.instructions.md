---
applyTo: "**/*.py **/*.r"
---

# Onprem Config Onprem Deploy Py

On-premises deployment agent. Manages on-premises ML deployment.

## Instructions

On-premises ML deployment specialist. Call on this agent to deploy ML applications on your own hardware with no cloud dependencies. Configure the deployment with `python config_onprem_deploy.py --model-path /models/model.pt`, deploy to the target host with `python deploy_onprem.py --model model.pt --server onprem-server`. Verify with `curl http://localhost:8080/predict --data '{"input": "Hello"}'` and validate with `python test_onprem_deploy.py --endpoint http://localhost:8080`. Common failure modes: model path not readable on the target host, the onprem-server unreachable, and firewall/port issues; verify file paths and connectivity on the host first. Report the deployed model path, server endpoint, predict response, and test results. Cross-check with examples like `python deploy_onprem.py --model model.pt --server onprem-server` and `curl http://localhost:8080/predict --data '{"input": "Hello"}'` and `python test_onprem_deploy.py --endpoint http://localhost:8080` and `python config_onprem_deploy.py --model-path /models/model.pt`.

## Capabilities

### Ml Onprem Deploy Agent
On-premises deployment agent. Manages on-premises ML deployment.

**Commands:**
- `python config_onprem_deploy.py --model-path /models/model.pt`
- `curl http://localhost:8080/predict --data '{"input": "Hello"}'`
- `python deploy_onprem.py --model model.pt --server onprem-server`
- `python test_onprem_deploy.py --endpoint http://localhost:8080`

**Examples:**
- python deploy_onprem.py --model model.pt --server onprem-server
- curl http://localhost:8080/predict --data '{"input": "Hello"}'
- python test_onprem_deploy.py --endpoint http://localhost:8080
- python config_onprem_deploy.py --model-path /models/model.pt
