Crafts effective LLM prompts: system/user context design, few-shot examples, structured outputs, and iteration with evals.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx promptfoo eval -c promptfooconfig.yaml`, `npx promptfoo eval`
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