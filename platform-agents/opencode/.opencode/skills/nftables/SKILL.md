---
name: "nftables"
description: "Manages firewall rules using nftables to create tables, chains, rules, and sets, and applies persistent configuration files enabling packet filtering. Use when working with nftables rules, api or when the user mentions nftables rules, api."
---

Manages firewall rules using nftables to create tables, chains, rules, and sets, and applies persistent configuration files enabling packet filtering.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nft list ruleset`
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

# nftables

nftables is the modern Linux packet filtering framework, successor to iptables.

## What this skill does

- Creates tables, chains and rules
- Uses sets for efficient address/port matching
- Applies persistent rule files

## When to use

- Replacing iptables with nftables
- Writing firewall rules for new servers

## Real commands

```bash
# Inspect current ruleset
nft list ruleset

# Table and base chain
nft add table inet filter
nft add chain inet filter input '{ type filter hook input priority 0; policy drop; }'

# Rules
nft add rule inet filter input tcp dport 22 accept
nft add rule inet filter input tcp dport 443 accept
nft add rule inet filter input ct state established,related accept

# Delete a rule by handle
nft -a list chain inet filter input
nft delete rule inet filter input handle 3

# Apply config file
nft -f /etc/nftables.conf
```

## Config file

```nft
#!/usr/sbin/nft -f
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    tcp dport 22 accept
    iif lo accept
  }
}
```

## Best practices

- Always keep a policy that still allows your SSH (or fallback access)
- Test with `nft -c -f` (check mode) before applying
- Persist to /etc/nftables.conf and enable the service

## Capabilities

### nftables-rules
Create tables/chains/rules, manage sets and apply nftables config files.

**Parameters:**
- `table` (string): Table name and family, e.g. inet filter
- `chain` (string): Chain name with hook and policy
- `rule` (string): nft rule expression

**Commands:**
- `nft list ruleset`
- `nft add table inet filter`
- `nft add chain inet filter input '{ type filter hook input priority 0; policy drop; }'`
- `nft add rule inet filter input tcp dport 22 accept`
- `nft -f /etc/nftables.conf`

**Examples:**
- nft add rule inet filter input tcp dport 443 accept
- nft add set inet filter allowed '{ type ipv4_addr; flags interval; }'
- nft list ruleset | grep -A5 'chain input'

## References
- [nftables Wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
- [nft man page](https://man7.org/linux/man-pages/man8/nft.8.html)
