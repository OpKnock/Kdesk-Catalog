---
name: "api-test-pact-broker"
description: "Implements contract testing with Pact: consumer expectations, provider verification, Pact Broker versioning, and can-i-deploy gating."
---

# Api Test Pact Broker

Implements contract testing with Pact: consumer expectations, provider verification, Pact Broker versioning, and can-i-deploy gating.

## Instructions

# API Test v2 - Contract Testing

Contract testing with Pact.

## What This Skill Does
- Defines consumer expectations as pacts
- Verifies providers against pacts
- Gates deploys with Pact Broker

## When to Use
- Service-to-service APIs
- Preventing breaking changes
- Independent deployments

## Real Commands

```bash
pact-broker publish ./pacts --consumer-app-version 1.2.3 --broker-base-url https://broker.example.com
npx pact-verifier --provider-base-url http://localhost:3000 --pact-url ./pacts/order-consumer-order-service.json
pact-broker can-i-deploy --pacticipant OrderService --version 1.2.3 --to prod
```

## Contract Flow
1. Consumer generates pacts in tests
2. Publish pacts to the broker
3. Provider verifies on each build
4. can-i-deploy gates releases

## Testing
- Run verification in provider CI
- Tag versions for environment tracking
- Check matrix results for compatibility


## Best Practices
- One pact per consumer-provider pair
- Keep pacts small and focused
- Automate can-i-deploy in release pipelines

## Capabilities

### pact-broker
Publish and manage contracts with Pact Broker

**Commands:**
- `pact-broker create-or-update-pacticipant --name OrderService --broker-base-url http://localhost:8080`
- `pact-broker publish ./pacts --consumer-app-version 1.2.3 --broker-base-url http://localhost:8080`
- `pact-broker create-version-tag --pacticipant OrderService --version 1.2.3 --tag prod --broker-base-url https://broker.example.com`
- `pact-broker can-i-deploy --pacticipant OrderService --version 1.2.3 --to prod --broker-base-url http://localhost:8080`

**Examples:**
- publish uploads generated pact files
- create-version-tag marks prod versions
- can-i-deploy blocks incompatible releases

### pact-testing
Verify provider against consumer contracts

**Commands:**
- `npm install @pact-foundation/pact --save-dev`
- `npx pact-verifier --provider-base-url http://localhost:3000 --pact-url ./pacts/order-consumer-order-service.json`
- `npx jest --verbose`
- `pact-broker list-latest-pact-versions --broker-base-url http://localhost:8080`

**Examples:**
- -cli --help
- -api --help
