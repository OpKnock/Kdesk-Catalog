---
trigger: glob
description: "Architects API gateway landscapes: gateway selection, multi-gateway topology, Nginx/Traefik/Kong patterns, and failover design. Use when working with gateway selection, topology design or when the user mentions gateway selection, topology design."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Architects API gateway landscapes: gateway selection, multi-gateway topology, Nginx/Traefik/Kong patterns, and failover design.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const g=[{name:'Kong',use:'plugins'},{name:'Traefik`, `node -e "console.log('edge LB -> gateway pool -> services')"`
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

# API Gateway Architect

Designs the gateway layer of the system: choice, topology, and operations.

## When to Use
- Choosing a gateway for the org
- Designing gateway redundancy
- Splitting public/internal/partner traffic

## Real Commands

```bash
# Compare candidates
node -e "const g=[{name:'Kong',use:'plugins'},{name:'Traefik',use:'k8s-native'},{name:'NGINX',use:'lua/openresty'},{name:'AWS',use:'managed'}];console.table(g)"

# Inventory current gateways
kubectl get svc -A | grep -E 'traefik|kong'

# Health of the gateway pool
curl -s http://localhost:8000/status | python -m json.tool
```

## Topology
edge LB -> gateway pool (active-active) -> services, with separate zones for public, internal, and partner traffic.

## Failover Design
- Two or more gateway nodes
- Health checks on every node
- Shared config state (DB or Git)

## Testing
Kill a gateway node and verify traffic keeps flowing.

## Best Practices
- Match the gateway to team skills
- Isolate zones to limit blast radius

## Capabilities

### gateway-selection
Evaluate and select gateway technologies for the architecture

**Parameters:**
- `criteria` (string): Selection criteria
- `candidate` (string): Gateway candidate

**Commands:**
- `node -e "const g=[{name:'Kong',use:'plugins'},{name:'Traefik',use:'k8s-native'},{name:'NGINX',use:'lua/openresty'},{name:'AWS',use:'managed'}];console.table(g)"`
- `helm repo add traefik https://helm.traefik.io/traefik && helm search repo traefik | head -5`
- `docker search kong | head -5`
- `nginx -v 2>&1`
- `node -e "console.log('criteria: team skills, traffic, plugins, cost')"`

**Examples:**
- node -e "const g=[{name:'Kong',use:'plugins'},{name:'Traefik',use:'k8s-native'},{name:'NGINX',use:'lua/openresty'},{name:'AWS',use:'managed'}];console.table(g)"
- helm repo add traefik https://helm.traefik.io/traefik && helm search repo traefik | head -5
- nginx -v 2>&1

### topology-design
Design multi-gateway topologies with failover and isolation

**Parameters:**
- `zone` (string): Gateway zone: public, internal, partner
- `nodes` (string): Number of gateway nodes

**Commands:**
- `node -e "console.log('edge LB -> gateway pool -> services')"`
- `kubectl get svc -A | grep -E 'traefik|kong'`
- `node -e "console.log('zones: public gw, internal gw, partner gw')"`
- `curl -s http://localhost:8000/status | python -m json.tool`
- `node -e "console.log('failover: active-active with health checks')"`

**Examples:**
- kubectl get svc -A | grep -E 'traefik|kong'
- curl -s http://localhost:8000/status | python -m json.tool
- node -e "console.log('zones: public gw, internal gw, partner gw')"

## References
- [API Gateway Comparison](https://www.getambassador.io/resources/kubernetes-api-gateway)
- [NGINX Docs](https://nginx.org/en/docs/)
- [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
