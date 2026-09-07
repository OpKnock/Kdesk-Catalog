---
type: agent_requested
description: "Develops EVM smart contracts with Hardhat and Foundry: compilation, deployment, testing, and on-chain verification. Use when working with evm smart contracts, onchain interaction or when the user mentions evm smart contracts, onchain interaction."
---

Develops EVM smart contracts with Hardhat and Foundry: compilation, deployment, testing, and on-chain verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx hardhat compile`, `cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"`
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

**Parameters:**
- `network` (string): Target network: sepolia, mainnet
- `contract` (string): Contract name

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

**Parameters:**
- `address` (string): Contract address
- `signature` (string): Function signature
- `rpc-url` (string): RPC endpoint

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

## References
- [Solidity Docs](https://docs.soliditylang.org)
- [Hardhat Docs](https://hardhat.org/docs)
- [Foundry Book](https://book.getfoundry.sh)