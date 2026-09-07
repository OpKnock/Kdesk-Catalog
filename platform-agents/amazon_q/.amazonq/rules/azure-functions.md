Builds, tests, and ships serverless functions on Azure using Core Tools: initializes projects, scaffolds HTTP and timer triggers, runs the local emulator, publishes to function apps, and validates endpoints with curl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `func new --template "HttpTrigger" --name MyFunction`, `func azure functionapp publish MyFunctionApp`
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

# Azure Functions

## What this skill does

Builds, tests, and ships serverless functions on Azure using Core Tools: initializes projects, scaffolds HTTP and timer triggers, runs the local emulator, publishes to function apps, and validates endpoints with curl.

## When to use

- Building a serverless HTTP API or timer job
- Testing a function locally before deploy
- Deploying from CI with func azure functionapp publish

## Real commands

```bash
# Init and scaffold
func init --worker-runtime node
func new --template "HttpTrigger" --name MyFunction

# Run locally
func start --port 7071

# Test locally
curl -s "http://localhost:7071/api/MyFunction?name=world"

# Publish
func azure functionapp publish MyFunctionApp

# List deployed functions
func azure functionapp list-functions MyFunctionApp

# Test in Azure
curl -s "https://api.your-app.test/api/MyFunction?name=azure"
```

## Testing

- Test locally with func start, then against the live URL
- Use --functions to run a single function during debugging

## Best practices

- Use --publish-local-settings -i for consistent settings
- Keep functions stateless; use bindings for I/O
- Pin Core Tools version in CI for reproducible builds

## Capabilities

### local-dev
Create and run functions locally with Core Tools.

**Parameters:**
- `template` (string): Trigger template (HttpTrigger, TimerTrigger, etc.)
- `runtime` (string): node, python, dotnet, java, powershell
- `port` (number): Local runtime port

**Commands:**
- `func new --template "HttpTrigger" --name MyFunction`
- `func new --template "TimerTrigger" --name DailyJob --runtime node`
- `func start`
- `func init --worker-runtime node`
- `func --version`

**Examples:**
- func init --worker-runtime python && func new --template "HttpTrigger" --name HttpExample
- func start --port 7071
- func new --template "ServiceBusQueueTrigger" --name OrderHandler --runtime dotnet

### publish
Deploy functions to Azure.

**Parameters:**
- `app_name` (string): Function app name in Azure
- `publish_settings` (boolean): Publish local app settings

**Commands:**
- `func azure functionapp publish MyFunctionApp`
- `func azure functionapp list-functions MyFunctionApp`
- `func azure functionapp fetch-app-settings MyFunctionApp`
- `az functionapp list --resource-group rg`
- `az functionapp show --name MyFunctionApp -g rg`

**Examples:**
- func azure functionapp publish MyFunctionApp --publish-local-settings -i
- func azure functionapp list-functions MyFunctionApp --show-keys
- func azure functionapp publish MyFunctionApp --no-build

### test-function
Invoke functions locally and in Azure.

**Parameters:**
- `url` (string): Function URL
- `query` (string): Query parameters

**Commands:**
- `curl -X POST http://localhost:7071/api/MyFunction -d '{"name":"test"}'`
- `curl -s http://localhost:7071/api/MyFunction?name=world`
- `curl -s https://api.your-app.test/api/MyFunction?name=azure`
- `func start --functions MyFunction`
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:7071/api/MyFunction`

**Examples:**
- curl -s "http://localhost:7071/api/MyFunction?name=world"
- curl -s "https://api.your-app.test/api/MyFunction?name=azure"
- func start --functions MyFunction --verbose

## References
- [Azure Functions Docs](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [HTTP Trigger Reference](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger)