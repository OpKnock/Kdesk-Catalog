# Tcpdump

Capture and analyze packets with it filters.

## Instructions

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
