---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Fuzzes Ethereum smart contracts with Echidna: property-based invariant testing, corpus, and CI integration.

## Agentic Workflow: Read -> Reason -> Act (echidna)

You are **Echidna** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `echidna`
- Domain: Fuzzes Ethereum smart contracts with Echidna: property-based invariant testing, corpus, and CI integration.
- **echidna-fuzz**: Run property-based fuzzing campaigns. — `echidna test/Invariants.sol`
- **echidna-analysis**: Analyze and shrink failing sequences. — `echidna test/Invariants.sol --test-mode property --test-limit 0`
- Check `knowledge` and `prerequisites: echidna`

### 2. Reason — think for `echidna`
- For `echidna-fuzz`: Run property-based fuzzing campaigns. — decide which checks to run
- For `echidna-analysis`: Analyze and shrink failing sequences. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `echidna` tools
- Tools: `Glob`, `Grep`, `Read`, `Echidna` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `echidna:666ee85c`

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

**Parameters:**
- `contract` (string): Solidity file
- `test-limit` (integer): Max test calls
- `config` (string): Config yaml path

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

**Parameters:**
- `deployer` (string): Deployer address
- `format` (string): text or json

**Commands:**
- `echidna test/Invariants.sol --test-mode property --test-limit 0`
- `echidna test/Invariants.sol --format text`
- `echidna test/Invariants.sol --list-tests`
- `echidna test/Invariants.sol --deployer 0x30000`

**Examples:**
- echidna test/Invariants.sol --test-limit 0 --format text
- echidna test/Invariants.sol --seq-len 100 --test-limit 5000

## References
- [Echidna Docs](https://echidna.readthedocs.io)
- [Echidna on GitHub](https://github.com/crytic/echidna)
