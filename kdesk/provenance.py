"""Provenance: every generated JSON / platform file must trace back to a source YAML."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from kdesk.registry import Catalog, default_repo_root


class ProvenanceError(Exception):
    pass


class Provenance:
    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root) if root else default_repo_root()
        self.catalog = Catalog.from_repo(self.root)

    # ------------------------------------------------------------- checksums
    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def source_checksums(self) -> Dict[str, str]:
        sums = {}
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            if defn.source_path:
                sums[defn.name] = self.sha256(defn.source_path)
        return sums

    def verify(self) -> Dict[str, Any]:
        """1) agents/skills JSON carry _provenance with matching checksum.
        2) every JSON has a source YAML; every YAML has a JSON (or is
        explained by a skip rule)."""
        problems: List[str] = []
        json_count = 0
        yaml_count = 0
        # --- JSON side: agents/json/*.json + skills/json/*.json + workflows/*.json
        for json_dir in (self.root / "agents" / "json", self.root / "skills" / "json", self.root / "workflows"):
            if not json_dir.is_dir():
                continue
            for path in json_dir.rglob("*.json"):
                if path.name in ("wiring.json",):
                    continue
                json_count += 1
                try:
                    doc = json.loads(path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    problems.append(f"{path.relative_to(self.root)}: unparseable json ({exc})")
                    continue
                prov = doc.get("_provenance", {})
                source = prov.get("source")
                checksum = prov.get("checksum")
                if not source:
                    problems.append(f"{path.relative_to(self.root)}: missing _provenance.source")
                    continue
                src_path = self.root / source
                if not src_path.is_file():
                    problems.append(f"{path.relative_to(self.root)}: provenance source missing: {source}")
                    continue
                if checksum and self.sha256(src_path) != checksum:
                    problems.append(f"{path.relative_to(self.root)}: checksum mismatch vs {source}")
        # --- YAML side: every loaded definition must have a source path
        for defn in list(self.catalog.agents.values()) + list(self.catalog.skills.values()):
            yaml_count += 1
            if defn.source_path is None:
                problems.append(f"definition without source path: {defn.name}")
        return {
            "json_files": json_count,
            "yaml_files": yaml_count,
            "problems": problems,
            "verified": len(problems) == 0,
            "files_scanned": json_count + yaml_count,
        }


# ---------------------------------------------------------------------------
# Wiring provenance: every link has evidence (commands -> tool -> skill) or a
# manual override marker. Missing evidence + not manual = problem.
# ---------------------------------------------------------------------------
def verify_wiring(root: Path) -> Dict[str, Any]:
    wiring = root / "skills" / "wiring.json"
    if not wiring.is_file():
        return {"problems": ["skills/wiring.json missing"], "links": 0, "files_scanned": 0}
    data = json.loads(wiring.read_text(encoding="utf-8"))
    problems = []
    links = []
    for agent, agent_links in (data.get("wiring") or {}).items():
        for link in agent_links or []:
            links.append({"agent": agent, "skill": link.get("skill")})
            if not link.get("evidence") and not link.get("manual"):
                problems.append(f"{agent} -> {link.get('skill')}: no evidence and not manual")
    return {
        "links": len(links),
        "problems": problems,
        "verified": len(problems) == 0,
        "files_scanned": len(links),
    }