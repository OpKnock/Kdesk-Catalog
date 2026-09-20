---
type: agent_requested
description: "Configures load balancing tiers: HAProxy and NGINX proxies, Kubernetes Services (ClusterIP/NodePort/LoadBalancer), MetalLB, and keepalived."
---

# Load Balancing

Configures load balancing tiers: HAProxy and NGINX proxies, Kubernetes Services (ClusterIP/NodePort/LoadBalancer), MetalLB, and keepalived.

## Instructions

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