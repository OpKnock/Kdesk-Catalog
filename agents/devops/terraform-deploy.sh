#!/usr/bin/env bash
# Terraform Deployment Agent - Infrastructure deployment with Terraform
# Part of Kdesk-Catalog agents

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat <<EOF
Usage: $0 <command> [options]

Terraform Deployment Agent - Infrastructure deployment with Terraform

Commands:
  init          Initialize Terraform working directory
  plan          Generate execution plan
  apply         Apply Terraform plan
  destroy       Destroy infrastructure
  validate      Validate Terraform configuration
  fmt           Format Terraform files
  validate      Validate Terraform configuration
  output        Show Terraform outputs
  workspace     Manage workspaces
  import        Import existing resources
  state         Manage Terraform state

Options:
  -d, --dir PATH        Terraform directory (default: .)
  -w, --workspace NAME  Workspace name (default: default)
  -v, --var KEY=VALUE   Set variable (can be repeated)
  -f, --var-file FILE   Variable file
  -a, --auto-approve    Auto approve (skip confirmation)
  -h, --help            Show this help

Examples:
  $0 init --dir ./infra
  $0 plan --dir ./infra --var environment=prod
  $0 apply --dir ./infra --auto-approve
  $0 destroy --dir ./infra --auto-approve
  $0 workspace select prod

Environment Variables:
  TF_VAR_*              Terraform variables
  TF_WORKSPACE          Default workspace
  TF_DATA_DIR           Terraform data directory
EOF
}

# Parse global options
TERRAFORM_DIR="."
WORKSPACE="default"
AUTO_APPROVE=false
VAR_FILES=()
VARS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir) TERRAFORM_DIR="$2"; shift 2 ;;
        -w|--workspace) WORKSPACE="$2"; shift 2 ;;
        -v|--var) VARS+=("$2"); shift 2 ;;
        -f|--var-file) VAR_FILES+=("$2"); shift 2 ;;
        -a|--auto-approve) AUTO_APPROVE=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) break ;;
    esac
done

COMMAND="${1:-}"
shift || true

[[ ! -d "$TERRAFORM_DIR" ]] && { log_error "Directory not found: $TERRAFORM_DIR"; exit 1; }

cd "$TERRAFORM_DIR"

case "${1:-}" in
    init)
        log_info "Initializing Terraform..."
        terraform init -upgrade
        ;;
    plan)
        log_info "Generating execution plan..."
        terraform plan ${VAR_FILES[@]/#/-var-file=} ${VARS[@]/#/-var=} -out=tfplan
        ;;
    apply)
        log_info "Applying Terraform plan..."
        if [[ "$AUTO_APPROVE" == "true" ]]; then
            terraform apply -auto-approve ${VAR_FILES[@]/#/-var-file=} ${VARS[@]/#/-var=}
        else
            terraform apply ${VAR_FILES[@]/#/-var-file=} ${VARS[@]/#/-var=}
        fi
        ;;
    destroy)
        log_warn "Destroying infrastructure..."
        if [[ "$AUTO_APPROVE" == "true" ]]; then
            terraform destroy -auto-approve ${VAR_FILES[@]/#/-var-file=} ${VARS[@]/#/-var=}
        else
            terraform destroy ${VAR_FILES[@]/#/-var-file=} ${VARS[@]/#/-var=}
        fi
        ;;
    validate)
        log_info "Validating Terraform configuration..."
        terraform validate
        ;;
    fmt)
        log_info "Formatting Terraform files..."
        terraform fmt -recursive
        ;;
    output)
        terraform output -json
        ;;
    workspace)
        case "${2:-}" in
            select) terraform workspace select "${3:-default}" ;;
            list) terraform workspace list ;;
            new) terraform workspace new "${3:-}" ;;
            delete) terraform workspace delete "${3:-}" ;;
            *) usage; exit 1 ;;
        esac
        ;;
    state)
        case "${2:-}" in
            list) terraform state list ;;
            show) terraform state show "${3:-}" ;;
            rm) terraform state rm "${3:-}" ;;
            mv) terraform state mv "${3:-}" "${4:-}" ;;
            *) usage; exit 1 ;;
        esac
        ;;
    import)
        [[ $# -lt 3 ]] && { log_error "Usage: $0 import ADDRESS ID"; exit 1; }
        terraform import "$2" "$3"
        ;;
    *)
        usage
        exit 1
        ;;
esac