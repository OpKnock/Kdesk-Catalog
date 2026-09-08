---
name: "threat-modeling"
description: "Create structured threat models, diagram attacks, and document mitigations using OWASP Threat Dragon, threatspec, and pytm. Use when working with Model threats with OWASP Threat Dragon, Document threats with threatspec, Generate models with pytm or when the user mentions Model threats with OWASP Threat Dragon, Document threats with threatspec, Generate models with pytm."
globs: ["**/*.go", "**/*.html", "**/*.r", "**/*.rs"]
alwaysApply: false
---

Create structured threat models, diagram attacks, and document mitigations using OWASP Threat Dragon, threatspec, and pytm.

## Agentic Workflow: Read -> Reason -> Act (threat-modeling)

You are **threat-modeling** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `threat-modeling`
- Domain: Create structured threat models, diagram attacks, and document mitigations using OWASP Threat Dragon, threatspec, and pytm.
- **Model threats with OWASP Threat Dragon**: Run the OWASP Threat Dragon web app locally and draw STRIDE-based data-flow diagrams with per-elemen — `docker run -d --name threat-dragon -p 3000:3000 owasp/threat-dragon`
- **Document threats with threatspec**: Annotate code with threatspec comments and compile them into reports, graphs, and CI check results. — `threatspec init`
- **Generate models with pytm**: Describe architecture as Python objects in a threatmodel file, then render diagrams and full STRIDE- — `pytm --rm threatmodel.py --dfd diagram.png --report report.md`
- Check `knowledge` and `prerequisites: drawio, threat-modeler, OWASP, STRIDE`

### 2. Reason — think for `threat-modeling`
- For `Model threats with OWASP Threat Dragon`: Run the OWASP Threat Dragon web app locally and draw STRIDE-based data-flow diagrams with per-element threat notes. — decide which checks to run
- For `Document threats with threatspec`: Annotate code with threatspec comments and compile them into reports, graphs, and CI check results. — decide which checks to run
- For `Generate models with pytm`: Describe architecture as Python objects in a threatmodel file, then render diagrams and full STRIDE-based reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `threat-modeling` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Threatspec` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `threat-modeling:dab5f2bf`

# Threat Modeling

Create and maintain threat models that capture data flows, trust boundaries, attack surfaces, and mitigations.

## When to Use

- Design reviews of new features, APIs, and auth flows
- Security requirements capture before implementation
- Compliance evidence for standards like PCI-DSS or SOC 2
- Re-review when architecture changes (new third-party integration, new data store)

## Workflow

1. Draw the system: elements (processes, data stores, external actors) and data-flow arrows crossing trust boundaries.
2. Apply STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
3. For each flow, ask what an attacker gains if they can control the source, the channel, or the destination.
4. Record each threat with: affected element, STRIDE category, likelihood, impact, and one or more mitigations.
5. Wire threats to issues or test cases so the model stays actionable.
6. Validate in CI: fail the build when a new component has no threats or when mitigations are missing.

## Tooling

- Threat Dragon: interactive diagramming, best for stakeholder workshops.
- threatspec: inline comments in source code keep the model close to the code; run in CI to block unreviewed changes.
- pytm: code-first models that render diagrams and reports, good for large systems with many repeatable patterns.

## Good Model Qualities

- Every trust boundary is explicit; label what crosses it and with what authentication.
- Data at rest, in transit, and in use is called out separately.
- Defaults are analyzed, not just the happy path.
- Mitigations reference concrete controls (encryption libraries, authN/authZ services, logging).

## Common Pitfalls

- Modeling the whole enterprise in one diagram; split by feature.
- Forgetting external actors like batch jobs, cron, and vendor webhooks.
- Copying OWASP Top 10 text verbatim without tying it to a flow.
- Leaving the model to rot; update it in the same PR as the architecture change.

## CI Integration

- threatspec validate in the pipeline with a comment bot on failures.
- Export reports nightly and store them as reviewable artifacts.
- Alert on new threats that lack an owner or a due date.

## Capabilities

### Model threats with OWASP Threat Dragon
Run the OWASP Threat Dragon web app locally and draw STRIDE-based data-flow diagrams with per-element threat notes.

**Parameters:**
- `host port` (integer): Local port mapped to the container (default 3000).
- `container name` (string): Name for the running container so it can be stopped later.

**Commands:**
- `docker run -d --name threat-dragon -p 3000:3000 owasp/threat-dragon`
- `docker logs -f threat-dragon`
- `docker stop threat-dragon && docker rm threat-dragon`
- `docker pull owasp/threat-dragon:latest`

**Examples:**
- docker run -d --name threat-dragon -p 3000:3000 owasp/threat-dragon
- docker logs -f threat-dragon

### Document threats with threatspec
Annotate code with threatspec comments and compile them into reports, graphs, and CI check results.

**Parameters:**
- `output format` (string): Report format: markdown, html, json, csv.
- `project path` (string): Root of the project containing the threatspec config.

**Commands:**
- `threatspec init`
- `threatspec model --project ./`
- `threatspec validate --project ./`
- `threatspec report --format markdown --output threat-model.md --project ./`
- `threatspec graph --output threat-model.dot`

**Examples:**
- threatspec init
- threatspec report --format markdown --output threat-model.md --project ./

### Generate models with pytm
Describe architecture as Python objects in a threatmodel file, then render diagrams and full STRIDE-based reports.

**Parameters:**
- `dfd format` (string): Diagram output format: png, svg, pdf.
- `levels` (string): Only report threats up to the given STRIDE level (L0-L3).

**Commands:**
- `pytm --rm threatmodel.py --dfd diagram.png --report report.md`
- `pytm --rm threatmodel.py --dfd diagram.svg --format svg --levels L1`
- `pytm --rm threatmodel.py --list`
- `pytm --rm threatmodel.py --dfd diagram.pdf --format pdf --report report.html`

**Examples:**
- pytm --rm threatmodel.py --dfd diagram.png --report report.md
- pytm --rm threatmodel.py --list

## References
- [](https://github.com/OWASP/threat-dragon)
- [](https://threatspec.org)
- [](https://github.com/OWASP/pytm)
- [](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)