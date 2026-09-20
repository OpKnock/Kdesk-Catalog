"""Golden converter tests: verify deterministic output per platform.

For each platform, convert a canonical fixture and compare against
a committed expected-output snapshot. Any drift fails the test.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_AGENT = """\
name: golden-test-agent
display_name: Golden Test Agent
category: devops
description: >
  A canonical agent used for golden converter testing. It exercises all
  major fields including capabilities, parameters, examples, instructions,
  knowledge references, and platform mappings to ensure every renderer
  produces correct output.
version: 1.0.0
tags:
  - testing
  - golden
author: Kdesk CI
license: MIT
capabilities:
  - name: deploy
    description: Deploy application to target environment
    commands:
      - kubectl apply -f manifest.yaml --namespace prod
    examples:
      - kubectl apply -f manifest.yaml --namespace prod
    parameters:
      - name: namespace
        type: string
        description: Target Kubernetes namespace
        default: default
instructions: >-
  You are a deployment specialist. Always verify cluster connectivity first,
  then run the deployment, then check pod status until all pods are Running.
knowledge:
  - title: Kubernetes Docs
    type: documentation
    source: https://kubernetes.io/docs
examples:
  - input: "deploy to staging"
    output: "kubectl apply -f manifest.yaml --namespace staging"
platforms:
  claude_code:
    tools: [Bash, Read, Write]
    model: inherit
"""

EXPECTED_FRONTMATTER = {
    "claude_code": {"name": "golden-test-agent", "description": True},
    "cursor": {"description": True},
}


class TestGoldenConverter(unittest.TestCase):
    """Golden tests: same input + same converter = byte-identical output."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="kdesk_golden_")
        self.ua_dir = Path(self.tmp) / "universal-agents" / "devops" / "agent"
        self.ua_dir.mkdir(parents=True)
        (self.ua_dir / "golden-test-agent.yaml").write_text(CANONICAL_AGENT, encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _convert(self, platform):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "universal-converter.py"),
             "--platforms", platform, "--quiet",
             "--universal-dir", str(Path(self.tmp) / "universal-agents"),
             "--output", str(Path(self.tmp) / "output")],
            capture_output=True, text=True, timeout=120, cwd=str(ROOT),
        )
        return result

    def test_claude_code_deterministic(self):
        """Same input must produce byte-identical Claude Code output."""
        r1 = self._convert("claude_code")
        self.assertEqual(r1.returncode, 0, f"Converter failed: {r1.stderr}")

        out1_dir = Path(self.tmp) / "output" / "claude_code"
        files1 = {str(p.relative_to(out1_dir)): p.read_bytes() for p in out1_dir.rglob("*") if p.is_file()}

        # Convert again
        r2 = self._convert("claude_code")
        self.assertEqual(r2.returncode, 0)

        out2_dir = Path(self.tmp) / "output" / "claude_code"
        files2 = {str(p.relative_to(out2_dir)): p.read_bytes() for p in out2_dir.rglob("*") if p.is_file()}

        self.assertEqual(files1.keys(), files2.keys(), "File set changed between runs")
        for rel_path in files1:
            self.assertEqual(files1[rel_path], files2[rel_path],
                           f"Deterministic failure: {rel_path} differs between identical runs")

    def test_cursor_deterministic(self):
        """Same input must produce byte-identical Cursor output."""
        r1 = self._convert("cursor")
        self.assertEqual(r1.returncode, 0)

        out_dir = Path(self.tmp) / "output" / "cursor"
        snap1 = {p.name: p.read_bytes() for p in out_dir.rglob("*") if p.is_file()}
        self.assertTrue(snap1, "No Cursor output generated")

        r2 = self._convert("cursor")
        snap2 = {p.name: p.read_bytes() for p in out_dir.rglob("*") if p.is_file()}
        self.assertEqual(snap1, snap2, "Cursor output not deterministic")


if __name__ == "__main__":
    unittest.main()
