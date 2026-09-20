import yaml
from pathlib import Path
from collections import defaultdict

SRC = Path(__file__).resolve().parents[1] / "universal-agents"

def main():
    all_files = sorted(SRC.rglob("*.yaml"))
    all_files = [p for p in all_files if p.name != "registry.yaml"]
    by_name = defaultdict(list)
    all_names = set()
    for p in all_files:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(doc, dict) and doc.get("name"):
            by_name[doc["name"]].append(p)
            all_names.add(doc["name"])

    dups = {k: v for k, v in by_name.items() if len(v) > 1}
    renamed = 0
    for name, paths in sorted(dups.items()):
        keeper, *rest = paths
        for p in rest:
            rel = p.relative_to(SRC)
            category = rel.parts[0]
            new_name = f"{name}-{category}"
            counter = 2
            while new_name in all_names:
                new_name = f"{name}-{category}-{counter}"
                counter += 1
            doc = yaml.safe_load(p.read_text(encoding="utf-8"))
            doc["name"] = new_name
            if doc.get("display_name") and doc.get("display_name") == name:
                doc["display_name"] = new_name
            with open(p, "w", encoding="utf-8") as f:
                yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"renamed {name} -> {new_name}  ({rel})")
            renamed += 1
            all_names.add(new_name)
    print(f"total renamed: {renamed}")

if __name__ == "__main__":
    main()
