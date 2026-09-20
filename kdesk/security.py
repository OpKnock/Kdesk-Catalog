"""Path security utilities for KDesk.

Provides safe path resolution with traversal and symlink protection.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any

from kdesk.models import Agent, Skill  # noqa: F401  # keep for re-export compat


class PathSecurityError(Exception):
    """Raised when a path fails security checks."""
    pass


def safe_path(
    requested: Path | str,
    allowed_root: Path | str,
    *,
    must_exist: bool = False,
    allow_write: bool = False,
    follow_symlinks: bool = False,
) -> Path:
    """Resolve a requested path safely within an allowed root.

    Args:
        requested: The path to resolve (can be relative or absolute).
        allowed_root: The root directory that bounds allowed paths.
        must_exist: If True, raise if the path doesn't exist.
        allow_write: If True, allows write operations (used for permission checks).
        follow_symlinks: If True, resolve symlinks before checking.

    Returns:
        The resolved Path if it's within allowed_root.

    Raises:
        PathSecurityError: If the path is outside allowed_root or fails checks.
    """
    requested = Path(requested)
    allowed_root = Path(allowed_root).resolve()

    # Resolve the requested path
    try:
        if follow_symlinks:
            requested_resolved = requested.resolve()
        else:
            # Without following symlinks: lexically normalize but don't resolve last component if it's a symlink
            # Use absolute() then resolve parent only
            requested_resolved = (Path.cwd() / requested).resolve() if not requested.is_absolute() else requested.resolve()
            # If requested itself is a symlink, detect without following
            if requested.is_symlink():
                # Check symlink target would escape - treat symlink itself as unsafe if target outside root
                target = requested.readlink()
                # If symlink is absolute or escapes, block it
                candidate = (requested.parent / target).resolve() if not target.is_absolute() else target.resolve()
                try:
                    candidate.relative_to(allowed_root)
                except ValueError:
                    raise PathSecurityError(
                        f"Symlink '{requested}' -> '{target}' escapes allowed root '{allowed_root}'"
                    )
                # Also ensure the symlink path itself is inside root
                (requested.parent.resolve() / requested.name).relative_to(allowed_root)
    except OSError as exc:
        raise PathSecurityError(f"Cannot resolve path: {exc}") from exc

    # Check if resolved path is within allowed_root
    if follow_symlinks:
        try:
            requested_resolved.relative_to(allowed_root)
        except ValueError:
            raise PathSecurityError(
                f"Path '{requested}' resolves to '{requested_resolved}' "
                f"which is outside allowed root '{allowed_root}'"
            )
    else:
        # Lexical check when not following symlinks: ensure requested is inside root before resolve
        try:
            (allowed_root / requested).resolve().relative_to(allowed_root) if not requested.is_absolute() else requested.resolve().relative_to(allowed_root)
        except ValueError:
            raise PathSecurityError(
                f"Path '{requested}' escapes allowed root '{allowed_root}'"
            )
        # Final resolved check too
        try:
            requested_resolved.relative_to(allowed_root)
        except ValueError:
            raise PathSecurityError(
                f"Path '{requested}' resolves to '{requested_resolved}' "
                f"which is outside allowed root '{allowed_root}'"
            )

    # Check existence if required
    if must_exist and not requested_resolved.exists():
        raise PathSecurityError(f"Path does not exist: {requested_resolved}")

    # Check write permission if requested
    if allow_write:
        # Check if parent directory is writable
        parent = requested_resolved.parent
        if not parent.exists():
            raise PathSecurityError(f"Parent directory does not exist: {parent}")
        # Try to create a temporary file to test write access
        try:
            test_file = requested_resolved.parent / ".kdesk_write_test"
            test_file.touch()
            test_file.unlink()
        except (OSError, PermissionError) as exc:
            raise PathSecurityError(f"Write access denied to {requested_resolved}: {exc}") from exc

    return requested_resolved


def safe_join(allowed_root: Path | str, *parts: str) -> Path:
    """Safely join path components within an allowed root.

    Args:
        allowed_root: The root directory that bounds the result.
        *parts: Path components to join.

    Returns:
        A Path within allowed_root.

    Raises:
        PathSecurityError: If the joined path escapes allowed_root.
    """
    allowed_root = Path(allowed_root).resolve()
    requested = (Path(allowed_root) / Path(*parts)).resolve()

    try:
        requested.relative_to(Path(allowed_root).resolve())
    except ValueError:
        raise PathSecurityError(
            f"Joined path escapes allowed root: {requested}"
        )

    return requested


def is_safe_path(path: Path | str, allowed_root: Path | str) -> bool:
    """Check if a path is within the allowed root without raising.

    Args:
        path: The path to check.
        allowed_root: The root directory that bounds allowed paths.

    Returns:
        True if the path is within allowed_root, False otherwise.
    """
    try:
        safe_path(Path(path), Path(allowed_root))
        return True
    except PathSecurityError:
        return False


def resolve_safely(allowed_root: Path | str, *parts: str) -> Path:
    """Resolve path components safely within allowed_root.

    Args:
        allowed_root: The root directory that bounds the result.
        *parts: Path components to join.

    Returns:
        A resolved Path within allowed_root.

    Raises:
        PathSecurityError: If the path escapes allowed_root.
    """
    allowed_root = Path(allowed_root).resolve()
    requested = Path(allowed_root).joinpath(*parts).resolve()

    try:
        requested.relative_to(allowed_root)
    except ValueError:
        raise PathSecurityError(
            f"Path escapes allowed root: {requested}"
        )

    return requested


# Secret redaction patterns and constants
REDACTED = "[REDACTED]"

_PATTERNS = {
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
    "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
    "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
    "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
    "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
}


def scan_repo(root: Path, exceptions_path: Path) -> Dict[str, Any]:
    """Scan a repository for secrets and security issues.

    Args:
        root: Repository root directory
        exceptions_path: Path to security exceptions file

    Returns:
        Dictionary with findings and blocking count
    """
    import json
    from pathlib import Path
    import re

    # Load exceptions
    exceptions = set()
    if exceptions_path.is_file():
        try:
            with open(exceptions_path, 'r') as f:
                data = json.load(f)
                exceptions = set(data.get("exceptions", []))
        except (OSError, json.JSONDecodeError):
            pass

    # Secret patterns to detect
    patterns = {
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
        "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
    }

    findings = []
    blocking_count = 0

    skip_dirs = {'.git', '.venv', '.venv-clean', '__pycache__', '.pytest_cache', 'platform-agents', '.kdesk', 'node_modules', '.vscode-kdesk'}
    # Use os.walk with pruning to avoid descending into heavy dirs
    import os
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        # also skip if any part is skip_dirs
        if any(part in skip_dirs for part in Path(dirpath).parts):
            continue
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
            # Ensure file is within root
            try:
                file_path.resolve().relative_to(Path(root).resolve())
            except ValueError:
                continue  # Skip files outside root
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    finding = {
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern_name,
                        "match": match.group()[:100],
                    }
                    findings.append(finding)

    # Filter out exceptions
    filtered_findings = []
    for finding in findings:
        if finding["match"] not in exceptions:
            findings.append(finding)

    return {
        "findings": findings,
        "blocking_count": len(findings),
        "total_scanned": 0,  # TODO: count scanned files
    }


class SecurityExceptions:
    """Manages security exception rules for scanning."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = set()
        if exceptions_path and exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    self.exceptions = set(data.get("exceptions", []))
            except (OSError, json.JSONDecodeError):
                pass

    @classmethod
    def load(cls, exceptions_path: Path) -> "SecurityExceptions":
        """Load security exceptions from a file."""
        instance = cls()
        if exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    instance = cls()
                    instance.exceptions = set(data.get("exceptions", []))
                    return instance
            except (OSError, json.JSONDecodeError):
                pass
        return cls()

    def is_exception(self, match: str) -> bool:
        """Check if a match is in the exception list."""
        return match in self.exceptions

    def add_exception(self, pattern: str):
        """Add a pattern to the exception list."""
        self.exceptions.add(pattern)

    def remove_exception(self, pattern: str):
        """Remove a pattern from the exception list."""
        self.exceptions.discard(pattern)


