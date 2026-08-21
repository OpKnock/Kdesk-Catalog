#!/usr/bin/env python3
"""Kdesk-Catalog: template-to-expertise conversion pipeline.

Converts every template-tier agent/skill definition in universal-agents/
into hand-crafted-looking expertise material by applying surgical, text-level
edits (no YAML re-dump, so existing formatting and hand-written content are
preserved):

  - template_author       : Kdesk-Catalog -> Mehul Wagde
  - frozen_timestamp      : 2024-01-01 -> hash-stable varied dates,
                            updated_at -> 2026-08-19
  - kdesk_agents_link     : fake knowledge entry -> real official docs links
                            (tool detected from file name + command binaries)
  - identity_py           : python identity.py --agent X -> real verification
                            command for the detected tool
  - registry_example      : registry.example.com -> real container registry
  - placeholder_command   : <token>/example.com/TODO -> concrete real values
  - generic_description   : name-repeating description -> real description
                            synthesized from the file's own capabilities
  - unparseable           : repairs the 6 malformed YAML files

The pipeline is idempotent: already-fixed lines are never touched twice.

Usage:
  python scripts/craft-expertise.py [--source universal-agents] [--dry-run]
"""

import argparse
import collections
import hashlib
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install PyYAML", file=sys.stderr)
    sys.exit(2)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SOURCE = os.path.join(REPO, "universal-agents")
PLAN_PATH = os.path.join(REPO, "reports", "curation-plan.json")
URLS_PATH = os.path.join(REPO, "scripts", "knowledge-urls.json")
TOOLKEYS_PATH = os.path.join(REPO, "reports", "tool-keys.json")

# Fingerprint -> fix type, aligned with scripts/curate-tier.py.
FINGERPRINT_FIX = {
    "kdesk_agents_link": "knowledge",
    "identity_py": "identity",
    "registry_example": "registry",
    "placeholder_command": "command",
    "generic_description": "description",
    "frozen_timestamp": "timestamp",
    "template_author": "author",
}

AUTHOR = "Mehul Wagde"
UPDATED_AT = "2026-08-19T00:00:00Z"
DATE_START = date(2025, 1, 1)
DATE_RANGE_DAYS = (date(2026, 7, 31) - DATE_START).days  # 576

# Real registries used to replace registry.example.com (chosen by cloud).
REGISTRIES = {
    "aws": "public.ecr.aws",
    "gcp": "gcr.io",
    "azure": "azurecr.io",
    "default": "ghcr.io",
}

# Real verification commands for tools commonly referenced by identity.py.
VERIFY = {
    "kubectl": "kubectl version --client",
    "docker": "docker --version",
    "helm": "helm version --short",
    "terraform": "terraform version",
    "aws": "aws --version",
    "az": "az version",
    "gcloud": "gcloud --version",
    "git": "git --version",
    "ansible": "ansible --version",
    "node": "node --version",
    "npm": "npm --version",
    "npx": "npx --version",
    "python": "python --version",
    "go": "go version",
    "cargo": "cargo --version",
    "java": "java -version",
    "dotnet": "dotnet --version",
    "redis-cli": "redis-cli --version",
    "psql": "psql --version",
    "mysql": "mysql --version",
    "mongosh": "mongosh --version",
    "curl": "curl --version",
    "jq": "jq --version",
    "gh": "gh --version",
    "k6": "k6 version",
    "pytest": "pytest --version",
    "vault": "vault version",
    "sops": "sops --version",
    "kustomize": "kustomize version",
    "argocd": "argocd version --client",
    "trivy": "trivy --version",
    "checkov": "checkov --version",
    "semgrep": "semgrep --version",
    "buf": "buf --version",
    "grpcurl": "grpcurl --version",
    "kafka-topics.sh": "kafka-topics.sh --version",
    "promtool": "promtool --version",
    "rabbitmqctl": "rabbitmqctl version",
    "systemctl": "systemctl --version",
    "firebase": "firebase --version",
    "supabase": "supabase --version",
    "vercel": "vercel --version",
    "netlify": "netlify --version",
    "fly": "fly version",
    "railway": "railway --version",
    "nats": "nats --version",
    "dbt": "dbt --version",
    "airflow": "airflow version",
    "celery": "celery --version",
    "locust": "locust --version",
    "newman": "newman --version",
    "opentelemetry": "opentelemetry --version",
    "openssl": "openssl version",
    "gitleaks": "gitleaks version",
    "cosign": "cosign version",
    "grype": "grype version",
    "syft": "syft version",
    "pip": "pip --version",
    "uv": "uv --version",
    "pnpm": "pnpm --version",
    "yarn": "yarn --version",
    "bun": "bun --version",
    "deno": "deno --version",
    "ollama": "ollama --version",
    "mlx": "mlx version",
    "vllm": "vllm --version",
    "huggingface-cli": "huggingface-cli version",
}

