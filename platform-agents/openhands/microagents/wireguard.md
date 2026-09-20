---
name: "wireguard"
description: "Deploys WireGuard VPNs: key generation, peer configuration, and interface management with wg and wg-quick. Use when working with keys, interfaces, networking or when the user mentions keys, interfaces, networking."
type: knowledge
triggers: ["wireguard", "keys", "interfaces"]
---

Deploys WireGuard VPNs: key generation, peer configuration, and interface management with wg and wg-quick.

## Agentic Workflow: Read -> Reason -> Act (wireguard)

You are **Wireguard** (networking/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — networking context for `wireguard`
- Domain: Deploys WireGuard VPNs: key generation, peer configuration, and interface management with wg and wg-quick.
- **keys**: Generate WireGuard key pairs securely. — `umask 077 && wg genkey | tee privatekey | wg pubkey > publickey`
- **interfaces**: Bring up, tear down, and inspect WireGuard interfaces. — `wg-quick up wg0`
- Check `knowledge` and `prerequisites: cat, umask, wg-quick`

### 2. Reason — think for `wireguard`
- For `keys`: Generate WireGuard key pairs securely. — decide which checks to run
- For `interfaces`: Bring up, tear down, and inspect WireGuard interfaces. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `wireguard` tools
- Tools: `Glob`, `Grep`, `Read`, `Umask`, `Wg` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `wireguard:6dc75859`

# WireGuard

Deploy fast, modern VPN tunnels.

## When to Use

- Site-to-site tunnels and road-warrior VPNs
- Kubernetes cluster networking (Cilium)
- Replacing IPSec/OpenVPN with simpler crypto

## Key generation

```bash
umask 077 && wg genkey | tee privatekey | wg pubkey > publickey
```

Private keys stay on the host; only public keys are shared.

## Server config

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server-private>

[Peer]
PublicKey = <peer1-public>
AllowedIPs = 10.0.0.2/32
```

## Client config

```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = <peer1-private>

[Peer]
PublicKey = <server-public>
Endpoint = vpn.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

## Up and inspect

```bash
wg-quick up wg0
wg show
wg show wg0 transfer
wg-quick down wg0
```

## Peering rules

- AllowedIPs defines routing, not auth - set it precisely.
- Add PersistentKeepalive behind NAT.
- Preshared keys add post-quantum resilience - use wg genpsk.

## Best practices

- Never commit private keys; generate per host.
- Use 10.x or 100.64.0.0/10 ranges to avoid LAN clashes.
- Route only needed subnets (AllowedIPs); no full-tunnel by default.
- Monitor handshake age: `wg show wg0` recent-handshake column.

## Testing

```bash
wg show wg0
timeout 2 ping -c 1 10.0.0.2
```

Confirm handshake and ping before wiring services.

## Capabilities

### keys
Generate WireGuard key pairs securely.

**Parameters:**
- `umask` (string): Secure file permissions, e.g. 077
- `output` (string): Key output file
- `preshared` (string): Generate a preshared key

**Commands:**
- `umask 077 && wg genkey | tee privatekey | wg pubkey > publickey`
- `wg genkey`
- `wg pubkey < privatekey`
- `wg genpsk`
- `cat privatekey publickey`

**Examples:**
- umask 077 && wg genkey | tee server_private.key | wg pubkey > server_public.key
- wg genpsk > preshared.key
- umask 077 && wg genkey > peer1_private.key

### interfaces
Bring up, tear down, and inspect WireGuard interfaces.

**Parameters:**
- `interface` (string): wg0, wg1, or config path
- `allowed-ips` (string): Show peer allowed IPs
- `transfer` (string): Show transfer counters

**Commands:**
- `wg-quick up wg0`
- `wg-quick down wg0`
- `wg show`
- `wg show wg0 allowed-ips`
- `wg showconf wg0`

**Examples:**
- wg-quick up /etc/wireguard/wg0.conf
- wg show wg0 transfer
- wg show wg0 peers | wc -l

## References
- [WireGuard Quickstart](https://www.wireguard.com/quickstart/)
- [wg man page](https://man7.org/linux/man-pages/man8/wg.8.html)
- [wg-quick man page](https://man7.org/linux/man-pages/man8/wg-quick.8.html)
