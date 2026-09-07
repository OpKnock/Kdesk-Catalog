---
name: "defi-protocols"
description: "Develops and tests DeFi protocols with Foundry: compile, test, fork mainnet, and deploy. Use when working with foundry workflow or when the user mentions foundry workflow."
---

Develops and tests DeFi protocols with Foundry: compile, test, fork mainnet, and deploy.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `forge init my_protocol`
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