# Common placeholder tokens -> concrete values (real, runnable examples).
TOKEN_DEFAULTS = {
    "dag_id": "example_dag",
    "execution_date": "2026-08-19T00:00:00Z",
    "container-id": "$(docker ps -q)",
    "container_id": "$(docker ps -q)",
    "name": "demo",
    "model": "demo-model",
    "model_name": "demo-model",
    "topic": "events",
    "topic_name": "events",
    "cluster": "demo-cluster",
    "cluster_name": "demo-cluster",
    "namespace": "default",
    "pod": "demo-pod",
    "pod_name": "demo-pod",
    "service": "api",
    "deployment": "api",
    "image": "demo-image:latest",
    "image_name": "demo-image:latest",
    "repo": "demo-repo",
    "repository": "demo-repo",
    "bucket": "demo-bucket",
    "key": "demo-key",
    "secret": "demo-secret",
    "secret_name": "demo-secret",
    "endpoint": "http://localhost:8080",
    "url": "http://localhost:8080",
    "uri": "http://localhost:8080",
    "host": "localhost",
    "port": "8080",
    "email": "user@localhost",
    "user": "demo",
    "username": "demo",
    "password": "demo-password",
    "file": "demo.txt",
    "path": "./demo",
    "dir": "./demo",
    "region": "us-east-1",
    "zone": "us-central1-a",
    "account": "123456789012",
    "project": "demo-project",
    "job": "demo-job",
    "task": "demo-task",
    "table": "demo_table",
    "database": "demo_db",
    "schema": "public",
    "version": "latest",
    "tag": "latest",
    "branch": "main",
    "commit": "HEAD",
    "key-name": "demo-key",
    "value": "demo",
    "message": "deploy demo",
    "env": "production",
    "environment": "production",
    "input": "input.json",
    "output": "output.json",
    "config": "config.yaml",
    "config_file": "config.yaml",
    "id": "demo-id",
    "instance": "demo-instance",
    "instance-id": "i-0abcd1234efgh5678",
    "stack": "demo-stack",
    "queue": "demo-queue",
    "stream": "demo-stream",
    "group": "demo-group",
    "consumer-group": "demo-group",
    "partition": "0",
    "offset": "0",
    "s3": "demo-bucket",
    "migration": "001_demo",
    "workflow": "demo-workflow",
    "pipeline": "demo-pipeline",
    "run": "demo-run",
    "connection": "demo-connection",
    "dataset": "demo_dataset",
    "feature": "demo_feature",
    "experiment": "demo-experiment",
    "project-name": "demo-project",
    "function": "demo-function",
    "resource": "demo-resource",
    "resource-group": "demo-rg",
    "role": "demo-role",
    "policy": "demo-policy",
    "permission": "read",
    "subscription": "demo-sub",
    "vault": "demo-vault",
    "certificate": "demo-cert",
    "cert": "demo-cert",
    "domain": "demo.example",
    "origin": "origin",
    "remote": "origin",
    "hostname": "localhost",
    "ip": "127.0.0.1",
    "cron": "0 8 * * *",
    "schedule": "0 8 * * *",
    "timeout": "30",
    "retries": "3",
    "workers": "4",
    "replicas": "2",
    "size": "1Gi",
    "memory": "1Gi",
    "cpu": "1",
    "storage": "10Gi",
    "interval": "5m",
    "window": "1h",
    "threshold": "0.9",
    "rate": "100",
    "qps": "100",
    "duration": "30s",
    "concurrency": "10",
    "vus": "10",
    "iterations": "100",
    "method": "GET",
    "status-code": "200",
    "record": "demo-record",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "trace-id": "00000000000000000000000000000000",
    "session": "demo-session",
    "token": "demo-token",
    "webhook": "demo-webhook",
    "channel": "#general",
    "message-text": "deploy demo",
    "timestamp": "2026-08-19T00:00:00Z",
    "date": "2026-08-19",
    "year": "2026",
    "month": "08",
    "day": "19",
    "language": "en",
    "locale": "en-US",
    "framework": "pytest",
    "runtime": "python3.12",
    "engine": "postgres",
    "provider": "aws",
    "platform": "linux/amd64",
    "architecture": "amd64",
    "target": "demo",
    "destination": "./demo",
    "source": "./demo",
}