class SecurityScanner:
    """Scans repositories for security issues."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = SecurityExceptions(Path("reports/security-exceptions.json") if Path("reports/security-exceptions.json").exists() else None)
        self.patterns = {
            "aws_key": r"AKIA[0-9A-Z]{16}",
            "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
            "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
            "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
            "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
            "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
            "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
            "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
        }

    def scan(self, root: Path) -> Dict[str, Any]:
        """Scan a repository for security issues.

        Args:
            root: Repository root directory

        Returns:
            Dictionary with findings and blocking count
        """
        import re

        findings = []

        for file_path in Path(root).rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
                # Ensure file is within root
                try:
                    file_path.resolve().relative_to(Path(root).resolve())
                except ValueError:
                    continue  # Skip files outside root
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                except (OSError, UnicodeDecodeError):
                    continue

                for pattern_name, pattern in self.patterns.items():
                    for match in re.finditer(pattern, content):
                        finding = {
                            "file": str(file_path.relative_to(Path(root).resolve())),
                            "line": content[:match.start()].count('\n') + 1,
                            "pattern": pattern_name,
                            "match": match.group()[:100],
                        }
                        findings.append(finding)

        return {
            "findings": findings,
            "blocking_count": len(findings),
            "total_scanned": 0,  # TODO: count scanned files
        }


def scan_repo(root: Path, exceptions_path: Path) -> Dict[str, Any]:
    """Scan a repository for secrets and security issues.

    Args:
        root: Repository root directory
        exceptions_path: Path to security exceptions file

    Returns:
        Dictionary with findings and blocking count
    """
    import json
    from pathlib import Path
    import re

    # Load exceptions
    exceptions = set()
    if exceptions_path.is_file():
        try:
            with open(exceptions_path, 'r') as f:
                data = json.load(f)
                exceptions = set(data.get("exceptions", []))
        except (OSError, json.JSONDecodeError):
            pass

    # Secret patterns to detect
    patterns = {
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
        "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
    }

    findings = []
    blocking_count = 0

    skip_dirs = {'.git', '.venv', '.venv-clean', '__pycache__', '.pytest_cache', 'platform-agents', '.kdesk', 'node_modules', '.vscode-kdesk'}
    # Use os.walk with pruning to avoid descending into heavy dirs
    import os
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        # also skip if any part is skip_dirs
        if any(part in skip_dirs for part in Path(dirpath).parts):
            continue
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
            # Ensure file is within root
            try:
                file_path.resolve().relative_to(Path(root).resolve())
            except ValueError:
                continue  # Skip files outside root
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    finding = {
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern_name,
                        "match": match.group()[:100],
                    }
                    findings.append(finding)
                    blocking_count += 1

    # Filter out exceptions
    filtered_findings = []
    for finding in findings:
        if finding["match"] not in exceptions:
            findings.append(finding)

    return {
        "findings": findings,
        "blocking_count": len(findings),
        "total_scanned": 0,  # TODO: count scanned files
    }


class SecurityExceptions:
    """Manages security exception rules for scanning."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = set()
        if exceptions_path and exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    self.exceptions = set(data.get("exceptions", []))
            except (OSError, json.JSONDecodeError):
                pass

    @classmethod
    def load(cls, exceptions_path: Path) -> "SecurityExceptions":
        """Load security exceptions from a file."""
        instance = cls()
        if exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    instance = cls()
                    instance.exceptions = set(data.get("exceptions", []))
                    return instance
            except (OSError, json.JSONDecodeError):
                pass
        return cls()

    def is_exception(self, match: str) -> bool:
        """Check if a match is in the exception list."""
        return match in self.exceptions

    def add_exception(self, pattern: str):
        """Add a pattern to the exception list."""
        self.exceptions.add(pattern)

    def remove_exception(self, pattern: str):
        """Remove a pattern from the exception list."""
        self.exceptions.discard(pattern)


