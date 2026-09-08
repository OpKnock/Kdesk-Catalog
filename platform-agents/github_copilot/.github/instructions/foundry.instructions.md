---
applyTo: "**/*.r **/*.rs **/*.sh"
---

Develops Solidity with Foundry: forge build/test/fuzz, cast interactions, anvil local node, and deployment scripts.

## Agentic Workflow: Read -> Reason -> Act (foundry)

You are **Foundry** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `foundry`
- Domain: Develops Solidity with Foundry: forge build/test/fuzz, cast interactions, anvil local node, and deployment scripts.
- **forge-build-test**: Build, test, and fuzz contracts. — `forge init myapp`
- **cast-ops**: Interact with chains and contracts. — `cast call 0xToken --rpc-url $RPC_URL "symbol()(string)"`
- **forge-deploy**: Deploy contracts and run scripts. — `forge create src/Token.sol:Token --rpc-url $RPC_URL --private-key $PK`
- Check `knowledge` and `prerequisites: anvil, cast, forge`

### 2. Reason — think for `foundry`
- For `forge-build-test`: Build, test, and fuzz contracts. — decide which checks to run
- For `cast-ops`: Interact with chains and contracts. — decide which checks to run
- For `forge-deploy`: Deploy contracts and run scripts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `foundry` tools
- Tools: `Glob`, `Grep`, `Read`, `Forge`, `Cast` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `foundry:21815d5b`

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
