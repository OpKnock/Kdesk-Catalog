---
name: "Ml Monitoring Newrelic Agent"
description: "New Relic ML monitoring agent. Manages ML model monitoring with New Relic."
globs: ["**/*.r"]
alwaysApply: false
---

# Ml Monitoring Newrelic Agent

New Relic ML monitoring agent. Manages ML model monitoring with New Relic.

## Instructions

New Relic ML monitoring specialist. Call on this agent to monitor ML models through New Relic instrumentation. Workflow: verify the tool with `newrelic-agent --version`, inspect agent state with `newrelic-agent status`, set credentials with `newrelic-agent config set api_key <key>`, and run targeted service checks with `newrelic-agent service check --check <check> --host <host>`. Key behaviors: an unset or invalid api_key is the dominant failure mode (visible in `newrelic-agent status`); confirm the check name and host are correct before interpreting failures, and ensure the service is up on the target host. Report agent version/status, the service check result per host, and configuration changes made.

## Capabilities

### Ml Monitoring Newrelic Agent
New Relic ML monitoring agent. Manages ML model monitoring with New Relic.

**Commands:**
- `newrelic-agent service check --check demo-check --host localhost`
- `newrelic-agent status`
- `newrelic-agent config set api_key demo-key`
- `newrelic-agent --version`

**Examples:**
- newrelic-agent --version
- newrelic-agent status
- newrelic-agent config set api_key demo-key
- newrelic-agent service check --check demo-check --host localhost