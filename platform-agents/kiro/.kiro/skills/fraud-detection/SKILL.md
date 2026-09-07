---
name: "fraud-detection"
description: "Builds fraud detection pipelines with pandas, scikit-learn, and MLflow: feature engineering, model training, evaluation, and experiment tracking. Use when working with data pipeline, mlflow or when the user mentions data pipeline, mlflow."
license: "MIT"
compatibility: "Requires python, scikit-learn, tensorflow, kafka, redis."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(jupyter:*) Bash(mlflow:*) Bash(pip:*) Bash(python:*)"
---

Builds fraud detection pipelines with pandas, scikit-learn, and MLflow: feature engineering, model training, evaluation, and experiment tracking.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m venv .venv && .venv/Scripts/activate`, `mlflow run . -e train --env-manager local`
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

# Fraud Detection

Build, evaluate, and serve fraud models with reproducible data pipelines.

## When to Use

- Detecting transaction fraud in real-time or batch
- Feature engineering on customer/device/velocity signals
- Comparing model versions before production rollout

## Setup

```bash
python -m venv .venv
pip install pandas scikit-learn imbalanced-learn mlflow pytest
```

## Data inspection

```bash
python -c "import pandas as pd; df=pd.read_csv('transactions.csv'); print(df['is_fraud'].value_counts(normalize=True))"
```

Fraud is rare (often < 1%). Class imbalance will dominate model behavior - always report precision/recall, not accuracy.

## Feature engineering

Compute velocity features (count and sum of transactions per card in the last 1h/24h), device fingerprints, and normalized amounts. Test features first:

```bash
python -m pytest tests/test_features.py -v
```

## Training

Train with class weighting or SMOTE, then log to MLflow:

```bash
mlflow experiments create --experiment-name fraud-v3
mlflow run . -e train -P max_depth=7 -P scale_pos_weight=10
```

## Evaluation

Track ROC AUC, precision at 0.1% FPR, and cost-weighted loss. Pick thresholds by business cost matrix, not the default 0.5.

## Serving

```bash
mlflow models serve -m models:/fraud-detector/Production -p 5001
```

## Best practices

- Keep train/test split temporal - never shuffle across time.
- Monitor drift on score distribution and feature means daily.
- Review false positives weekly with the risk team and relabel.
- Shadow-deploy new models for two weeks before promotion.

## Testing

```bash
python -m pytest tests/ -v
```

Include golden-path unit tests for each engineered feature.

## Capabilities

### data-pipeline
Prepare and inspect transaction datasets with Python data tooling.

**Parameters:**
- `dataset` (string): Path to transactions CSV
- `test-path` (string): pytest path filter
- `notebook` (string): Notebook path to export

**Commands:**
- `python -m venv .venv && .venv/Scripts/activate`
- `pip install pandas scikit-learn imbalanced-learn mlflow pytest`
- `python -c "import pandas as pd; df=pd.read_csv('transactions.csv'); print(df.isna().sum()); print(df['is_fraud'].value_counts(normalize=True))"`
- `python -m pytest tests/ -k fraud -v`
- `jupyter nbconvert --to script notebooks/eda.ipynb --output eda`

**Examples:**
- python -c "import pandas as pd; df=pd.read_csv('tx.csv'); print(df.describe())"
- python -c "import pandas as pd; df=pd.read_csv('tx.csv'); print(df.groupby('channel')['amount'].sum())"
- python -m pytest tests/test_features.py -v

### mlflow
Track experiments, log models, and compare fraud detection runs.

**Parameters:**
- `experiment-name` (string): MLflow experiment name
- `model-uri` (string): Registered model URI like models:/fraud-detector/Production
- `max_depth` (number): Tree depth hyperparameter for training run

**Commands:**
- `mlflow run . -e train --env-manager local`
- `mlflow experiments create --experiment-name fraud-v3`
- `mlflow runs list --experiment-id 42`
- `mlflow models serve -m models:/fraud-detector/Production -p 5001`
- `mlflow ui --host 0.0.0.0 --port 5000`

**Examples:**
- mlflow run . -e train -P max_depth=7 -P scale_pos_weight=10
- mlflow models serve -m models:/fraud-detector/Production -p 5001
- mlflow runs list --experiment-id 42 --order-by 'metrics.auc desc'

## References
- [scikit-learn](https://scikit-learn.org/stable/)
- [imbalanced-learn](https://imbalanced-learn.org/stable/)
- [MLflow Docs](https://mlflow.org/docs/latest/)
