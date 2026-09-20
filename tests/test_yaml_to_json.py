import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c = load_module("yaml_to_json", "yaml-to-json.py")


def reset_stats():
    c.stats["errors"][:] = []
    c.stats["warnings"][:] = []


class TestIsSkill(unittest.TestCase):
    def test_skill_subdir(self):
        self.assertTrue(c.is_skill(Path("api/foo/skill/bar.yaml")))

    def test_skill_suffix(self):
        self.assertTrue(c.is_skill(Path("api/foo-skill.yaml")))

    def test_agent(self):
        self.assertFalse(c.is_skill(Path("api/agent/foo.yaml")))


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(c.slugify("Async API Agent!"), "async-api-agent")

    def test_unicode_strip(self):
        self.assertEqual(c.slugify("  GraphQL Schema  "), "graphql-schema")


class TestBuildDefinition(unittest.TestCase):
    def setUp(self):
        reset_stats()

    def test_keys_preserved_and_derived_added(self):
        doc = {"name": "alpha", "display_name": "Alpha", "category": "api",
               "version": "1.0.0", "capabilities": []}
        out = c.build_definition(doc, "agent", "api/agent/alpha.yaml")
        for k in ("name", "display_name", "category", "version", "capabilities"):
            self.assertEqual(out[k], doc[k])
        self.assertEqual(out["id"], "alpha")
        self.assertEqual(out["type"], "agent")
        self.assertEqual(out["skills"], [])
        self.assertEqual(out["tools"], [])
        self.assertEqual(out["outputs"], {})
        self.assertEqual(out["dependencies"], [])
        self.assertEqual(out["conversion"]["source_yaml"], "api/agent/alpha.yaml")

    def test_inputs_from_capability_parameters(self):
        doc = {"name": "beta", "capabilities": [
            {"name": "Deploy", "parameters": [
                {"name": "env", "type": "string", "description": "target env"},
                {"name": "count", "type": "int", "description": "replicas"},
            ]},
            {"name": "NoParams", "parameters": []},
        ]}
        out = c.build_definition(doc, "skill", "api/beta-skill.yaml")
        params = out["inputs"]["parameters"]
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["capability"], "Deploy")
        self.assertEqual(params[0]["name"], "env")
        self.assertEqual(params[0]["type"], "string")
        self.assertEqual(out["conversion"]["derived"]["inputs"], "capability.parameters")

    def test_no_params_means_empty_inputs(self):
        out = c.build_definition({"name": "gamma", "capabilities": []}, "agent", "x.yaml")
        self.assertEqual(out["inputs"], {})

    def test_tools_explicit_key_takes_priority(self):
        doc = {"name": "delta", "tools": ["helm"],
               "platforms": {"claude_code": {"tools": ["Bash"]}}}
        out = c.build_definition(doc, "agent", "x.yaml")
        self.assertEqual(out["tools"], ["helm"])
        self.assertEqual(out["conversion"]["derived"]["tools"], "tools")

    def test_tools_fallback_claude_code(self):
        doc = {"name": "epsilon", "platforms": {"claude_code": {"tools": ["Bash", "Read"]}}}
        out = c.build_definition(doc, "agent", "x.yaml")
        self.assertEqual(out["tools"], ["Bash", "Read"])
        self.assertEqual(out["conversion"]["derived"]["tools"], "platforms.claude_code.tools")

    def test_deps_from_prerequisites(self):
        doc = {"name": "zeta", "prerequisites": ["nodejs >= 18", "npm"]}
        out = c.build_definition(doc, "skill", "x-skill.yaml")
        self.assertEqual(out["dependencies"], ["nodejs >= 18", "npm"])

    def test_wiring_merges_into_skills(self):
        doc = {"name": "eta", "capabilities": []}
        wiring = [{"skill": "checkov-skill", "evidence": ["checkov"], "score": 1.0}]
        out = c.build_definition(doc, "agent", "x.yaml", wiring=wiring, wiring_src="skills/wiring.json")
        self.assertEqual(out["skills"], ["checkov-skill"])
        self.assertEqual(out["conversion"]["derived"]["skills"], "wiring (skills/wiring.json)")

    def test_wiring_does_not_duplicate_source_skills(self):
        doc = {"name": "theta", "skills": ["local-skill"]}
        wiring = [{"skill": "local-skill", "evidence": ["tool"], "score": 1.0},
                  {"skill": "wired-skill", "evidence": ["tool"], "score": 1.0}]
        out = c.build_definition(doc, "agent", "x.yaml", wiring=wiring, wiring_src="skills/wiring.json")
        self.assertEqual(out["skills"], ["local-skill", "wired-skill"])

    def test_wiring_never_applied_to_skills(self):
        out = c.build_definition({"name": "iota", "capabilities": []}, "skill", "x-skill.yaml",
                                 wiring=[{"skill": "nope", "evidence": []}], wiring_src="skills/wiring.json")
        self.assertEqual(out["skills"], [])


class TestBuildWorkflow(unittest.TestCase):
    def test_agent_then_capability_steps(self):
        doc = {"name": "kappa", "capabilities": [
            {"name": "Deploy", "commands": ["helm upgrade --install demo"]},
        ]}
        wf = c.build_workflow(doc, "kappa", "x.yaml", [], [])
        step_types = [s["type"] for s in wf["steps"]]
        self.assertEqual(step_types, ["agent", "capability"])
        self.assertEqual(wf["steps"][0]["agent"], "kappa")
        cap = wf["steps"][1]
        self.assertEqual(cap["capability"], "Deploy")
        self.assertEqual(cap["requires"], "step-1-agent")
        self.assertEqual(cap["tool"], "helm")
        self.assertEqual(wf["output"]["result"], "{{step-2-capability-deploy.output}}")

    def test_load_skill_steps_precede_agent(self):
        doc = {"name": "lambda", "capabilities": []}
        wf = c.build_workflow(doc, "lambda", "x.yaml", ["skill-a", "skill-b"], [])
        steps = wf["steps"]
        self.assertEqual([s["type"] for s in steps], ["skill", "skill", "agent"])
        self.assertEqual(steps[0]["id"], "step-1-load-skill-skill-a")
        self.assertEqual(steps[2]["id"], "step-3-agent")

    def test_no_skills_no_load_steps(self):
        doc = {"name": "mu", "capabilities": []}
        wf = c.build_workflow(doc, "mu", "x.yaml", [], [])
        self.assertEqual(len(wf["steps"]), 1)


if __name__ == "__main__":
    unittest.main()