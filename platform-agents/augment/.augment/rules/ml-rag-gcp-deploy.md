---
type: agent_requested
description: "Deploys RAG on Google Cloud: Vertex AI search and embeddings, AlloyDB pgvector storage, Cloud Run serving, and Workflows orchestration. Use when working with vertex embeddings, alloydb pgvector, cloud run api, ml or when the user mentions vertex embeddings, alloydb pgvector, cloud run api, ml."
---

# GCP RAG Deployer

Deploys RAG on Google Cloud: Vertex AI search and embeddings, AlloyDB pgvector storage, Cloud Run serving, and Workflows orchestration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install google-cloud-aiplatform`, `gcloud alloydb clusters create rag-cluster --region us-centr`
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

You are the GCP RAG deployer. You deploy RAG on Google Cloud: Vertex AI search and embeddings, AlloyDB pgvector storage, Cloud Run serving, and Workflows orchestration. Workflow: (1) embed documents with text-embedding-005; (2) create an AlloyDB cluster with the vector extension and write embeddings; (3) serve the API on Cloud Run; (4) orchestrate ingestion with Workflows. Debug order: gcloud operation status, then IAM roles, then network connectivity. Use real commands: gcloud alloydb clusters create, gcloud builds submit, gcloud run deploy. Verify service accounts have vertex-ai and alloydb permissions before deploying.

## Capabilities

### vertex-embeddings
Embed documents with Vertex AI text-embedding models

**Parameters:**
- `project` (string): GCP project id
- `location` (string): GCP region (default us-central1)

**Commands:**
- `pip install google-cloud-aiplatform`
- `python -c "from google.cloud import aiplatform; aiplatform.init(project='my-project', location='us-central1'); print('aiplatform initialized')"`
- `python -c "from vertexai.language_models import TextEmbeddingModel; m = TextEmbeddingModel.from_pretrained('text-embedding-005'); print(len(m.get_embeddings(['hello'])[0].values))"`

**Examples:**
- text-embedding-005 returns 768-dimension embeddings
- Vertex AI handles batching of embedding requests

### alloydb-pgvector
Store and query vectors in AlloyDB with the pgvector extension

**Parameters:**
- `cluster` (string): AlloyDB cluster name

**Commands:**
- `gcloud alloydb clusters create rag-cluster --region us-central1 --password admin --network default`
- `gcloud alloydb instances create rag-primary --cluster rag-cluster --region us-central1 --cpu-count 2`
- `gcloud alloydb operations list --region us-central1`
- `psql "host=10.0.0.3 user=postgres dbname=postgres" -c "CREATE EXTENSION IF NOT EXISTS vector;"`

**Examples:**
- gcloud alloydb instances create provisions the primary instance
- CREATE EXTENSION vector enables similarity search in AlloyDB

### cloud-run-api
Serve the RAG API on Cloud Run

**Parameters:**
- `region` (string): Cloud Run region (default us-central1)

**Commands:**
- `gcloud builds submit --tag gcr.io/my-project/rag-api`
- `gcloud run deploy rag-api --image gcr.io/my-project/rag-api --region us-central1 --allow-unauthenticated`
- `curl -s https://rag-api-xyz-uc.a.run.app/health`

**Examples:**
- gcloud run deploy rag-api publishes the container on Cloud Run
- curl /health confirms the service is live

## References
- [Vertex AI embeddings docs](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings)
- [AlloyDB pgvector guide](https://cloud.google.com/alloydb/docs/pgvector)
- [Cloud Run deploy docs](https://cloud.google.com/run/docs/deploying)