# Kubernetes Configmap

Manage Kubernetes ConfigMaps: create from literals/files, mount into pods, update without redeploying, and verify environment consumption.

## Instructions

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