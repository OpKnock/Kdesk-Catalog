---
name: "packer"
description: "Builds machine images with Packer: builders (AWS, VMware, Docker), provisioners, HCL2 templates, and CI pipelines. Use when working with template authoring, build and verify, devops or when the user mentions template authoring, build and verify, devops."
---

Builds machine images with Packer: builders (AWS, VMware, Docker), provisioners, HCL2 templates, and CI pipelines.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `packer init .`, `packer build -var-file=prod.pkrvars.hcl template.pkr.hcl`
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

**Parameters:**
- `template` (string): Template file or directory
- `var-file` (string): Variable values file

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

**Parameters:**
- `var-file` (string): pkrvars file for environment values
- `only` (string): Build only named builders
- `on-error` (string): Error behavior: cleanup, abort, run-cleanup-provisioner

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

## References
- [Packer Documentation](https://developer.hashicorp.com/packer/docs)
- [Packer HCL2 Guide](https://developer.hashicorp.com/packer/guides/hcl)
- [Amazon Builder](https://developer.hashicorp.com/packer/integrations/hashicorp/amazon)