class SecurityScanner:
    """Scans repositories for security issues."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = SecurityExceptions(Path("reports/security-exceptions.json") if Path("reports/security-exceptions.json").exists() else None)
        self.patterns = {
            "aws_key": r"AKIA[0-9A-Z]{16}",
            "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
            "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
            "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
            "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
            "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
            "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
            "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
        }

    def scan(self, root: Path) -> Dict[str, Any]:
        """Scan a repository for security issues.

        Args:
            root: Repository root directory

        Returns:
            Dictionary with findings and blocking count
        """
        import re

        findings = []

        for file_path in Path(root).rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
                # Ensure file is within root
                try:
                    file_path.resolve().relative_to(Path(root).resolve())
                except ValueError:
                    continue  # Skip files outside root
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                except (OSError, UnicodeDecodeError):
                    continue

                for pattern_name, pattern in self.patterns.items():
                    for match in re.finditer(pattern, content):
                        finding = {
                            "file": str(file_path.relative_to(Path(root).resolve())),
                            "line": content[:match.start()].count('\n') + 1,
                            "pattern": pattern_name,
                            "match": match.group()[:100],
                        }
                        findings.append(finding)

        return {
            "findings": findings,
            "blocking_count": len(findings),
            "total_scanned": 0,  # TODO: count scanned files
        }


def scan_repo(root: Path, exceptions_path: Path) -> Dict[str, Any]:
    """Scan a repository for secrets and security issues.

    Args:
        root: Repository root directory
        exceptions_path: Path to security exceptions file

    Returns:
        Dictionary with findings and blocking count
    """
    import json
    from pathlib import Path
    import re

    # Load exceptions
    exceptions = set()
    if exceptions_path.is_file():
        try:
            with open(exceptions_path, 'r') as f:
                data = json.load(f)
                exceptions = set(data.get("exceptions", []))
        except (OSError, json.JSONDecodeError):
            pass

    # Secret patterns to detect
    patterns = {
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
        "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
    }

    findings = []
    blocking_count = 0

    skip_dirs = {'.git', '.venv', '.venv-clean', '__pycache__', '.pytest_cache', 'platform-agents', '.kdesk', 'node_modules', '.vscode-kdesk'}
    # Use os.walk with pruning to avoid descending into heavy dirs
    import os
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        # also skip if any part is skip_dirs
        if any(part in skip_dirs for part in Path(dirpath).parts):
            continue
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
            # Ensure file is within root
            try:
                file_path.resolve().relative_to(Path(root).resolve())
            except ValueError:
                continue  # Skip files outside root
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    finding = {
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern_name,
                        "match": match.group()[:100],
                    }
                    findings.append(finding)
                    blocking_count += 1

    # Filter out exceptions
    filtered_findings = []
    for finding in findings:
        if finding["match"] not in exceptions:
            findings.append(finding)

    return {
        "findings": findings,
        "blocking_count": len(findings),
        "total_scanned": 0,  # TODO: count scanned files
    }


class SecurityExceptions:
    """Manages security exception rules for scanning."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = set()
        if exceptions_path and exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    self.exceptions = set(data.get("exceptions", []))
            except (OSError, json.JSONDecodeError):
                pass

    @classmethod
    def load(cls, exceptions_path: Path) -> "SecurityExceptions":
        """Load security exceptions from a file."""
        instance = cls()
        if exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    instance = cls()
                    instance.exceptions = set(data.get("exceptions", []))
                    return instance
            except (OSError, json.JSONDecodeError):
                pass
        return cls()

    def is_exception(self, match: str) -> bool:
        """Check if a match is in the exception list."""
        return match in self.exceptions

    def add_exception(self, pattern: str):
        """Add a pattern to the exception list."""
        self.exceptions.add(pattern)

    def remove_exception(self, pattern: str):
        """Remove a pattern from the exception list."""
        self.exceptions.discard(pattern)


