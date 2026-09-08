---
trigger: glob
description: "Creates, updates, and invokes AWS Lambda functions with the AWS CLI, including packaging, configuration, and log inspection. Use when working with function lifecycle, invoke and config, logs and metrics, api or when the user mentions function lifecycle, invoke and config, logs and metrics, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Creates, updates, and invokes AWS Lambda functions with the AWS CLI, including packaging, configuration, and log inspection.

## Agentic Workflow: Read -> Reason -> Act (aws-lambda)

You are **Aws Lambda** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `aws-lambda`
- Domain: Creates, updates, and invokes AWS Lambda functions with the AWS CLI, including packaging, configuration, and log inspection.
- **function-lifecycle**: Create, update, and manage Lambda functions. — `aws lambda create-function --function-name my-fn --runtime nodejs20.x --role arn`
- **invoke-and-config**: Invoke functions and manage configuration. — `aws lambda invoke --function-name my-fn --payload '{"a":1}' out.json`
- **logs-and-metrics**: Inspect function logs and metric alarms. — `aws logs tail /aws/lambda/my-fn --follow`
- Check `knowledge` and `prerequisites: aws`

### 2. Reason — think for `aws-lambda`
- For `function-lifecycle`: Create, update, and manage Lambda functions. — decide which checks to run
- For `invoke-and-config`: Invoke functions and manage configuration. — decide which checks to run
- For `logs-and-metrics`: Inspect function logs and metric alarms. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `aws-lambda` tools
- Tools: `Glob`, `Grep`, `Read`, `Aws` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `aws-lambda:3a440b20`

# AWS Lambda

## What this skill does

Creates, updates, and invokes AWS Lambda functions: packaging code, managing configuration (memory/timeout/env), invoking with test payloads, and inspecting logs.

## When to use

- Deploying a serverless function from CI
- Debugging a failing invocation via logs
- Tuning memory/timeout for cost and latency

## Real commands

```bash
# Create
zip function.zip index.js
aws lambda create-function --function-name my-fn --runtime nodejs20.x --role arn:aws:iam::111122223333:role/lambda-basic --handler index.handler --zip-file fileb://function.zip

# Update code
aws lambda update-function-code --function-name my-fn --zip-file fileb://function.zip --publish

# Invoke and capture logs
aws lambda invoke --function-name my-fn --cli-binary-format raw-in-base64-out --payload '{"a":1}' --log-type Tail response.json
jq -r '.LogResult' <(cat /tmp/nonexistent) 2>/dev/null; aws lambda invoke ... | jq -r '.LogResult' | base64 -d

# Configuration
aws lambda update-function-configuration --function-name my-fn --memory-size 512 --timeout 15

# Logs
aws logs tail /aws/lambda/my-fn --follow
```

## Testing

- Invoke with sample events and check response.json
- Filter logs for ERROR after each deploy

## Best practices

- Keep the package small; use layers for common deps
- Set memory to minimize duration*cost product
- Publish versions and alias traffic for canary deploys
- Always set a timeout lower than the client's expectation

## Capabilities

### function-lifecycle
Create, update, and manage Lambda functions.

**Parameters:**
- `runtime` (string): Runtime: nodejs20.x, python3.12, go1.x, etc.
- `handler` (string): Handler entry point
- `zip_file` (string): Path to deployment package

**Commands:**
- `aws lambda create-function --function-name my-fn --runtime nodejs20.x --role arn:aws:iam::111122223333:role/lambda-basic --handler index.handler --zip-file fileb://function.zip`
- `aws lambda update-function-code --function-name my-fn --zip-file fileb://function.zip`
- `aws lambda list-functions`
- `aws lambda get-function --function-name my-fn`
- `aws lambda delete-function --function-name my-fn`

**Examples:**
- aws lambda create-function --function-name my-fn --runtime python3.12 --role arn:aws:iam::111122223333:role/lambda-basic --handler lambda_function.handler --zip-file fileb://function.zip
- aws lambda update-function-code --function-name my-fn --zip-file fileb://function.zip --publish
- aws lambda list-functions --query 'Functions[].{name:FunctionName,runtime:Runtime}'

### invoke-and-config
Invoke functions and manage configuration.

**Parameters:**
- `payload` (string): JSON event payload
- `memory_size` (number): Memory in MB
- `timeout` (number): Timeout in seconds

**Commands:**
- `aws lambda invoke --function-name my-fn --payload '{"a":1}' out.json`
- `aws lambda invoke --function-name my-fn --cli-binary-format raw-in-base64-out --payload '{"a":1}' --log-type Tail response.json`
- `aws lambda get-function-configuration --function-name my-fn`
- `aws lambda update-function-configuration --function-name my-fn --memory-size 512 --timeout 15`
- `aws lambda list-versions-by-function --function-name my-fn`

**Examples:**
- aws lambda invoke --function-name my-fn --payload '{"a":1}' out.json && cat out.json
- aws lambda invoke --function-name my-fn --payload '{}' --cli-binary-format raw-in-base64-out --log-type Tail resp.json | jq -r '.LogResult' | base64 -d
- aws lambda update-function-configuration --function-name my-fn --environment Variables={LOG_LEVEL=info}

### logs-and-metrics
Inspect function logs and metric alarms.

**Parameters:**
- `function_name` (string): Lambda function name
- `filter_pattern` (string): Log filter pattern

**Commands:**
- `aws logs tail /aws/lambda/my-fn --follow`
- `aws logs filter-log-events --log-group-name /aws/lambda/my-fn --filter-pattern "ERROR"`
- `aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Errors --dimensions Name=FunctionName,Value=my-fn --period 300 --statistics Sum --start-time ... --end-time ...`
- `aws lambda get-account-settings`

**Examples:**
- aws logs tail /aws/lambda/my-fn --follow --format short
- aws logs filter-log-events --log-group-name /aws/lambda/my-fn --filter-pattern "ERROR" | jq '.events[].message'
- aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Duration --dimensions Name=FunctionName,Value=my-fn --period 300 --statistics Average --start-time ... --end-time ...

## References
- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [AWS CLI lambda Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/index.html)
