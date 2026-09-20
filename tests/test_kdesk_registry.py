"""kdesk unit tests: catalog registry."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.registry import Catalog, CatalogError


def _write_universal(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "skill").mkdir(parents=True)
    (base / "devops" / "agent" / "helm-master.yaml").write_text(
        """
name: helm-master
display_name: Helm Master
category: devops
description: Operates Helm charts end to end, with linting, testing, packaging, and release workflows.
version: "1.0.0"
type: agent
capabilities:
  - name: lint-charts
    description: Lint a Helm chart.
    commands: ["helm lint ./chart"]
examples: ["helm lint ./chart"]
instructions: Always verify chart output before committing.
knowledge:
  - title: helm docs
    content: https://helm.sh/docs
platforms:
  claude_code:
    format: agent-md
""",
        encoding="utf-8",
    )
    (base / "devops" / "skill" / "helm-lint-skill.yaml").write_text(
        """
name: helm-lint
display_name: Helm Lint
category: devops
description: Lints Helm charts and reports violations before deployment. This skill covers the full lint cycle.
version: "1.0.0"
type: skill
capabilities:
  - name: lint
    description: Lint charts.
    commands: ["helm lint ./chart"]
""",
        encoding="utf-8",
    )
    return base


def test_catalog_loads_nested_layout(tmp_path):
    catalog = Catalog(_write_universal(tmp_path))
    assert catalog.stats()["agents"] == 1
    assert catalog.stats()["skills"] == 1
    assert catalog.get_agent("helm-master") is not None
    assert catalog.get_skill("helm-lint") is not None


def test_catalog_flat_layout_skill_suffix(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops").mkdir(parents=True)
    (base / "devops" / "foo-agent.yaml").write_text(
        "name: foo\ncategory: devops\ndescription: x" + "y" * 250 + "\ntype: agent\n",
        encoding="utf-8",
    )
    (base / "devops" / "bar-skill.yaml").write_text(
        "name: bar\ncategory: devops\ndescription: x" + "y" * 250 + "\ntype: skill\n",
        encoding="utf-8",
    )
    catalog = Catalog(base)
    assert catalog.get_agent("foo") is not None
    assert catalog.get_skill("bar") is not None


def test_catalog_duplicate_names_error(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    for i in (1, 2):
        (base / "devops" / "agent" / f"dup-{i}.yaml").write_text(
            f"name: dup\ncategory: c\ndescription: {'x' * 250}\ntype: agent\n",
            encoding="utf-8",
        )
    with pytest.raises(CatalogError):
        Catalog(base)


def test_catalog_missing_dir():
    with pytest.raises(CatalogError):
        Catalog(Path("C:/definitely/not/here"))


def test_catalog_search_and_checksum(tmp_path):
    catalog = Catalog(_write_universal(tmp_path))
    hits = catalog.search("helm")
    assert any(h.name == "helm-master" for h in hits)
    assert catalog.checksum("helm-master") is not None
    assert catalog.checksum("nope") is None


def test_catalog_error_recording(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    (base / "devops" / "agent" / "bad.yaml").write_text("not: [valid: yaml: [", encoding="utf-8")
    catalog = Catalog(base)
    assert catalog.stats()["errors"] == 1
    assert catalog.errors[0].startswith(str(base))


def test_flat_layout_slash_type_overrides(tmp_path):
    base = tmp_path / "universal-agents"
    (base / "devops").mkdir(parents=True)
    (base / "devops" / "s.yaml").write_text(
        "name: s\ncategory: c\ndescription: " + "x" * 250 + "\ntype: skill\n",
        encoding="utf-8",
    )
    assert Catalog(base).get_skill("s") is not None