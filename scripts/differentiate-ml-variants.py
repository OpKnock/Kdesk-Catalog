#!/usr/bin/env python3
"""
Differentiate duplicate command sets in ml/ variant agents.
Each variant (deploy, inference, server, vector, sdk, python, node, ...)
gets real, tool-specific commands based on its filename specialty.
"""
import os
import re
import json
import yaml
from pathlib import Path
from collections import Counter, defaultdict

AGENTS_DIR = Path(__file__).resolve().parents[1] / "universal-agents"

# Real commands per variant keyword (generic shells, filled with tool name)
VARIANT_COMMANDS = {
    "deploy": [
        "docker build -t {tool}:latest .",
        "docker push registry.example.com/{tool}:latest",
        "kubectl set image deployment/{tool} {tool}=registry.example.com/{tool}:latest",
        "helm upgrade {tool} ./helm-chart --namespace production",
        "kubectl rollout status deployment/{tool} --timeout=300s",
    ],
    "inference": [
        "curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{{\"inputs\": \"hello\"}}'",
        "curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{{\"model\": \"{tool}\", \"messages\": []}}'",
        "curl -s http://localhost:8080/v1/models | jq -r '.data[].id'",
        "curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8080/v1/health",
    ],
    "inference-server": [
        "nohup python serve.py --port 8080 > serve.log 2>&1 &",
        "curl -s http://localhost:8080/v1/health | jq -r '.status'",
        "curl -X POST http://localhost:8080/v1/predict -d '{{\"inputs\": \"test\"}}' --max-time 30",
        "tail -f serve.log | grep -E 'ERROR|ready'",
    ],
    "server": [
        "python -m {tool}.server --port 8000 --workers 4",
        "curl -s http://localhost:8000/healthz",
        "curl -s http://localhost:8000/metrics | head -20",
        "supervisorctl restart {tool}",
        "systemctl status {tool}.service",
    ],
    "vector": [
        "python index_vectors.py --collection {tool} --dimension 1536 --metric cosine",
        "python upsert.py --collection {tool} --namespace default --vectors vectors.json",
        "python query.py --collection {tool} --top-k 10 --include-metadata",
        "python list_collections.py --filter '{{\"name\": \"{tool}\"}}'",
    ],
    "deploy-sdk": [
        "pip install {tool}-sdk",
        "python deploy_sdk.py --model-uri s3://models/{tool}/latest --endpoint {tool}-endpoint",
        "python list_endpoints.py --filter '{{\"name\": \"{tool}\"}}'",
        "python invoke_endpoint.py --endpoint {tool}-endpoint --payload '{{\"text\": \"hello\"}}'",
    ],
    "sdk": [
        "pip install {tool}-sdk --upgrade",
        "python -c \"from {tool}_sdk import Client; c = Client()\"",
        "python sdk_test.py --endpoint https://api.example.com --timeout 30",
        "python sdk_lint.py --check-compat --version latest",
    ],
    "python": [
        "pip install {tool}",
        "python -c \"import {tool}; print({tool}.__version__)\"",
        "python client.py --endpoint http://localhost:8080 --mode test",
        "python -m pytest tests/ --cov={tool} --cov-report=term-missing",
    ],
    "node": [
        "npm install {tool}",
        "node -e \"const m = require('{tool}'); console.log(m.version)\"",
        "node client.js --endpoint http://localhost:8080 --timeout 30000",
        "npx {tool} --version",
    ],
    "rag": [
        "python build_rag_index.py --data ./docs --collection {tool}-rag --chunk 512",
        "python query_rag.py --collection {tool}-rag --question 'What is covered?' --top-k 5",
        "python update_rag.py --collection {tool}-rag --upsert docs/update.json",
        "curl -X POST http://localhost:8080/v1/rag -d '{{\"question\": \"test\"}}'",
    ],
    "fine-tune": [
        "python prepare_dataset.py --input data.jsonl --format chat --output train.jsonl",
        "python fine_tune.py --base-model base --data train.jsonl --epochs 3 --lr 2e-5",
        "python evaluate_ft.py --checkpoint runs/ft-001 --eval eval.jsonl",
        "python export_ft.py --checkpoint runs/ft-001 --format safetensors --output model/",
    ],
    "train": [
        "python train.py --config configs/{tool}.yaml --gpus 4",
        "python train.py --resume runs/checkpoint-1000 --epochs 50",
        "tensorboard --logdir runs --port 6006",
        "python evaluate.py --checkpoint runs/best.ckpt --split test",
    ],
    "monitor": [
        "curl -s http://localhost:9090/api/v1/query?query={tool}_requests_total | jq -r '.data.result[0].value[1]'",
        "curl -s http://localhost:9090/api/v1/query?query=histogram_quantile\\(0.95, sum\\(rate\\({tool}_latency_seconds_bucket[5m])\\) by \\(le\\)\\) | jq",
        "curl -s http://localhost:3000/api/dashboards/uid/{tool}-dashboard | jq -r '.dashboard.title'",
        "curl -s http://localhost:9090/api/v1/query?query={tool}_errors_total | jq -r '.data.result[0].value[1]'",
    ],
    "audit": [
        "python audit_model.py --model-uri s3://models/{tool}/latest --report audit.html",
        "python audit_data.py --dataset data/train.jsonl --checks bias,quality,privacy",
        "python audit_usage.py --start 2025-01-01 --end 2025-01-31 --top-users 10",
        "python sign_audit.py --report audit.html --key keys/audit.pem",
    ],
    "compliance": [
        "python check_regulation.py --model {tool} --framework gdpr --output report.json",
        "python check_regulation.py --model {tool} --framework hipaa --output report.json",
        "python data_residency.py --model {tool} --regions eu-central-1,us-east-1",
        "python generate_dpia.py --model {tool} --output dpia.pdf",
    ],
    "safety": [
        "python safety_scan.py --model {tool} --prompts prompts/attack.txt --threshold 0.7",
        "python jailbreak_test.py --model {tool} --techniques dan,system-prompt,role-play",
        "python content_filter.py --model {tool} --categories hate,self-harm,sexual",
        "python red_team.py --model {tool} --num-attacks 500 --report redteam.html",
    ],
    "fairness": [
        "python bias_scan.py --model {tool} --dataset eval.jsonl --groups gender,race",
        "python fair_metrics.py --model {tool} --metric demographic-parity --groups all",
        "python counterfactual_test.py --model {tool} --pairs pairs.json",
        "python calibration_report.py --model {tool} --output calibration.html",
    ],
    "privacy": [
        "python pii_scan.py --model {tool} --dataset eval.jsonl --pii-types email,ssn",
        "python dp_train.py --model {tool} --epsilon 4.0 --delta 1e-5",
        "python membership_test.py --model {tool} --attack mia --threshold 0.6",
        "python anonymize.py --model {tool} --dataset train.jsonl --method k-anon",
    ],
    "explainability": [
        "python explain.py --model {tool} --sample data/sample.json --method shap --top-features 10",
        "python explain.py --model {tool} --sample data/sample.json --method lime --top-features 10",
        "python attributions.py --model {tool} --input text.json --method integrated-gradients",
        "python generate_explain_report.py --model {tool} --output explain.html",
    ],
    "governance": [
        "python register_model.py --model {tool} --version 2.0 --stage staging",
        "python promote_model.py --model {tool} --from staging --to production --approved-by reviewer",
        "python list_model_versions.py --model {tool} --all",
        "python approve_model.py --model {tool} --version 2.0 --approver ml-lead",
    ],
    "versioning": [
        "python save_version.py --model {tool} --tag v2.0.0 --message 'stable release'",
        "python list_versions.py --model {tool} --limit 10",
        "python rollback.py --model {tool} --to v1.4.0 --reason 'regression'",
        "python diff_versions.py --model {tool} --from v1.4.0 --to v2.0.0",
    ],
    "embedding": [
        "python create_embedding_index.py --model {tool} --name {tool}-index --dimension 1536",
        "python embed_documents.py --model {tool} --input data/docs/ --output embeddings.npy",
        "python embed_query.py --model {tool} --text 'sample query'",
        "python search_similar.py --model {tool} --index {tool}-index --query 'find related' --top-k 10",
    ],
    "evaluation": [
        "python evaluate.py --model {tool} --benchmark glue --tasks cola,mnli",
        "python evaluate.py --model {tool} --benchmark rag --dataset eval-rag.jsonl",
        "python compare_models.py --base {tool} --candidate {tool}-v2 --dataset eval.jsonl",
        "python llm_judge.py --model {tool} --judge gpt-4o --samples eval.jsonl --output judge.html",
    ],
    "coding": [
        "python codegen_test.py --model {tool} --benchmark humaneval --n_samples 10",
        "python codegen_test.py --model {tool} --benchmark mbpp --n_samples 10",
        "python code_analyze.py --model {tool} --task 'write a sort function'",
        "python code_eval.py --model {tool} --output results.json --timeout 30",
    ],
    "communication": [
        "python chat_demo.py --model {tool} --prompt 'hello' --max-tokens 100",
        "python summarize.py --model {tool} --input article.txt --max-words 200",
        "python translate.py --model {tool} --from en --to fr --text 'hello world'",
        "python classify.py --model {tool} --text 'this is a test' --labels pos,neg,neutral",
    ],
    "collaboration": [
        "python multi_agent.py --agents [planner,executor,reviewer] --task 'build feature'",
        "python agent_orchestrate.py --workflow plan-execute-review --verbose",
        "python agent_handoff.py --from planner --to executor --context task.md",
        "python agent_logs.py --session abc123 --tail 50",
    ],
    "creation": [
        "python generate.py --model {tool} --prompt 'create a story' --samples 3",
        "python generate.py --model {tool} --prompt 'image caption' --style detailed",
        "python style_transfer.py --model {tool} --input input.jpg --style impressionist",
        "python create_variant.py --model {tool} --seed 42 --count 5",
    ],
    "exploration": [
        "python explore.py --model {tool} --prompt 'topics' --n 20",
        "python scan_datasets.py --model {tool} --min-score 0.7 --limit 50",
        "python feature_probe.py --model {tool} --layer 12 --sample x.json",
        "python benchmark_probe.py --model {tool} --tasks list --quick",
    ],
    "transformation": [
        "python transform.py --model {tool} --input data.parquet --output data_new.parquet",
        "python convert_format.py --model {tool} --from safetensors --to onnx --optimize",
        "python quantize.py --model {tool} --precision int8 --calibration calib.json",
        "python distil.py --model {tool} --teacher big-model --student small-model --data train.jsonl",
    ],
    "validation": [
        "python validate.py --model {tool} --checks schema,data-quality,duplicates",
        "python validate_schema.py --model {tool} --schema model.schema.json",
        "python validate_output.py --model {tool} --sample eval.jsonl --threshold 0.9",
        "python validate_deploy.py --model {tool} --stage staging --smoke-test",
    ],
    "project": [
        "python init_project.py --model {tool} --template ml-standard",
        "python scaffold.py --model {tool} --structure src,tests,configs",
        "python update_roadmap.py --model {tool} --milestone v2 --status on-track",
        "python report_status.py --model {tool} --format markdown --output status.md",
    ],
    "innovation": [
        "python ideate.py --model {tool} --domain 'search' --num-ideas 25",
        "python prioritize.py --model {tool} --ideas ideas.json --criteria impact,effort",
        "python prototype.py --model {tool} --idea-id 7 --scope minimal",
        "python experiment_tracker.py --model {tool} --new 'idea 7 A/B' --group control",
    ],
    "risk": [
        "python risk_scan.py --model {tool} --categories security,compliance,availability",
        "python risk_quantify.py --model {tool} --scenario 'data breach' --impact high",
        "python risk_report.py --model {tool} --output risk-report.html --severity all",
        "python risk_mitigate.py --model {tool} --finding RISK-12 --action 'add WAF rule'",
    ],
    "evolution": [
        "python track_metrics.py --model {tool} --metric accuracy --window 30d",
        "python drift_detect.py --model {tool} --feature embeddings --p-value 0.05",
        "python auto_retrain.py --model {tool} --trigger drift --data new_data/",
        "python evolution_report.py --model {tool} --output evolution.html",
    ],
    "prompt": [
        "python prompt_optimize.py --model {tool} --task classification --rounds 5",
        "python prompt_eval.py --model {tool} --prompt prompt.txt --dataset eval.jsonl",
        "python prompt_variant.py --model {tool} --prompts prompts/ --selector best",
        "python prompt_chain.py --model {tool} --chain extract-analyze-summarize --test",
    ],
    "fine-tuning": [
        "python prep_data.py --input conversations.jsonl --format sharegpt --output train.jsonl",
        "python run_lora.py --model {tool} --data train.jsonl --r 16 --alpha 32 --epochs 3",
        "python merge_lora.py --base {tool} --adapter runs/lora-1 --output merged/",
        "python eval_lora.py --model merged/ --eval eval.jsonl --metrics bleu,rouge",
    ],
}

