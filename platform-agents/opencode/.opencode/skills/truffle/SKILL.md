---
name: "truffle"
description: "Develops, compiles, tests, and deploys Ethereum smart contracts with the Truffle suite. Use when working with truffle workflow, code quality or when the user mentions truffle workflow, code quality."
---

Develops, compiles, tests, and deploys Ethereum smart contracts with the Truffle suite.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `truffle init`
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

# Truffle

Development environment, testing framework, and asset pipeline for Ethereum
contracts.

## When to Use

- Scaffolding a Solidity project with migrations
- Running contract tests against Ganache
- Deploying to test networks and mainnet

## Real Commands

```bash
# Scaffold a project
truffle init

# Compile contracts
sudo truffle compile

# Run tests
sudo truffle test
sudo truffle test ./test/Token.test.js

# Start the built-in dev network and console
sudo truffle develop

# Migrate (deploy) to a configured network
sudo truffle migrate --network development --reset

# Deploy a specific migration
sudo truffle migrate --f 2 --to 2 --network development

# Interactive console on a network
sudo truffle console --network mainnet

# Run a script with Truffle artifacts
sudo truffle exec scripts/seed.js
```

## Example Test (test/Token.test.js)

```js
const Token = artifacts.require('Token');

contract('Token', (accounts) => {
  it('mints to owner', async () => {
    const t = await Token.deployed();
    await t.mint(accounts[1], 1000);
    assert.equal((await t.balanceOf(accounts[1])).toString(), '1000');
  });
});
```

## Best Practices

- Use `--reset` only on disposable networks
- Keep migrations idempotent; re-runs must not double-deploy
- Test with `truffle develop`, deploy with a network that matches your target
- Verify contracts on Etherscan after deployment

## Example Response

Shows compile warnings, test pass/fail summary with gas usage, and migration
addresses with transaction hashes.

## Capabilities

### truffle-workflow
Compile, test, migrate, and interact with contracts via Truffle

**Parameters:**
- `network` (string): Network name from truffle-config.js to target
- `reset` (boolean): Re-run all migrations from scratch
- `verbose-rpc` (boolean): Log every RPC request/response during migration

**Commands:**
- `truffle init`
- `truffle compile`
- `truffle test ./test/Token.test.js`
- `truffle migrate --network development --reset`
- `truffle console --network mainnet`

**Examples:**
- truffle develop
- truffle migrate --network rinkeby --verbose-rpc
- truffle exec scripts/seed.js

## References
- [Truffle suite docs](https://archive.trufflesuite.com/docs/)
- [Truffle networks guide](https://archive.trufflesuite.com/docs/truffle/reference/configuration/)
