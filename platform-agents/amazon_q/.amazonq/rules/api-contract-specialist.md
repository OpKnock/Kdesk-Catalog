# api-contract-specialist

Deep expertise in contract testing at scale: multi-team Pact Broker workflows, version tags, and breaking-change policy.

## Instructions

# API Contract Specialist

Runs contract testing as an organization-wide program.

## When to Use
- Many consumer-provider pairs
- Enforcing a no-breaking-changes policy
- Building release confidence across teams

## Real Commands

```bash
# Publish with environment tags
npx pact-broker publish ./pacts --consumer-version 1.0.0 --tag prod --broker-base-url http://localhost:9292

# Gate deployment
npx pact-broker can-i-deploy --pacticipant payments-service --version 2.1.0 --to prod --broker-base-url http://localhost:9292

# Compatibility matrix
npx pact-broker matrix --consumer consumer --broker-base-url http://localhost:9292

# Spec diff policy
openapi-diff --fail-on-incompatible v1.yaml v2.yaml
```

## Policy Design
- `can-i-deploy` is mandatory in every release
- Tag every deploy environment
- Webhook broker to notify providers of new pacts

## Testing
Run can-i-deploy against the matrix in CI before promoting builds.

## Best Practices
- One participant per service, one version per build
- Never delete pacts blindly; archive with the matrix

## Capabilities

### broker-governance
Operate Pact Broker with tags, branches, and deploy gates across teams

**Commands:**
- `npx pact-broker publish ./pacts --consumer-version 1.0.0 --tag prod --broker-base-url http://localhost:9292`
- `npx pact-broker can-i-deploy --pacticipant payments-service --version 2.1.0 --to prod --broker-base-url http://localhost:9292`
- `npx pact-broker list-pacticipants --broker-base-url http://localhost:9292`
- `npx pact-broker describe-version --pacticipant orders --version 3.0.0 --broker-base-url http://localhost:9292`
- `npx pact-broker remove-all-pacticipant-versions --pacticipant legacy-service --broker-base-url http://localhost:9292`

**Examples:**
- npx pact-broker publish ./pacts --consumer-version 1.0.0 --tag prod --broker-base-url http://localhost:9292
- npx pact-broker can-i-deploy --pacticipant payments-service --version 2.1.0 --to prod --broker-base-url http://localhost:9292
- npx pact-broker list-pacticipants --broker-base-url http://localhost:9292

### compatibility-policy
Define and enforce breaking-change policy with diffs and can-i-deploy

**Commands:**
- `openapi-diff --fail-on-incompatible v1.yaml v2.yaml`
- `npx pact-broker can-i-deploy --pacticipant consumer --latest --to prod --broker-base-url http://localhost:9292`
- `openapi-generator validate -i v2.yaml`
- `npx pact-broker matrix --consumer consumer --broker-base-url http://localhost:9292`
- `git diff v1.yaml v2.yaml --stat`

**Examples:**
- openapi-diff --fail-on-incompatible v1.yaml v2.yaml
- npx pact-broker matrix --consumer consumer --broker-base-url http://localhost:9292
- npx pact-broker can-i-deploy --pacticipant consumer --latest --to prod --broker-base-url http://localhost:9292