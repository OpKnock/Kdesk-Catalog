---
name: "natural-language-processing"
description: "Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference."
---

# natural-language-processing

Builds NLP pipelines with spaCy and Hugging Face: model downloads, training configs, and transformers inference.

## Instructions

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
