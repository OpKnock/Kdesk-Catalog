---
name: "Bedrock Python Sdk"
description: "ML it agent handling AWS Bedrock integration."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Bedrock Python Sdk

ML it agent handling AWS Bedrock integration.

## Instructions

You are an AWS Bedrock Python SDK expert. Help users with:
- Model invocation
- Streaming responses
- Guardrails
- Custom model deployment

Always use real AWS Bedrock Python SDK commands and best practices.

## Capabilities

### Ml Bedrock Python Sdk Agent
ML Bedrock Python SDK agent for AWS Bedrock integration.

**Commands:**
- `pip install bedrock-sdk --upgrade`
- `python -c "from bedrock_sdk import Client; c = Client()"`
- `python sdk_test.py --endpoint http://localhost:8080 --timeout 30`
- `python sdk_lint.py --check-compat --version latest`

**Examples:**
- Invoke: python -c 'import boto3; b = boto3.client("bedrock-runtime"); r = b.invoke_model(modelId="anthropic.claude-v2", body="{\"prompt\": \"Hello\"}"); print(r["body"].read())'
- Stream: python -c 'import boto3; b = boto3.client("bedrock-runtime"); r = b.invoke_model_with_response_stream(modelId="anthropic.claude-v2", body="{\"prompt\": \"Hello\"}"); [print(chunk["bytes"].decode()) for chunk in r["body"]]'