class SecurityScanner:
    """Scans repositories for security issues."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = SecurityExceptions(Path("reports/security-exceptions.json") if Path("reports/security-exceptions.json").exists() else None)
        self.patterns = {
            "aws_key": r"AKIA[0-9A-Z]{16}",
            "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
            "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
            "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
            "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
            "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
            "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
            "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
        }

    def scan(self, root: Path) -> Dict[str, Any]:
        """Scan a repository for security issues.

        Args:
            root: Repository root directory

        Returns:
            Dictionary with findings and blocking count
        """
        import re

        findings = []

        for file_path in Path(root).rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
                # Ensure file is within root
                try:
                    file_path.resolve().relative_to(Path(root).resolve())
                except ValueError:
                    continue  # Skip files outside root
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                except (OSError, UnicodeDecodeError):
                    continue

                for pattern_name, pattern in self.patterns.items():
                    for match in re.finditer(pattern, content):
                        finding = {
                            "file": str(file_path.relative_to(Path(root).resolve())),
                            "line": content[:match.start()].count('\n') + 1,
                            "pattern": pattern_name,
                            "match": match.group()[:100],
                        }
                        findings.append(finding)

        return {
            "findings": findings,
            "blocking_count": len(findings),
            "total_scanned": 0,  # TODO: count scanned files
        }


def scan_repo(root: Path, exceptions_path: Path) -> Dict[str, Any]:
    """Scan a repository for secrets and security issues.

    Args:
        root: Repository root directory
        exceptions_path: Path to security exceptions file

    Returns:
        Dictionary with findings and blocking count
    """
    import json
    from pathlib import Path
    import re

    # Load exceptions
    exceptions = set()
    if exceptions_path.is_file():
        try:
            with open(exceptions_path, 'r') as f:
                data = json.load(f)
                exceptions = set(data.get("exceptions", []))
        except (OSError, json.JSONDecodeError):
            pass

    # Secret patterns to detect
    patterns = {
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
        "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
    }

    findings = []
    blocking_count = 0

    skip_dirs = {'.git', '.venv', '.venv-clean', '__pycache__', '.pytest_cache', 'platform-agents', '.kdesk', 'node_modules', '.vscode-kdesk'}
    # Use os.walk with pruning to avoid descending into heavy dirs
    import os
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        # also skip if any part is skip_dirs
        if any(part in skip_dirs for part in Path(dirpath).parts):
            continue
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
            # Ensure file is within root
            try:
                file_path.resolve().relative_to(Path(root).resolve())
            except ValueError:
                continue  # Skip files outside root
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    finding = {
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern_name,
                        "match": match.group()[:100],
                    }
                    findings.append(finding)
                    blocking_count += 1

    # Filter out exceptions
    filtered_findings = []
    for finding in findings:
        if finding["match"] not in exceptions:
            findings.append(finding)

    return {
        "findings": findings,
        "blocking_count": len(findings),
        "total_scanned": 0,  # TODO: count scanned files
    }


class SecurityExceptions:
    """Manages security exception rules for scanning."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = set()
        if exceptions_path and exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    self.exceptions = set(data.get("exceptions", []))
            except (OSError, json.JSONDecodeError):
                pass

    @classmethod
    def load(cls, exceptions_path: Path) -> "SecurityExceptions":
        """Load security exceptions from a file."""
        instance = cls()
        if exceptions_path.is_file():
            try:
                with open(exceptions_path, 'r') as f:
                    data = json.load(f)
                    instance = cls()
                    instance.exceptions = set(data.get("exceptions", []))
                    return instance
            except (OSError, json.JSONDecodeError):
                pass
        return cls()

    def is_exception(self, match: str) -> bool:
        """Check if a match is in the exception list."""
        return match in self.exceptions

    def add_exception(self, pattern: str):
        """Add a pattern to the exception list."""
        self.exceptions.add(pattern)

    def remove_exception(self, pattern: str):
        """Remove a pattern from the exception list."""
        self.exceptions.discard(pattern)


