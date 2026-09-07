Manages Tenable Nessus scans from the CLI: creating, launching, and reporting vulnerability scans.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nessuscli scan list`
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

# Nessus

Tenable Nessus is a commercial vulnerability scanner. This skill covers driving it
from the CLI on the scan server.

## When to Use

- Launching credentialed or uncredentialed scans from a terminal
- Downloading reports in Nessus, HTML, or CSV formats
- Managing scan schedules and users on the server

## Real Commands

```bash
# List existing scans
nessuscli scan list

# Create a new scan
nessuscli scan new --name web-scan --targets 10.0.0.10 --policy "Basic Network Scan"

# Launch it (use the ID from scan list)
nessuscli scan start --scan-id 42

# Check status / stop
nessuscli scan status --scan-id 42
nessuscli scan stop --scan-id 42

# Download results
nessuscli report download --scan-id 42 --format nessus --output /tmp/web-scan.nessus

# Manage users
nessuscli lsuser
nessuscli user add --username auditor --password <pw> --role basic
```

## Workflow

```bash
# Create, start, wait, export in one flow
nessuscli scan new --name ci-scan --targets 172.16.0.5 --policy "Basic Network Scan"
nessuscli scan list | grep ci-scan
nessuscli scan start --scan-id $(nessuscli scan list | awk -F'|' '/ci-scan/{print $1}')
nessuscli report download --scan-id <id> --format html --output report.html
```

## Best Practices

- Always scan with credentials for accurate results
- Use `--policy "Basic Network Scan"` for quick checks, "Advanced Scan" for full tests
- Store reports in `.nessus` for Nessus UI import
- Limit targets to scoped assets; scanning outside scope has legal implications

## Example Response

The agent returns the scan ID, status transitions, and a summary of findings grouped
by severity (Critical/High/Medium/Low) parsed from the downloaded report.

## Capabilities

### nessus-cli
Manage Nessus scans, users, and reports via nessuscli

**Parameters:**
- `scan-id` (integer): Numeric ID of the scan to start, stop, or report on
- `targets` (string): IP addresses, CIDRs, or hostnames to scan
- `format` (string): Report format: nessus, html, pdf, csv, or db

**Commands:**
- `nessuscli scan list`
- `nessuscli scan new --name web-scan --targets 10.0.0.10 --policy Basic Network Scan`
- `nessuscli scan start --scan-id 42`
- `nessuscli scan stop --scan-id 42`
- `nessuscli report download --scan-id 42 --format nessus --output /tmp/scan.nessus`

**Examples:**
- nessuscli scan new --name prod-scan --targets 10.1.2.0/24 --policy 'Advanced Scan'
- nessuscli scan list | grep -i prod
- nessuscli report download --scan-id 7 --format html --output scan-report.html

## References
- [Tenable Nessus docs](https://docs.tenable.com/nessus/)
- [Nessus CLI commands](https://docs.tenable.com/nessus/Content/CLICommands.htm)