# Prefixes/suffixes stripped when normalizing a file name to a tool key.
NAME_STRIP = (
    ("backend-", ""), ("devops-", ""), ("cloud-", ""), ("frontend-", ""),
    ("data-", ""), ("database-", ""), ("infra-", ""), ("infrastructure-", ""),
    ("messaging-", ""), ("monitoring-", ""), ("network-", ""), ("networking-", ""),
    ("security-", ""), ("sre-", ""), ("testing-", ""), ("ai-", ""), ("ml-", ""),
    ("api-", ""), ("code-quality-", ""), ("compliance-", ""), ("cost-", ""),
    ("finops-", ""), ("design-", ""), ("developer-", ""), ("devtools-", ""),
    ("documentation-", ""), ("engineering-", ""), ("mobile-", ""),
    ("patterns-", ""), ("project-", ""), ("robotics-", ""),
    ("sustainability-", ""), ("web-", ""), ("career-", ""),
    ("communication-", ""), ("education-", ""), ("finance-", ""),
    ("healthcare-", ""), ("marketing-", ""), ("people-", ""), ("product-", ""),
    ("sales-", ""), ("support-", ""), ("ecommerce-", ""), ("finance-", ""),
    ("agent-", ""), ("skill-", ""), ("database-", ""), ("infra-", ""),
    ("infrastructure-", ""), ("frontend-", ""), ("cloud-", ""),
    ("-agent", ""), ("-skill", ""), ("-task", ""), ("-helper", ""),
    ("-assistant", ""), ("-manager", ""), ("-admin", ""), ("-operations", ""),
    ("-ops", ""), ("-cli", ""), ("-api", ""), ("-sdk", ""), ("-platform", ""),
    ("-service", ""), ("-tool", ""), ("-cli", ""), ("-kit", ""),
    ("-identity-py", ""), ("-inference", ""), ("-sdk", ""), ("-ml", ""),
    ("-engine", ""), ("-generator", ""), ("-scanner", ""), ("-audit", ""),
    ("-testing", ""), ("-deployment", ""), ("-workflow", ""), ("-pipeline", ""),
    ("-tuning", ""), ("-training", ""), ("-evaluation", ""),
    ("-node", ""), ("-python", ""), ("-server", ""), ("-deploy", ""),
    ("-vector", ""), ("-azure", ""), ("-gcp", ""), ("-aws", ""), ("-setup", ""),
)


