"""Platform renderer interface for modular conversion.

Each platform renderer implements this interface. The converter iterates
renderers instead of maintaining a monolithic switch.

Usage:
    class MyRenderer(Renderer):
        def render(self, definition: dict, platform: str) -> list[Artifact]:
            ...

    converter = Converter()
    converter.register(MyRenderer())
    artifacts = converter.convert(definition, "my_platform")
"""

from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Artifact:
    """A single generated output file."""
    path: str          # relative output path (e.g. ".claude/agents/foo.md")
    content: str       # file contents
    platform: str      # platform ID
    source_id: str     # definition name that produced this
    extension: str     # file extension

    @property
    def checksum(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "platform": self.platform,
            "source_id": self.source_id,
            "extension": self.extension,
            "checksum": self.checksum,
        }


class Renderer(ABC):
    """Base class for platform-specific renderers."""

    platform_id: str = ""
    agent_extension: str = ""
    skill_extension: str = ""

    @abstractmethod
    def render_agent(self, definition: Dict[str, Any]) -> List[Artifact]:
        """Render an agent definition into platform-specific artifacts."""
        ...

    @abstractmethod
    def render_skill(self, definition: Dict[str, Any]) -> List[Artifact]:
        """Render a skill definition into platform-specific artifacts."""
        ...

    def render(self, definition: Dict[str, Any], def_type: str) -> List[Artifact]:
        """Dispatch to render_agent or render_skill based on type."""
        if def_type == "skill":
            return self.render_skill(definition)
        return self.render_agent(definition)

    @staticmethod
    def _make_artifact(path: str, content: str, platform: str,
                       source_id: str, ext: str) -> Artifact:
        return Artifact(
            path=path, content=content, platform=platform,
            source_id=source_id, extension=ext,
        )


class RendererRegistry:
    """Registry of platform renderers."""

    def __init__(self):
        self._renderers: Dict[str, Renderer] = {}

    def register(self, renderer: Renderer) -> None:
        self._renderers[renderer.platform_id] = renderer

    def get(self, platform_id: str) -> Optional[Renderer]:
        return self._renderers.get(platform_id)

    def ids(self) -> List[str]:
        return sorted(self._renderers.keys())

    def convert(self, definition: Dict[str, Any], def_type: str,
                platforms: List[str]) -> Dict[str, List[Artifact]]:
        """Convert a definition for multiple platforms."""
        results = {}
        for pid in platforms:
            renderer = self._renderers.get(pid)
            if renderer:
                results[pid] = renderer.render(definition, def_type)
        return results
