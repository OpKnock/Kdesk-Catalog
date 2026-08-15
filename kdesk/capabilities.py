"""Capability model: tools, parameters, and cross-catalog capability queries."""
from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional

from kdesk.models import BaseDefinition, Capability


class CapabilityIndex:
    """Inverted index: tool binary -> capabilities that invoke it."""

    def __init__(self, definitions: List[BaseDefinition]):
        self.definitions = definitions
        self.by_tool: Dict[str, List[tuple]] = {}
        self.tool_frequency: Counter = Counter()
        self._build()

    def _build(self) -> None:
        for defn in self.definitions:
            for cap in defn.capabilities:
                for tool in set(cap.tool_binaries()):
                    if tool.startswith("$SKILL_TEMPLATE"):
                        continue
                    self.by_tool.setdefault(tool, []).append((defn.name, cap.name))
                    self.tool_frequency[tool] += 1

    def capabilities_for_tool(self, tool: str) -> List[tuple]:
        """(definition name, capability name) pairs invoking `tool`."""
        return list(self.by_tool.get(tool, []))

    def tools(self) -> List[str]:
        return sorted(self.by_tool)

    def generic_tools(self, threshold: int = 20) -> set:
        """Tools used by many definitions (generic CLIs) - weak wiring evidence alone."""
        return {t for t, n in self.tool_frequency.items() if n >= threshold}

    def definitions_with_tool(self, tool: str) -> List[str]:
        return sorted({d for d, _ in self.by_tool.get(tool, [])})

    def parameters(self, capability: Capability) -> List[Dict]:
        return list(capability.parameters)

    def definitions_without_parameters(self) -> List[str]:
        return [
            d.name
            for d in self.definitions
            if not any(c.parameters for c in d.capabilities)
        ]

    def definitions_without_commands(self) -> List[str]:
        return [d.name for d in self.definitions if not d.all_commands()]

    def summary(self) -> Dict[str, int]:
        return {
            "definitions": len(self.definitions),
            "tools": len(self.by_tool),
            "definitions_without_parameters": len(self.definitions_without_parameters()),
            "definitions_without_commands": len(self.definitions_without_commands()),
        }


def merge_capability_parameters(cap: Capability) -> Dict[str, List[Dict]]:
    """Input block convention: capability parameters surfaced as workflow inputs."""
    return {"parameters": list(cap.parameters)}