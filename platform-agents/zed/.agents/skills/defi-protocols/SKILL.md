---
name: "defi-protocols"
description: "Develops and tests DeFi protocols with Foundry: compile, test, fork mainnet, and deploy. Use when working with foundry workflow or when the user mentions foundry workflow."
license: "MIT"
compatibility: "Requires solidity, uniswap, aave, hardhat, the-graph."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "web3"}
allowed-tools: "Glob Grep Read Bash(cast:*) Bash(forge:*)"
---

Develops and tests DeFi protocols with Foundry: compile, test, fork mainnet, and deploy.

## Agentic Workflow: Read -> Reason -> Act (defi-protocols)

You are **defi-protocols** (web3) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — web3 context for `defi-protocols`
- Domain: Develops and tests DeFi protocols with Foundry: compile, test, fork mainnet, and deploy.
- **foundry-workflow**: Build, test, and deploy smart contracts with forge and cast — `forge init my_protocol`
- Check `knowledge` and `prerequisites: solidity, uniswap, aave, hardhat`

### 2. Reason — think for `defi-protocols`
- For `foundry-workflow`: Build, test, and deploy smart contracts with forge and cast — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `defi-protocols` tools
- Tools: `Glob`, `Grep`, `Read`, `Forge`, `Cast` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `defi-protocols:c3216307`

# DeFi Protocols

Develops DeFi contracts with Foundry: fuzz/unit tests, mainnet forks for
integration tests, and deployment.

## When to Use

- Building ERC-20/ERC-721 or AMM-style contracts
- Testing against real mainnet state (forks)
- Verifying invariants with fuzzing

## Real Commands

```bash
# Scaffold
sudo forge init my_protocol

# Compile
sudo forge build

# Unit + fuzz tests with verbosity
sudo forge test --match-test testFuzz_* -vvv

# Fork mainnet for integration tests
sudo forge test --fork-url $RPC_URL --fork-block-number 19000000

# Gas report
sudo forge test --gas-report

# Deploy
sudo forge create src/Token.sol:Token \
  --rpc-url $RPC_URL --private-key $PRIVATE_KEY --broadcast

# Interact with cast
sudo cast call 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D "totalSupply()(uint256)" --rpc-url $RPC_URL
sudo cast balance 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B --rpc-url $RPC_URL
```

## Test Example (test/Token.t.sol)

```solidity
contract TokenTest is Test {
    function testMint(uint256 amount) public {
        vm.assume(amount < 1e30);
        token.mint(address(this), amount);
        assertEq(token.balanceOf(address(this)), amount);
    }
}
```

## Best Practices

- Write invariants and fuzz them, not just happy paths
- Test with mainnet forks for DeFi integrations
- Check reentrancy: use OpenZeppelin ReentrancyGuard or checks-effects-interactions
- Audit before mainnet; run slither and mythril as a first pass
- Never log or commit private keys

## Example Response

Builds and tests the protocol, reports pass/fail and gas per function, then
outlines the deployment and verification steps.

## Capabilities

### foundry-workflow
Build, test, and deploy smart contracts with forge and cast

**Parameters:**
- `match-test` (string): Test name filter, e.g. testFuzz_*
- `fork-url` (string): RPC URL to fork mainnet state for tests
- `fork-block-number` (integer): Block to fork at for deterministic tests

**Commands:**
- `forge init my_protocol`
- `forge build`
- `forge test --match-test testFuzz_* -vvv`
- `forge test --fork-url $RPC_URL --fork-block-number 19000000`
- `cast call 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D "totalSupply()(uint256)" --rpc-url $RPC_URL`

**Examples:**
- forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK
- cast balance 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B --rpc-url $RPC_URL
- forge test --gas-report

## References
- [Foundry Book](https://book.getfoundry.sh/)
- [EIP-20 token standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin contracts](https://docs.openzeppelin.com/contracts/)
