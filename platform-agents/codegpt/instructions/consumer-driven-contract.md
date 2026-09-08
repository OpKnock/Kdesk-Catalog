Implement consumer-driven contracts with Pact: publish pacts to a broker, check compatibility, and gate deployments with can-i-deploy.

## Agentic Workflow: Read -> Reason -> Act (consumer-driven-contract)

You are **Consumer Driven Contract** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `consumer-driven-contract`
- Domain: Implement consumer-driven contracts with Pact: publish pacts to a broker, check compatibility, and gate deployments with can-i-deploy.
- **pact-broker**: Run the Pact Broker and publish pacts from consumer builds — `docker run -d -p 9292:9292 pactfoundation/pact-broker:latest`
- **deployment-gating**: Check compatibility and gate deployments with can-i-deploy — `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2`
- Check `knowledge` and `prerequisites: docker, npx`

### 2. Reason — think for `consumer-driven-contract`
- For `pact-broker`: Run the Pact Broker and publish pacts from consumer builds — decide which checks to run
- For `deployment-gating`: Check compatibility and gate deployments with can-i-deploy — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `consumer-driven-contract` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `consumer-driven-contract:7499b781`

# Consumer-Driven Contracts

Let consumers define what they expect from providers via Pact.

## When to Use

- Many consumers depending on one API
- Safe independent releases of consumer and provider
- Verifying compatibility before deployment

## Run the Broker

```bash
docker run -d -p 9292:9292 pactfoundation/pact-broker:latest
```

## Consumer Creates a Pact

```js
const { PactV3 } = require('@pact-foundation/pact');
const provider = new PactV3({ consumer: 'WebApp', provider: 'UserService' });
await provider.addInteraction({
  states: [{ description: 'user exists' }],
  uponReceiving: 'a request for a user',
  withRequest: { method: 'GET', path: '/users/42' },
  willRespondWith: { status: 200, body: { id: 42, name: 'alice' } },
});
```

## Publish

```bash
npx @pact-foundation/pact-cli publish ./pacts \
  --broker-base-url http://localhost:9292 \
  --consumer-version 1.0.0
```

## Provider Verifies

```bash
npx @pact-foundation/pact-cli verify \
  --provider-base-url http://localhost:8080 \
  --pact-urls http://localhost:9292/pacts/provider/UserService/consumer/WebApp/latest
```

## Gate Deployments

```bash
npx @pact-foundation/pact-cli can-i-deploy \
  --pacticipant UserService --version 2.0.0 --to-environment production
npx @pact-foundation/pact-cli record-deployment \
  --pacticipant UserService --version 2.0.0 --environment production
```

## Testing

```bash
# Break a contract: remove a field the consumer expects, then verify
npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.1 --to-environment production
```

## Best Practices

- Keep contract tests on the consumer side
- Verify provider against the latest pact of every consumer
- Use provider states to control test data
- Run can-i-deploy before every production deploy
- Record deployments to track the version matrix
- Fail CI when verification fails

## Capabilities

### pact-broker
Run the Pact Broker and publish pacts from consumer builds

**Parameters:**
- `pacts_dir` (string): Directory with pact json files
- `broker_url` (string): Pact Broker base URL

**Commands:**
- `docker run -d -p 9292:9292 pactfoundation/pact-broker:latest`
- `npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0`
- `npx @pact-foundation/pact-cli list-latest-pact-versions --broker-base-url http://localhost:9292`
- `curl -s http://localhost:9292/ | grep -i pact`

**Examples:**
- npx @pact-foundation/pact-cli publish ./pacts --broker-base-url http://localhost:9292 --consumer-version 1.0.0
- npx @pact-foundation/pact-cli list-latest-pact-versions --broker-base-url http://localhost:9292
- curl -s http://localhost:9292/pacts/provider/UserService/consumer/WebApp/version/1.0.0 | jq '.interactions | length'

### deployment-gating
Check compatibility and gate deployments with can-i-deploy

**Parameters:**
- `pacticipant` (string): Service name (consumer or provider)
- `version` (string): Version to check
- `environment` (string): Target environment such as production

**Commands:**
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production`
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant WebApp --version 1.0.0 --to-environment production`
- `npx @pact-foundation/pact-cli record-deployment --pacticipant UserService --version 2.0.0 --environment production`
- `npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --latest`

**Examples:**
- npx @pact-foundation/pact-cli can-i-deploy --pacticipant UserService --version 2.0.0 --to-environment production
- npx @pact-foundation/pact-cli record-deployment --pacticipant UserService --version 2.0.0 --environment production
- npx @pact-foundation/pact-cli can-i-deploy --pacticipant WebApp --version 1.0.0 --to-environment production

## References
- [Pact Consumer-Driven Contracts](https://docs.pact.io/consumer-driven-contracts)
- [Pact CLI Docs](https://docs.pact.io/pact_broker/client_cli)
