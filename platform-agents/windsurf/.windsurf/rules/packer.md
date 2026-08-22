---
trigger: glob
description: "Builds machine images with Packer: builders (AWS, VMware, Docker), provisioners, HCL2 templates, and CI pipelines."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# packer

Builds machine images with Packer: builders (AWS, VMware, Docker), provisioners, HCL2 templates, and CI pipelines.

## Instructions

# Packer Image Building

Create golden machine images reproducibly with Packer HCL2.

## What This Skill Does

- Authors HCL2 templates (source builders + provisioners + post-processors)
- Validates and formats templates before building
- Builds for AWS, GCP, Azure, VMware, and Docker
- Parameterizes with pkrvars files per environment
- Emits machine-readable output for CI pipelines

## When to Use

- Golden AMIs with hardened baselines
- Reproducible dev box images (VirtualBox/VMware)
- CI image baking with scheduled builds

## Real Commands

```bash
# Author and validate
packer init .                              # installs plugins from template
packer fmt -check template.pkr.hcl
packer validate -var-file=prod.pkrvars.hcl template.pkr.hcl
packer inspect template.pkr.hcl

# Build
packer build -var-file=prod.pkrvars.hcl template.pkr.hcl
packer build -only amazon-ebs.amazonlinux template.pkr.hcl
packer build -on-error=cleanup template.pkr.hcl
packer build -machine-readable template.pkr.hcl | grep artifact_id
```

## Template Sketch

```hcl
variable "region" { default = "us-east-1" }
variable "ami_name" { type = string }

source "amazon-ebs" "baseline" {
  region        = var.region
  source_ami_filter {
    filters = { virtualization-type = "hvm", name = "al2023-ami-*" }
    most_recent = true
    owners = ["137112412989"]
  }
  instance_type = "t3.small"
  ssh_username  = "ec2-user"
  ami_name      = var.ami_name
}

build {
  sources = ["source.amazon-ebs.baseline"]
  provisioner "shell" {
    script = "scripts/harden.sh"
  }
}
```

## Best Practices

- Always run packer init + validate in CI before builds
- Keep base OS patched inside the build, not after boot
- Store secrets in pkrvars with CI secret injection, not in templates
- Use -on-error=cleanup so broken builds do not leak AMIs
- Tag AMIs and set retention to avoid image sprawl

## Capabilities

### template-authoring
Create and validate HCL2 Packer templates.

**Commands:**
- `packer init .`
- `packer validate template.pkr.hcl`
- `packer fmt template.pkr.hcl`
- `packer inspect template.pkr.hcl`
- `packer plugins install github.com/hashicorp/amazon`

**Examples:**
- packer init .
- packer validate template.pkr.hcl
- packer fmt template.pkr.hcl

### build-and-verify
Build images and verify outputs across clouds.

**Commands:**
- `packer build -var-file=prod.pkrvars.hcl template.pkr.hcl`
- `packer build -only amazon-ebs.amazonlinux template.pkr.hcl`
- `packer build -on-error=cleanup template.pkr.hcl`
- `aws ec2 describe-images --owners self --filters Name=name,Values=*baseline*`
- `packer build -machine-readable template.pkr.hcl | jq '.artifact_id'`

**Examples:**
- packer build -var-file=prod.pkrvars.hcl template.pkr.hcl
- packer build -only amazon-ebs.amazonlinux template.pkr.hcl
- packer build -on-error=cleanup template.pkr.hcl
