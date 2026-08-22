# Kubernetes Secret

Handle sensitive data in clusters: create generic and TLS secrets from CLI input or files, inject as environment variables or mounted volumes, and decode base64 values for auditing without exposing them in manifests.

## Instructions

# Kubernetes Secrets

Store and inject sensitive data into Kubernetes workloads.

## What this skill does

- Creates generic and TLS secrets from CLI input or files.
- Injects secrets as env vars or mounted files.
- Decodes values safely for audits.

## When to use

- DB credentials, API keys, and tokens for workloads.
- TLS cert/key pairs for ingress and service TLS.
- Keeping secrets out of images and git.

## Real commands

```bash
# Generic secret
kubectl create secret generic db-creds \
  --from-literal=DB_USER=admin --from-literal=DB_PASSWORD=s3cret

# From env file
kubectl create secret generic app-secrets --from-env-file=secrets.env

# TLS secret for ingress
kubectl create secret tls my-tls --cert=cert.pem --key=key.pem

# List
kubectl get secrets

# Decode a value (base64 in etcd/API)
kubectl get secret db-creds -o jsonpath='{.data.DB_PASSWORD}' | base64 -d

# Describe shows keys only, not values
kubectl describe secret db-creds
```

## Pod reference example

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.2
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-creds
              key: DB_PASSWORD
      volumeMounts:
        - name: tls
          mountPath: /etc/tls
          readOnly: true
  volumes:
    - name: tls
      secret:
        secretName: my-tls
```

## Testing

```bash
kubectl exec deploy/app -- env | grep DB_PASSWORD
kubectl exec deploy/app -- cat /etc/tls/tls.crt
```

## Best practices

- Values are base64, not encrypted; use encryption at rest (KMS) or ExternalSecrets.
- Prefer mounted secrets over env vars for large or rotating values.
- Never commit secret manifests; generate them in pipelines.

## Capabilities

### secret-create
Create generic and TLS secrets.

**Commands:**
- `kubectl create secret generic db-creds --from-literal=DB_USER=admin --from-literal=DB_PASSWORD=s3cret`
- `kubectl create secret generic app-secrets --from-file=tls.crt=cert.pem --from-file=tls.key=key.pem`
- `kubectl create secret tls my-tls --cert=cert.pem --key=key.pem`
- `kubectl create secret generic app-secrets --from-env-file=secrets.env`

**Examples:**
- kubectl create secret generic db-creds --from-literal=DB_USER=admin --from-literal=DB_PASSWORD=s3cret
- kubectl create secret tls my-tls --cert=cert.pem --key=key.pem
- kubectl create secret generic app-secrets --from-env-file=secrets.env

### secret-ops
List, decode, and reference secrets in workloads.

**Commands:**
- `kubectl get secrets`
- `kubectl get secret db-creds -o jsonpath='{.data.DB_PASSWORD}' | base64 -d`
- `kubectl describe secret db-creds`
- `kubectl delete secret db-creds`
- `kubectl get secret my-tls -o yaml`

**Examples:**
- kubectl get secret db-creds -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
- kubectl get secrets
- kubectl describe secret db-creds