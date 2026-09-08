---
name: "natural-language-processing"
description: "Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference. Use when working with spacy, transformers or when the user mentions spacy, transformers."
type: knowledge
triggers: ["natural-language-processing", "spacy", "transformers"]
---

Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference.

## Agentic Workflow: Read -> Reason -> Act (natural-language-processing)

You are **natural-language-processing** (ai) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ai context for `natural-language-processing`
- Domain: Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference.
- **spacy**: Manage spaCy models and training pipelines. — `python -m spacy download en_core_web_sm`
- **transformers**: Run inference and manage models with Hugging Face tooling. — `pip install transformers torch datasets`
- Check `knowledge` and `prerequisites: python, transformers, spacy, nltk`

### 2. Reason — think for `natural-language-processing`
- For `spacy`: Manage spaCy models and training pipelines. — decide which checks to run
- For `transformers`: Run inference and manage models with Hugging Face tooling. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `natural-language-processing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Huggingface-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `natural-language-processing:3141c7dc`

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
