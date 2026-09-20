# falco

Detects abnormal container and host behavior at runtime with Falco rule engines, event generators, and falcoctl artifact management.

## Instructions

# Falco

Runtime security monitoring for containers and hosts using syscall-driven rules.

## What This Skill Does

- Deploys Falco on hosts or in-cluster (DaemonSet via Helm)
- Loads default and custom rule files
- Generates realistic attack events for testing rule coverage
- Manages rules artifacts and kernel drivers with falcoctl
- Streams alerts to stdout, files, or external sinks

## When to Use

- Detecting shell access, privilege escalation, or odd syscall patterns
- Validating that custom detection rules fire
- Auditing container runtime behavior after an incident

## Real Commands

```bash
# Install drivers and run
falcoctl driver install
falco

# Custom rules
falco -r /etc/falco/rules.d/custom.yaml

# Configure via --set
falco --set rules_files=[] --set rules_files[0]=/etc/falco/rules.d/custom.yaml

# Manage artifacts
falcoctl artifact install falcosecurity/falco-rules
falcoctl index list

# Generate test events
falco-event-generator run syscall
falco-event-generator run network
```

## Sample Custom Rule

```yaml
- rule: Write Below Binary Dir
  desc: Detect writes to /usr/bin
  condition: evt.dir = < and fd.name startswith /usr/bin and evt.type in (open, openat, rename)
  output: "File below /usr/bin opened for writing (user=%user.name file=%fd.name)"
  priority: WARNING
  tags: [filesystem, mitre_persistence]
```

## Best Practices

- Run Falco as a DaemonSet so every node is covered
- Validate new rules against the event generator before production
- Forward alerts to a SIEM or alertmanager for correlation
- Keep rules artifacts versioned via falcoctl and pin versions
- Update the kernel driver on node upgrades before enabling Falco

## Capabilities

### falco-runtime
Run Falco, configure rules, and view detected events.

**Commands:**
- `falco`
- `falco --version`
- `falco -r /etc/falco/rules.d/custom.yaml`
- `falco --set rules_files=[] --set rules_files[0]=/etc/falco/custom.yaml`
- `falco -e /dev/null -c falco.yaml`

**Examples:**
- falco -r rules.d/custom.yaml
- falco --version
- falco --set output.format='%evt.time %user.name %proc.name'

### falcoctl-artifacts
Manage rules artifacts and drivers with falcoctl.

**Commands:**
- `falcoctl driver install`
- `falcoctl driver list`
- `falcoctl artifact install falcosecurity/falco-rules`
- `falcoctl index list`
- `falcoctl artifact list falcosecurity`

**Examples:**
- falcoctl driver install
- falcoctl artifact install falcosecurity/falco-rules
- falcoctl index list

### event-generation
Generate test events to validate rule coverage.

**Commands:**
- `falco-event-generator run`
- `falco-event-generator run syscall`
- `falco-event-generator list`
- `kubectl apply -f https://raw.githubusercontent.com/falcosecurity/event-generator/main/deploy/kubernetes/event-generator.yaml`

**Examples:**
- falco-event-generator run syscall
- falco-event-generator list
- falco-event-generator run network
