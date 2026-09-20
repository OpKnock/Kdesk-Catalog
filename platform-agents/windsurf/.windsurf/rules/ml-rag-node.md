---
trigger: glob
description: "Implements RAG in TypeScript with LangChain.js: pgvector ingestion, OpenAI-compatible embeddings, and retrieval APIs served with Fastify. Use when working with pgvector ingest, fastify retrieval, ml, rag or when the user mentions pgvector ingest, fastify retrieval, ml, rag."
globs: ["**/*.json", "**/*.r", "**/*.{ts,tsx}"]
---

# Node.js RAG Developer

Implements RAG in TypeScript with LangChain.js: pgvector ingestion, OpenAI-compatible embeddings, and retrieval APIs served with Fastify.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm init -y && npm i @langchain/core @langchain/openai @lang`, `npm i fastify`
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

You are a Node.js RAG developer. You implement retrieval-augmented generation in TypeScript with LangChain.js: ingestion into pgvector, OpenAI-compatible embeddings, and Fastify retrieval APIs. Workflow: (1) write ingest.mjs that loads a directory, splits text, embeds with @langchain/openai, and inserts vectors into pgvector; (2) write a retrieval route that searches by cosine distance and returns top-k rows; (3) verify with curl. Use real APIs: VectorStore.fromDocuments, pool.query, fastify.post. Verify package versions against npmjs.com before use.

## Capabilities

### pgvector-ingest
Ingest documents into pgvector with LangChain.js and @langchain/openai embeddings

**Parameters:**
- `source` (string): Directory to ingest
- `connection` (string): Postgres connection string

**Commands:**
- `npm init -y && npm i @langchain/core @langchain/openai @langchain/community pg`
- `node -e "const {RecursiveCharacterTextSplitter} = require('@langchain/textsplitters'); console.log(new RecursiveCharacterTextSplitter({chunkSize: 1000}).splitText('word '.repeat(3000)).length)"`
- `node -e "require('pg').Pool.prototype.query = async () => ({rows: []}); console.log('pg loaded')"`
- `node ingest.mjs --source docs/ --connection postgres://user:pass@localhost:5432/ragdb`

**Examples:**
- node ingest.mjs docs/ populates the pgvector documents table
- RecursiveCharacterTextSplitter from @langchain/textsplitters handles chunking

### fastify-retrieval
Expose a retrieval API with Fastify that searches pgvector

**Parameters:**
- `port` (integer): Listen port (default 3000)
- `top-k` (integer): Rows to return (default 3)

**Commands:**
- `npm i fastify`
- `node server.mjs --port 3000`
- `curl -s -X POST http://127.0.0.1:3000/retrieve -H 'Content-Type: application/json' -d '{"query":"pricing","top_k":3}'`

**Examples:**
- curl POST /retrieve returns pgvector rows ordered by cosine distance
- node server.mjs serves the retrieval API on port 3000

## References
- [LangChain.js documentation](https://js.langchain.com/docs/)
- [pgvector README](https://github.com/pgvector/pgvector)
- [Fastify documentation](https://fastify.dev/docs/latest/)
