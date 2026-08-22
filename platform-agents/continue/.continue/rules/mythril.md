---
name: "Mythril"
description: "Security analysis of Ethereum smart contracts with Mythril, finding reentrancy, overflow, and other EVM vulnerabilities."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Mythril

Security analysis of Ethereum smart contracts with Mythril, finding reentrancy, overflow, and other EVM vulnerabilities.

## Instructions

# Mythril

Symbolic-execution security analyzer for Ethereum smart contracts. Flags reentrancy,
integer over/underflow, and dangerous call patterns.

## When to Use

- Auditing a contract before deployment
- Analyzing an already-deployed contract on-chain
- Checking that a fix removed the flagged vulnerability

## Real Commands

```bash
# Install via Docker (recommended)
docker pull mythril/myth

# Analyze a source file
docker run -v $(pwd):/tmp mythril/myth analyze /tmp/Token.sol

# Analyze with a timeout
myth analyze --execution-timeout 120 contracts/Vault.sol

# Analyze a deployed contract
myth analyze -a 0xABC123 --rpc https://eth.llamarpc.com --blocks 5

# With custom solc settings
myth analyze --solc-json solc.json contracts/

# Control the graph output
myth analyze --graph contracts/Counter.sol
```

## Detector Example Output

```
==== Reentrancy ====
SWC ID: 107
Severity: High
In function: withdraw(uint256)
State variables written after the call:
  balances[msg.sender]
```

## Best Practices

- Run on a local fork with `--rpc` against staging, never mainnet with live funds
- Pair Mythril with Slither and a manual review; no tool is exhaustive
- Use `--execution-timeout` to bound long analysis runs
- Re-run after every Solidity change; issues disappear quickly

## Example Response

A reentrancy finding is reported with SWC ID 107, affected function, and the
state-variable write that happens after the external call; the agent suggests the
checks-effects-interactions fix.

## Capabilities

### smart-contract-analysis
Run Mythril symbolic-execution analysis against Solidity contracts

**Commands:**
- `myth analyze contracts/Token.sol`
- `myth analyze --execution-timeout 120 contract.sol`
- `myth analyze -a 0x1234... --rpc https://eth.llamarpc.com --blocks 5`
- `myth analyze --solc-json solc.json contracts/`
- `myth analyze --mode diamond --favorites detector-reentrancy contracts/`

**Examples:**
- myth analyze --execution-timeout 90 contracts/Vault.sol
- myth analyze -a 0xdeadbeef --infura-id $INFURA_ID
- myth analyze --graph contracts/Tok.sol