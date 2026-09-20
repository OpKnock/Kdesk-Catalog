"""Automatic fix engine: safely applies fixes to compatibility issues."""
from __future__ import annotations

import shutil
import json
import yaml
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from pathlib import Path

from kdesk.diagnostics import Issue, FixResult, FixReport, Severity


@dataclass
class FixEngine:
    """Applies safe fixes to compatibility issues."""
    project_root: Path
    platform: str
    dry_run: bool = False
    backup_dir: Optional[Path] = None

    def __post_init__(self):
        if self.backup_dir is None:
            self.backup_dir = self.project_root / ".kdesk_doctor_backups"

    def apply_fixes(self, issues: List[Any], catalog, platform: str, registry_root: Path, project_root: Optional[Path] = None) -> FixReport:
        """Apply fixes for all fixable issues."""
        from kdesk.diagnostics import FixReport

        # Use provided project_root or fall back to self.project_root
        active_root = project_root or self.project_root
        
        report = FixReport(
            project_root=str(active_root),
            platform=platform,
            before_score=0,
            after_score=0,
        )

        if not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        fixable_issues = [i for i in issues if i.fixable]

        for issue in fixable_issues:
            result = self._apply_fix(issue, project_root=project_root or self.project_root)
            report.fixes.append(result)

            if not result.success:
                report.manual_actions.append(
                    f"Manual action required for {issue.id}: {issue.suggested_fix}"
                )

        # Calculate scores (placeholder - would be computed from diagnostics)
        report.before_score = 0
        report.after_score = 0

        return report

    def _apply_fix(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Apply a single fix based on issue type."""
        fix_data = issue.fix_data
        action = fix_data.get("action", "")

        # Use provided project_root or fall back to self.project_root
        active_root = project_root or self.project_root

        try:
            if action == "add_field":
                return self._fix_add_field(issue, project_root=active_root)
            elif action == "remove_field":
                return self._fix_remove_field(issue, project_root=active_root)
            elif action == "replace_tool":
                return self._fix_replace_tool(issue, project_root=active_root)
            elif action == "add_step_type":
                return self._fix_add_step_type(issue, project_root=active_root)
            elif action == "replace_field":
                return self._fix_replace_field(issue, project_root=active_root)
            elif action == "replace_value":
                return self._fix_replace_value(issue, project_root=active_root)
            else:
                return FixResult(
                    issue_id=issue.id,
                    success=False,
                    message=f"Unknown fix action: {action}",
                )
        except Exception as e:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"Fix failed with exception: {e}",
            )

    def _backup_file(self, file_path: Path) -> Path:
        """Create a backup of a file."""
        rel_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _load_file(self, file_path: Path) -> tuple:
        """Load file content based on extension."""
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(content), "yaml"
        elif file_path.suffix in (".json",):
            return json.loads(content), "json"
        elif file_path.suffix in (".md", ".mdc", ".instructions.md"):
            return content, "markdown"
        else:
            return content, "text"

    def _save_file(self, file_path: Path, data: Any, format_type: str) -> None:
        """Save file based on format."""
        if format_type == "yaml":
            file_path.write_text(yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True), encoding="utf-8")
        elif format_type == "json":
            file_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        else:
            file_path.write_text(str(data), encoding="utf-8")

    def _fix_add_field(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Add a missing required field."""
        active_root = project_root or self.project_root
        file_path = active_root / issue.file
        if not file_path.exists():
            return FixResult(issue_id=issue.id, success=False, message=f"File not found: {file_path}")

        field = issue.fix_data.get("field", "")
        if not field:
            return FixResult(issue_id=issue.id, success=False, message="No field specified")

        # Backup
        if not self.dry_run:
            self._backup_file(file_path)

        # Load and modify
        data, fmt = self._load_file(file_path)
        if not isinstance(data, dict):
            return FixResult(issue_id=issue.id, success=False, message="File is not a dictionary")

        # Add default value based on field
        defaults = {
            "name": "unnamed",
            "description": "No description provided",
            "tools": [],
            "model": "inherit",
            "mode": "subagent",
            "applyTo": "**",
            "trigger": "model_decision",
            "globs": ["**"],
            "alwaysApply": False,
            "title": "Untitled",
            "version": "1.0.0",
            "prompt": "Act as the agent and handle the task.",
            "instructions": "",
            "type": "knowledge",
            "triggers": [],
        }

        data[field] = defaults.get(field, "")

        # Save
        if not self.dry_run:
            self._save_file(file_path, data, "yaml" if file_path.suffix in (".yaml", ".yml") else "json" if file_path.suffix == ".json" else "markdown")

        return FixResult(
            issue_id=issue.id,
            success=True,
            message=f"Added field '{field}' with default value",
            backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
        )

    def _fix_remove_field(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Remove an unsupported field."""
        active_root = project_root or self.project_root
        file_path = active_root / issue.file
        if not file_path.exists():
            return FixResult(issue_id=issue.id, success=False, message=f"File not found: {file_path}")

        field = issue.fix_data.get("field", "")
        path = issue.fix_data.get("path", "")
        if not field and not path:
            return FixResult(issue_id=issue.id, success=False, message="No field or path specified")

        if not self.dry_run:
            self._backup_file(file_path)

        data, fmt = self._load_file(file_path)
        if not isinstance(data, dict):
            return FixResult(issue_id=issue.id, success=False, message="File is not a dictionary")

        # Handle nested path (e.g., "platforms.claude_code.plugin")
        if path:
            path_parts = path.split(".")
            current = data
            for part in path_parts[:-1]:
                if part not in current:
                    return FixResult(issue_id=issue.id, success=False, message=f"Path not found: {path}")
                current = current[part]

            final_key = path_parts[-1]
            if final_key in current:
                del current[final_key]

                if not self.dry_run:
                    self._save_file(file_path, data, fmt)

                return FixResult(
                    issue_id=issue.id,
                    success=True,
                    message=f"Removed unsupported field at '{path}'",
                    backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
                )
            else:
                return FixResult(
                    issue_id=issue.id,
                    success=False,
                    message=f"Field '{path_parts[-1]}' not found in path",
                )
        else:
            # Top-level field removal
            if field in data:
                del data[field]

                if not self.dry_run:
                    self._save_file(file_path, data, fmt)

                return FixResult(
                    issue_id=issue.id,
                    success=True,
                    message=f"Removed unsupported field '{field}'",
                    backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
                )
            else:
                return FixResult(
                    issue_id=issue.id,
                    success=False,
                    message=f"Field '{field}' not found in file",
                )

    def _fix_replace_tool(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Replace an unsupported tool with a supported one."""
        active_root = project_root or self.project_root
        file_path = active_root / issue.file
        if not file_path.exists():
            return FixResult(issue_id=issue.id, success=False, message=f"File not found: {file_path}")

        old_tool = issue.fix_data.get("tool", "")
        if not old_tool:
            return FixResult(issue_id=issue.id, success=False, message="No tool specified")

        if not self.dry_run:
            self._backup_file(file_path)

        data, fmt = self._load_file(file_path)
        if not isinstance(data, dict):
            return FixResult(issue_id=issue.id, success=False, message="File is not a dictionary")

        tools = data.get("tools", [])
        if isinstance(tools, list) and old_tool in tools:
            # Simple replacement map
            replacements = {
                "rm": "bash",
                "sudo": "bash",
                "docker": "bash",
                "kubectl": "bash",
                "helm": "bash",
                "terraform": "bash",
            }

            new_tool = replacements.get(old_tool, "bash")
            idx = tools.index(old_tool)
            tools[idx] = new_tool

            if not self.dry_run:
                self._save_file(file_path, data, fmt)

            return FixResult(
                issue_id=issue.id,
                success=True,
                message=f"Replaced tool '{old_tool}' with '{new_tool}'",
                backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
            )
        else:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"Tool '{old_tool}' not found in tools list",
            )

    def _fix_add_step_type(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Add missing step type to workflow step."""
        active_root = project_root or self.project_root
        file_path = active_root / issue.file
        if not file_path.exists():
            return FixResult(issue_id=issue.id, success=False, message=f"File not found: {file_path}")

        step_index = issue.fix_data.get("step_index", 0)

        if not self.dry_run:
            self._backup_file(file_path)

        data, fmt = self._load_file(file_path)
        if not isinstance(data, dict):
            return FixResult(issue_id=issue.id, success=False, message="File is not a dictionary")

        steps = data.get("steps", [])
        if 0 <= step_index < len(steps):
            steps[step_index]["type"] = "skill"  # Default

            if not self.dry_run:
                self._save_file(file_path, data, fmt)

            return FixResult(
                issue_id=issue.id,
                success=True,
                message=f"Added step type 'skill' to step {step_index}",
                backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
            )
        else:
            return FixResult(
                issue_id=issue.id,
                success=False,
                message=f"Step index {step_index} out of range",
            )

    def _fix_replace_field(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Replace a field value."""
        # Similar to add_field but replaces existing
        return self._fix_add_field(issue, project_root=project_root)

    def _fix_replace_value(self, issue, project_root: Optional[Path] = None) -> FixResult:
        """Replace a field value (e.g., change model value from gpt-4 to inherit)."""
        active_root = project_root or self.project_root
        file_path = active_root / issue.file
        if not file_path.exists():
            return FixResult(issue_id=issue.id, success=False, message=f"File not found: {file_path}")

        path = issue.fix_data.get("path", "")
        new_value = issue.fix_data.get("value", "")
        if not path:
            return FixResult(issue_id=issue.id, success=False, message="No path specified")

        if not self.dry_run:
            self._backup_file(file_path)

        data, fmt = self._load_file(file_path)
        if not isinstance(data, dict):
            return FixResult(issue_id=issue.id, success=False, message="File is not a dictionary")

        # Navigate to the nested path (e.g., "platforms.claude_code.model")
        path_parts = path.split(".")
        current = data
        for part in path_parts[:-1]:
            if part not in current:
                return FixResult(issue_id=issue.id, success=False, message=f"Path not found: {path}")
            current = current[part]

        final_key = path_parts[-1]
        if final_key not in current:
            return FixResult(issue_id=issue.id, success=False, message=f"Key '{final_key}' not found in path")

        old_value = current[final_key]
        current[final_key] = new_value

        if not self.dry_run:
            self._save_file(file_path, data, "yaml" if file_path.suffix in (".yaml", ".yml") else "json" if file_path.suffix == ".json" else "markdown")

        return FixResult(
            issue_id=issue.id,
            success=True,
            message=f"Replaced value at '{path}' from '{current[final_key]}' to '{new_value}'",
            backup_path=str(self.backup_dir / issue.file) if not self.dry_run else None,
        )


def apply_fixes(
    issues,
    project_root: Path,
    platform: str,
    catalog,
    registry_root: Path,
    dry_run: bool = False
) -> FixReport:
    """Convenience function to apply fixes."""
    engine = FixEngine(project_root, platform, dry_run)
    return engine.apply_fixes(issues, catalog, platform, registry_root)