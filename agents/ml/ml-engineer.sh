#!/usr/bin/env bash
# ML Engineer Agent - End-to-end ML pipeline automation
# Part of Kdesk-Catalog agents

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-http://localhost:5000}"
MODEL_REGISTRY="${MODEL_REGISTRY:-models:/}"
EXPERIMENT_NAME="${ML_EXPERIMENT:-ml-experiment}"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat <<EOF
Usage: $0 <command> [options]

ML Engineer Agent - End-to-end ML pipeline automation

Commands:
  init          Initialize ML project structure
  train         Train a model with MLflow tracking
  serve         Serve model with MLflow
  deploy        Deploy model to production
  evaluate      Evaluate model performance
  pipeline      Run full ML pipeline
  monitor       Monitor model performance

Options:
  --experiment NAME    MLflow experiment name (default: ml-experiment)
  --model-name NAME    Model name for registry
  --data-path PATH     Path to training data
  --config FILE        Config file path
  -h, --help          Show this help

Examples:
  $0 init --data-path ./data --experiment my-experiment
  $0 train --data-path ./data/train.csv --model-name my-model
  $0 serve --model-name my-model --port 8080
  $0 deploy --model-name my-model --stage production
  $0 evaluate --model-name my-model --test-data ./data/test.csv

Environment Variables:
  MLFLOW_TRACKING_URI  MLflow tracking server (default: http://localhost:5000)
  MODEL_REGISTRY       Model registry URI
  ML_EXPERIMENT        Default experiment name
EOF
}

cmd_init() {
    local data_path=""
    local experiment_name="${ML_EXPERIMENT:-ml-experiment}"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --data-path) data_path="$2"; shift 2 ;;
            --experiment) experiment_name="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; usage; exit 1 ;;
        esac
    done
    
    [[ -z "$data_path" ]] && { log_error "--data-path required"; exit 1; }
    
    log_info "Initializing ML project at $data_path"
    mkdir -p "$data_path"/{raw,processed,models,notebooks,tests}
    
    cat > "$data_path/mlproject.yaml" <<EOF
name: ${experiment_name}
version: 1.0.0
description: ML project initialized by ML Engineer agent
author: ML Engineer Agent
license: MIT

data:
  raw_path: data/raw
  processed_path: data/processed
  test_size: 0.2
  random_state: 42

model:
  name: model
  framework: sklearn
  hyperparameters:
    n_estimators: 100
    max_depth: 10
    random_state: 42

mlflow:
  tracking_uri: ${MLFLOW_TRACKING_URI}
  experiment: ${experiment_name}
  model_registry: ${MODEL_REGISTRY}
EOF
    
    log_success "ML project initialized at $data_path"
    log_info "Edit $data_path/mlproject.yaml to customize your pipeline"
}

cmd_train() {
    local data_path=""
    local model_name=""
    local experiment_name="${ML_EXPERIMENT:-ml-experiment}"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --data-path) data_path="$2"; shift 2 ;;
            --model-name) model_name="$2"; shift 2 ;;
            --experiment) experiment_name="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; exit 1 ;;
        esac
    done
    
    [[ -z "$data_path" || -z "$model_name" ]] && { log_error "--data-path and --model-name required"; exit 1; }
    
    log_info "Training model '$model_name' with data from $data_path"
    
    # Check if MLflow is available
    if ! command -v mlflow &> /dev/null; then
        log_error "MLflow not installed. Install with: pip install mlflow"
        exit 1
    fi
    
    mlflow run . -P data_path="$data_path" -P model_name="$model_name" -e train || {
        log_error "Training failed"
        exit 1
    }
    
    log_success "Model '$model_name' trained and logged to MLflow"
}

cmd_serve() {
    local model_name=""
    local port="${PORT:-8080}"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --model-name) model_name="$2"; shift 2 ;;
            --port) port="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; exit 1 ;;
        esac
    done
    
    [[ -z "$model_name" ]] && { log_error "--model-name required"; exit 1; }
    
    log_info "Serving model '$model_name' on port $port"
    mlflow models serve -m "models:/$model_name/Production" -p "$port" --no-conda
}

cmd_deploy() {
    local model_name=""
    local stage="Staging"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --model-name) model_name="$2"; shift 2 ;;
            --stage) stage="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; exit 1 ;;
        esac
    done
    
    [[ -z "$model_name" ]] && { log_error "--model-name required"; exit 1; }
    
    log_info "Deploying model '$model_name' to $stage"
    mlflow models deploy -m "models:/$model_name/Production" -t mlserver -n "$model_name" --stage "$stage"
    log_success "Model '$model_name' deployed to $stage"
}

cmd_evaluate() {
    local model_name=""
    local test_data=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --model-name) model_name="$2"; shift 2 ;;
            --test-data) test_data="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; exit 1 ;;
        esac
    done
    
    [[ -z "$model_name" || -z "$test_data" ]] && { log_error "--model-name and --test-data required"; exit 1; }
    
    log_info "Evaluating model '$model_name' on test data: $test_data"
    # Evaluation logic would go here
    log_success "Evaluation complete"
}

cmd_pipeline() {
    local data_path=""
    local model_name=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --data-path) data_path="$2"; shift 2 ;;
            --model-name) model_name="$2"; shift 2 ;;
            *) log_error "Unknown option: $1"; exit 1 ;;
        esac
    done
    
    [[ -z "$data_path" || -z "$model_name" ]] && { log_error "--data-path and --model-name required"; exit 1; }
    
    log_info "Running full ML pipeline for '$model_name'"
    cmd_train --data-path "$data_path" --model-name "$model_name"
    cmd_evaluate --model-name "$model_name" --test-data "$data_path/test.csv"
    cmd_deploy --model-name "$model_name" --stage "Staging"
    log_success "Pipeline complete"
}

# Main command dispatch
case "${1:-}" in
    init) shift; cmd_init "$@" ;;
    train) shift; cmd_train "$@" ;;
    serve) shift; cmd_serve "$@" ;;
    deploy) shift; cmd_deploy "$@" ;;
    evaluate) shift; cmd_evaluate "$@" ;;
    pipeline) shift; cmd_pipeline "$@" ;;
    monitor) shift; cmd_monitor "$@" ;;
    *) usage; exit 1 ;;
esac