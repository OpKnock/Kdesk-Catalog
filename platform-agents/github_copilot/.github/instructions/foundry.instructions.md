---
applyTo: "**/*.r **/*.rs **/*.sh"
---

Develops Solidity with Foundry: forge build/test/fuzz, cast interactions, anvil local node, and deployment scripts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `forge init myapp`, `cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"`
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

# Foundry

Rust-based Solidity development toolkit.

## When to Use

- Fast contract compilation and tests
- Fuzz and invariant testing
- On-chain interaction without custom tooling
- Local forking with anvil

## Commands

```bash
# Project
forge init myapp
forge build
forge build --sizes

# Test
forge test
forge test -vvv
forge test --fuzz-runs 1000
forge test --gas-report

# Deploy
forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK
forge script script/Deploy.s.sol:Deploy --rpc-url $RPC_URL --broadcast

# Interact
cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"
cast send 0xToken --private-key $PK "transfer(address,uint256)" 0xTo 1000
cast balance 0xAddress
cast block latest
cast sig "transfer(address,uint256)"

# Local node
anvil
anvil --fork-url $RPC_URL
```

## Test Example

```solidity
function testMintOnlyOwner() public {
    vm.prank(owner);
    token.mint(address(this), 100);
    assertEq(token.balanceOf(address(this)), 100);
}
```

## Best Practices

- Never put private keys in command history; use env vars
- Use vm.prank/vm.expectRevert in tests
- Run fuzz campaigns before audits
- Test against an anvil fork of mainnet for integration
- Use cast sig to double-check selectors
- Keep scripts idempotent; verify with --slow on mainnet

## Capabilities

### forge-build-test
Build, test, and fuzz contracts.

**Parameters:**
- `match-test` (string): Test name filter
- `fuzz-runs` (integer): Fuzz iterations

**Commands:**
- `forge init myapp`
- `forge build`
- `forge test`
- `forge test -vvv`
- `forge test --fuzz-runs 1000`

**Examples:**
- forge test --match-test testOnlyOwner -vvvv
- forge test --gas-report
- forge build --sizes

### cast-ops
Interact with chains and contracts.

**Parameters:**
- `address` (string): Contract address
- `signature` (string): Function signature
- `rpc-url` (string): RPC endpoint

**Commands:**
- `cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"`
- `cast send 0xToken --private-key $PK "transfer(address,uint256)" 0xTo 1000`
- `cast balance 0xAddress`
- `cast block latest`
- `cast code 0xContract`

**Examples:**
- cast call --rpc-url $RPC_URL 0xToken "balanceOf(address)(uint256)" 0xAccount
- cast receipt 0xtxhash --rpc-url $RPC_URL
- cast sig "transfer(address,uint256)"

### forge-deploy
Deploy contracts and run scripts.

**Parameters:**
- `contract` (string): Contract path:Name
- `broadcast` (boolean): Broadcast the transaction

**Commands:**
- `forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK`
- `forge script script/Deploy.s.sol:Deploy --rpc-url $RPC_URL --broadcast`
- `forge script script/Deploy.s.sol --fork-url $RPC_URL --verify`
- `anvil`

**Examples:**
- forge script script/Deploy.s.sol --rpc-url $RPC_URL --broadcast --slow
- anvil --fork-url $RPC_URL
- forge create src/Token.sol:Token --constructor-args "MyToken" "MTK" 18

## References
- [Foundry Book](https://book.getfoundry.sh)
- [Forge Test Reference](https://book.getfoundry.sh/forge/test-examples)
