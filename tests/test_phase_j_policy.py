"""Phase J: persisted review policies (license, duplicates, security exceptions)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.duplicates import DuplicateDetector, DuplicatePolicy
from kdesk.license import LicenseAudit, LicensePolicy
from kdesk.registry import Catalog
from kdesk.security import (
    SEVERITY_INDEX,
    REDACTED,
    SecurityExceptions,
    SecurityScanner,
    scan_repo,
)


def _write_def(base: Path, name: str, **kwargs) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    body = f"name: {name}\ncategory: {kwargs.get('category', 'devops')}\n"
    body += f"description: {kwargs.get('description', 'x' * 250)}\n"
    body += f"type: {kwargs.get('type', 'agent')}\n"
    if kwargs.get("license") is not None:
        body += f"license: {kwargs['license']}\n"
    body += "capabilities:\n  - name: run\n    description: run\n    commands: ['helm lint']\n"
    path = base / f"{name}.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def _catalog(tmp_path, defs):
    base = tmp_path / "universal-agents" / "devops" / "agent"
    for name, kwargs in defs:
        _write_def(base, name, **kwargs)
    return Catalog(tmp_path / "universal-agents")


# ------------------------------------------------------------------ license
def test_license_policy_round_trip(tmp_path):
    policy = LicensePolicy()
    policy.set_entry(
        "agent-a",
        "intentionally_unspecified",
        "Public skill manifest: license intentionally unspecified.",
        reviewer="kdesk-platform",
        date="2026-08-15",
    )
    path = tmp_path / "reports" / "license-policy.json"
    policy.save(path)
    loaded = LicensePolicy.load(path)
    entry = loaded.classification_for("agent-a")
    assert entry["class"] == "intentionally_unspecified"
    assert entry["reviewer"] == "kdesk-platform"
    assert entry["date"] == "2026-08-15"
    assert json.loads(path.read_text(encoding="utf-8"))["schema"] == "license-policy-v1"


def test_license_policy_load_missing_file(tmp_path):
    assert LicensePolicy.load(tmp_path / "nope.json").entries == {}


def test_license_audit_policy_resolves_missing(tmp_path):
    catalog = _catalog(tmp_path, [("agent-a", {})])
    bare = LicenseAudit(catalog).audit()
    assert bare["missing_count"] == 1
    assert bare["unresolved_count"] == 1

    policy = LicensePolicy()
    policy.set_entry("agent-a", "intentionally_unspecified", "intentionally unspecified")
    report = LicenseAudit(catalog).audit(policy=policy)
    assert report["policy_applied"] is True
    assert report["missing_count"] == 0
    assert report["unspecified_count"] == 1
    assert report["unresolved_count"] == 0
    assert report["classification"]["agent-a"]["class"] == "intentionally_unspecified"


def test_license_audit_unknown_class_bucket(tmp_path):
    catalog = _catalog(tmp_path, [("agent-a", {})])
    policy = LicensePolicy()
    policy.set_entry("agent-a", "not-a-class", "bad")
    report = LicenseAudit(catalog).audit(policy=policy)
    assert report["unknown_count"] == 1
    assert report["unresolved_count"] == 1


def test_license_audit_explicit_and_inherited(tmp_path):
    catalog = _catalog(tmp_path, [("agent-a", {}), ("agent-b", {})])
    policy = LicensePolicy()
    policy.set_entry("agent-a", "explicit", "declared", license_="MIT")
    policy.set_entry("agent-b", "inherited", "from repo", license_="Apache-2.0")
    report = LicenseAudit(catalog).audit(policy=policy)
    assert "agent-a" in report["valid"]
    assert "agent-b" in report["inherited"]
    assert report["unresolved_count"] == 0
    assert report["license_counts"]["mit"] >= 1


def test_license_audit_third_party(tmp_path):
    catalog = _catalog(tmp_path, [("agent-a", {})])
    policy = LicensePolicy()
    policy.set_entry("agent-a", "third_party", "bundled dependency")
    report = LicenseAudit(catalog).audit(policy=policy)
    assert "agent-a" in report["third_party"]
    assert report["unresolved_count"] == 0


# ---------------------------------------------------------------- duplicates
def test_duplicate_policy_family_id_sorted():
    assert DuplicatePolicy.family_id(["b", "a"]) == "a|b"


def test_duplicate_policy_round_trip(tmp_path):
    policy = DuplicatePolicy()
    policy.set_entry(
        "deepseek-deployment|deepseek-sdk",
        "merge",
        "Same project split across deploy and SDK.",
        members=["deepseek-deployment", "deepseek-sdk"],
        reviewer="kdesk-platform",
        date="2026-08-15",
    )
    path = tmp_path / "reports" / "duplicate-classifications.json"
    policy.save(path)
    loaded = DuplicatePolicy.load(path)
    entry = loaded.classification_for("deepseek-deployment|deepseek-sdk")
    assert entry["class"] == "merge"
    assert sorted(entry["members"]) == ["deepseek-deployment", "deepseek-sdk"]


DESC = "Deploy and operate containerized workloads with production-grade tooling " * 3


def _dupe_catalog(tmp_path):
    base = tmp_path / "universal-agents" / "devops" / "agent"
    _write_def(base, "agent-a", description=DESC)
    _write_def(base, "agent-b", description=DESC.replace("operate", "manage"))
    return Catalog(tmp_path / "universal-agents")


def test_duplicate_detect_unresolved_then_classified(tmp_path):
    catalog = _dupe_catalog(tmp_path)
    bare = DuplicateDetector(catalog).detect()
    assert bare["family_count"] == 1
    assert bare["unresolved_count"] == 1

    fid = DuplicatePolicy.family_id(["agent-a", "agent-b"])
    policy = DuplicatePolicy()
    policy.set_entry(fid, "keep_variant", "deliberate platform variant")
    report = DuplicateDetector(catalog).detect(policy=policy)
    assert report["classified_count"] == 1
    assert report["unresolved_count"] == 0
    assert report["families"][0]["class"] == "keep_variant"


def test_duplicate_detect_clean(tmp_path):
    catalog = _catalog(
        tmp_path,
        [("agent-a", {"description": "x" * 250}), ("agent-b", {"description": "y" * 250})],
    )
    assert DuplicateDetector(catalog).detect()["family_count"] == 0


# ---------------------------------------------------------------- security
def test_security_exceptions_reject_wildcard():
    exc = SecurityExceptions()
    with pytest.raises(ValueError):
        exc.add("agent-a", "agent", "*", "aws_key", "no wildcards")
    with pytest.raises(ValueError):
        exc.add("agent-*", "agent", "description", "aws_key", "no wildcards")


def test_security_exceptions_match_exact():
    exc = SecurityExceptions()
    exc.add("agent-a", "agent", "description", "aws_key", "fixture key")
    finding = {
        "definition": "agent-a",
        "type": "agent",
        "field": "description",
        "pattern": "aws_key",
    }
    assert exc.matches(finding) is True
    finding["field"] = "instructions"
    assert exc.matches(finding) is False


def test_security_exceptions_round_trip(tmp_path):
    exc = SecurityExceptions()
    exc.add("agent-a", "agent", "description", "aws_key", "fixture", reviewer="kdesk-platform")
    path = tmp_path / "reports" / "security-exceptions.json"
    exc.save(path)
    loaded = SecurityExceptions.load(path)
    assert loaded.matches({"definition": "agent-a", "type": "agent",
                           "field": "description", "pattern": "aws_key"}) is True


def test_security_scan_redacts_and_severity(tmp_path):
    secret = "AKIA0000000000000000"
    catalog = _catalog(tmp_path, [("agent-a", {"description": "key " + secret})])
    findings = SecurityScanner(catalog).scan()
    assert len(findings) == 1
    assert findings[0]["pattern"] == "aws_key"
    assert findings[0]["severity"] == "HIGH"
    assert REDACTED in findings[0]["excerpt"]
    assert secret not in findings[0]["excerpt"]


def test_security_scan_repo_blocking_requires_exception(tmp_path):
    secret = "AKIA0000000000000000"
    catalog = _catalog(tmp_path, [("agent-a", {"description": "key " + secret})])
    assert scan_repo(tmp_path)["blocking_count"] == 1

    exc = SecurityExceptions()
    exc.add("agent-a", "agent", "description", "aws_key", "fixture key", reviewer="kdesk-platform")
    exc_path = tmp_path / "reports" / "security-exceptions.json"
    exc.save(exc_path)
    report = scan_repo(tmp_path, exceptions_path=exc_path)
    assert report["blocking_count"] == 0
    assert report["excepted_count"] == 1
    assert report["exceptions_applied"] is True


def test_security_scan_medium_not_blocking(tmp_path):
    catalog = _catalog(tmp_path, [("agent-a", {"description": "password = 'hunter2secret'"})])
    findings = SecurityScanner(catalog).scan()
    assert findings and findings[0]["pattern"] == "password_eq"
    assert SEVERITY_INDEX[findings[0]["severity"]] < SEVERITY_INDEX["HIGH"]
    assert scan_repo(tmp_path)["blocking_count"] == 0
