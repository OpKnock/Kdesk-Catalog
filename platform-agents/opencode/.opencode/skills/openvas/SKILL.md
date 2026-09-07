---
name: "openvas"
description: "Runs vulnerability scans with Greenbone OpenVAS/GVM via gvm-cli and the OMP protocol. Use when working with gvm scans, code quality or when the user mentions gvm scans, code quality."
---

Runs vulnerability scans with Greenbone OpenVAS/GVM via gvm-cli and the OMP protocol.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `greenbone-nvt-sync`
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

# OpenVAS / GVM

Greenbone Vulnerability Manager (GVM) with OpenVAS scanner: schedule and run network
vulnerability scans and export reports.

## When to Use

- Periodic vulnerability scanning of internal infrastructure
- Credentialed scans against Linux/Windows hosts
- Generating compliance reports (CVE/CPE based)

## Real Commands

```bash
# Update the NVT feed (VTs)
greenbone-nvt-sync

# Confirm the daemon is up
sudo -u gvm gvmd --version

# XML via gvm-cli socket
gvm-cli socket --xml "<get_version/>"

# List tasks
gvm-cli socket --xml "<get_tasks/>"

# List scanners
sudo -u gvm gvmd --list-scanners

# Create a task from CLI
sudo -u gvm gvmd --create-task --name ci-scan --target 10.0.0.0/24 --scanner <uuid>
```

## Typical Flow

1. `greenbone-nvt-sync` to refresh the feed
2. Create target + task via gvmd or GMP XML
3. Start the task: `gvm-cli socket --xml "<start_task task_id='...'/>"`
4. Poll `get_reports` and export XML or PDF

## Best Practices

- Run `greenbone-nvt-sync` before scans; stale feeds produce stale results
- Use credentialed scans (`ssh`/`smb` credentials) for accurate coverage
- Scope scans to owned infrastructure
- Schedule via GSA (web UI) or cron + gvm-cli for recurring checks

## Example Response

Returns task status, scan duration, and findings grouped by severity with CVE IDs,
so the agent can map each CVE to a remediation.

## Capabilities

### gvm-scans
Manage OpenVAS targets, tasks, and reports via gvm-cli/omp

**Parameters:**
- `socketpath` (string): Path to the gvmd unix socket (default /var/run/gvmd.sock)
- `gmp-username` (string): GMP username for gvm-cli authentication
- `gmp-password` (string): GMP password for gvm-cli authentication

**Commands:**
- `greenbone-nvt-sync`
- `gvmd --list-scanners`
- `gvm-cli socket --xml "demo-get-version"`
- `gvm-cli socket --xml "demo-create-target...demowebdemo-namedemo-create-target"`
- `gvm-cli socket --xml "demo-get-reports"`

**Examples:**
- gvm-cli socket --xml "demo-get-tasks"
- gvmd --create-task --name daily-scan --target web --scanner openvas
- gvm-cli socket --xml "demo-get-results-task-id"

## References
- [Greenbone GVM docs](https://greenbone.github.io/docs/)
- [OpenVAS protocol reference](https://greenbone.github.io/gmp/)
