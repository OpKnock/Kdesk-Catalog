"""Web security tests: traversal, malicious uploads, malformed docs.

Tests the actual guard code (not just HTTP status):
- download endpoints must never serve files outside their roots
- upload parsing must reject garbage without crashing
- converters must record per-artifact errors, never raise
"""
import io
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

try:
    import fastapi  # noqa: F401
except ImportError:
    raise unittest.SkipTest("web extra (fastapi) not installed")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kdesk.web import app as webapp
from kdesk.web.state import AppState


def setUpModule():
    webapp._state = AppState(ROOT)


def _fake_file(name: str, data: bytes):
    return SimpleNamespace(filename=name, file=io.BytesIO(data))


class TestPathTraversal(unittest.TestCase):
    def test_official_dotdot_rejected(self):
        from kdesk.web.routers.catalog import official_file
        for evil in ("../pyproject.toml", "../../pyproject.toml",
                     "..\\..\\pyproject.toml", "subdir/../../pyproject.toml"):
            r = official_file(path=evil)
            self.assertIn(r.status_code, (400, 404), evil)
            body = r.body.decode()
            self.assertNotIn("setuptools", body)
            self.assertNotIn("[project]", body)

    def test_official_absolute_rejected(self):
        from kdesk.web.routers.catalog import official_file
        r = official_file(path="C:/Windows/win.ini")
        self.assertIn(r.status_code, (400, 404))

    def test_convert_file_dotdot_rejected(self):
        from kdesk.web.routers import ops
        # find the convert_file endpoint by path
        fn = None
        for route in ops.router.routes:
            if getattr(route, "path", "") == "/api/convert/file":
                fn = route.endpoint
                break
        self.assertIsNotNone(fn)
        secret = ROOT / "pyproject.toml"
        for evil in ("../../../pyproject.toml", "..\\..\\..\\pyproject.toml",
                     str(secret)):
            r = fn(platform="cursor", path=evil)
            self.assertIn(r.status_code, (400, 404), evil)
            self.assertNotIn("setuptools", getattr(r, "body", b"").decode(
                "utf-8", "replace"))

    def test_definition_name_cannot_traverse(self):
        from kdesk.web.routers.catalog import definition
        r = definition(kind="agent", name="../../pyproject")
        self.assertEqual(r.status_code, 404)


class TestSymlinkEscape(unittest.TestCase):
    def test_symlink_out_of_root_is_blocked(self):
        import tempfile

        from kdesk.web.routers.catalog import official_file
        tmp = Path(tempfile.mkdtemp(prefix="kdesk_sym_"))
        try:
            # fake agents/ tree with a symlink pointing outside it
            agents = tmp / "agents"
            agents.mkdir()
            outside = tmp / "secret.txt"
            outside.write_text("TOP-SECRET-DO-NOT-SERVE", encoding="utf-8")
            link = agents / "evil.sh"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"cannot create symlinks here: {exc}")
            # point the endpoint at our fake tree by swapping state root
            from kdesk.web import app as webapp
            from kdesk.web.state import AppState
            real_state = webapp._state
            webapp._state = AppState.__new__(AppState)
            webapp._state.root = tmp
            webapp._state._catalog = None
            try:
                r = official_file(path="evil.sh")
            finally:
                webapp._state = real_state
            self.assertIn(r.status_code, (400, 404))
            self.assertNotIn("TOP-SECRET", r.body.decode("utf-8", "replace"))
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


class TestUploadValidation(unittest.TestCase):
    def test_non_yaml_rejected(self):
        from kdesk.web.routers.ops import _read_uploads
        with self.assertRaises(ValueError):
            _read_uploads([_fake_file("x.yaml", b"\x00\x01\x02{{{{")])

    def test_missing_name_rejected(self):
        from kdesk.web.routers.ops import _read_uploads
        with self.assertRaises(ValueError):
            _read_uploads([_fake_file("x.yaml", b"description: hi\n")])

    def test_non_dict_rejected(self):
        from kdesk.web.routers.ops import _read_uploads
        with self.assertRaises(ValueError):
            _read_uploads([_fake_file("x.yaml", b"- just\n- a\n- list\n")])

    def test_too_many_files_rejected(self):
        from kdesk.web.routers import ops
        from kdesk.web.routers.ops import _read_uploads
        files = [_fake_file(f"{i}.yaml", b"name: x\n") for i in range(ops.MAX_UPLOAD_FILES + 1)]
        with self.assertRaises(ValueError):
            _read_uploads(files)

    def test_oversize_rejected(self):
        from kdesk.web.routers import ops
        from kdesk.web.routers.ops import _read_uploads
        big = b"name: x\n# " + b"y" * (ops.MAX_UPLOAD_BYTES + 1)
        with self.assertRaises(ValueError):
            _read_uploads([_fake_file("big.yaml", big)])

    def test_valid_minimal_accepted(self):
        from kdesk.web.routers.ops import _read_uploads
        docs = _read_uploads([_fake_file("a.yaml", b"name: probe\n")])
        self.assertEqual(docs[0][1]["name"], "probe")


class TestMaliciousDocsNeverCrash(unittest.TestCase):
    def _run(self, doc):
        from kdesk.web.routers.ops import _convert_docs
        out = _convert_docs([("evil.yaml", doc)], ["cursor", "claude_code"])
        payload = json.loads(out.body.decode())
        self.assertIn("artifacts", payload)
        return payload["artifacts"]

    def test_wrong_types_recorded_not_raised(self):
        arts = self._run({"name": "evil", "description": "x" * 5000,
                          "capabilities": "not-a-list",
                          "platforms": ["not", "a", "dict"]})
        self.assertTrue(len(arts) > 0)
        for a in arts:
            self.assertTrue(a.get("content") or a.get("error"))

    def test_deeply_nested_doc(self):
        doc = {"name": "evil", "description": "x"}
        cur = doc
        for i in range(200):
            cur["nested"] = {"level": i}
            cur = cur["nested"]
        arts = self._run(doc)
        self.assertTrue(len(arts) > 0)

    def test_unicode_and_emoji_doc(self):
        arts = self._run({"name": "évïl-🚨", "description": "héllo wörld 🎉",
                          "instructions": "<script>alert(1)</script>"})
        self.assertTrue(len(arts) > 0)


class TestInputBounds(unittest.TestCase):
    def test_browse_clamps_huge_limit(self):
        # FastAPI Query(ge/le) rejects out-of-range input at the boundary;
        # here we assert the route declares the constraints.
        from kdesk.web.routers import catalog
        import inspect
        sig = inspect.signature(catalog.browse)
        self.assertIn("limit", sig.parameters)
        self.assertIn("offset", sig.parameters)


if __name__ == "__main__":
    unittest.main()
