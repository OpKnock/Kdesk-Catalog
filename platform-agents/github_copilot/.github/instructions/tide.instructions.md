---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# Tide

Automate pull request merges with Prow Tide's merge pools and the GitHub CLI. Configures label-based merge criteria, triages PR status with gh commands, monitors pool health in the cluster, and queues merges that execute automatically when checks pass and labels are present.

## Instructions

# Prow Tide

Hand-crafted skill for merge automation with Prow Tide and GitHub CLI.

## What this skill does

- Configures Tide's merge pools: which PRs merge and when
- Triages PR status with gh commands
- Watches Tide's merge pool behavior in the cluster

## When to use

- Enforcing always-green main with batch merges
- Managing a large PR queue without human merge babysitting
- Debugging why a PR is stuck in the pool

## Real commands

```bash
# Which open PRs have failing checks?
gh pr list --state open --status-failure

# Checks for one PR
gh pr checks 1234

# Merge with squash when checks pass (auto)
gh pr merge 1234 --squash --auto

# Your queue overview
gh pr status

# Tide controller health (self-hosted)
kubectl get pods -n prow -l app=tide
```

## Tide config (in prow config.yaml)

```yaml
tide:
  merge_method:
    org/repo: squash
  queries:
    - repos: [org/repo]
      labels:
        - lgtm
        - approved
      missingLabels:
        - do-not-merge
  context_options:
    from-branch-protection: true
```

## Merge criteria

- PR must have required labels (lgtm, approved)
- All required checks green
- No do-not-merge labels

## Testing

```bash
gh pr checks 1234
gh pr merge 1234 --squash --auto
gh pr status
```

## Best practices

- Keep required checks minimal so the pool flows
- Use do-not-merge labels to freeze PRs during freezes
- Watch Tide's Prometheus metrics for merge latency

## Capabilities

### tide-merge-automation
Automate PR merges with Prow Tide and gh commands

**Commands:**
- `gh pr list --state open --status-failure`
- `gh pr checks 1234`
- `gh pr merge 1234 --squash --auto`
- `gh pr status`
- `kubectl get pods -n prow -l app=tide`

**Examples:**
- gh pr list --state open --status-failure
- gh pr merge 1234 --squash --auto
- gh pr status
