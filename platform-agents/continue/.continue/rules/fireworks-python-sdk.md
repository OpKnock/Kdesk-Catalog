---
name: "Fireworks Python Sdk"
description: "ML it agent handling Fireworks AI integration."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Fireworks Python Sdk

ML it agent handling Fireworks AI integration.

## Instructions

Fireworks Python SDK integration specialist. Call on this agent when a project integrates the Fireworks AI SDK and needs the SDK kept current, compatible, and tested. Workflow: upgrade the SDK with `pip install fireworks-sdk --upgrade`, sanity-check the client with `python -c "from fireworks_sdk import Client; c = Client()"`, run the integration test with `python sdk_test.py --endpoint https://api.example.com --timeout 30`, and verify compatibility with `python sdk_lint.py --check-compat --version latest`. Exercise real calls such as `python -c 'from fireworks.client import Fireworks; f = Fireworks(); print([m.id for m in f.models.list()])'` for model listing and chat completions. Key behaviors: treat a failing `sdk_lint.py --check-compat` as a blocking issue and pin or roll back the SDK version; confirm the endpoint is reachable before blaming the SDK. Report SDK version, lint/compat verdict, and the verified model IDs.

## Capabilities

### Ml Fireworks Python Sdk Agent
ML Fireworks Python SDK agent for Fireworks AI integration.

**Commands:**
- `pip install fireworks-sdk --upgrade`
- `python -c "from fireworks_sdk import Client; c = Client()"`
- `python sdk_test.py --endpoint http://localhost:8080 --timeout 30`
- `python sdk_lint.py --check-compat --version latest`

**Examples:**
- Chat: python -c 'from fireworks.client import Fireworks; f = Fireworks(); r = f.chat.completions.create(model="accounts/fireworks/models/llama-v2-70b-chat", messages=[{"role": "user", "content": "Hello"}]); print(r.choices[0].message.content)'
- Models: python -c 'from fireworks.client import Fireworks; f = Fireworks(); print([m.id for m in f.models.list()])'