---
trigger: glob
description: "Fuzzes Ethereum smart contracts with Echidna: property-based invariant testing, corpus, and CI integration."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Echidna

Fuzzes Ethereum smart contracts with Echidna: property-based invariant testing, corpus, and CI integration.

## Instructions

# Echidna

Fuzz EVM smart contracts with property testing.

## When to Use

- Verifying invariants (balance sums, roles, limits)
- Finding assertion failures in complex contracts
- Testing upgrade and reentrancy scenarios
- Pre-audit and CI regression checks

## Invariant Example

```solidity
// test/Invariants.sol
import "echidna/Test.sol";

contract Invariants is Test {
    Vault vault;

    function setUp() public {
        vault = new Vault();
    }

    // total supply must equal sum of balances
    function echidna_total_never_changes() public view returns (bool) {
        return vault.total() == vault.balanceOf(address(this));
    }
}
```

## Commands

```bash
# Property fuzzing
echidna test/Invariants.sol

# Assertion mode (fail on assert failures)
echidna test/Invariants.sol --test-mode assertion

# Limit the campaign
echidna test/Invariants.sol --test-limit 100000

# Config driven
echidna test/Invariants.sol --config echidna.yaml

# Corpus for reuse
echidna test/Invariants.sol --corpus-dir corpus
```

## Config Example

```yaml
# echidna.yaml
testMode: assertion
testLimit: 50000
seqLen: 100
deployer: "0x30000"
sender: ["0x10000", "0x20000"]
```

## Best Practices

- Write invariants as named echidna_* functions
- Use --test-mode assertion for existing assert tests
- Save corpora to accelerate future runs
- Run a long campaign (millions of calls) before audits
- Shrink sequences on failure to find minimal repro
- Integrate into CI with a fixed fuzz budget

## Capabilities

### echidna-fuzz
Run property-based fuzzing campaigns.

**Commands:**
- `echidna test/Invariants.sol`
- `echidna test/Invariants.sol --test-mode assertion`
- `echidna test/Invariants.sol --test-limit 100000`
- `echidna test/Invariants.sol --config echidna.yaml`
- `echidna test/Invariants.sol --corpus-dir corpus`

**Examples:**
- echidna test/Invariants.sol --test-mode assertion --test-limit 50000
- echidna test/Invariants.sol --config echidna.yaml --corpus-dir corpus
- echidna test/Invariants.sol --seq-len 100

### echidna-analysis
Analyze and shrink failing sequences.

**Commands:**
- `echidna test/Invariants.sol --test-mode property --test-limit 0`
- `echidna test/Invariants.sol --format text`
- `echidna test/Invariants.sol --list-tests`
- `echidna test/Invariants.sol --deployer 0x30000`

**Examples:**
- echidna test/Invariants.sol --test-limit 0 --format text
- echidna test/Invariants.sol --seq-len 100 --test-limit 5000
