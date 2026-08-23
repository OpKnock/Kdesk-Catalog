#!/usr/bin/env python3
"""Generate a platform × feature compatibility matrix (Markdown + JSON)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kdesk.platforms import PlatformRegistry


def main():
    registry = PlatformRegistry.load()
    matrix = registry.compatibility_matrix()
    platforms = sorted(matrix.keys())
    features = ["frontmatter", "tools", "instructions", "examples", "parameters", "sub_agents"]

    # Markdown
    lines = [
        "# Platform Compatibility Matrix",
        "",
        "| Platform | " + " | ".join(features) + " |",
        "|---|" + "---|" * len(features),
    ]
    for pid in platforms:
        row = matrix[pid]
        cells = []
        for feat in features:
            v = row.get(feat, "?")
            icon = {"supported": "✅", "transformed": "🔄", "embedded": "📝",
                    "unsupported": "❌", "n/a": "—"}.get(v, v)
            cells.append(icon)
        lines.append(f"| **{pid}** | " + " | ".join(cells) + " |")

    lines.append("")
    lines.append("Legend: ✅ supported · 🔄 transformed · 📝 embedded · ❌ unsupported")

    md_path = ROOT / "reports" / "compatibility-matrix.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {md_path}")

    # JSON
    json_path = ROOT / "reports" / "compatibility-matrix.json"
    json_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] wrote {json_path}")


if __name__ == "__main__":
    main()
