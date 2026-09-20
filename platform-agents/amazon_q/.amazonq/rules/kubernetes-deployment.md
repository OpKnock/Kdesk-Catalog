# Kubernetes Deployment

Deploy and operate workloads with kubectl: create deployments, scale replicas, update images, and manage rollouts.

## Instructions

# Kubernetes Deployments

Create and operate declarative workloads with kubectl.

## What this skill does

- Creates deployments from images with replica counts.
- Scales replicas and updates images.
- Manages rollouts and status checks.

## When to use

- Deploying stateless services.
- Day-2 operations: scaling, image bumps, restarts.
- Checking rollout health during releases.

## Real commands

```bash
# Create
kubectl create deployment nginx --image=nginx:1.27 --replicas=3

# Scale
kubectl scale deployment nginx --replicas=5

# Update image (triggers a rollout)
kubectl set image deployment/nginx nginx=nginx:1.28

# Expose as a service
kubectl expose deployment nginx --port=80 --type=ClusterIP

# Rollout status
kubectl rollout status deployment/nginx

# Restart (re-pull, new rollout)
kubectl rollout restart deployment/nginx

# Inspect
kubectl get deployments
kubectl get pods -l app=nginx -o wide
kubectl describe deployment nginx
```

## Deployment YAML example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

## Testing

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/nginx
kubectl get pods --watch
```

## Best practices

- Always set resource requests/limits on containers.
- Use apply -f with versioned manifests, not ad-hoc create.
- Check rollout status before declaring a release done.

## Capabilities

### deploy-basic
Create, scale, and update deployments.

**Commands:**
- `kubectl create deployment nginx --image=nginx:1.27 --replicas=3`
- `kubectl scale deployment nginx --replicas=5`
- `kubectl set image deployment/nginx nginx=nginx:1.28`
- `kubectl expose deployment nginx --port=80 --type=ClusterIP`

**Examples:**
- kubectl create deployment nginx --image=nginx:1.27 --replicas=3
- kubectl scale deployment nginx --replicas=5
- kubectl set image deployment/nginx nginx=nginx:1.28

### rollout-ops
Monitor rollout progress and status.

**Commands:**
- `kubectl rollout status deployment/nginx`
- `kubectl rollout restart deployment/nginx`
- `kubectl get deployments`
- `kubectl get pods -l app=nginx -o wide`
- `kubectl describe deployment nginx`

**Examples:**
- kubectl rollout status deployment/nginx
- kubectl rollout restart deployment/nginx
- kubectl get deployments