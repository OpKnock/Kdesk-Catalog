---
name: "wireshark"
description: "Capture and analyze API network traffic using tshark (Wireshark's CLI) and the Wireshark GUI. Use BPF capture filters, display filters, field extraction, and protocol statistics to debug HTTP/TLS issues."
---

# Wireshark

Capture and analyze API network traffic using tshark (Wireshark's CLI) and the Wireshark GUI. Use BPF capture filters, display filters, field extraction, and protocol statistics to debug HTTP/TLS issues.

## Instructions

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
