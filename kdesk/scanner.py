"""Project scanner: discovers AI development configuration in a project directory."""
from __future__ import annotations

import json
import os
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from kdesk.adapters import AdapterRegistry
from kdesk.registry import default_repo_root


@dataclass
class ScannedFile:
    path: Path
    rel_path: str
    content: Any
    parse_error: Optional[str] = None


@dataclass
class ProjectScanResult:
    project_root: Path
    platform: Optional[str] = None
    agents: List[ScannedFile] = field(default_factory=list)
    skills: List[ScannedFile] = field(default_factory=list)
    commands: List[ScannedFile] = field(default_factory=list)
    workflows: List[ScannedFile] = field(default_factory=list)
    configuration: List[ScannedFile] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_root": str(self.project_root),
            "platform": self.platform,
            "agents": [{"path": str(f.rel_path), "error": f.parse_error} for f in self.agents],
            "skills": [{"path": str(f.rel_path), "error": f.parse_error} for f in self.skills],
            "commands": [{"path": str(f.rel_path), "error": f.parse_error} for f in self.commands],
            "workflows": [{"path": str(f.rel_path), "error": f.parse_error} for f in self.workflows],
            "configuration": [{"path": str(f.rel_path), "error": f.parse_error} for f in self.configuration],
            "metadata": self.metadata,
            "errors": self.errors,
            "warnings": self.warnings,
        }


# Platform-specific configuration patterns
PLATFORM_CONFIG_PATTERNS: Dict[str, List[str]] = {
    "claude_code": [
        ".claude/agents/**/*.md",
        ".claude/skills/**/*.md",
        ".claude/agents/**/*.yaml",
        ".claude/skills/**/*.yaml",
        "CLAUDE.md",
    ],
    "cursor": [
        ".cursor/rules/**/*.mdc",
        ".cursor/rules/**/*.md",
    ],
    "github_copilot": [
        ".github/instructions/**/*.instructions.md",
        ".github/copilot-instructions.md",
    ],
    "windsurf": [
        ".windsurf/rules/**/*.md",
    ],
    "opencode": [
        ".opencode/agents/**/*.md",
        ".opencode/skills/**/*.md",
        ".opencode/plugin/**/*.ts",
    ],
    "codex_cli": [
        ".agents/skills/**/*.md",
        "AGENTS.md",
    ],
    "gemini_cli": [
        ".gemini/skills/**/*.md",
    ],
    "zed": [
        ".agents/skills/**/*.md",
    ],
    "cline": [
        ".clinerules/skills/**/*.md",
    ],
    "roo_code": [
        ".roo/skills/**/*.md",
    ],
    "goose": [
        ".goose/recipes/**/*.yaml",
        "recipes/**/*.yaml",
    ],
    "aider": [
        ".aider.conf.yml",
        "conventions/**/*.md",
    ],
    "openhands": [
        ".openhands/microagents/**/*.md",
    ],
    "google_jules": [
        "AGENTS.md",
    ],
    "warp": [
        "WARP.md",
    ],
    "codegpt": [
        "AGENTS.md",
    ],
    "cody": [
        ".vscode/cody.json",
    ],
    "firebender": [
        ".firebender/agents/**/*.md",
        ".firebender/firebender.json",
    ],
    "continue": [
        ".continue/rules/**/*.md",
    ],
    "tabnine": [
        ".tabnine/guidelines/**/*.md",
    ],
    "supermaven": [
        ".supermaven/rules/**/*.md",
    ],
    "grok_build": [
        ".grok/rules/**/*.md",
    ],
    "amazon_q": [
        ".amazonq/rules/**/*.md",
    ],
    "augment": [
        ".augment/rules/**/*.md",
    ],
    "firebase_studio": [
        ".idx/rules/**/*.mdc",
    ],
}


# Generic AI project configuration files
GENERIC_CONFIG_PATTERNS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".agents/**/*.yaml",
    ".agents/**/*.yml",
    "skills/**/*.yaml",
    "skills/**/*.yml",
    "agents/**/*.yaml",
    "agents/**/*.yml",
    "commands/**/*.yaml",
    "commands/**/*.yml",
    "workflows/**/*.yaml",
    "workflows/**/*.yml",
    "*.yaml",
    "*.yml",
    "*.md",
]