class SecurityScanner:
    """Scans repositories for security issues."""

    def __init__(self, exceptions_path: Path = None):
        self.exceptions = SecurityExceptions(Path("reports/security-exceptions.json") if Path("reports/security-exceptions.json").exists() else None)
        self.patterns = {
            "aws_key": r"AKIA[0-9A-Z]{16}",
            "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
            "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
            "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
            "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
            "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
            "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
            "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
        }

    def scan(self, root: Path) -> Dict[str, Any]:
        """Scan a repository for security issues.

        Args:
            root: Repository root directory

        Returns:
            Dictionary with findings and blocking count
        """
        import re

        findings = []

        for file_path in Path(root).rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
                # Ensure file is within root
                try:
                    file_path.resolve().relative_to(Path(root).resolve())
                except ValueError:
                    continue  # Skip files outside root
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                except (OSError, UnicodeDecodeError):
                    continue

                for pattern_name, pattern in self.patterns.items():
                    for match in re.finditer(pattern, content):
                        finding = {
                            "file": str(file_path.relative_to(Path(root).resolve())),
                            "line": content[:match.start()].count('\n') + 1,
                            "pattern": pattern_name,
                            "match": match.group()[:100],
                        }
                        findings.append(finding)

        return {
            "findings": findings,
            "blocking_count": len(findings),
            "total_scanned": 0,  # TODO: count scanned files
        }


