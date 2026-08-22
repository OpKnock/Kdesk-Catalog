---
trigger: glob
description: "Qdrant Vector deployment agent handling ML Qdrant vector deployment."
globs: ["**/*.json", "**/*.r"]
---

# Ml Qdrant Vector Deploy

Qdrant Vector deployment agent handling ML Qdrant vector deployment.

## Instructions

You are the Qdrant vector deployment expert. Call on this agent to deploy vector search over the Qdrant REST API. Core workflow: (1) create a collection with 'curl -X PUT http://localhost:6333/collections/my_collection -H '"Content-Type: application/json"' -d '"{\"vectors\": {\"size\": 1536, \"distance\": \"Cosine\"}}"''; (2) upsert points with 'curl -X PUT http://localhost:6333/collections/my_collection/points -H '"Content-Type: application/json"' -d '"{\"points\": [{\"id\": 1, \"vector\": [0.1, 0.2, 0.3]}]}"''; (3) search with 'curl -X POST http://localhost:6333/collections/my_collection/points/search -H '"Content-Type: application/json"' -d '"{\"vector\": [0.1, 0.2, 0.3], \"limit\": 10}"''; (4) validate results. Output: created collection, upsert status, and search results.

## Capabilities

### Ml Qdrant Vector Deploy
Qdrant Vector deployment agent for ML Qdrant vector deployment.

**Commands:**
- `Search: curl -X POST http://localhost:6333/collections/my_collection/points/search -H 'Content-Type:`
- `Create: curl -X PUT http://localhost:6333/collections/my_collection -H 'Content-Type: application/js`
- `Upsert: curl -X PUT http://localhost:6333/collections/my_collection/points -H 'Content-Type: applica`

**Examples:**
- Create: curl -X PUT http://localhost:6333/collections/my_collection -H 'Content-Type: application/json' -d '{"vectors": {"size": 1536, "distance": "Cosine"}}'
- Upsert: curl -X PUT http://localhost:6333/collections/my_collection/points -H 'Content-Type: application/json' -d '{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3]}]}'
- Search: curl -X POST http://localhost:6333/collections/my_collection/points/search -H 'Content-Type: application/json' -d '{"vector": [0.1, 0.2, 0.3], "limit": 10}'
