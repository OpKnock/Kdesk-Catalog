---
name: "hardhat"
description: "Develops and tests Solidity with Hardhat: compile, test, deploy scripts, network management, and Etherscan verification."
---

# Hardhat

Develops and tests Solidity with Hardhat: compile, test, deploy scripts, network management, and Etherscan verification.

## Instructions

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