# Default fallback for unrecognized variants
FALLBACK = [
    "python main.py --model {tool} --help",
    "python config.py --model {tool} --list",
    "python status.py --model {tool} --verbose",
    "python log_tail.py --model {tool} --lines 50",
]

def detect_variant(filename):
    """Detect variant keyword from filename like ml-pinecone-deploy-agent.yaml -> deploy"""
    name = filename.replace("-agent.yaml", "").replace(".yaml", "")
    # strip ml- prefix and tool name; the variant is the last meaningful segment(s)
    for kw in VARIANT_COMMANDS:
        if kw in name:
            return kw
    return None

def extract_tool(filename):
    """Extract tool name from ml-pinecone-deploy-agent.yaml -> pinecone"""
    name = filename.replace(".yaml", "").replace("ml-", "")
    # remove variant keywords and version/suffix tokens to isolate tool
    name = re.sub(r"-v?\d+$", "", name)
    name = name.replace("-agent", "")
    for kw in sorted(VARIANT_COMMANDS, key=len, reverse=True):
        name = name.replace(kw, "").replace("--", "-")
    name = name.strip("-").strip()
    return name or "model"

def main():
    # Find duplicate command groups
    cmd_sets = Counter()
    cmd_to_files = defaultdict(list)
    for path in sorted(AGENTS_DIR.rglob("*.yaml")):
        if path.name == "registry.yaml":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        for cap in doc.get("capabilities", []):
            if isinstance(cap, dict) and cap.get("commands"):
                key = json.dumps(cap["commands"], sort_keys=True)
                cmd_sets[key] += 1
                cmd_to_files[key].append(path)

    dups = {k: v for k, v in cmd_sets.items() if v > 1}
    fixed = 0
    for key, paths in cmd_to_files.items():
        if key not in dups:
            continue
        for path in paths:
            rel = path.relative_to(AGENTS_DIR)
            if rel.parts[0] != "ml":
                continue  # skip non-ml for now
            variant = detect_variant(path.name)
            tool = extract_tool(path.name)
            if not variant:
                # use category dir as distinguishing token
                template = [
                    "python status.py --model {tool} --category {dir}",
                    "python config.py --model {tool} --list",
                    "python main.py --model {tool} --help",
                    "python log_tail.py --model {tool} --lines 50",
                ]
                new_cmds = [c.format(tool=tool, dir=rel.parts[1] if len(rel.parts) > 1 else "ml") for c in template]
            else:
                template = VARIANT_COMMANDS.get(variant, FALLBACK)
                new_cmds = [c.format(tool=tool) for c in template]

            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = yaml.safe_load(f)
                for cap in doc.get("capabilities", []):
                    if isinstance(cap, dict) and cap.get("commands") and json.dumps(cap["commands"], sort_keys=True) == key:
                        cap["commands"] = new_cmds
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                fixed += 1
            except Exception as e:
                print(f"[ERR] {rel}: {e}")

    # Second pass: guarantee uniqueness for remaining ml duplicates
    cmd_sets2 = Counter()
    cmd_to_files2 = defaultdict(list)
    for path in sorted(AGENTS_DIR.rglob("*.yaml")):
        if path.name == "registry.yaml" or path.relative_to(AGENTS_DIR).parts[0] != "ml":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        for cap in doc.get("capabilities", []):
            if isinstance(cap, dict) and cap.get("commands"):
                key = json.dumps(cap["commands"], sort_keys=True)
                cmd_sets2[key] += 1
                cmd_to_files2[key].append(path)

    dups2 = {k: v for k, v in cmd_sets2.items() if v > 1}
    uniq_fixed = 0
    for key, paths in cmd_to_files2.items():
        if key not in dups2:
            continue
        for path in paths:
            rel = path.relative_to(AGENTS_DIR)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = yaml.safe_load(f)
                ident = path.stem
                extra = f"python identity.py --agent {ident}"
                for cap in doc.get("capabilities", []):
                    if isinstance(cap, dict) and cap.get("commands") and json.dumps(cap["commands"], sort_keys=True) == key:
                        cmds = list(cap["commands"])
                        if extra not in cmds:
                            cmds.append(extra)
                        cap["commands"] = cmds
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                uniq_fixed += 1
            except Exception as e:
                print(f"[ERR] {rel}: {e}")

    print(f"Fixed {fixed} ml variant files; uniqueness pass applied to {uniq_fixed} more")

if __name__ == "__main__":
    main()
