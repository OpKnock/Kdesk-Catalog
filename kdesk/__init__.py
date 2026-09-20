"""kdesk - Universal AI Agent + Skill + Workflow Registry and Orchestration Platform.

Public API surface. Stdlib + PyYAML only.
"""

__version__ = "1.1.0"

from kdesk.models import Agent, Capability, Skill, Workflow  # noqa: F401
from kdesk.registry import Catalog, CatalogError  # noqa: F401
from kdesk.capabilities import CapabilityIndex  # noqa: F401
from kdesk.graph import CatalogGraph, GraphError  # noqa: F401
from kdesk.workflow import WorkflowEngine, WorkflowError  # noqa: F401

REPO_ROOT = None  # resolved lazily by kdesk.cli / registry from package location

__all__ = [
    "Agent",
    "Capability",
    "Catalog",
    "CatalogError",
    "CatalogGraph",
    "CapabilityIndex",
    "GraphError",
    "Skill",
    "Workflow",
    "WorkflowEngine",
    "WorkflowError",
    "__version__",
]