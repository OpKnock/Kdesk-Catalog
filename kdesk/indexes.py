"""Runtime indexes: fast lookup structures over the catalog for resolution.

Built once per catalog tree (mtime-keyed cache, like Catalog itself), so
repeated CLI calls over an unchanged tree are free.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Set

from kdesk.capabilities import CapabilityIndex
from kdesk.contracts import Contract, derive_contract
from kdesk.registry import Catalog
from kdesk.resolvers import _tokens

_INTENT_KEYWORDS: Dict[str, List[str]] = {
    "analyze": ["analyze", "analyse", "inspect", "examine", "understand", "explain", "study"],
    "audit": ["audit", "auditing", "compliance", "policy", "governance"],
    "security": ["security", "secure", "secret", "vulnerab", "exploit", "threat", "cve", "pwn"],
    "review": ["review", "code review", "quality", "pr review", "pull request"],
    "test": ["test", "testing", "unit test", "integration test", "e2e", "coverage", "verify"],
    "deploy": ["deploy", "release", "ship", "rollout", "canary", "blue-green", "production"],
    "build": ["build", "compile", "bundle", "package", "artifact", "dockerfile", "image"],
    "lint": ["lint", "format", "style", "formatting", "static analysis", "sast"],
    "refactor": ["refactor", "restructure", "modernize", "cleanup", "clean up"],
    "optimize": ["optimize", "performance", "latency", "throughput", "benchmark", "speed up"],
    "migrate": ["migrate", "migration", "upgrade", "port", "convert"],
    "generate": ["generate", "create", "scaffold", "boilerplate", "codegen", "produce"],
    "document": ["document", "documentation", "docs", "readme", "comment"],
    "monitor": ["monitor", "observe", "observability", "metrics", "logs", "alert", "tracing"],
    "debug": ["debug", "fix", "bug", "issue", "trace", "root cause", "troubleshoot"],
    "install": ["install", "setup", "configure", "provision", "bootstrap"],
    "validate": ["validate", "check", "verify", "lint", "schema", "conformance"],
    "api": ["api", "rest", "graphql", "grpc", "endpoint", "openapi", "webhook", "http"],
    "data": ["data", "database", "sql", "pipeline", "etl", "analytics", "query", "storage"],
    "cloud": ["cloud", "aws", "gcp", "azure", "kubernetes", "container", "serverless", "infra"],
    "frontend": ["frontend", "ui", "react", "vue", "css", "web", "component", "typescript"],
    "backend": ["backend", "server", "service", "microservice", "python", "node", "go", "java"],
    "ml": ["ml", "machine learning", "model", "training", "inference", "llm", "ai"],
}


class IntentClassifier:
    """Keyword-based deterministic intent classification."""

    def classify(self, text: str) -> Dict[str, Any]:
        lowered = text.lower()
        tokens = set(_tokens(text))
        scores: Dict[str, int] = {}
        for intent, keywords in _INTENT_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw in lowered:
                    score += 1
            if score:
                scores[intent] = score
        if not scores:
            return {"intent": "general", "confidence": 0.0, "matched_keywords": []}
        best = max(scores.items(), key=lambda kv: (kv[1], kv[0]))
        total = sum(scores.values())
        return {
            "intent": best[0],
            "confidence": round(best[1] / total, 3),
            "matched_keywords": sorted(
                kw for kw in _INTENT_KEYWORDS[best[0]] if kw in lowered
            )[:8],
        }


class RuntimeIndexes:
    """Indexes over the catalog used by the resolver/planner."""

    _cache: Dict[str, "RuntimeIndexes"] = {}

    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        definitions = list(catalog.agents.values()) + list(catalog.skills.values())
        self.contracts: Dict[str, Contract] = {
            d.name: derive_contract(d) for d in definitions
        }
        self.capability_index = CapabilityIndex(definitions)
        self._capability_tokens: Dict[str, List[str]] = defaultdict(list)
        self._requirements: Dict[str, List[str]] = defaultdict(list)
        self._platforms: Dict[str, List[str]] = defaultdict(list)
        self._tags: Dict[str, List[str]] = defaultdict(list)
        self._tokens: Dict[str, Set[str]] = {}
        for defn in definitions:
            self._tokens[defn.name] = set(_tokens(defn.name)) | set(_tokens(defn.display_name))
            for kw in [defn.category, defn.subcategory or ""]:
                self._tokens[defn.name].update(_tokens(kw))
            self._tokens[defn.name].update(_tokens(defn.description))
            for t in defn.tags:
                self._tokens[defn.name].update(_tokens(t))
            for kw in defn.keywords:
                self._tokens[defn.name].update(_tokens(kw))
            for cap in defn.capabilities:
                self._tokens[defn.name].update(_tokens(cap.name))
                self._tokens[defn.name].update(_tokens(cap.description))
            contract = self.contracts[defn.name]
            for cap in contract.capabilities:
                self._capability_tokens[cap.lower()].append(defn.name)
            for req in contract.requirements:
                self._requirements[req.lower()].append(defn.name)
            for platform in contract.platforms:
                self._platforms[platform.lower()].append(defn.name)
            for tag in defn.tags:
                self._tags[tag.lower()].append(defn.name)

    @classmethod
    def from_catalog(cls, catalog: Catalog) -> "RuntimeIndexes":
        key = catalog.universal_dir
        cached = cls._cache.get(str(key))
        if cached is not None and cached.catalog is catalog:
            return cached
        indexes = cls(catalog)
        cls._cache[str(key)] = indexes
        return indexes

    def definitions_with_token(self, token: str) -> List[str]:
        hits = set()
        for defn, tokens in self._tokens.items():
            if token in tokens:
                hits.add(defn)
        return sorted(hits)

    def definitions_with_capability(self, capability: str) -> List[str]:
        return sorted(set(self._capability_tokens.get(capability.lower(), [])))

    def capabilities(self) -> List[str]:
        return sorted(self._capability_tokens)

    def definitions_with_requirement(self, requirement: str) -> List[str]:
        return sorted(set(self._requirements.get(requirement.lower(), [])))

    def requirements(self) -> List[str]:
        return sorted(self._requirements)

    def definitions_on_platform(self, platform: str) -> List[str]:
        return sorted(set(self._platforms.get(platform.lower(), [])))

    def platforms(self) -> List[str]:
        return sorted(self._platforms)

    def definitions_with_tag(self, tag: str) -> List[str]:
        return sorted(set(self._tags.get(tag.lower(), [])))

    def tools(self) -> List[str]:
        return self.capability_index.tools()

    def capabilities_for_tool(self, tool: str) -> List[tuple]:
        return self.capability_index.capabilities_for_tool(tool)

    def tool_frequency(self) -> Counter:
        return self.capability_index.tool_frequency

    def summary(self) -> Dict[str, int]:
        return {
            "definitions": len(self._tokens),
            "capabilities": len(self.capabilities()),
            "requirements": len(self.requirements()),
            "platforms": len(self.platforms()),
            "tools": len(self.tools()),
            "tags": len(self._tags),
        }