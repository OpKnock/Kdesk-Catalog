Manage Kubernetes ConfigMaps: create from literals/files, mount into pods, update without redeploying, and verify environment consumption.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl create configmap app-config --from-literal=APP_ENV=p`, `kubectl get configmaps`
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

# Kubernetes ConfigMaps

Manage configuration data decoupled from container images.

## What this skill does

- Creates ConfigMaps from literals, files, and env files.
- Mounts config data as files or environment variables.
- Updates configs and verifies pods pick them up.

## When to use

- Externalizing app settings across environments.
- Sharing config between replicas of a workload.
- Rotating config without rebuilding images.

## Real commands

```bash
# From literals
kubectl create configmap app-config \
  --from-literal=APP_ENV=prod --from-literal=LOG_LEVEL=info

# From a file (key = filename)
kubectl create configmap app-config-file --from-file=app.properties

# From an env file
kubectl create configmap app-config-env --from-env-file=config.env

# Generate manifest without applying
kubectl create configmap app-config \
  --dry-run=client -o yaml > configmap.yaml

# Inspect
kubectl get configmaps
kubectl describe configmap app-config
kubectl get cm app-config -o yaml

# Update
kubectl edit configmap app-config

# Delete
kubectl delete configmap app-config
```

## Mount example

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.2
      envFrom:
        - configMapRef:
            name: app-config
      volumeMounts:
        - name: config
          mountPath: /etc/app
          readOnly: true
  volumes:
    - name: config
      configMap:
        name: app-config-file
```

## Testing

```bash
# Verify env vars inside the pod
kubectl exec deploy/app -- env | grep APP_ENV
kubectl exec deploy/app -- cat /etc/app/app.properties
```

## Best practices

- Prefer mounted files for large configs; envFrom for small key/value sets.
- ConfigMap updates don't restart pods; combine with a rollout restart.
- Keep secrets out of ConfigMaps; use Secrets for sensitive data.

## Capabilities

### configmap-create
Create ConfigMaps from literals, files, or env files.

**Parameters:**
- `name` (string): ConfigMap name.
- `from_literal` (string): key=value pairs.
- `from_file` (string): File(s) to embed.

**Commands:**
- `kubectl create configmap app-config --from-literal=APP_ENV=prod --from-literal=LOG_LEVEL=info`
- `kubectl create configmap app-config-file --from-file=app.properties`
- `kubectl create configmap app-config-env --from-env-file=config.env`
- `kubectl create configmap app-config --dry-run=client -o yaml > configmap.yaml`

**Examples:**
- kubectl create configmap app-config --from-literal=APP_ENV=prod --from-literal=LOG_LEVEL=info
- kubectl create configmap app-config-file --from-file=app.properties
- kubectl create configmap app-config --dry-run=client -o yaml > configmap.yaml

### configmap-ops
Inspect, update, and delete ConfigMaps.

**Parameters:**
- `name` (string): ConfigMap name.
- `namespace` (string): Namespace (default: current context).

**Commands:**
- `kubectl get configmaps`
- `kubectl describe configmap app-config`
- `kubectl edit configmap app-config`
- `kubectl delete configmap app-config`
- `kubectl get cm app-config -o yaml`

**Examples:**
- kubectl get configmaps
- kubectl describe configmap app-config
- kubectl get cm app-config -o yaml

## References
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [kubectl create configmap](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create_configmap/)