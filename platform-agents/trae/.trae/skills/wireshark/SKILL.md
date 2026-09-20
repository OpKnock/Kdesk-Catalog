---
name: "wireshark"
description: "Capture and analyze API network traffic using tshark (Wireshark's CLI) and the Wireshark GUI. Use BPF capture filters, display filters, field extraction, and protocol statistics to debug HTTP/TLS issues. Use when working with packet capture, api or when the user mentions packet capture, api."
license: "MIT"
compatibility: "Requires dumpcap, tshark."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(dumpcap:*) Bash(tshark:*)"
---

Capture and analyze API network traffic using tshark (Wireshark's CLI) and the Wireshark GUI. Use BPF capture filters, display filters, field extraction, and protocol statistics to debug HTTP/TLS issues.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tshark -i eth0 -f 'tcp port 443' -w capture.pcapng`
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

# Wireshark / tshark

## What this skill does
Capture and analyze API network traffic using tshark (Wireshark's CLI) and the Wireshark GUI. Use BPF capture filters, display filters, field extraction, and protocol statistics to debug HTTP/TLS issues.

## When to use
- Debugging slow or failing API requests
- Verifying TLS handshakes and SNI
- Confirming payloads leave the client unchanged

## Real commands
```bash
# Capture HTTPS traffic to file
sudo tshark -i eth0 -f 'tcp port 443' -w capture.pcapng

# Capture local API traffic for 60s
dumpcap -i lo -f 'tcp port 8080' -a duration:60 -w api.pcapng

# List HTTP requests
 tshark -r capture.pcapng -Y 'http.request' -T fields -e http.host -e http.request.uri

# Error responses
 tshark -r capture.pcapng -Y 'http.response.code >= 400' -T fields -e http.response.code -e http.request.uri | head

# Protocol hierarchy stats
tshark -r capture.pcapng -z io,phs

# TLS SNI values
tshark -r capture.pcapng -Y 'tls.handshake.type == 1' -T fields -e tls.handshake.extensions_server_name

# Unique POST user agents
tshark -r capture.pcapng -Y 'http.request.method == POST' -T fields -e http.user_agent | sort | uniq -c
```

## Common filters
```
http.request
http.response.code >= 400
tcp.port == 8080
ip.addr == 10.0.0.5
dns.qry.name contains api
```

## Best practices
- Capture with BPF filters to keep files small
- Use `-a duration:N` or `-c N` to bound captures
- Decrypt TLS with a keylog file for payload inspection
- Correlate with server logs by timestamp and IP

## Testing
```bash
sudo tshark -i lo -f 'tcp port 8080' -a duration:10 -w test.pcapng &
curl -s http://localhost:8080/api/users > /dev/null
sleep 12
 tshark -r test.pcapng -Y 'http.request' -T fields -e http.request.method -e http.request.uri
```

## Capabilities

### packet-capture
Capture and analyze network traffic for API debugging

**Parameters:**
- `interface` (string): Capture interface, e.g. eth0, lo, Wi-Fi
- `filter` (string): BPF capture filter, e.g. 'tcp port 443'
- `duration` (string): Stop capture after N seconds (-a duration:N)

**Commands:**
- `tshark -i eth0 -f 'tcp port 443' -w capture.pcapng`
- `tshark -r capture.pcapng -Y 'http.request' -T fields -e http.host -e http.request.uri`
- `tshark -r capture.pcapng -Y 'http.response.code >= 400' -T fields -e http.response.code -e http.request.uri | head`
- `tshark -r capture.pcapng -z io,phs`
- `dumpcap -i eth0 -c 5000 -w sample.pcapng`

**Examples:**
- tshark -i lo -f 'tcp port 8080' -a duration:60 -w api.pcapng
- tshark -r capture.pcapng -Y 'http.request.method == POST' -T fields -e ip.src -e http.user_agent | sort | uniq -c
- tshark -r capture.pcapng -Y 'tls.handshake.type == 1' -T fields -e tls.handshake.extensions_server_name

## References
- [Wireshark Docs](https://www.wireshark.org/docs/)
- [tshark man page](https://www.wireshark.org/docs/man-pages/tshark.html)
