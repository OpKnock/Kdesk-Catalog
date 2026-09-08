Configures load balancing tiers: HAProxy and NGINX proxies, Kubernetes Services (ClusterIP/NodePort/LoadBalancer), MetalLB, and keepalived.

## Agentic Workflow: Read -> Reason -> Act (load-balancing)

You are **Load Balancing** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `load-balancing`
- Domain: Configures load balancing tiers: HAProxy and NGINX proxies, Kubernetes Services (ClusterIP/NodePort/LoadBalancer), MetalLB, and keepalived.
- **proxy-configuration**: Configure and validate HAProxy and NGINX frontends and backends. — `haproxy -c -f /etc/haproxy/haproxy.cfg`
- **kubernetes-lb**: Expose workloads with Services and MetalLB bare-metal load balancers. — `kubectl expose deployment web --type=LoadBalancer --port=80`
- Check `knowledge` and `prerequisites: haproxy, kubectl, nginx, systemctl`

### 2. Reason — think for `load-balancing`
- For `proxy-configuration`: Configure and validate HAProxy and NGINX frontends and backends. — decide which checks to run
- For `kubernetes-lb`: Expose workloads with Services and MetalLB bare-metal load balancers. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `load-balancing` tools
- Tools: `Glob`, `Grep`, `Read`, `Haproxy`, `Systemctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `load-balancing:1d22957d`

# Load Balancing

Build and tune load balancing across proxy layers and Kubernetes Services.

## What This Skill Does

- Configures HAProxy/NGINX frontends, backends, health checks, and stickiness
- Exposes Kubernetes workloads via Service types
- Provides external IPs on bare metal with MetalLB
- Validates configs before reload and checks stats
- Diagnoses uneven distribution and backend failures

## When to Use

- Running HAProxy or NGINX as an edge or internal balancer
- Bare-metal clusters needing LoadBalancer IPs
- Tuning session affinity and health checks

## Real Commands

```bash
# HAProxy
haproxy -c -f /etc/haproxy/haproxy.cfg
systemctl reload haproxy
curl -s http://127.0.0.1:8404/stats | grep -c "UP"

# NGINX
nginx -t
nginx -s reload

# Kubernetes Services
kubectl expose deployment web --type=LoadBalancer --port=80
kubectl get svc -o wide
kubectl apply -f metallb-config.yaml
kubectl get ipaddresspool -n metallb-system
kubectl get endpointslices -l kubernetes.io/service-name=web
```

## HAProxy Backend

```
backend web_servers
  balance roundrobin
  option httpchk GET /health
  server web1 10.0.0.11:8080 check inter 3s fall 3 rise 2
  server web2 10.0.0.12:8080 check inter 3s fall 3 rise 2
```

## Best Practices

- Validate (`-c` / `nginx -t`) before reloading — never reload broken config
- Pair health checks with sticky sessions only when required
- Prefer L4 services (ClusterIP + LB) for internal traffic, L7 only at the edge
- In bare-metal, MetalLB + Service of type LoadBalancer beats hostPort hacks
- Watch backend UP counts in stats endpoints for capacity signals

## Capabilities

### proxy-configuration
Configure and validate HAProxy and NGINX frontends and backends.

**Parameters:**
- `config` (string): Proxy config file path
- `backend` (string): Backend pool name

**Commands:**
- `haproxy -c -f /etc/haproxy/haproxy.cfg`
- `systemctl reload haproxy`
- `nginx -t`
- `nginx -s reload`
- `haproxy -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid`
- `curl -s http://127.0.0.1:8404/stats`

**Examples:**
- haproxy -c -f /etc/haproxy/haproxy.cfg
- nginx -t
- nginx -s reload

### kubernetes-lb
Expose workloads with Services and MetalLB bare-metal load balancers.

**Parameters:**
- `type` (string): Service type: ClusterIP, NodePort, LoadBalancer
- `port` (integer): Service port

**Commands:**
- `kubectl expose deployment web --type=LoadBalancer --port=80`
- `kubectl get svc -o wide`
- `kubectl apply -f metallb-config.yaml`
- `kubectl get ipaddresspool -n metallb-system`
- `kubectl apply -f svc-nodeport.yaml`
- `kubectl get endpointslices -l kubernetes.io/service-name=web`

**Examples:**
- kubectl expose deployment web --type=LoadBalancer --port=80
- kubectl apply -f metallb-config.yaml
- kubectl get endpointslices -l kubernetes.io/service-name=web

## References
- [HAProxy Documentation](https://www.haproxy.org/documentation/)
- [NGINX Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [MetalLB](https://metallb.universe.tf/)
