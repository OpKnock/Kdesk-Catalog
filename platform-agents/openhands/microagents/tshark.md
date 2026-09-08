---
name: "tshark"
description: "Analyzes network traffic from the terminal using Wireshark's tshark CLI. Captures live packets, filters with display syntax, extracts fields to CSV, follows TCP streams, and inspects HTTP/TLS handshakes without a GUI. Use when working with capture analyze, api, network, troubleshooting or when the user mentions capture analyze, api, network, troubleshooting."
type: knowledge
triggers: ["tshark", "capture-analyze"]
---

Analyzes network traffic from the terminal using Wireshark's tshark CLI. Captures live packets, filters with display syntax, extracts fields to CSV, follows TCP streams, and inspects HTTP/TLS handshakes without a GUI.

## Agentic Workflow: Read -> Reason -> Act (tshark)

You are **Tshark** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `tshark`
- Domain: Analyzes network traffic from the terminal using Wireshark's tshark CLI. Captures live packets, filters with display syntax, extracts fields to CSV, follows TCP streams, and inspects HTTP/TLS handshak
- **capture-analyze**: Capture, filter, and decode packets from the CLI — `tshark -i eth0 -f "tcp port 443" -w capture.pcapng -c 1000`
- Check `knowledge` and `prerequisites: tshark`

### 2. Reason — think for `tshark`
- For `capture-analyze`: Capture, filter, and decode packets from the CLI — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tshark` tools
- Tools: `Glob`, `Grep`, `Read`, `Tshark` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tshark:cf61bfe4`

# Tshark

CLI packet analysis with Wireshark's tshark.

## What this skill does

- Captures live traffic to pcapng with capture filters
- Decodes and filters captures with display filters
- Extracts individual fields into CSV/plain output
- Follows TCP streams from the terminal

## When to use

- Reproducing connectivity bugs without Wireshark GUI
- Extracting request URLs or SNI hostnames at scale
- Auditing what a service actually sends on the wire

## Real commands

```bash
# Capture 1000 packets of 443 traffic
tshark -i eth0 -f "tcp port 443" -w capture.pcapng -c 1000

# Display-filter analysis
tshark -r capture.pcapng -Y "http.request"
tshark -r capture.pcapng -Y "tls.handshake.type==1"

# Field extraction
tshark -r capture.pcapng -T fields -e http.host -e http.request.uri
tshark -r capture.pcapng -T fields -e ip.src -e tcp.port

# Follow stream 0 (handshake stream index from first frames)
tshark -r capture.pcapng -z follow,tcp,ascii,0

# SNI from TLS handshakes
tshark -r capture.pcapng -Y "tls.handshake.type==1" -T fields -e tls.handshake.extensions_server_name
```

## Common filters

- http.request / http.response
- dns.qry.name
- tls.handshake.extensions_server_name
- ip.addr == 10.0.0.5
- tcp.flags.syn == 1

## Testing

```bash
tshark -r capture.pcapng -Y "http.request" | wc -l
tshark -r capture.pcapng -T fields -e http.request.uri
```

## Best practices

- Use capture filters (-f) for big captures, display filters (-Y) for analysis
- Prefer field extraction (-T fields) over parsing text output
- Redact payloads before sharing captures

## Capabilities

### capture-analyze
Capture, filter, and decode packets from the CLI

**Parameters:**
- `interface` (string): Interface to capture, e.g. eth0
- `filter` (string): Display filter, e.g. http.request
- `fields` (string): Comma-separated field extractors

**Commands:**
- `tshark -i eth0 -f "tcp port 443" -w capture.pcapng -c 1000`
- `tshark -r capture.pcapng -Y "http.request"`
- `tshark -r capture.pcapng -T fields -e http.host -e http.request.uri`
- `tshark -r capture.pcapng -z follow,tcp,ascii,0`
- `tshark -r capture.pcapng -Y "tls.handshake.type==1" -T fields -e tls.handshake.extensions_server_name`

**Examples:**
- tshark -r capture.pcapng -Y "http.request"
- tshark -r capture.pcapng -T fields -e ip.src -e tcp.port
- tshark -i eth0 -Y "dns" -T fields -e dns.qry.name

## References
- [tshark man page](https://www.wireshark.org/docs/man-pages/tshark.html)
- [Display filters reference](https://www.wireshark.org/docs/dfref/)
- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [TLS handshake analysis](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTLS.html)
