---
trigger: glob
description: "Capture and analyze packets with it filters. Use when working with tcpdump capture, api or when the user mentions tcpdump capture, api."
globs: ["**/*.r", "**/*.sh"]
---

Capture and analyze packets with it filters.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tcpdump -i eth0 -nn port 443`
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

# tcpdump

Hand-crafted skill for capturing and reading network traffic.

## What this skill does

- Captures live packets with BPF filters on ports and hosts
- Writes pcap files for later analysis
- Inspects payloads with -A (ASCII) and -X (hex) dumps

## When to use

- Is an API request even leaving the host?
- What payload did the client send to port 5432?
- Reproducing a network bug from a captured pcap

## Real commands

```bash
# Live capture on 443 with numeric output
tcpdump -i eth0 -nn port 443

# Any interface, verbose, stop after 100 packets
tcpdump -i any -nnv -c 100

# Capture to a file (full payloads)
tcpdump -i eth0 -w capture.pcap -s 0

# Read and filter the file
tcpdump -r capture.pcap -nn 'tcp port 8080'

# Payload as ASCII
tcpdump -i eth0 -A -c 20 'tcp port 80'

# Hex + ASCII dump
tcpdump -X -r capture.pcap | head -50

# Host and port combo
tcpdump -i eth0 -nn host 10.0.0.5 and port 5432

# SYN packets only (TCP flags bit 2)
tcpdump -r capture.pcap -nn 'tcp[13] & 2 != 0'
```

## Capture workflow

1. tcpdump -i eth0 -w file.pcap -s 0 'port 443'
2. Reproduce the issue
3. Ctrl+C, then tcpdump -r file.pcap -nn

## Testing

```bash
tcpdump -i lo -nn port 8080 &
curl -s localhost:8080/health
kill %1
```

## Best practices

- Always use -nn to skip slow DNS/service lookups
- Use -c N to bound live captures
- Prefer pcap files over live output for anything longer than a minute

## Capabilities

### tcpdump-capture
Capture and analyze packets with tcpdump filters

**Parameters:**
- `interface` (string): Capture interface, e.g. eth0 or any
- `filter` (string): BPF filter expression
- `pcap_file` (string): Capture or read file name

**Commands:**
- `tcpdump -i eth0 -nn port 443`
- `tcpdump -i any -nnv -c 100`
- `tcpdump -i eth0 -w capture.pcap -s 0`
- `tcpdump -r capture.pcap -nn 'tcp port 8080'`
- `tcpdump -i eth0 -A -c 20 'tcp port 80'`
- `tcpdump -X -r capture.pcap | head -50`

**Examples:**
- tcpdump -i eth0 -nn host 10.0.0.5 and port 5432
- tcpdump -r capture.pcap -nn 'tcp[13] & 2 != 0'
- tcpdump -i any -nn -c 50 port 53

## References
- [tcpdump man page](https://www.tcpdump.org/manpages/tcpdump.1.html)
- [pcap-filter man page](https://www.tcpdump.org/manpages/pcap-filter.7.html)
