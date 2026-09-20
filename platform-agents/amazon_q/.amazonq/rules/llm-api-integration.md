Integrates LLM APIs (OpenAI, Anthropic, local models) into applications: streaming, tool calling, retries, cost control, and evaluation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl https://api.openai.com/v1/chat/completions -H "Authoriz`, `pip install promptfoo`
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

# LLM API Integration

Connect applications to LLM providers reliably.

## When to Use

- Chat, summarization, extraction, and classification features
- Tool/function calling to ground models in your systems
- Local models via Ollama for privacy or offline needs
- Evaluation-driven prompt development

## Commands

```bash
# OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Hello"}]}'

# Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"claude-3-5-haiku","max_tokens":100,"messages":[{"role":"user","content":"hi"}]}'

# Local with Ollama
ollama pull llama3.2
ollama run llama3.2 "summarize this"

# Evals
npx promptfoo eval -c promptfooconfig.yaml
npx promptfoo view
```

## Python Example

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## Best Practices

- Always set timeouts and retry on 429/5xx with exponential backoff
- Stream responses instead of waiting for full completion
- Validate and cap max_tokens to control cost
- Store keys in environment variables, never in code or repos
- Evaluate prompts with promptfoo before promoting them
- Log prompt and response pairs for debugging, with PII scrubbed

## Capabilities

### llm-clients
Call LLM providers with the official CLIs and SDKs.

**Parameters:**
- `model` (string): Model identifier
- `temperature` (number): Sampling temperature
- `max-tokens` (integer): Output token limit

**Commands:**
- `curl https://api.openai.com/v1/chat/completions -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" -d "{\"model\":\"gpt-4o-mini\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}"`
- `pip install openai anthropic`
- `npm install openai @anthropic-ai/sdk`
- `ollama run llama3.2`
- `ollama list`

**Examples:**
- ollama run qwen2.5:7b "summarize this"
- curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -d "{\"model\":\"claude-3-5-haiku\",\"max_tokens\":100,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}"
- python -m venv .venv

### llm-ops
Manage prompts, evals, and cost guardrails.

**Parameters:**
- `config` (string): Eval config path
- `provider` (string): openai, anthropic, or ollama

**Commands:**
- `pip install promptfoo`
- `npx promptfoo eval`
- `npx promptfoo eval -c promptfooconfig.yaml --share`
- `openai api keys`
- `python -c "from openai import OpenAI; print(len(OpenAI().models.list().data))"`

**Examples:**
- npx promptfoo init
- npx promptfoo eval -c promptfooconfig.yaml
- ollama pull mistral

## References
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic API Docs](https://docs.anthropic.com/en/docs)
- [Ollama Docs](https://ollama.com/library)