Manages AWS AppSync GraphQL APIs: creating APIs, schema updates, resolvers, API keys, and executing GraphQL queries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `aws appsync create-graphql-api --name MyApi --authentication`, `aws appsync start-schema-creation --api-id abc123xyz --defin`
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

# AWS AppSync

## What this skill does

Manages AWS AppSync GraphQL APIs: creating APIs with auth types, pushing schemas, wiring resolvers to data sources, issuing API keys, and executing GraphQL operations via curl.

## When to use

- Building a managed GraphQL API over DynamoDB/Lambda
- Updating a schema or resolver without redeploying the app
- Debugging GraphQL errors from the CLI

## Real commands

```bash
# Create an API
aws appsync create-graphql-api --name MyApi --authentication-type API_KEY

# Push the schema
aws appsync start-schema-creation --api-id abc123xyz --definition file://schema.graphql
aws appsync get-schema-creation-status --api-id abc123xyz

# Create a resolver
aws appsync create-resolver --api-id abc123xyz --type-name Query --field-name listItems --data-source-name items --request-mapping-template file://req.vtl --response-mapping-template file://resp.vtl

# Get a key and query
aws appsync create-api-key --api-id abc123xyz
curl -X POST https://abc123xyz.appsync-api.us-east-1.amazonaws.com/graphql -H "x-api-key: $API_KEY" -H "Content-Type: application/json" -d '{"query":"{ listItems { id } }"}'
```

## Testing

- Use { __typename } as a smoke query to confirm auth works
- Check schema status before creating resolvers

## Best practices

- Use AWS_IAM or Cognito auth for production; API_KEY for dev
- Put VTL templates in version control
- Rotate API keys before expiry via list-api-keys

## Capabilities

### api-lifecycle
Create and configure AppSync GraphQL APIs.

**Parameters:**
- `api_name` (string): GraphQL API name
- `auth_type` (string): API_KEY, AWS_IAM, AMAZON_COGNITO_USER_POOLS, OPENID_CONNECT

**Commands:**
- `aws appsync create-graphql-api --name MyApi --authentication-type API_KEY`
- `aws appsync list-graphql-apis`
- `aws appsync get-graphql-api --api-id abc123xyz`
- `aws appsync update-graphql-api --api-id abc123xyz --authentication-type AMAZON_COGNITO_USER_POOLS --user-pool-config '{...}'`
- `aws appsync delete-graphql-api --api-id abc123xyz`

**Examples:**
- aws appsync create-graphql-api --name MyApi --authentication-type API_KEY
- aws appsync create-graphql-api --name MyApi --authentication-type AWS_IAM
- aws appsync list-graphql-apis --query 'graphqlApis[].{id:apiId,name:name}'

### schema-resolvers
Update schemas and manage resolvers.

**Parameters:**
- `type_name` (string): GraphQL type (Query/Mutation)
- `field_name` (string): Field the resolver attaches to
- `data_source` (string): Data source name

**Commands:**
- `aws appsync start-schema-creation --api-id abc123xyz --definition file://schema.graphql`
- `aws appsync get-schema-creation-status --api-id abc123xyz`
- `aws appsync create-resolver --api-id abc123xyz --type-name Query --field-name listItems --data-source-name items --request-mapping-template file://req.vtl --response-mapping-template file://resp.vtl`
- `aws appsync list-resolvers --api-id abc123xyz --type-name Query`
- `aws appsync get-introspection-schema --api-id abc123xyz --format JSON introspection.json`

**Examples:**
- aws appsync start-schema-creation --api-id abc123xyz --definition file://schema.graphql
- aws appsync create-resolver --api-id abc123xyz --type-name Query --field-name getItem --data-source-name items --request-mapping-template file://req.vtl --response-mapping-template file://resp.vtl
- aws appsync get-introspection-schema --api-id abc123xyz --format SDL schema.graphql

### invoke-graphql
Create API keys and execute GraphQL operations.

**Parameters:**
- `api_id` (string): AppSync API ID
- `api_key` (string): API key for x-api-key header
- `query` (string): GraphQL query/mutation document

**Commands:**
- `aws appsync create-api-key --api-id abc123xyz`
- `aws appsync list-api-keys --api-id abc123xyz`
- `curl -X POST https://abc123xyz.appsync-api.us-east-1.amazonaws.com/graphql -H "x-api-key: $API_KEY" -H "Content-Type: application/json" -d '{"query":"{ listItems { id } }"}'`
- `curl -X POST https://abc123xyz.appsync-api.us-east-1.amazonaws.com/graphql -H "x-api-key: $API_KEY" -H "Content-Type: application/json" -d '{"query":"mutation { createItem(input: {name: \"x\"}) { id } }"}'`

**Examples:**
- curl -X POST https://abc123xyz.appsync-api.us-east-1.amazonaws.com/graphql -H "x-api-key: $API_KEY" -H "Content-Type: application/json" -d '{"query":"{ listItems { id name } }"}'
- aws appsync create-api-key --api-id abc123xyz --description "ci-key" --expires 1767225600
- curl -s -X POST https://abc123xyz.appsync-api.us-east-1.amazonaws.com/graphql -H "x-api-key: $API_KEY" -H "Content-Type: application/json" -d '{"query":"{ __typename }"}'

## References
- [AppSync Developer Guide](https://docs.aws.amazon.com/appsync/latest/devguide/)
- [AWS CLI appsync Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/appsync/index.html)
- [GraphQL Foundation](https://graphql.org/learn/)