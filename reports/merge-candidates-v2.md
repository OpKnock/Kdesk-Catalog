# Family merge candidates (v2, evidence-gated)
Same-name-family pairs measured on command overlap (Jaccard) + instruction token Jaccard.
MATCHES are evidence-strong (command-identical or near); NEAR needs a look; DIFFERENT stays.
Every line is a RANKING, not a decision - each merge is a human call.
Name-families are role/persona suffix groups (architect/engineer/specialist/v2/...), not a duplicate count: 144 families with >1 member are intentional persona variants.

## MATCHES (0)

## NEAR (15)
- `universal-agents/api/agent/rate-limiter-architect.yaml` / `universal-agents/backend/agent/rate-limiter.yaml` (fam rate-limiter, ovl 0.6, sim 0.545, 4/4 cmds)
- `universal-agents/cloud/agent/service-discovery.yaml` / `universal-agents/devops/agent/service-discovery-engineer.yaml` (fam service-discovery, ovl 0.5, sim 0.454, 3/3 cmds)
- `universal-agents/ml/deployment/ml-eks.yaml` / `universal-agents/ml/deployment/ml-gke.yaml` (fam ml, ovl 0.333, sim 0.774, 4/4 cmds)
- `universal-agents/backend/agent/idempotency-designer.yaml` / `universal-agents/backend/agent/idempotency-engineer.yaml` (fam idempotency, ovl 0.2, sim 0.629, 4/2 cmds)
- `universal-agents/ml/deployment/ml-aks.yaml` / `universal-agents/ml/deployment/ml-gke.yaml` (fam ml, ovl 0.143, sim 0.833, 4/4 cmds)
- `universal-agents/ml/deployment/ml-aks.yaml` / `universal-agents/ml/deployment/ml-eks.yaml` (fam ml, ovl 0.143, sim 0.75, 4/4 cmds)
- `universal-agents/devops/deployment/devops-fnm.yaml` / `universal-agents/devops/deployment/devops-nvm.yaml` (fam devops, ovl 0.0, sim 0.742, 4/4 cmds)
- `universal-agents/sre/operations/sre-sli.yaml` / `universal-agents/sre/operations/sre-slo.yaml` (fam sre, ovl 0.0, sim 0.742, 4/4 cmds)
- `universal-agents/api/agent/pagination-designer.yaml` / `universal-agents/backend/agent/pagination-engineer.yaml` (fam pagination, ovl 0.0, sim 0.667, 3/2 cmds)
- `universal-agents/ml/deployment/ml-ecs.yaml` / `universal-agents/ml/deployment/ml-gke.yaml` (fam ml, ovl 0.0, sim 0.618, 4/4 cmds)
- `universal-agents/ml/deployment/ml-aks.yaml` / `universal-agents/ml/deployment/ml-ecs.yaml` (fam ml, ovl 0.0, sim 0.6, 4/4 cmds)
- `universal-agents/ml/deployment/ml-ecs.yaml` / `universal-agents/ml/deployment/ml-eks.yaml` (fam ml, ovl 0.0, sim 0.6, 4/4 cmds)
- `universal-agents/ml/agent/ai-agent-architect.yaml` / `universal-agents/ml/agent/ai-agent-builder.yaml` (fam ai, ovl 0.0, sim 0.578, 3/3 cmds)
- `universal-agents/compliance/audit/compliance-soc2.yaml` / `universal-agents/compliance/compliance/compliance-helper.yaml` (fam compliance, ovl 0.0, sim 0.575, 4/4 cmds)
- `universal-agents/ml/inference/langchain-python-sdk.yaml` / `universal-agents/ml/inference/langchain-python.yaml` (fam langchain-python, ovl 0.0, sim 0.51, 3/4 cmds)

## DIFFERENT (295)
_Not listed._

## REVIEWED (2026-08-12)
Human verdicts for every NEAR pair above. None met the strict MATCHES bar (ovl >= 0.7 AND sim >= 0.4); all are real variants kept as-is.

| Pair | Evidence | Verdict | Reason |
|------|----------|---------|--------|
| rate-limiter-architect / rate-limiter | ovl 0.6, 3/4 shared cmds | KEEP | persona split: design/policy-authoring vs implement/diagnostics |
| service-discovery / service-discovery-engineer | ovl 0.5 | KEEP | per-tool variant: kubectl vs dig (k8s vs DNS) |
| ml-eks / ml-gke | sim 0.77, ovl 0.33 | KEEP | per-cloud commands (eksctl vs gcloud) |
| idempotency-designer / idempotency-engineer | ovl 0.2 | KEEP | distinct command sets |
| ml-aks / ml-gke | sim 0.83, ovl 0.14 | KEEP | per-cloud commands |
| ml-aks / ml-eks | sim 0.75, ovl 0.14 | KEEP | per-cloud commands |
| devops-fnm / devops-nvm | ovl 0.0 | KEEP | different node version managers |
| sre-sli / sre-slo | ovl 0.0 | KEEP | different SRE concepts; sim is shared template boilerplate |
| pagination-designer / pagination-engineer | ovl 0.0 | KEEP | persona variants |
| ml-ecs / ml-gke | ovl 0.0 | KEEP | per-cloud commands |
| ml-aks / ml-ecs | ovl 0.0 | KEEP | per-cloud commands |
| ml-ecs / ml-eks | ovl 0.0 | KEEP | per-cloud commands |
| ai-agent-architect / ai-agent-builder | ovl 0.0 | KEEP | distinct scopes |
| compliance-soc2 / compliance-helper | ovl 0.0 | KEEP | soc2-specific vs generic helper |
| langchain-python-sdk / langchain-python | ovl 0.0 | KEEP | distinct commands |
