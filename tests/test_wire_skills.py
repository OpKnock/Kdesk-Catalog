import importlib.util
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


w = load_module("wire_skills", "wire-skills.py")

CHECKOV_SKILL = {"name": "checkov-skill", "tools": ["checkov"], "prerequisites": []}
BANDIT_SKILL = {"name": "bandit-skill", "tools": ["bandit"], "prerequisites": []}
PYTHON_SKILLS = {f"python-{i}-skill": {"name": f"python-{i}-skill", "tools": ["python", "pip"]}
                 for i in range(1, 8)}  # 'python' appears 7x -> rarity 1/7 < 0.15


def agent(name, commands):
    return {"name": name, "capabilities": [
        {"name": "Run", "commands": commands}, {"name": "Labels", "commands": []},
    ]}


class TestComputeWiring(unittest.TestCase):
    def test_strong_single_token_wires(self):
        wiring, stats = w.compute_wiring(
            {"iam-auditor": agent("iam-auditor", ["checkov -d .", "pmapper query"])},
            {"checkov-skill": CHECKOV_SKILL})
        links = wiring["iam-auditor"]
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["skill"], "checkov-skill")
        self.assertEqual(links[0]["evidence"], ["checkov"])
        self.assertEqual(stats["agents_wired"], 1)
        self.assertEqual(stats["total_links"], 1)

    def test_generic_token_alone_does_not_wire(self):
        skills = dict(PYTHON_SKILLS)
        skills["checkov-skill"] = CHECKOV_SKILL
        wiring, _ = w.compute_wiring(
            {"py-runner": agent("py-runner", ["python train.py"])},
            skills)
        self.assertNotIn("py-runner", wiring)

    def test_curl_excluded(self):
        wiring, _ = w.compute_wiring(
            {"fetcher": agent("fetcher", ["curl -s http://x"])},
            {"health-skill": {"name": "health-skill", "tools": ["curl", "httpie"]}})
        self.assertNotIn("fetcher", wiring)

    def test_label_word_excluded(self):
        skills = dict(PYTHON_SKILLS)
        wiring, _ = w.compute_wiring(
            {"labeller": agent("labeller", ["install:", "status:"])},
            skills)
        self.assertNotIn("labeller", wiring)

    def test_two_weak_tokens_wire(self):
        wiring, _ = w.compute_wiring(
            {"cloud-ops": agent("cloud-ops", ["aws s3 ls", "docker ps"])},
            {"cloud-skill": {"name": "cloud-skill", "tools": ["aws", "docker"]}})
        links = wiring["cloud-ops"]
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["skill"], "cloud-skill")
        self.assertEqual(links[0]["evidence"], ["aws", "docker"])

    def test_rarer_skill_sorted_first(self):
        skills = {"checkov-skill": CHECKOV_SKILL,
                  "openapi-skill": {"name": "openapi-skill", "tools": ["openapi-generator", "swagger-cli"]}}
        for i in range(6):
            skills[f"openapi-clone-{i}"] = {"name": f"openapi-clone-{i}",
                                            "tools": ["openapi-generator", "swagger-cli"]}
        wiring, _ = w.compute_wiring(
            {"a": agent("a", ["swagger-cli spec", "openapi-generator gen", "checkov -d ."])},
            skills)
        # checkov is rarer (1/1) and must rank above the openapi family (1/7 + 1/7)
        self.assertEqual(wiring["a"][0]["skill"], "checkov-skill")
        self.assertIn("openapi-skill", [l["skill"] for l in wiring["a"]])

    def test_max_links_cap(self):
        skills = {"checkov-skill": CHECKOV_SKILL, "bandit-skill": BANDIT_SKILL,
                  "openapi-skill": {"name": "openapi-skill", "tools": ["openapi-generator"]}}
        wiring, _ = w.compute_wiring(
            {"multi": agent("multi", ["checkov -d .", "bandit -r .", "openapi-generator gen"])},
            skills, max_links=2)
        self.assertEqual(len(wiring["multi"]), 2)

    def test_unknown_tokens_yield_no_links(self):
        wiring, _ = w.compute_wiring(
            {"alien": agent("alien", ["gobbledygook --run"])},
            {"checkov-skill": CHECKOV_SKILL})
        self.assertNotIn("alien", wiring)

    def test_no_evidence_skills_ignored(self):
        wiring, stats = w.compute_wiring(
            {"x": agent("x", ["checkov -d ."])},
            {"checkov-skill": CHECKOV_SKILL,
             "no-tools-skill": {"name": "no-tools-skill", "tools": []}})
        self.assertEqual(len(wiring["x"]), 1)
        self.assertEqual(stats["skills_with_tool_evidence"], 1)

    def test_digit_and_one_char_tokens_dropped(self):
        wiring, _ = w.compute_wiring(
            {"y": agent("y", ["x run", "tool1236 --go"])},
            {"abc-skill": {"name": "abc-skill", "tools": ["x xyz123", "7z", "1236"]}})
        self.assertNotIn("y", wiring)

    def test_two_char_cli_wires(self):
        wiring, stats = w.compute_wiring(
            {"secret-ops": agent("secret-ops", ["op item get prod", "bw get password"])},
            {"1password-skill": {"name": "1password-skill", "tools": ["op"]},
             "bitwarden-skill": {"name": "bitwarden-skill", "tools": ["bw"]}})
        self.assertEqual(len(wiring["secret-ops"]), 2)
        self.assertIn("1password-skill", [l["skill"] for l in wiring["secret-ops"]])
        self.assertEqual(stats["skills_with_tool_evidence"], 2)
        self.assertEqual(stats["skills_without_evidence"], 0)

    def test_two_char_weak_cli_alone_does_not_wire(self):
        wiring, _ = w.compute_wiring(
            {"t": agent("t", ["cd /var/www"])},
            {"cd-skill": {"name": "cd-skill", "tools": ["cd"]}})
        self.assertNotIn("t", wiring)


if __name__ == "__main__":
    unittest.main()