def scan_repo(root: Path, exceptions_path: Path) -> Dict[str, Any]:
    """Scan a repository for secrets and security issues.

    Args:
        root: Repository root directory
        exceptions_path: Path to security exceptions file

    Returns:
        Dictionary with findings and blocking count
    """
    import json
    from pathlib import Path
    import re

    # Load exceptions
    exceptions = set()
    if exceptions_path.is_file():
        try:
            with open(exceptions_path, 'r') as f:
                data = json.load(f)
                exceptions = set(data.get("exceptions", []))
        except (OSError, json.JSONDecodeError):
            pass

    # Secret patterns to detect
    patterns = {
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9_-]{20}",
        "slack_token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "connection_string": r"(?i)(server|host|database|uid|user|pwd|password)\s*=\s*[^\s;]+",
    }

    findings = []
    blocking_count = 0

    skip_dirs = {'.git', '.venv', '.venv-clean', '__pycache__', '.pytest_cache', 'platform-agents', '.kdesk', 'node_modules', '.vscode-kdesk'}
    # Use os.walk with pruning to avoid descending into heavy dirs
    import os
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        # also skip if any part is skip_dirs
        if any(part in skip_dirs for part in Path(dirpath).parts):
            continue
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix in {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.toml', '.ini', '.cfg', '.conf', '.config', '.properties'}:
            # Ensure file is within root
            try:
                file_path.resolve().relative_to(Path(root).resolve())
            except ValueError:
                continue  # Skip files outside root
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    finding = {
                        "file": str(file_path.relative_to(Path.cwd())),
                        "line": content[:match.start()].count('\n') + 1,
                        "pattern": pattern_name,
                        "match": match.group()[:100],
                    }
                    findings.append(finding)
                    blocking_count += 1

    # Filter out exceptions
    filtered_findings = []
    for finding in findings:
        if finding["match"] not in exceptions:
            findings.append(finding)

    return {
        "findings": findings,
        "blocking_count": len(findings),
        "total_scanned": 0,  # TODO: count scanned files
    }