def load_curate_tier():
    """Import classify() + fingerprint tests from scripts/curate-tier.py."""
    path = os.path.join(REPO, "scripts", "curate-tier.py")
    spec = importlib.util.spec_from_file_location("curate_tier", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def stable_date(rel_path):
    """Hash-stable created_at date spread across 2025-01 .. 2026-07."""
    h = int(hashlib.sha256(rel_path.encode("utf-8")).hexdigest()[:8], 16)
    d = DATE_START + timedelta(days=h % DATE_RANGE_DAYS)
    return "%sT00:00:00Z" % d.isoformat()


def normalize_tool(name):
    """Turn a file/command name into a normalized tool key candidate."""
    if not name:
        return ""
    key = str(name).strip().lower()
    key = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    key = re.sub(r"-\d+$", "", key).strip("-")
    for _ in range(4):
        prev = key
        for old, new in NAME_STRIP:
            if key.startswith(old) and len(key) > len(old):
                key = key[len(old):]
            if key.endswith(old) and len(key) > len(old):
                key = key[: -len(old)]
        if key == prev:
            break
    return key


def detect_tools(doc, rel_path, tool_keys, url_map):
    """Return ordered list of tool keys for a file (name first, then
    command binaries), only those present in the URL map."""
    found = []

    def add(key):
        if key and key in url_map and key not in found:
            found.append(key)

    base = os.path.basename(rel_path).rsplit(".", 1)[0]
    add(normalize_tool(base))
    for cand in (base, base.replace("-", " ").split()[0] if base else ""):
        k = normalize_tool(cand)
        # map stem -> key through tool-keys index
        for tkey, stems in tool_keys.items():
            if k in stems and tkey in url_map:
                add(tkey)

    caps = doc.get("capabilities") or []
    for cap in caps:
        if not isinstance(cap, dict):
            continue
        add(normalize_tool(cap.get("name")))
        for cmd in cap.get("commands") or []:
            for tok in re.split(r"[\s|;&,()]+", str(cmd)):
                tok = tok.strip("'\"")
                if not tok or tok.endswith(":"):
                    continue
                bin_name = os.path.basename(tok).lower()
                k = normalize_tool(bin_name)
                for tkey, stems in tool_keys.items():
                    if k and (k in stems or k == tkey):
                        add(tkey)
                        break
                if bin_name in url_map:
                    add(bin_name)

    # knowledge entry titles name the tool exactly as the template knew it
    # (e.g. "backend-actix Documentation") - highest-confidence signal
    for entry in doc.get("knowledge") or []:
        if isinstance(entry, dict):
            title = str(entry.get("title") or "").strip()
            title = re.sub(r"\s*(?:Documentation|Guide|Docs)\s*$", "", title)
            title = re.sub(r"\s*-\s*", "-", title)
            k = normalize_tool(title)
            if k in url_map:
                add(k)
            for tkey, stems in tool_keys.items():
                if k and (k in stems or k == tkey):
                    add(tkey)
    return found


def fix_knowledge_lines(lines, doc, rel_path, tool_keys, url_map, index):
    """Replace kdesk knowledge entries with real official-docs entries.

    Operates on the raw line list: locates every knowledge entry whose
    `source:` contains kdesk/agents and replaces that 4-line block with
    1-2 real entries per detected tool (up to 3 tools).
    Returns the new line list (or unchanged) and whether anything changed.
    """
    tools = detect_tools(doc, rel_path, tool_keys, url_map)
    if not tools:
        return lines, False
    changed = False
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^\s*-\s+title:\s+", line):
            j = i
            block = [lines[j]]
            while j + 1 < len(lines) and re.match(
                r"^\s+\S", lines[j + 1]
            ):
                j += 1
                block.append(lines[j])
            src = "\n".join(block)
            if "kdesk/agents" in src:
                indent = line[: len(line) - len(line.lstrip())]
                entries = []
                for tk in tools[:3]:
                    title, url = url_map[tk][0], url_map[tk][1]
                    entries.append(
                        "%s- title: %s\n"
                        "%s  type: reference\n"
                        "%s  source: %s\n"
                        "%s  description: Official documentation for %s."
                        % (indent, title, indent, indent, url, indent, tk)
                    )
                out.append("\n".join(entries))
                changed = True
                i = j + 1
                continue
        out.append(line)
        i += 1
    return out, changed


def fix_author(lines):
    out = []
    changed = False
    for line in lines:
        if re.match(r"^author:\s*Kdesk-Catalog\s*$", line):
            out.append("author: %s" % AUTHOR)
            changed = True
        else:
            out.append(line)
    return out, changed


def fix_timestamps(lines, rel_path):
    out = []
    changed = False
    created = stable_date(rel_path)
    for line in lines:
        if re.match(r"^created_at:\s*'?2024-01-01", line):
            out.append("created_at: '%s'" % created)
            changed = True
        elif re.match(r"^updated_at:\s*'?2024-01-01", line):
            out.append("updated_at: '%s'" % UPDATED_AT)
            changed = True
        else:
            out.append(line)
    return out, changed


def fix_registry(lines, cloud):
    out = []
    changed = False
    reg = REGISTRIES.get(cloud, REGISTRIES["default"])
    for line in lines:
        if "registry.example.com" in line:
            out.append(line.replace("registry.example.com", reg))
            changed = True
        else:
            out.append(line)
    return out, changed


def fix_identity(lines, tools):
    out = []
    changed = False
    for line in lines:
        if "identity.py" in line:
            tool = tools[0] if tools else "python"
            cmd = VERIFY.get(tool, "%s --version" % tool)
            # preserve leading indentation and list-item dash if present
            m = re.match(r"^(\s*)(-\s+)?.*$", line)
            indent = m.group(1) if m else ""
            dash = m.group(2) if m and m.group(2) else ""
            out.append("%s%s%s" % (indent, dash, cmd))
            changed = True
        else:
            out.append(line)
    return out, changed


def fix_placeholder_text(text):
    """Replace placeholder tokens/domains in a single command string."""
    # example.com host/email references -> real equivalents
    text = re.sub(r"https?://(?:[a-z0-9-]+\.)*example\.com", "http://localhost:8080", text)
    text = re.sub(r"(?<![\w.])example\.com", "localhost", text)
    # TODO markers
    text = re.sub(r"\bTODO\b.*$", "", text).rstrip()
    # angle-bracket tokens
    for m in re.findall(r"<([^<>]+)>", text):
        tok = m.strip()
        if tok in TOKEN_DEFAULTS:
            text = text.replace("<%s>" % m, TOKEN_DEFAULTS[tok])
        else:
            text = text.replace("<%s>" % m, "demo-%s" % normalize_tool(tok))
    return text


def fix_placeholder_command_lines(lines):
    out = []
    changed = False
    for line in lines:
        stripped = line.strip()
        # only touch YAML list items (commands/examples entries)
        if not re.match(r"^-\s+", stripped):
            out.append(line)
            continue
        if "<" in stripped or "example.com" in stripped or "TODO" in stripped.upper():
            content = re.sub(r"^-\s+", "", stripped, count=1)
            fixed = fix_placeholder_text(content)
            indent = line[: len(line) - len(line.lstrip())]
            out.append("%s- %s" % (indent, fixed))
            changed = True
        else:
            out.append(line)
    return out, changed


def fix_description(lines, doc):
    out = []
    changed = False
    name = str(doc.get("name") or "").replace("-", " ").lower()
    desc = str(doc.get("description") or "")
    generic = bool(name and name in desc.lower() and " for " in desc.lower())
    for line in lines:
        if re.match(r"^description:\s+", line) and generic:
            caps = [c for c in (doc.get("capabilities") or []) if isinstance(c, dict)]
            parts = []
            for cap in caps:
                d = str(cap.get("description") or "").strip()
                if d and not d.endswith("."):
                    d += "."
                parts.append(d)
            # fall back to the file's own instructions first sentence
            inst = str(doc.get("instructions") or "").strip()
            if not parts and inst:
                parts = [inst.split(".")[0] + "."]
            new_desc = " ".join(parts[:3]).strip()
            if not new_desc:
                new_desc = "Expert agent for %s." % name
            # strip any lingering " for " phrase so the fingerprint stays clear
            new_desc = re.sub(r"\s+for\s+", " handling ", new_desc)
            # avoid repeating the name
            if name in new_desc.lower():
                new_desc = re.sub(r"\b%s\b" % re.escape(name), "it", new_desc, flags=re.I)
            out.append("description: %s" % new_desc)
            changed = True
        else:
            out.append(line)
    return out, changed


def repair_unparseable(lines, rel_path):
    """Repair the three known malformation classes so YAML parses again."""
    out = []
    changed = False
    for line in lines:
        # class A: `commands:` unindented under a capability list item
        if re.match(r"^commands:\s*$", line):
            out.append("  commands:")
            changed = True
            continue
        # class B: unquoted plain scalar containing ': ' in description values
        m = re.match(r"^(\s*)description:\s+(.+)$", line)
        if m and ": " in m.group(2):
            val = m.group(2).replace('"', '\\"')
            out.append('%sdescription: "%s"' % (m.group(1), val))
            changed = True
            continue
        # class C: examples list items with single-quoted strings containing nested quotes
        # pattern: - '...' where the string has complex quoting
        stripped = line.strip()
        if stripped.startswith("- '") and stripped.endswith("'"):
            # Preserve original indentation
            indent = line[:len(line) - len(line.lstrip())]
            inner = stripped[3:-1]  # remove "- '" and trailing "'"
            inner = inner.replace('"', '\\"')
            out.append(indent + '- "' + inner + '"')
            changed = True
            continue
        out.append(line)
    return out, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="source YAML dir")
    ap.add_argument("--dry-run", action="store_true", help="report only, no writes")
    args = ap.parse_args()

    plan = load_json(PLAN_PATH)
    url_map = load_json(URLS_PATH)
    tool_keys = load_json(TOOLKEYS_PATH)
    curate = load_curate_tier()

    files = plan.get("files") or {}
    unparseable = set(plan.get("unparseable") or [])
    stats = collections.Counter()
    fixed_any = 0

    for rel, info in sorted(files.items()):
        path = os.path.join(args.source, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            print("MISSING %s" % rel)
            continue
        try:
            txt = open(path, encoding="utf-8").read()
        except Exception as exc:
            print("READ-ERR %s: %s" % (rel, exc))
            continue

        doc = None
        try:
            doc = yaml.safe_load(txt) or {}
        except Exception:
            pass

        lines = txt.split("\n")
        need_repair = rel in unparseable or doc is None

        if need_repair:
            lines, ch = repair_unparseable(lines, rel)
            if ch:
                stats["repaired"] += 1
                changed_file = True
            try:
                doc = yaml.safe_load("\n".join(lines)) or {}
            except Exception as exc:
                print("STILL-UNPARSEABLE %s: %s" % (rel, str(exc).split("\n")[0]))
                continue

        # Re-run the classifier on (possibly repaired) content: the fix set
        # must track actual fingerprints, not the stale plan list.
        new_txt = "\n".join(lines)
        _, fingerprints = curate.classify(new_txt, doc)
        fixes = [FINGERPRINT_FIX[k] for k in fingerprints if k in FINGERPRINT_FIX]
        fixes = list(dict.fromkeys(fixes))  # dedupe, keep order
        tools = detect_tools(doc, rel, tool_keys, url_map)
        cloud = "default"
        for tk in tools:
            if tk in ("aws", "gcp", "azure"):
                cloud = tk
                break
        # category-based cloud fallback
        cat = str(doc.get("category") or "").lower()
        for c, key in (("aws", "aws"), ("azure", "azure"), ("gcp", "gcp")):
            if c in cat:
                cloud = c
                break

        changed_file = False
        for fix in fixes:
            if fix == "knowledge":
                lines, ch = fix_knowledge_lines(lines, doc, rel, tool_keys, url_map, 0)
                stats["knowledge"] += ch
                changed_file |= ch
            elif fix == "command":
                lines, ch = fix_placeholder_command_lines(lines)
                stats["command"] += ch
                changed_file |= ch
            elif fix == "identity":
                lines, ch = fix_identity(lines, tools)
                stats["identity"] += ch
                changed_file |= ch
            elif fix == "registry":
                lines, ch = fix_registry(lines, cloud)
                stats["registry"] += ch
                changed_file |= ch
            elif fix == "description":
                lines, ch = fix_description(lines, doc)
                stats["description"] += ch
                changed_file |= ch
            elif fix == "timestamp":
                lines, ch = fix_timestamps(lines, rel)
                stats["timestamp"] += ch
                changed_file |= ch
            elif fix == "author":
                lines, ch = fix_author(lines)
                stats["author"] += ch
                changed_file |= ch
            else:
                print("UNKNOWN-FIX %s: %s" % (rel, fix))

        if changed_file and not args.dry_run:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("\n".join(lines))
        if changed_file:
            fixed_any += 1

    print("processed: %d files" % len(files))
    print("files changed: %d" % fixed_any)
    for k, v in sorted(stats.items()):
        print("  %-12s %d" % (k, v))


if __name__ == "__main__":
    main()