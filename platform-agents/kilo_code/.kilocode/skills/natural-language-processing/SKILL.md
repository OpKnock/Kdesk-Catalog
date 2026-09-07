---
name: "natural-language-processing"
description: "Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference. Use when working with spacy, transformers or when the user mentions spacy, transformers."
license: "MIT"
compatibility: "Requires python, transformers, spacy, nltk, openai."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "ai"}
allowed-tools: "Glob Grep Read Bash(huggingface-cli:*) Bash(pip:*) Bash(python:*)"
---

Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m spacy download en_core_web_sm`, `pip install transformers torch datasets`
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

# Natural Language Processing

Build NLP systems with spaCy and Hugging Face.

## When to Use

- Text classification, NER, and summarization
- Fine-tuning language models for domain data
- Extracting structured info from free text

## spaCy quickstart

```bash
python -m spacy download en_core_web_sm
```

```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp('Ada Lovelace wrote the first algorithm.')
for ent in doc.ents:
    print(ent.text, ent.label_)
```

## Training project

```bash
python -m spacy init config config.cfg --lang en --pipeline ner
python -m spacy debug data config.cfg
python -m spacy train config.cfg --output training/
```

## Transformers pipelines

```bash
python -c "from transformers import pipeline; nlp = pipeline('sentiment-analysis'); print(nlp('This is great!'))"
```

## Model management

```bash
huggingface-cli login
huggingface-cli download gpt2
```

## Best practices

- Pin model versions for reproducibility.
- Validate training data before training (spacy debug data).
- Use a small model for smoke tests, large for production.
- Monitor drift on predictions with a golden set.

## Testing

```bash
python -m spacy evaluate config.cfg training/model-best
```

Maintain a fixed eval set per release.

## Capabilities

### spacy
Manage spaCy models and training pipelines.

**Parameters:**
- `model` (string): spaCy model name
- `config` (string): Training config.cfg path
- `pipeline` (string): Components: ner, textcat, parser

**Commands:**
- `python -m spacy download en_core_web_sm`
- `python -m spacy project run all`
- `python -m spacy debug data config.cfg`
- `python -m spacy debug train config.cfg`
- `python -m spacy init config config.cfg --lang en --pipeline ner`

**Examples:**
- python -m spacy download en_core_web_lg
- python -m spacy project assets
- python -m spacy evaluate config.cfg models/best

### transformers
Run inference and manage models with Hugging Face tooling.

**Parameters:**
- `model` (string): Hugging Face model id
- `task` (string): Pipeline task: sentiment-analysis, ner, text-generation
- `repo-type` (string): model, dataset, or space

**Commands:**
- `pip install transformers torch datasets`
- `huggingface-cli login`
- `huggingface-cli download gpt2 --repo-type model`
- `python -c "from transformers import pipeline; nlp = pipeline('sentiment-analysis'); print(nlp('This is great!'))"`
- `python -c "from transformers import AutoTokenizer, AutoModel; t = AutoTokenizer.from_pretrained('bert-base-uncased'); print(t.tokenize('hello world'))"`

**Examples:**
- huggingface-cli download meta-llama/Llama-3.1-8B-Instruct --include '*.safetensors'
- python -c "from transformers import pipeline; nlp = pipeline('ner'); print(nlp('Ada works at OpenAI in San Francisco'))"
- huggingface-cli whoami

## References
- [spaCy CLI](https://spacy.io/api/cli)
- [Hugging Face Hub CLI](https://huggingface.co/docs/huggingface_hub/guides/cli)
- [Transformers](https://huggingface.co/docs/transformers/index)
