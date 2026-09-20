"""catalog-rename.py - L1: replace combinatorial agent/skill names with content-derived names.

Detects generator-style names (vN suffix, -deploy-sdk / -server-agent / -sdk-agent /
-rag-agent / -inference-server stacks, trailing -agent noise) and derives a meaningful
name from the document's own content: the family subject stem plus role words taken
from real capability names, command labels, or command tools. Never invents words.

Usage:
  python scripts/catalog-rename.py            # preview: print mapping, change nothing
  python scripts/catalog-rename.py --apply    # rename files/folders + rewrite document fields
"""
import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = ROOT / "universal-agents"

TAIL_RE = re.compile(
    r"-deploy-sdk-agent|-inference-server-agent|-deploy-sdk|-inference-server"
    r"|-deploy-agent|-server-agent|-sdk-agent|-rag-agent|-engineer|-specialist"
    r"|-designer|-expert|-developer|-practitioner|-agent|-inference|-engine|-v\d+$",
    re.IGNORECASE,
)

# Words that carry no identity signal in names. Language/SDK words are informative.
STOP = {
    "the", "a", "an", "you", "are", "for", "with", "and", "or", "to", "of", "in",
    "on", "ml", "ai", "api", "agent", "agents", "expert", "skill", "engineer",
    "specialist", "app", "application", "module", "service", "operations", "operate",
    "build", "run", "manage", "use", "help", "users", "framework", "integration",
    "integrate", "component", "components", "basic", "general", "common", "quick",
    "example", "examples", "note", "standard", "setup", "set", "get", "deploy",
    "deployment", "server", "client", "tool", "tools",
}

MECH_MAP = {
    "jwt-auth": "jwt",
    "oidc-flow": "oidc",
    "mtls-auth": "mtls",
    "api-key-mgmt": "keys",
    "api-key-management": "keys",
}


def norm(w):
    return re.sub(r"[^a-z0-9]", "-", re.sub(r"\s+", " ", (w or "").lower().strip())).strip("-")


def role_candidates(d, subject):
    subj = {subject} | set(subject.split("-"))
    out = []
    for cap in d.get("capabilities") or []:
        if not isinstance(cap, dict):
            continue
        raw = norm(cap.get("name"))
        known = MECH_MAP.get(raw)
        if known:
            out.append(known)
            break
        words = [w for w in raw.split("-")
                 if w not in STOP and w not in subj and not re.fullmatch(r"v?\d+", w)]
        if words:
            out.append("-".join(words[:2]))
    for cap in d.get("capabilities") or []:
        for cmd in cap.get("commands") or []:
            if not isinstance(cmd, str):
                continue
            m = re.match(r"^\s*([A-Za-z][\w-]*):", cmd)
            if m:
                lab = norm(m.group(1))
                if lab and lab not in STOP and lab not in subj and lab not in out:
                    out.append(lab)
    for cap in d.get("capabilities") or []:
        for cmd in cap.get("commands") or []:
            if not isinstance(cmd, str):
                continue
            for t in re.findall(r"[a-zA-Z][a-zA-Z0-9_.]{1,}", cmd):
                w = t.split("/")[-1]
                if w.count(".") != 1:
                    continue
                if w.split(".")[0] in ("python", "node", "npx"):
                    w = w.split(".")[-1]
                elif w.split(".")[0] == subject:
                    w = w.split(".")[-1]
                if w not in STOP and w not in subj and w not in out:
                    out.append(w)
    return out


def needs_rename(name):
    n = str(name)
    if re.search(r"-v\d+$", n, re.IGNORECASE):
        return True
    return bool(re.search(
        r"-(?:deploy-sdk|deploy-agent|server-agent|sdk-agent|rag-agent"
        r"|inference-server)(?:-(?:agent|engine))?(?:-v\d+)?$",
        n, re.IGNORECASE))


def subject_stem(name, category):
    n = str(name)
    cat = norm(category) if category else None
    if cat and n.startswith(cat + "-"):
        n = n[len(cat) + 1:]
    n = TAIL_RE.sub("", n).strip("-")
    if not n:
        n = norm(name)
    return n


def cmd_fingerprint(d):
    fp = []
    for cap in d.get("capabilities") or []:
        if not isinstance(cap, dict):
            continue
        for c in cap.get("commands") or []:
            fp.append(norm(c))
    return fp


