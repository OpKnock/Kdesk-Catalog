---
applyTo: "**/*.json **/*.py **/*.r **/*.sh **/*.{yaml,yml}"
---

Builds reproducible ML pipelines: DVC for data/model versioning, MLflow for experiment tracking and serving, and Kubeflow Pipelines for orchestration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `dvc init`, `mlflow run . -P alpha=0.5`
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

# AI/ML Pipeline

## What this skill does

Creates reproducible ML pipelines: DVC versions raw data and model artifacts, MLflow tracks experiments and serves models, and Kubeflow Pipelines orchestrates training end to end.

## When to use

- Reproducing a training run from a git commit
- Tracking hyperparameters/metrics without spreadsheets
- Deploying an ML training workflow to Kubernetes

## Real commands

```bash
# Version training data
dvc init
dvc add data/train.csv
git add data/train.csv.dvc .dvc/config
git commit -m "add training data"

# Reproduce pipeline stages
dvc repro

# Track an experiment
mlflow run . -P alpha=0.5 -P batch_size=64

# Compare metric deltas
dvc metrics diff --sort-by=accuracy

# Serve a model
mlflow models serve -m runs:/<run-id>/model -p 5000
```

## dvc.yaml pipeline

```yaml
stages:
  featurize:
    cmd: python featurize.py
    deps:
      - data/train.csv
    outs:
      - features.pkl
  train:
    cmd: python train.py --params params.yaml
    deps:
      - features.pkl
    metrics:
      - metrics.json
```

## Testing

- Run `dvc repro` on a clean clone to verify reproducibility
- Add a CI job running `dvc metrics diff --branch main` that fails when accuracy drops

## Best practices

- Never commit binaries into git; DVC stores them in remote storage
- Pin Python deps so runs are deterministic
- Log a params snapshot in MLflow for every run
- Set `dvc remote add` to S3/GCS for team sharing

## Capabilities

### data-versioning
Track datasets and model artifacts with DVC so training runs reproduce from any git commit.

**Parameters:**
- `stage` (string): DVC stage file (e.g. train.dvc) to reproduce
- `targets` (string): Space-separated stages for dvc repro

**Commands:**
- `dvc init`
- `dvc add data/train.csv`
- `dvc repro`
- `dvc push`
- `dvc metrics show`

**Examples:**
- dvc add data/train.csv && git add data/train.csv.dvc .dvc/config && git commit -m 'add training data'
- dvc repro train.dvc
- dvc metrics diff --sort-by=accuracy

### experiment-tracking
Log parameters, metrics, and models with MLflow and serve models as REST endpoints.

**Parameters:**
- `experiment` (string): MLflow experiment name or ID
- `run_id` (string): Run ID used to reference a registered model
- `params` (string): Hyperparameters passed with -P key=value

**Commands:**
- `mlflow run . -P alpha=0.5`
- `mlflow experiments create --experiment-name ab-test`
- `mlflow models serve -m runs:/demo-run-id/model -p 5000`
- `mlflow ui --host 0.0.0.0 --port 5000`

**Examples:**
- mlflow run . -P alpha=0.5 -P batch_size=64
- mlflow models serve -m runs:/abc123/model -p 5000
- mlflow experiments list

### pipeline-orchestration
Package and run component pipelines on Kubeflow Pipelines.

**Parameters:**
- `pipeline_file` (string): Path to the compiled pipeline YAML/JSON
- `run_id` (string): Pipeline run identifier for logs

**Commands:**
- `kubectl apply -f pipeline.yaml`
- `kfp pipeline upload`
- `kubectl get pods -n kubeflow -l pipeline-sdk-type=component`
- `kubectl logs -l pipeline-run-id=demo-run-id --all-containers`

**Examples:**
- kfp pipeline upload --name iris-pipeline pipeline.yaml
- kubectl logs -n kubeflow -l pipeline-run-id=run-123 --tail=200
- kubectl get experiments.pipelines.kubeflow.org

## References
- [DVC Documentation](https://dvc.org/doc)
- [MLflow Docs](https://mlflow.org/docs/latest/index.html)
- [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)
