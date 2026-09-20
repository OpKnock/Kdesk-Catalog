# Databricks

Works with Databricks: clusters, jobs, notebooks, and DBFS from the Databricks CLI.

## Instructions

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