def title_display(new_name):
    out = []
    for p in new_name.split("-"):
        if p == "mtls":
            out.append("mTLS")
        elif p == "jwt":
            out.append("JWT")
        elif p == "oidc":
            out.append("OIDC")
        else:
            out.append(p.capitalize())
    return " ".join(out)


def iter_docs():
    for f in sorted(UA.rglob("*.yaml")):
        txt = f.read_text(encoding="utf-8")
        d = yaml.safe_load(txt)
        if not isinstance(d, dict) or not d.get("name"):
            continue
        yield f, d, txt


def build_mapping():
    mapping, used, fam = {}, {}, {}
    for f, d, _ in iter_docs():
        if not needs_rename(d["name"]):
            continue
        old = norm(d["name"])
        stem = subject_stem(old, d.get("category"))
        if stem not in fam:
            fam[stem] = []
        fam[stem].append((f, d))
    for f, d in [x for v in fam.values() for x in v]:
        old = norm(d["name"])
        stem = subject_stem(old, d.get("category"))
        cands = role_candidates(d, stem)
        fp = cmd_fingerprint(d)
        chosen = None
        for c in cands:
            maybe = norm(f"{stem}-{c}")
            if maybe not in used:
                chosen = maybe
                break
            holder = used[maybe]
            if holder["fp"] == fp:
                chosen = maybe
                break
        if not chosen:
            sub = norm(d.get("subcategory"))
            base = norm(f"{stem}-{sub}") if sub and sub not in (stem, "general") else stem
            if base == stem:
                subj = {stem} | set(stem.split("-"))
                for tok in re.findall(r"[a-zA-Z][a-zA-Z0-9_]{3,}", norm(d.get("description") or " ")):
                    if tok not in STOP and tok not in subj and not re.fullmatch(r"v?\d+", tok):
                        base = norm(f"{stem}-{tok}")
                        break
            n = 2
            while True:
                maybe = base if n == 2 and base not in used else norm(f"{base}-{n}")
                if maybe not in used:
                    chosen = maybe
                    break
                n += 1
        used[chosen] = {"fp": fp, "doc": d}
        mapping[f] = (chosen, d)
    return mapping


def mutate_blob(blob, d, old, new):
    for key in ("name", "display_name"):
        val = d.get(key)
        if not val or norm(str(val)) != old:
            continue
        repl = new if key == "name" else title_display(new)
        blob = re.sub(
            r'(?m)^(\s*' + re.escape(key) + r":\s*)[\"']?" + re.escape(str(val)) + r"[\"']?\s*$",
            r"\1" + repl, blob)
    platforms = d.get("platforms") or {}
    gh = (platforms.get("github_copilot") or {}).get("prompt_file")
    if gh == old + ".md":
        blob = blob.replace("prompt_file: " + old + ".md", "prompt_file: " + new + ".md")
    oc = (platforms.get("opencode") or {}).get("plugin")
    if oc == "opencode-" + old:
        blob = blob.replace("opencode-" + old, "opencode-" + new)
    out_lines = []
    for line in blob.splitlines(keepends=True):
        if re.match(r"^\s*(?:name|display_name):", line):
            out_lines.append(line)
        elif old in line:
            out_lines.append(line.replace(old, new))
        else:
            out_lines.append(line)
    return "".join(out_lines)


def apply(mapping):
    moved = 0
    for f, (new, d) in mapping.items():
        old = norm(d["name"])
        blob = mutate_blob(f.read_text(encoding="utf-8"), d, old, new)
        dest_dir = f.parent
        if f.parent.name in ("agent", "skill") and f.parent.parent.name == old:
            dest_dir = f.parent.parent.parent / new / f.parent.name
        target = dest_dir / f"{new}.yaml"
        if target == f:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(blob, encoding="utf-8")
        f.unlink()
        moved += 1
    for d in sorted(UA.iterdir(), key=lambda p: len(str(p)), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    return moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    mapping = build_mapping()
    rows = sorted(mapping.items(), key=lambda kv: str(kv[0]))
    print(f"files to rename: {len(mapping)}")
    print("--- sample (first 45) ---")
    for f, (new, d) in rows[:45]:
        print(f"  {str(f.relative_to(ROOT)):<72} -> {new}")
    print("--- sample (last 25) ---")
    for f, (new, d) in rows[-25:]:
        print(f"  {str(f.relative_to(ROOT)):<72} -> {new}")
    if args.apply:
        print(f"applied: {apply(mapping)} files renamed")


if __name__ == "__main__":
    main()