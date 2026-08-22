---
name: "kompose"
description: "Converts docker-compose files to Kubernetes manifests with kompose: conversion, direct deployment, and reverse tooling."
---

# kompose

Converts docker-compose files to Kubernetes manifests with kompose: conversion, direct deployment, and reverse tooling.

## Instructions

# Kompose Conversion

Move from docker-compose to Kubernetes by translating compose files into manifests.

## What This Skill Does

- Converts compose services to Deployment + Service YAML
- Handles volumes (hostPath, PVC, emptyDir), networks, and ports
- Deploys stacks directly with kompose up
- Generates Helm charts from compose files
- Applies replica counts, env files, and group mode

## When to Use

- Migrating a local compose app to Kubernetes
- Bootstrapping manifests quickly before refining
- Teaching the mapping compose-service -> Deployment

## Real Commands

```bash
# Basic conversion
kompose convert -f docker-compose.yml
kompose convert -f docker-compose.yml -c          # to stdout
kompose convert -o k8s-manifests/
kompose convert --volumes persistentVolumeClaim

# Direct deploy
kompose up -f docker-compose.yml
kompose down -f docker-compose.yml

# Advanced
kompose convert --controller statefulset
kompose convert --replicas 3
kompose convert --chart                            # Helm chart output
kompose convert --env-file .env
```

## Conversion Notes

- `ports:` become Service + targetPort
- `volumes:` default to emptyDir; use `--volumes persistentVolumeClaim` for data
- `networks:` map to multi-service exposure; `--service-group-mode` groups services
- build: context becomes image; `--image` pins registry target

## Best Practices

- Review generated YAML: kompose output is a starting point, not production
- Add probes and resource limits after conversion
- Prefer PVC strategy for databases and stateful workloads
- Validate converted manifests with `kubectl apply --dry-run=client -f .`
- Use --controller statefulset for apps with stable identity

## Capabilities

### compose-to-kubernetes
Translate compose services into Deployment/Service manifests with options for volumes and networks.

**Commands:**
- `kompose convert -f docker-compose.yml`
- `kompose convert -f docker-compose.yml -c`
- `kompose convert --volumes hostPath`
- `kompose convert -o k8s-manifests/`
- `kompose convert --replicas 3`
- `kompose convert --chart`

**Examples:**
- kompose convert -f docker-compose.yml
- kompose convert --volumes hostPath
- kompose convert --chart

### deploy-and-rollback
Deploy compose stacks directly to Kubernetes and tear them down.

**Commands:**
- `kompose up -f docker-compose.yml`
- `kompose down -f docker-compose.yml`
- `kompose convert -f docker-compose.yml --controller deployment`
- `kompose convert --service-group-mode`
- `kompose convert --env-file .env`

**Examples:**
- kompose up -f docker-compose.yml
- kompose down -f docker-compose.yml
- kompose convert --controller deployment
