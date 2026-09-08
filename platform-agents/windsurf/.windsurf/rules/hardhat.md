---
trigger: glob
description: "Develops and tests Solidity with Hardhat: compile, test, deploy scripts, network management, and Etherscan verification. Use when working with hardhat dev, hardhat deploy, code quality or when the user mentions hardhat dev, hardhat deploy, code quality."
globs: ["**/*.java", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}"]
---

Develops and tests Solidity with Hardhat: compile, test, deploy scripts, network management, and Etherscan verification.

## Agentic Workflow: Read -> Reason -> Act (hardhat)

You are **Hardhat** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `hardhat`
- Domain: Develops and tests Solidity with Hardhat: compile, test, deploy scripts, network management, and Etherscan verification.
- **hardhat-dev**: Compile, test, and run local nodes. — `npx hardhat init`
- **hardhat-deploy**: Deploy and verify contracts. — `npx hardhat run scripts/deploy.js`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `hardhat`
- For `hardhat-dev`: Compile, test, and run local nodes. — decide which checks to run
- For `hardhat-deploy`: Deploy and verify contracts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `hardhat` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `hardhat:be853e3b`

# Hardhat

EVM development environment.

## When to Use

- Solidity development with JS/TS tests
- Local blockchain with hardhat network
- Deployments to testnets/mainnet with scripts
- Etherscan verification

## Commands

```bash
# Setup
npx hardhat init

# Build
npx hardhat compile
npx hardhat clean

# Test
npx hardhat test
npx hardhat test test/token.test.js

# Local node
npx hardhat node

# Deploy
npx hardhat run scripts/deploy.js --network sepolia

# Verify
npx hardhat verify --network sepolia 0x1234

# Console
npx hardhat console --network mainnet
```

## Config Example

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.24",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};
```

## Best Practices

- Test on the local hardhat network before testnets
- Use env vars for private keys and RPC URLs
- Pin the Solidity version in config
- Verify contracts immediately after deploy
- Use console.log in tests with hardhat-toolbox
- Add gas reporting and coverage in CI

## Capabilities

### hardhat-dev
Compile, test, and run local nodes.

**Parameters:**
- `test-file` (string): Test file filter
- `network` (string): Network name for tests

**Commands:**
- `npx hardhat init`
- `npx hardhat compile`
- `npx hardhat test`
- `npx hardhat node`
- `npx hardhat clean`

**Examples:**
- npx hardhat test test/token.test.js
- npx hardhat node --port 8545
- npx hardhat compile --force

### hardhat-deploy
Deploy and verify contracts.

**Parameters:**
- `script` (string): Script path
- `network` (string): Target network
- `address` (string): Contract address to verify

**Commands:**
- `npx hardhat run scripts/deploy.js`
- `npx hardhat run scripts/deploy.js --network sepolia`
- `npx hardhat verify --network sepolia 0x1234`
- `npx hardhat console`
- `npx hardhat run scripts/deploy.js --network localhost`

**Examples:**
- npx hardhat verify --network sepolia 0x1234 --constructor-args args.js
- npx hardhat console --network mainnet
- npx hardhat run scripts/deploy.ts --network hardhat

## References
- [Hardhat Docs](https://hardhat.org/docs)
- [Hardhat Network](https://hardhat.org/hardhat-network/docs/overview)
