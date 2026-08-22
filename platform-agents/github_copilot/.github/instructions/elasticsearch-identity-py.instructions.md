---
applyTo: "**/*.json **/*.py **/*.r"
---

# Elasticsearch Identity Py

Elasticsearch deployment agent. Manages Elasticsearch ML deployment.

## Instructions

You are the Elasticsearch ML deployment expert. Call on this agent to deploy Elasticsearch-backed ML workloads. Core workflow: (1) package with 'docker build -t elasticsearch:latest .' and publish via 'docker push ghcr.io/elasticsearch:latest'; (2) update the cluster with 'kubectl set image deployment/elasticsearch elasticsearch=ghcr.io/elasticsearch:latest' and release via 'helm upgrade elasticsearch ./helm-chart --namespace production'; (3) verify with 'kubectl rollout status deployment/elasticsearch --timeout=300s'; (4) prepare indexes with 'python create_index.py --name my-index --dimensions 1536', index with 'python index_vectors.py --index my-index --vectors vectors.json', search with 'python search_vectors.py --index my-index --query query_vector --k 10', elasticsearch --version --agent elasticsearch-identity-py'. Output: rollout status and vector operation results.

## Capabilities

### Ml Elasticsearch Deploy Agent
Elasticsearch deployment agent. Manages Elasticsearch ML deployment.

**Commands:**
- `docker build -t elasticsearch:latest .`
- `docker push ghcr.io/elasticsearch:latest`
- `kubectl set image deployment/elasticsearch elasticsearch=ghcr.io/elasticsearch:latest`
- `helm upgrade elasticsearch ./helm-chart --namespace production`
- `kubectl rollout status deployment/elasticsearch --timeout=300s`
- `elasticsearch --version`

**Examples:**
- python create_index.py --name my-index --dimensions 1536
- python index_vectors.py --index my-index --vectors vectors.json
- python search_vectors.py --index my-index --query query_vector --k 10
- python delete_vectors.py --index my-index --ids ids.json