class ProjectScanner:
    """Scans a project directory for AI development configuration."""

    def __init__(self, project_root: Path, registry_root: Optional[Path] = None):
        self.project_root = Path(project_root).resolve()
        self.registry_root = Path(registry_root).resolve() if registry_root else default_repo_root()
        self.adapters = AdapterRegistry(self.registry_root)
        self._platform_hints: Dict[str, int] = {}

    def scan(self) -> ProjectScanResult:
        """Scan the project directory and return structured results."""
        result = ProjectScanResult(project_root=self.project_root)

        # Collect all relevant files
        all_files = self._collect_files()

        # Classify and parse each file
        for file_path in all_files:
            self._process_file(file_path, result)

        # Detect target platform
        result.platform = self._detect_platform()

        # Extract metadata
        result.metadata = self._extract_metadata(result)

        return result

    def _collect_files(self) -> List[Path]:
        """Collect all relevant configuration files."""
        files: Set[Path] = set()

        # Platform-specific patterns
        for platform, patterns in PLATFORM_CONFIG_PATTERNS.items():
            for pattern in patterns:
                for path in self.project_root.glob(pattern):
                    if path.is_file():
                        files.add(path)

        # Generic patterns
        for pattern in GENERIC_CONFIG_PATTERNS:
            for path in self.project_root.glob(pattern):
                if path.is_file():
                    files.add(path)

        return sorted(files)

    def _process_file(self, file_path: Path, result: ProjectScanResult) -> None:
        """Parse and classify a single file."""
        try:
            rel_path = file_path.relative_to(self.project_root)
        except ValueError:
            return

        content = None
        parse_error = None

        try:
            if file_path.suffix in (".yaml", ".yml"):
                content = yaml.safe_load(file_path.read_text(encoding="utf-8"))
            elif file_path.suffix in (".json",):
                content = json.loads(file_path.read_text(encoding="utf-8"))
            elif file_path.suffix in (".md", ".mdc", ".instructions.md"):
                content = file_path.read_text(encoding="utf-8")
            elif file_path.suffix in (".yaml", ".yml"):
                content = yaml.safe_load(file_path.read_text(encoding="utf-8"))
            else:
                content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            parse_error = str(e)

        scanned = ScannedFile(
            path=file_path,
            rel_path=str(file_path.relative_to(self.project_root)),
            content=content,
            parse_error=parse_error,
        )

        if parse_error:
            result.warnings.append(f"Parse error in {scanned.rel_path}: {parse_error}")

        # Classify by path and content
        rel_str = str(file_path.relative_to(self.project_root))
        self._classify_file(scanned, result)

    def _classify_file(self, scanned: ScannedFile, result: ProjectScanResult) -> None:
        """Classify a file by its path and content."""
        rel_str = scanned.rel_path
        content = scanned.content

        # Check for agent/skill YAML
        if isinstance(scanned.content, dict):
            content = scanned.content
            # Check for type field (new format) or subcategory field (legacy format)
            file_type = content.get("type") or content.get("subcategory")
            if file_type in ("agent", "skill") or "capabilities" in content:
                if file_type == "skill" or "skill" in str(scanned.path):
                    result.skills.append(scanned)
                else:
                    result.agents.append(scanned)
                return

        # Check by path patterns
        rel_str = str(scanned.rel_path)

        if "/agents/" in str(scanned.path) or rel_str.endswith("-agent.yaml") or rel_str.endswith("-agent.yml"):
            result.agents.append(scanned)
        elif "/skills/" in str(scanned.path) or rel_str.endswith("-skill.yaml") or rel_str.endswith("-skill.yml"):
            result.skills.append(scanned)
        elif "/commands/" in str(scanned.path) or "command" in str(scanned.path).lower():
            result.commands.append(scanned)
        elif "/workflows/" in str(scanned.path) or rel_str.endswith(".workflow.yaml") or rel_str.endswith(".workflow.yml"):
            result.workflows.append(scanned)
        elif any(name in rel_str for name in ["config", "setting", "setting", ".json", ".toml"]):
            result.configuration.append(scanned)
        else:
            result.configuration.append(scanned)

    def _detect_platform(self) -> Optional[str]:
        """Detect the target platform from project structure."""
        scores: Dict[str, int] = {}

        # Score based on directory presence
        for platform, patterns in PLATFORM_CONFIG_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if list(self.project_root.glob(pattern)):
                    score += 1
            if score > 0:
                scores[platform] = score

        if not scores:
            return None

        # Return highest scoring platform
        return max(scores.items(), key=lambda x: x[1])[0]

    def _extract_metadata(self, result: ProjectScanResult) -> Dict[str, Any]:
        """Extract metadata from scanned files."""
        metadata = {
            "total_files": len(result.agents) + len(result.skills) + len(result.commands) +
                          len(result.workflows) + len(result.configuration),
            "agent_count": len(result.agents),
            "skill_count": len(result.skills),
            "command_count": len(result.commands),
            "workflow_count": len(result.workflows),
            "config_count": len(result.configuration),
            "parse_errors": sum(1 for f in result.agents + result.skills + result.configuration if f.parse_error),
        }

        # Extract tool usage from agents/skills
        tools_used: Set[str] = set()
        for scanned in result.agents + result.skills:
            if isinstance(scanned.content, dict):
                caps = scanned.content.get("capabilities", [])
                for cap in caps:
                    if isinstance(cap, dict):
                        for cmd in cap.get("commands", []):
                            if isinstance(cmd, str):
                                first = cmd.strip().split()[0] if cmd.strip() else ""
                                if first:
                                    tools_used.add(first)

        metadata["tools_detected"] = sorted(tools_used)
        return metadata


def scan_project(project_root: Path, registry_root: Optional[Path] = None) -> ProjectScanResult:
    """Convenience function to scan a project."""
    scanner = ProjectScanner(project_root, registry_root)
    return scanner.scan()