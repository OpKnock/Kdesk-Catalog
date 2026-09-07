---
trigger: glob
description: "Works with Databricks: clusters, jobs, notebooks, and DBFS from the Databricks CLI. Use when working with databricks cli or when the user mentions databricks cli."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Works with Databricks: clusters, jobs, notebooks, and DBFS from the Databricks CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `databricks configure --token`
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

# Databricks

Manage Databricks workspaces from the CLI: clusters, jobs, notebooks, and DBFS
files for lakehouse workloads.

## When to Use

- Kicking off production jobs and monitoring runs
- Managing clusters for interactive and batch workloads
- Moving data in/out of DBFS

## Real Commands

```bash
# Auth setup
sudo databricks configure --token

# Cluster management
databricks clusters list
databricks clusters start --cluster-id 1234-5678-abcd

# Jobs
databricks jobs list
databricks jobs run-now --job-id 42
sudo databricks run now --job-id 42 --wait
sudo databricks run list --job-id 42 --limit 5

# Files
databricks fs ls dbfs:/mnt/data
databricks fs cp ./input.csv dbfs:/mnt/data/landing/input.csv
databricks fs mkdirs dbfs:/mnt/warehouse

# Workspace
databricks workspace list /
databricks workspace export notebook.py
```

## Run Monitoring

```bash
sudo databricks run get --run-id 12345
databricks run list --job-id 42 --limit 10 --output json | jq '.runs[].state'
```

## Best Practices

- Use a service principal token in CI; rotate regularly
- Pin cluster runtime versions in job configs
- Upload data to DBFS/Unity Catalog before jobs, never from notebooks
- Monitor run states; alert on FAILED/SKIPPED
- Use `--profile` per environment

## Example Response

For a failed job: gets the run details and log paths, pulls the Spark error from
logs, and proposes the fix or rerun with adjusted parameters.

## Capabilities

### databricks-cli
Manage workspaces, clusters, jobs, and files via databricks CLI

**Parameters:**
- `job-id` (integer): ID of the job to trigger
- `wait` (boolean): Block until the run completes
- `profile` (string): Named profile from the CLI config file

**Commands:**
- `databricks configure --token`
- `databricks clusters list`
- `databricks jobs list`
- `databricks fs ls dbfs:/mnt/data`
- `databricks run now --job-id 123 --wait`

**Examples:**
- databricks workspace list /
- databricks jobs run-now --job-id 42 --jar-params '["--env", "prod"]'
- databricks fs cp local.csv dbfs:/mnt/data/landing/

## References
- [Databricks CLI docs](https://docs.databricks.com/en/dev-tools/cli/index.html)
- [Databricks jobs API](https://docs.databricks.com/en/jobs/index.html)
