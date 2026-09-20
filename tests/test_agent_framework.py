"""Agent Testing Framework - Unit and integration testing utilities for agents.

Provides:
- AgentTestCase: Base test class for agent unit tests
- AgentTestRunner: Runs agent tests with fixtures
- MockToolExecutor: Mock tool execution for unit tests
- IntegrationTestRunner: Runs integration tests against real APIs
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kdesk.registry import Agent, Catalog, Capability
from kdesk.adapters import AdapterRegistry


class MockToolExecutor:
    """Mock tool executor for unit testing agents without real CLI tools."""
    
    def __init__(self):
        self.call_history: List[Dict[str, Any]] = []
        self.responses: Dict[str, Any] = {}
        self.default_response = {"success": True, "stdout": "", "stderr": "", "exit_code": 0}
    
    def set_response(self, tool: str, response: Dict[str, Any]) -> None:
        """Set a predefined response for a tool."""
        self.responses[tool] = response
    
    def execute(self, tool: str, args: List[str], env: Dict[str, str] = None, cwd: str = None) -> Dict[str, Any]:
        """Execute a tool (mocked)."""
        call = {"tool": tool, "args": args, "env": env, "cwd": cwd}
        self.call_history.append(call)
        
        if tool in self.responses:
            return self.responses[tool]
        return self.default_response
    
    def assert_tool_called(self, tool: str, args: List[str] = None) -> bool:
        """Assert a tool was called with specific arguments."""
        for call in self.call_history:
            if call["tool"] == tool:
                if args is None or call["args"] == args:
                    return True
        return False
    
    def get_calls_for_tool(self, tool: str) -> List[Dict[str, Any]]:
        """Get all calls for a specific tool."""
        return [c for c in self.call_history if c["tool"] == tool]
    
    def clear_history(self) -> None:
        self.call_history.clear()


class AgentTestCase(unittest.TestCase):
    """Base test case for agent unit tests."""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.mock_executor = MockToolExecutor()
        
        # Create minimal universal-agents structure for testing
        self.ua_dir = self.test_dir / "universal-agents"
        self.ua_dir.mkdir(parents=True)
        (self.ua_dir / "test" / "agent").mkdir(parents=True, exist_ok=True)
        (self.ua_dir / "test" / "skill").mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def create_test_agent(self, name: str, capabilities: List[Dict] = None, 
                         skills: List[str] = None, tools: List[str] = None,
                         sub_agents: List[str] = None, 
                         delegation_pattern: str = None) -> Path:
        """Create a test agent YAML file."""
        agent_dir = self.ua_dir / "test" / "agent"
        agent_file = agent_dir / f"{name}.yaml"
        
        doc = {
            "name": name,
            "display_name": name.replace("-", " ").title(),
            "category": "test",
            "description": f"Test agent: {name}",
            "version": "1.0.0",
            "capabilities": capabilities or [{
                "name": "test-capability",
                "description": "Test capability",
                "commands": ["echo test"],
                "examples": ["echo test"],
                "parameters": []
            }],
            "skills": skills or [],
            "tools": tools or ["echo"],
            "capabilities": capabilities or []
        }
        
        if sub_agents:
            doc["sub_agents"] = sub_agents
        if delegation_pattern:
            doc["delegation_pattern"] = delegation_pattern
        
        import yaml
        agent_file.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
        return agent_file
    
    def create_test_skill(self, name: str, tools: List[str] = None) -> Path:
        """Create a test skill YAML file."""
        skill_dir = self.ua_dir / "test" / "skill"
        skill_file = skill_dir / f"{name}.yaml"
        
        doc = {
            "name": name,
            "display_name": name.replace("-", " ").title(),
            "category": "test",
            "description": f"Test skill: {name}",
            "version": "1.0.0",
            "tools": tools or ["echo"],
            "capabilities": [{
                "name": f"{name}-capability",
                "description": f"Capability for {name}",
                "commands": ["echo skill"],
                "examples": ["echo skill"],
                "parameters": []
            }]
        }
        
        import yaml
        skill_file.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
        return skill_file
    
    def load_catalog(self):
        """Load the test catalog."""
        from kdesk.registry import Catalog
        return Catalog.from_repo(self.test_dir)
    
    def assert_capability_exists(self, agent_name: str, cap_name: str):
        """Assert an agent has a specific capability."""
        catalog = self.load_catalog()
        agent = catalog.get_agent(agent_name)
        self.assertIsNotNone(agent, f"Agent {agent_name} not found")
        cap_names = [c.name for c in agent.capabilities]
        self.assertIn(cap_name, cap_names, f"Capability {cap_name} not in {cap_names}")
    
    def assert_skill_referenced(self, agent_name: str, skill_name: str):
        """Assert an agent references a specific skill."""
        catalog = self.load_catalog()
        agent = catalog.get_agent(agent_name)
        self.assertIsNotNone(agent, f"Agent {agent_name} not found")
        self.assertIn(skill_name, agent.skills, f"Skill {skill_name} not in {agent.skills}")
    
    def assert_tool_available(self, agent_name: str, tool: str):
        """Assert an agent has a specific tool."""
        catalog = self.load_catalog()
        agent = catalog.get_agent(agent_name)
        self.assertIsNotNone(agent, f"Agent {agent_name} not found")
        self.assertIn(tool, agent.tools, f"Tool {tool} not in {agent.tools}")
    
    def assert_sub_agents(self, agent_name: str, expected_sub_agents: List[str]):
        """Assert an agent has specific sub-agents."""
        catalog = self.load_catalog()
        agent = catalog.get_agent(agent_name)
        self.assertIsNotNone(agent, f"Agent {agent_name} not found")
        for sa in expected_sub_agents:
            self.assertIn(sa, agent.sub_agents, f"Sub-agent {sa} not in {agent.sub_agents}")


class AgentTestRunner:
    """Runs agent tests with fixtures and reporting."""
    
    def __init__(self, test_dir: Path = None):
        self.test_dir = test_dir or Path.cwd()
        self.results: List[Dict[str, Any]] = []
    
    def discover_tests(self, pattern: str = "test_*.py") -> List[Path]:
        """Discover test files."""
        return list(Path(self.test_dir).rglob(pattern))
    
    def run_test_module(self, module_path: Path) -> Dict[str, Any]:
        """Run a single test module and return results."""
        import subprocess
        result = subprocess.run(
            ["python", "-m", "pytest", str(module_path), "-v", "--tb=short"],
            capture_output=True, text=True, timeout=120
        )
        return {
            "module": str(module_path),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "passed": result.returncode == 0
        }
    
    def run_all(self, pattern: str = "test_*.py") -> Dict[str, Any]:
        """Run all discovered tests."""
        test_files = self.discover_tests(pattern)
        results = []
        for tf in test_files:
            results.append(self.run_test_module(tf))
        
        passed = sum(1 for r in results if r["passed"])
        return {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "results": results
        }


class IntegrationTestRunner:
    """Runs integration tests against real APIs."""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
    
    def _get_session(self):
        if self.session is None:
            import requests
            self.session = requests.Session()
            if self.api_key:
                self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        return self.session
    
    def test_agent_endpoint(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Test an agent endpoint."""
        session = self._get_session()
        url = f"{self.base_url}/agents/{agent_name}/invoke"
        response = self._get_session().post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def test_skill_endpoint(self, skill_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Test a skill endpoint."""
        session = self._get_session()
        url = f"{self.base_url}/skills/{skill_name}/invoke"
        response = self._get_session().post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()


def create_test_fixture(name: str, agent_data: Dict = None, skill_data: Dict = None) -> Path:
    """Create a test fixture with agent and/or skill YAML files."""
    temp_dir = tempfile.mkdtemp(prefix=f"kdesk_test_{name}_")
    fixture_dir = Path(temp_dir)
    ua_dir = Path(temp_dir) / "universal-agents"
    ua_dir.mkdir(parents=True)
    
    import yaml
    
    if agent_data:
        agent_dir = ua_dir / "test" / "agent"
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_file = agent_dir / f"{name}.yaml"
        agent_file.write_text(yaml.dump(agent_data, sort_keys=False), encoding="utf-8")
    
    if skill_data:
        skill_dir = ua_dir / "test" / "skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.yaml"
        skill_file.write_text(yaml.dump(skill_data, sort_keys=False), encoding="utf-8")
    
    return Path(temp_dir)


# Example test class demonstrating the framework
class TestExampleAgent(AgentTestCase):
    """Example test demonstrating the framework."""
    
    def test_create_agent_with_capabilities(self):
        """Test creating an agent with custom capabilities."""
        agent_file = self.create_test_agent("test-ml-agent", capabilities=[{
            "name": "train-model",
            "description": "Train a machine learning model",
            "commands": ["python train.py --model rf"],
            "examples": ["python train.py --model rf --data data.csv"],
            "parameters": [{"name": "model", "type": "string", "description": "Model type"}]
        }], skills=["ml-training"], tools=["python"])
        
        catalog = self.load_catalog()
        agent = catalog.get_agent("test-ml-agent")
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "test-ml-agent")
        self.assertEqual(len(agent.capabilities), 1)
        self.assertEqual(agent.capabilities[0].name, "train-model")
        self.assertIn("ml-training", agent.skills)
        self.assertIn("python", agent.tools)
    
    def test_create_skill(self):
        """Test creating a skill."""
        self.create_test_skill("data-preprocessing", tools=["python", "pandas"])
        
        catalog = self.load_catalog()
        skill = catalog.get_skill("data-preprocessing")
        
        self.assertIsNotNone(skill)
        self.assertEqual(skill.name, "data-preprocessing")
        self.assertIn("python", skill.tools)
        self.assertIn("pandas", skill.tools)
    
    def test_agent_references_skill(self):
        """Test agent referencing a skill."""
        self.create_test_skill("data-cleaning")
        self.create_test_agent("data-engineer", skills=["data-cleaning"])
        
        catalog = self.load_catalog()
        agent = catalog.get_agent("data-engineer")
        
        self.assertIn("data-cleaning", agent.skills)
    
    def test_mock_tool_executor(self):
        """Test the mock tool executor."""
        executor = MockToolExecutor()
        executor.set_response("git", {"success": True, "stdout": "commit abc123", "exit_code": 0})
        
        result = executor.execute("git", ["commit", "-m", "test"])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["stdout"], "commit abc123")
        self.assertTrue(executor.assert_tool_called("git", ["commit", "-m", "test"]))
    
    def test_sub_agents(self):
        """Test sub-agent delegation."""
        self.create_test_agent("sub-agent-1")
        self.create_test_agent("sub-agent-2")
        self.create_test_agent("orchestrator", 
                              sub_agents=["sub-agent-1", "sub-agent-2"],
                              delegation_pattern="sequential")
        
        catalog = self.load_catalog()
        agent = catalog.get_agent("orchestrator")
        
        self.assertEqual(len(agent.sub_agents), 2)
        self.assertIn("sub-agent-1", agent.sub_agents)
        self.assertIn("sub-agent-2", agent.sub_agents)
        self.assertEqual(agent.delegation_pattern, "sequential")


if __name__ == "__main__":
    unittest.main()