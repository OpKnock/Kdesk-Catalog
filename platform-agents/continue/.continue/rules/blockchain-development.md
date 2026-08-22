---
name: "blockchain-development"
description: "Develops EVM smart contracts with Hardhat and Foundry: compilation, deployment, testing, and on-chain verification."
globs: ["**/*.go", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{ts,tsx}"]
alwaysApply: false
---

# blockchain-development

Develops EVM smart contracts with Hardhat and Foundry: compilation, deployment, testing, and on-chain verification.

## Instructions

# Blockchain Development

Build and deploy EVM smart contracts.

## When to Use

- Tokens, staking, and DeFi primitives
- DAO governance and voting
- NFT contracts and marketplaces
- Auditable, on-chain business logic

## Toolchains

- Hardhat: mature EVM dev env with TypeScript tests
- Foundry: blazing-fast Rust-based forge + cast CLI
- Anvil: local node for dev (foundry)

## Commands

```bash
# Hardhat
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.ts --network sepolia
npx hardhat verify --network sepolia 0x1234...

# Foundry
forge init
forge build
forge test -vvv
forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK

# Interaction
cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"
cast send 0xToken --private-key $PK "transfer(address,uint256)" 0xTo 1000
cast balance 0xAddress
cast block latest
```

## Example Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Greeter {
    string public greeting;

    constructor(string memory _greeting) {
        greeting = _greeting;
    }

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }
}
```

## Best Practices

- Never commit private keys; use env vars or keystores
- Test with forge fuzz and echidna invariants before audit
- Verify contracts on Etherscan after deploy
- Pin compiler versions and set evmVersion explicitly
- Always deploy to a testnet first; confirm with a block explorer

## Capabilities

### evm-smart-contracts
Compile, test, and deploy Solidity contracts.

**Commands:**
- `npx hardhat compile`
- `npx hardhat test`
- `npx hardhat run scripts/deploy.ts --network sepolia`
- `forge build`
- `forge test -vvv`

**Examples:**
- npx hardhat verify --network sepolia 0x1234...
- forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK
- npx hardhat coverage

### onchain-interaction
Query and interact with deployed contracts.

**Commands:**
- `cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"`
- `cast send 0xToken --private-key $PK "transfer(address,uint256)" 0xTo 1000`
- `cast balance 0xAddress`
- `cast code 0xContract`
- `cast block latest`

**Examples:**
- cast call 0xToken --rpc-url $RPC_URL "balanceOf(address)(uint256)" 0xAccount
- cast send --value 0.1ether 0xRecipient
- cast receipt 0xtxhash