---
type: agent_requested
description: "Crafts effective LLM prompts: system/user context design, few-shot examples, structured outputs, and iteration with evals. Use when working with prompt design, prompt eval, backend or when the user mentions prompt design, prompt eval, backend."
---

Crafts effective LLM prompts: system/user context design, few-shot examples, structured outputs, and iteration with evals.

## Agentic Workflow: Read -> Reason -> Act (prompt-engineering)

You are **Prompt Engineering** (backend/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `prompt-engineering`
- Domain: Crafts effective LLM prompts: system/user context design, few-shot examples, structured outputs, and iteration with evals.
- **prompt-design**: Structure system prompts and few-shot examples. — `npx promptfoo eval -c promptfooconfig.yaml`
- **prompt-eval**: Evaluate prompt variants with automated test cases. — `npx promptfoo eval`
- Check `knowledge` and `prerequisites: npx, python`

### 2. Reason — think for `prompt-engineering`
- For `prompt-design`: Structure system prompts and few-shot examples. — decide which checks to run
- For `prompt-eval`: Evaluate prompt variants with automated test cases. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `prompt-engineering` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `prompt-engineering:fc3a0a09`

# Prompt Engineering

Design and iterate on LLM prompts systematically.

## When to Use

- Building any feature where model output quality matters
- Diagnosing inconsistent or off-format model responses
- Comparing prompt variants or model versions
- Reducing cost by cutting redundant context

## Structure

- System: role, constraints, and behavior for the whole session
- Context: facts the model needs (docs, schema, examples)
- Task: clear instruction with the expected output shape
- Few-shot: 2-3 concrete examples of input/output pairs
- Guardrails: what to do when input is out of scope

## Commands

```bash
# Eval setup
npx promptfoo init
npx promptfoo eval -c promptfooconfig.yaml
npx promptfoo view

# Quick probe of a model
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Name 3 colors"}],"temperature":0}'
```

## Prompt Example

```
System: You extract structured fields from invoices. Reply with JSON only.
User: Invoice #1042, dated 2026-01-15, total $129.99, vendor "Acme Corp"
Assistant: {"number":"1042","date":"2026-01-15","total":129.99,"vendor":"Acme Corp"}
```

## Best Practices

- Always test with real negative examples, not just happy paths
- Keep instructions specific; vague prompts produce vague output
- Use temperature 0 for extraction, higher only for creative tasks
- Require structured output (JSON schema) for machine consumption
- Track prompt versions and eval scores in the repo
- Trim context ruthlessly; token cost scales with input length

## Capabilities

### prompt-design
Structure system prompts and few-shot examples.

**Parameters:**
- `temperature` (number): Sampling temperature
- `format` (string): json_object or json_schema output

**Commands:**
- `npx promptfoo eval -c promptfooconfig.yaml`
- `npx promptfoo run -c promptfooconfig.yaml`
- `python -c "from openai import OpenAI; c=OpenAI(); r=c.chat.completions.create(model=\"gpt-4o-mini\", messages=[{\"role\":\"system\",\"content\":\"You are a terse assistant\"},{\"role\":\"user\",\"content\":\"Hi\"}]); print(r.choices[0].message.content)"`

**Examples:**
- npx promptfoo init
- npx promptfoo eval --no-cache
- curl -s https://api.openai.com/v1/chat/completions -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" -d "{\"model\":\"gpt-4o-mini\",\"messages\":[{\"role\":\"user\",\"content\":\"Name 3 colors\"}],\"temperature\":0}"

### prompt-eval
Evaluate prompt variants with automated test cases.

**Parameters:**
- `config` (string): Eval config path
- `port` (integer): Viewer port

**Commands:**
- `npx promptfoo eval`
- `npx promptfoo view`
- `npx promptfoo share`
- `python -m venv .venv && .venv/bin/pip install openai`

**Examples:**
- npx promptfoo eval -c eval.yaml --max-concurrency 8
- npx promptfoo view --port 3000

## References
- [OpenAI Prompt Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Promptfoo Docs](https://www.promptfoo.dev/docs/)