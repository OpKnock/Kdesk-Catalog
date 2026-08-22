---
applyTo: "**/*.r **/*.sh"
---

# Tshark

Analyzes network traffic from the terminal using Wireshark's tshark CLI. Captures live packets, filters with display syntax, extracts fields to CSV, follows TCP streams, and inspects HTTP/TLS handshakes without a GUI.

## Instructions

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
