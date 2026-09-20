---
applyTo: "**/*.r **/*.sh"
---

# Truffle

Develops, compiles, tests, and deploys Ethereum smart contracts with the Truffle suite.

## Instructions

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
