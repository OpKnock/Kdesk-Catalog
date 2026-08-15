# Merge candidates (below auto bar)
Auto bar: identical commands + instruction Jaccard >= 0.55 and score gap <= 3.0.
Auto-merging would cancel the remaining differences: instructions vary ~80% even inside name families. Deciding these is human curation.

Status legend: RESOLVED = decided and applied (loser archived under archive/), KEPT = reviewed and kept apart.

## Resolved (2026-08-11)

- RESOLVED `universal-agents\ml\deployment\ml-pinecone-deploy.yaml` / `universal-agents\ml\deployment\ml-pinecone-vector-deploy.yaml`
  (fam ml pinecone, sim 0.547, gap 0, 6 cmds) — 5/6 commands identical, only identity.py differs;
  archived `ml-pinecone-vector-deploy.yaml` (vector story kept by live `ml-pinecone-vector-agent`).
- RESOLVED `universal-agents\ml\agent\ml-ecs-python-agent.yaml` / `universal-agents\ml\deployment\ml-ecs-aws-deploy.yaml`
  (fam ml ecs, sim 0.471, gap 1, 4 vs 3 cmds) — `ml-ecs-aws-deploy`'s commands are a strict subset of
  `ml-ecs-python-agent`'s (3/3 duplicated, agent has the extra `Status:` command); archived `ml-ecs-aws-deploy.yaml`.
- RESOLVED (family) `universal-agents\ml\inference\mlx-lm-identity-py.yaml` —
  this generator-artifact file was the loser in both its pairs (`mlx-lm-sdk` sim 0.518,
  `mlx-lm-inference` sim 0.504; partner already archived in L3); archived `mlx-lm-identity-py.yaml`.
- RESOLVED `universal-agents\ml\agent\fine-tuning-identity-py.yaml` / `universal-agents\ml\agent\fine-tuning-sdk.yaml`
  (fam fine tuning, sim 0.449, gap 2, 6 cmds) — 5/6 identical, only identity.py differs; archived
  `fine-tuning-identity-py.yaml`. (`fine-tuning-agent` was archived in L3.)

## Already resolved by L3 (archived both members)

- `universal-agents\ml\inference\llama-cpp-identity-py.yaml` / `universal-agents\ml\inference\llama-cpp-inference.yaml`
  (fam llama cpp, sim 0.513, gap 2, 6 cmds) — both in archive/ since `c96fa6d`.
- `universal-agents\ml\agent\fine-tuning-agent.yaml` / `universal-agents\ml\agent\fine-tuning-identity-py.yaml`
  (fam fine tuning, sim 0.436, gap 2, 6 cmds) — first member archived in L3 (`c96fa6d`),
  second member archived in this curation round.