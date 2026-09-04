"""Compatibility engine: analyzes project components against platform capabilities."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
from pathlib import Path

from kdesk.adapters import AdapterRegistry
from kdesk.capabilities import CapabilityIndex
from kdesk.contracts import Contract, derive_contract, compatibility as contract_compatibility
from kdesk.models import BaseDefinition
from kdesk.registry import Catalog
from kdesk.scanner import ProjectScanResult, ScannedFile


# Platform capability definitions
PLATFORM_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "claude_code": {
        "supported_fields": ["name", "description", "tools", "instructions", "examples", "tools", "system_prompt"],
        "required_fields": ["name", "description"],
        "supported_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "WebFetch", "WebSearch"],
        "unsupported_fields": ["plugin", "recipe", "microagent", "unsupported_field"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description", "tools"],
    },
    "opencode": {
        "supported_fields": ["name", "description", "mode", "model", "instructions", "examples", "tools"],
        "required_fields": ["name", "description", "mode"],
        "supported_tools": ["bash", "read", "write", "edit", "glob", "grep", "task", "web_fetch", "web_search"],
        "unsupported_fields": ["plugin", "recipe", "microagent"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description", "mode"],
    },
    "cursor": {
        "supported_fields": ["name", "description", "globs", "alwaysApply"],
        "required_fields": ["description", "globs"],
        "supported_tools": [],
        "unsupported_fields": ["model", "plugin", "recipe", "microagent"],
        "max_file_size": 50000,
        "supported_formats": [".mdc"],
        "frontmatter_required": ["description", "globs"],
    },
    "windsurf": {
        "supported_fields": ["trigger", "description", "globs", "alwaysApply"],
        "required_fields": ["trigger", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "plugin", "recipe", "microagent"],
        "max_file_size": 12000,
        "supported_formats": [".md"],
        "frontmatter_required": ["trigger", "description"],
    },
    "github_copilot": {
        "supported_fields": ["applyTo", "description"],
        "required_fields": ["applyTo"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe", "microagent"],
        "max_file_size": 50000,
        "supported_formats": [".instructions.md"],
        "frontmatter_required": ["applyTo"],
    },
    "codex_cli": {
        "supported_fields": ["name", "description"],
        "required_fields": ["name", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description"],
    },
    "gemini_cli": {
        "supported_fields": ["name", "description"],
        "required_fields": ["name", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description"],
    },
    "zed": {
        "supported_fields": ["name", "description"],
        "required_fields": ["name", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description"],
    },
    "cline": {
        "supported_fields": ["name", "description"],
        "required_fields": ["name", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description"],
    },
    "roo_code": {
        "supported_fields": ["name", "description"],
        "required_fields": ["name", "description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description"],
    },
    "goose": {
        "supported_fields": ["title", "description", "version", "instructions", "prompt"],
        "required_fields": ["title", "description", "prompt"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".yaml"],
        "frontmatter_required": ["title", "description", "prompt"],
    },
    "aider": {
        "supported_fields": ["description", "commands"],
        "required_fields": ["description"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe", "microagent"],
        "max_file_size": 100000,
        "supported_formats": [".md", ".yaml"],
        "frontmatter_required": ["description"],
    },
    "openhands": {
        "supported_fields": ["name", "description", "type", "triggers"],
        "required_fields": ["name", "description", "type"],
        "supported_tools": [],
        "unsupported_fields": ["model", "tools", "plugin", "recipe"],
        "max_file_size": 100000,
        "supported_formats": [".md"],
        "frontmatter_required": ["name", "description", "type"],
    },
}


@dataclass
class PlatformProfile:
    """Platform capability profile."""
    name: str
    supported_fields: List[str]
    required_fields: List[str]
    supported_tools: List[str]
    unsupported_fields: List[str]
    max_file_size: int
    supported_formats: List[str]
    frontmatter_required: List[str]


def get_platform_profile(platform: str) -> PlatformProfile:
    """Get platform capability profile."""
    caps = PLATFORM_CAPABILITIES.get(platform, {})
    return PlatformProfile(
        name=platform,
        supported_fields=caps.get("supported_fields", []),
        required_fields=caps.get("required_fields", []),
        supported_tools=caps.get("supported_tools", []),
        unsupported_fields=caps.get("unsupported_fields", []),
        max_file_size=caps.get("max_file_size", 100000),
        supported_formats=caps.get("supported_formats", []),
        frontmatter_required=caps.get("frontmatter_required", []),
    )


@dataclass
class CompatibilityEngine:
    """Analyzes project components against platform capabilities."""
    catalog: Catalog
    platform: str
    registry_root: Path

    def __post_init__(self):
        self.profile = get_platform_profile(self.platform)
        self.capability_index = CapabilityIndex(
            list(self.catalog.agents.values()) + list(self.catalog.skills.values())
        )
        self.adapters = AdapterRegistry(self.registry_root)

    def analyze(self, scan_result) -> List[Any]:
        """Analyze all scanned components and return issues."""
        from kdesk.diagnostics import Issue, Severity, Category

        issues = []

        # Analyze each component
        for scanned in scan_result.agents:
            issues.extend(self._analyze_component(scanned, "agent"))

        for scanned in scan_result.skills:
            issues.extend(self._analyze_component(scanned, "skill"))

        for scanned in scan_result.workflows:
            issues.extend(self._analyze_component(scanned, "workflow"))

        for scanned in scan_result.commands:
            issues.extend(self._analyze_component(scanned, "command"))

        for scanned in scan_result.configuration:
            issues.extend(self._analyze_component(scanned, "config"))

        return issues

    def _analyze_component(self, scanned, comp_type: str) -> List[Any]:
        """Analyze a single component."""
        from kdesk.diagnostics import Issue, Severity, Category

        issues = []

        if scanned.parse_error:
            issues.append(Issue(
                id=f"parse_error_{scanned.rel_path}",
                severity=Severity.ERROR,
                category=Category.INVALID_STRUCTURE,
                file=scanned.rel_path,
                component=scanned.rel_path,
                platform=self.platform,
                message=f"Failed to parse file: {scanned.parse_error}",
                reason="File could not be parsed as valid YAML/JSON/Markdown",
                suggested_fix="Fix syntax errors in the file",
                fixable=False,
            ))
            return issues

        content = scanned.content
        if not content:
            return issues

        # Type-specific analysis
        if comp_type == "agent" or scanned.rel_path in [s.rel_path for s in getattr(self, '_agents', [])] or "agent" in str(scanned.path).lower():
            issues.extend(self._analyze_agent(scanned))
        elif comp_type == "skill" or "skill" in str(scanned.path).lower():
            issues.extend(self._analyze_skill(scanned))
        elif comp_type == "workflow" or "workflow" in str(scanned.path).lower():
            issues.extend(self._analyze_workflow(scanned))

        # Common checks for all components
        issues.extend(self._check_common(scanned))

        return issues

    def _analyze_agent(self, scanned) -> List[Any]:
        """Analyze an agent definition."""
        from kdesk.diagnostics import Issue, Severity, Category

        issues = []
        content = scanned.content

        if not isinstance(content, dict):
            return issues

        # Check required fields
        for field in self.profile.required_fields:
            if field not in content:
                issues.append(Issue(
                    id=f"missing_required_{scanned.rel_path}_{field}",
                    severity=Severity.ERROR,
                    category=Category.MISSING_REQUIRED,
                    file=scanned.rel_path,
                    component=scanned.rel_path,
                    platform=self.platform,
                    message=f"Missing required field: {field}",
                    reason=f"Platform {self.platform} requires field '{field}'",
                    suggested_fix=f"Add '{field}' field to the definition",
                    fixable=True,
                    fix_data={"field": field, "action": "add_field"},
                ))

        # Check unsupported fields
        for field in self.profile.unsupported_fields:
            if field in content:
                issues.append(Issue(
                    id=f"unsupported_field_{scanned.rel_path}_{field}",
                    severity=Severity.WARNING,
                    category=Category.UNSUPPORTED_FIELD,
                    file=scanned.rel_path,
                    component=scanned.rel_path,
                    platform=self.platform,
                    message=f"Unsupported field: {field}",
                    reason=f"Platform {self.platform} does not support field '{field}'",
                    suggested_fix=f"Remove or convert field '{field}'",
                    fixable=True,
                    fix_data={"field": field, "action": "remove_field"},
                ))

        # Check tools
        tools = content.get("tools", [])
        if isinstance(tools, list):
            for tool in tools:
                if tool not in self.profile.supported_tools and tool not in ["inherit", "auto"]:
                    issues.append(Issue(
                        id=f"unsupported_tool_{scanned.rel_path}_{tool}",
                        severity=Severity.WARNING,
                        category=Category.UNSUPPORTED_TOOL,
                        file=scanned.rel_path,
                        component=scanned.rel_path,
                        platform=self.platform,
                        message=f"Unsupported tool: {tool}",
                        reason=f"Platform {self.platform} does not support tool '{tool}'",
                        suggested_fix=f"Replace '{tool}' with a supported tool or remove",
                        fixable=True,
                        fix_data={"tool": tool, "action": "replace_tool"},
                    ))

        # Check platform-specific unsupported fields (nested under platforms.<platform>)
        platforms = content.get("platforms", {})
        platform_config: dict = {}
        if isinstance(platforms, dict) and self.platform in platforms:
            platform_config = platforms[self.platform]
            if isinstance(platform_config, dict):
                for field in self.profile.unsupported_fields:
                    if field in platform_config:
                        issues.append(Issue(
                            id=f"unsupported_field_{scanned.rel_path}_platforms.{self.platform}.{field}",
                            severity=Severity.WARNING,
                            category=Category.UNSUPPORTED_FIELD,
                            file=scanned.rel_path,
                            component=scanned.rel_path,
                            platform=self.platform,
                            message=f"Unsupported field in platforms.{self.platform}: {field}",
                            reason=f"Platform {self.platform} does not support field '{field}' in platform-specific configuration",
                            suggested_fix=f"Remove or convert field '{field}' in platforms.{self.platform}",
                            fixable=True,
                            fix_data={"field": field, "action": "remove_field", "path": f"platforms.{self.platform}.{field}"},
                        ))

        # Check for invalid model values
        if "model" in platform_config:
            model_value = platform_config["model"]
            if model_value not in ["inherit", "auto"]:
                issues.append(Issue(
                    id=f"invalid_model_{scanned.rel_path}_platforms.{self.platform}",
                    severity=Severity.WARNING,
                    category=Category.UNSUPPORTED_FIELD,
                    file=scanned.rel_path,
                    component=scanned.rel_path,
                    platform=self.platform,
                    message=f"Invalid model value: {model_value}",
                    reason=f"Platform {self.platform} only supports 'inherit' or 'auto' for model field",
                    suggested_fix=f"Change model value to 'inherit' or 'auto'",
                    fixable=True,
                    fix_data={"field": "model", "action": "replace_value", "path": f"platforms.{self.platform}.model", "value": "inherit"},
                ))

        # Check frontmatter requirements
        if hasattr(self, '_check_frontmatter'):
            pass  # For markdown files with frontmatter

        return issues

    def _analyze_skill(self, scanned) -> List[Any]:
        """Analyze a skill definition."""
        # Similar to agent analysis
        return self._analyze_agent(scanned)

    def _analyze_workflow(self, scanned) -> List[Any]:
        """Analyze a workflow definition."""
        from kdesk.diagnostics import Issue, Severity, Category

        issues = []
        content = scanned.content

        if not isinstance(content, dict):
            return issues

        # Check workflow structure
        if "steps" not in content:
            issues.append(Issue(
                id=f"workflow_missing_steps_{scanned.rel_path}",
                severity=Severity.ERROR,
                category=Category.INVALID_STRUCTURE,
                file=scanned.rel_path,
                component=scanned.rel_path,
                platform=self.platform,
                message="Workflow missing 'steps' field",
                reason="Workflows must have a 'steps' array",
                suggested_fix="Add 'steps' array with workflow steps",
                fixable=False,
            ))

        # Validate step references
        if "steps" in content and isinstance(content["steps"], list):
            for i, step in enumerate(content["steps"]):
                if isinstance(step, dict):
                    if "type" not in step:
                        issues.append(Issue(
                            id=f"step_missing_type_{scanned.rel_path}_{i}",
                            severity=Severity.ERROR,
                            category=Category.INVALID_STRUCTURE,
                            file=scanned.rel_path,
                            line=i,
                            component=scanned.rel_path,
                            platform=self.platform,
                            message=f"Step {i} missing 'type' field",
                            reason="Each workflow step must have a 'type' field",
                            suggested_fix="Add 'type' field (skill, agent, capability, tool)",
                            fixable=True,
                            fix_data={"step_index": i, "action": "add_step_type"},
                        ))

        return issues

    def _check_common(self, scanned) -> List[Any]:
        """Common checks for all components."""
        from kdesk.diagnostics import Issue, Severity, Category

        issues = []
        content = scanned.content

        if not isinstance(content, dict):
            return issues

        # Check file size
        file_size = 0
        try:
            file_path = Path(scanned.path)
            if file_path.exists():
                file_size = file_path.stat().st_size
        except Exception:
            pass

        if file_size > self.profile.max_file_size:
            issues.append(Issue(
                id=f"file_too_large_{scanned.rel_path}",
                severity=Severity.WARNING,
                category=Category.INVALID_STRUCTURE,
                file=scanned.rel_path,
                component=scanned.rel_path,
                platform=self.platform,
                message=f"File size ({file_size} bytes) exceeds platform limit ({self.profile.max_file_size} bytes)",
                reason=f"Platform {self.platform} has a maximum file size limit",
                suggested_fix="Split the definition into smaller files or reduce content",
                fixable=False,
            ))

        # Check for template/placeholder content
        content_str = str(content)
        if any(placeholder in content_str.lower() for placeholder in [
            "todo", "fixme", "placeholder", "example.com", "your-", "your_",
            "<example>", "<placeholder>", "changeme", "change_me"
        ]):
            issues.append(Issue(
                id=f"placeholder_content_{scanned.rel_path}",
                severity=Severity.WARNING,
                category=Category.INVALID_STRUCTURE,
                file=scanned.rel_path,
                component=scanned.rel_path,
                platform=self.platform,
                message="Possible placeholder/template content detected",
                reason="File contains placeholder text that should be replaced",
                suggested_fix="Review and replace placeholder content with actual values",
                fixable=False,
            ))

        return issues


def analyze_compatibility(
    scan_result,
    platform: str,
    catalog: Catalog,
    registry_root: Path
) -> List[Any]:
    """Convenience function to analyze compatibility."""
    engine = CompatibilityEngine(catalog, platform, registry_root)
    return engine.analyze(scan_result)