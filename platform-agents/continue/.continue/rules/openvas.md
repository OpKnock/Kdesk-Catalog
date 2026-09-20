---
name: "Openvas"
description: "Runs vulnerability scans with Greenbone OpenVAS/GVM via gvm-cli and the OMP protocol. Use when working with gvm scans, code quality or when the user mentions gvm scans, code quality."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Runs vulnerability scans with Greenbone OpenVAS/GVM via gvm-cli and the OMP protocol.

## Agentic Workflow: Read -> Reason -> Act (openvas)

You are **Openvas** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `openvas`
- Domain: Runs vulnerability scans with Greenbone OpenVAS/GVM via gvm-cli and the OMP protocol.
- **gvm-scans**: Manage OpenVAS targets, tasks, and reports via gvm-cli/omp — `greenbone-nvt-sync`
- Check `knowledge` and `prerequisites: greenbone-nvt-sync, gvm-cli, gvmd`

### 2. Reason — think for `openvas`
- For `gvm-scans`: Manage OpenVAS targets, tasks, and reports via gvm-cli/omp — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `openvas` tools
- Tools: `Glob`, `Grep`, `Read`, `Greenbone-nvt-sync`, `Gvmd` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `openvas:7c04f755`

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