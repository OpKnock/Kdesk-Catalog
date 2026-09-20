"""Tests for Kdesk Doctor components."""
import tempfile
import yaml
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from kdesk.scanner import ProjectScanner, scan_project
from kdesk.compatibility import CompatibilityEngine, get_platform_profile
from kdesk.diagnostics import Issue, Severity, Category, DiagnosticReport, redact_secrets, redact_dict_secrets
from kdesk.fixer import FixEngine
from kdesk.registry import Catalog
from kdesk.registry import default_repo_root


def test_scanner_valid_project():
    """Test scanner with valid project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        (project_root / ".claude").mkdir()
        (project_root / ".claude" / "agents").mkdir()
        (project_root / ".claude" / "agents" / "test-agent.yaml").write_text("""
name: test-agent
display_name: Test Agent
category: test
subcategory: agent
description: A test agent
version: "1.0.0"
capabilities:
  - name: Test Capability
    description: Test
    commands:
      - echo hello
    examples:
      - echo hello
    parameters: []
knowledge:
  - title: Test Doc
    type: documentation
    source: https://example.com
    description: Test
instructions: |
  Test instructions
platforms:
  claude_code:
    tools: [Bash, Read]
    model: inherit
""")
        
        scanner = ProjectScanner(project_root)
        result = scanner.scan()
        
        assert len(result.agents) == 1
        # Handle both forward and backslashes on Windows
        assert result.agents[0].rel_path.replace("\\", "/") == ".claude/agents/test-agent.yaml"
        assert result.platform == "claude_code"
        assert result.metadata["agent_count"] == 1


def test_scanner_missing_directory():
    """Test scanner with missing directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir) / "nonexistent"
        scanner = ProjectScanner(project_root)
        result = scanner.scan()
        
        assert result.agents == []
        assert result.skills == []


def test_scanner_malformed_yaml():
    """Test scanner with malformed YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        (project_root / "bad.yaml").write_text("invalid: yaml: content: [")
        
        scanner = ProjectScanner(project_root)
        result = scanner.scan()
        
        # Should handle gracefully
        assert len(result.warnings) > 0 or len(result.agents) == 0


def test_compatibility_engine():
    """Test compatibility engine."""
    registry_root = default_repo_root()
    catalog = Catalog.from_repo(registry_root)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        (project_root / "test.yaml").write_text("""
name: test-agent
display_name: Test Agent
category: test
subcategory: agent
description: A test agent
version: "1.0.0"
capabilities:
  - name: Test
    description: Test
    commands:
      - kubectl apply -f config.yaml
    examples:
      - kubectl apply -f config.yaml
    parameters: []
knowledge: []
instructions: Test
platforms:
  claude_code:
    tools: [Bash, Read]
    model: gpt-4
    plugin: test-plugin
""")
        
        scan_result = scan_project(project_root, default_repo_root())
        engine = CompatibilityEngine(Catalog.from_repo(default_repo_root()), "claude_code", Path(default_repo_root()))
        issues = engine.analyze(scan_result)
        
        # Should detect unsupported model value and unsupported fields
        assert len(issues) > 0
        # Check for model warning
        model_issues = [i for i in issues if "model" in i.id.lower()]
        assert len(model_issues) > 0


def test_severity_system():
    """Test severity system."""
    assert Severity.CRITICAL.weight() == 10
    assert Severity.ERROR.weight() == 5
    assert Severity.WARNING.weight() == 2
    assert Severity.INFO.weight() == 1


def test_compatibility_score():
    """Test compatibility score calculation."""
    # Test the scoring logic directly
    critical = 1
    errors = 1
    warnings = 1
    penalty = min(critical * 20, 80) + min(errors * 10, 60) + min(warnings * 2, 40)
    score = max(0, 100 - penalty)
    assert score == 68
    
    # Test with no issues
    critical = 0
    errors = 0
    warnings = 0
    penalty = min(critical * 20, 80) + min(errors * 10, 60) + min(warnings * 2, 40)
    score = max(0, 100 - penalty)
    assert score == 100
    
    # Test with multiple critical
    critical = 5
    penalty = min(critical * 20, 80)  # capped at 80
    assert penalty == 80


def test_redact_secrets():
    """Test secret redaction."""
    # Test basic redaction - patterns match key=value format
    assert "REDACTED" in redact_secrets("api_key=secret123")
    assert "REDACTED" in redact_secrets('token="secret"')
    
    # Should not redact normal file paths
    assert redact_secrets("file.yaml") == "file.yaml"
    assert redact_secrets("path/to/file.yaml") == "path/to/file.yaml"
    
    # Test dict redaction - needs key=value format
    d = {"api_key": "api_key=secret123", "nested": {"token": 'token="secret"'}}
    redacted = redact_dict_secrets(d)
    assert "REDACTED" in redacted["api_key"]
    assert "REDACTED" in redacted["nested"]["token"]


def test_diagnostic_report():
    """Test diagnostic report."""
    from kdesk.diagnostics import DiagnosticReport, ComponentReport, Issue, Severity, Category
    
    issue = Issue(
        id="test",
        severity=Severity.WARNING,
        category=Category.UNSUPPORTED_FIELD,
        file="test.yaml",
        component="test",
        platform="claude_code",
        message="Test",
        reason="test",
        suggested_fix="fix",
        fixable=True,
    )
    
    component = ComponentReport(
        name="test",
        type="agent",
        file="test.yaml",
        platform="claude_code",
        issues=[Issue(id="1", severity=Severity.WARNING, category=Category.UNSUPPORTED_FIELD, file="test.yaml", component="test", platform="claude_code", message="test", reason="test", suggested_fix="fix", fixable=True)]
    )
    
    report = DiagnosticReport(
        project_root="/test",
        platform="claude_code",
        score=80,
        components=[component],
        issues=[Issue(id="1", severity=Severity.WARNING, category=Category.UNSUPPORTED_FIELD, file="test.yaml", component="test", platform="claude_code", message="test", reason="test", suggested_fix="fix", fixable=True)],
    )
    
    assert report.error_count == 0
    assert report.warning_count == 1
    assert report.fixable_count == 1
    assert report.score == 80
    
    # Test to_dict
    d = report.to_dict()
    assert d["score"] == 80
    assert d["error_count"] == 0
    assert d["warning_count"] == 1


def run_tests():
    """Run all tests."""
    tests = [
        test_scanner_valid_project,
        test_scanner_missing_directory,
        test_scanner_malformed_yaml,
        test_compatibility_engine,
        test_severity_system,
        test_compatibility_score,
        test_redact_secrets,
        test_diagnostic_report,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print("[PASS] " + test.__name__)
            passed += 1
        except Exception as e:
            print("[FAIL] " + test.__name__ + ": " + str(e))
            failed += 1
    
    print("\nResults: " + str(passed) + " passed, " + str(failed) + " failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)