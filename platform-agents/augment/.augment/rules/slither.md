---
type: agent_requested
description: "Run it detectors, printers, and inheritance checks on Solidity projects. printing contract info. Use when working with slither analysis, code quality or when the user mentions slither analysis, code quality."
---

Run it detectors, printers, and inheritance checks on Solidity projects. printing contract info.

## Agentic Workflow: Read -> Reason -> Act (slither)

You are **Slither** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `slither`
- Domain: Run it detectors, printers, and inheritance checks on Solidity projects. printing contract info.
- **slither-analysis**: Run Slither detectors, printers, and inheritance checks on Solidity projects — `slither contracts/`
- Check `knowledge` and `prerequisites: slither, slither-check-erc`

### 2. Reason — think for `slither`
- For `slither-analysis`: Run Slither detectors, printers, and inheritance checks on Solidity projects — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `slither` tools
- Tools: `Glob`, `Grep`, `Read`, `Slither`, `Slither-check-erc` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `slither:2b465807`

# Slither

Fast static analysis framework for Solidity that finds vulnerabilities, prints
contract structure, and generates inheritance graphs.

## When to Use

- Pre-deployment vulnerability scan of contracts
- Understanding an unfamiliar contract's structure
- CI gate for Solidity projects

## Real Commands

```bash
# Install
pip install slither-analyzer

# Analyze a project (uses truffle/hardhat config when present)
slither .

# Analyze a directory of contracts
slither contracts/

# Exclude vendored code
slither . --filter-paths node_modules

# Run specific detectors
slither --detect reentrancy-eth,uninitialized-state contracts/

# JSON report
slither . --json out.json

# Print contract summary
slither --print contract-summary contracts/Token.sol

# Check ERC compliance
slither-check-erc contracts/Token.sol --erc ERC20
```

## Common Detectors

- `reentrancy-eth` / `reentrancy-no-eth` - reentrancy
- `uninitialized-state` - uninitialized storage
- `suicidal` - selfdestruct paths
- `arbitrary-send-erc20` - arbitrary token sends

## CI

```bash
slither . --filter-paths node_modules --json slither-report.json
```

## Best Practices

- Run with the project's compiler config (hardhat.config.js / truffle-config.js)
- Combine with Mythril (symbolic execution) and manual review
- Treat every High finding as a blocker before mainnet deploy
- Check the upgradeability-detector (`--detect upgrades`) on proxy contracts

## Example Response

Lists findings as `file.sol:line: Impact: message [detector-name]`, plus the contract
summary and inheritance output requested.

## Capabilities

### slither-analysis
Run Slither detectors, printers, and inheritance checks on Solidity projects

**Parameters:**
- `detect` (string): Comma-separated detector list to run, e.g. reentrancy-eth,uninitialized-state
- `exclude` (string): Comma-separated detectors to skip
- `filter-paths` (string): Skip paths matching this regex, e.g. node_modules

**Commands:**
- `slither contracts/`
- `slither . --filter-paths node_modules`
- `slither --print contract-summary contracts/Token.sol`
- `slither --exclude-dependencies --json out.json contracts/`
- `slither-check-erc contracts/Token.sol --erc ERC20`

**Examples:**
- slither --exclude reentrancy-no-eth contracts/
- slither --detect assembly --json report.json .
- slither --print inheritance contracts/

## References
- [Slither docs](https://github.com/crytic/slither)
- [Slither wiki](https://github.com/crytic/slither/wiki)