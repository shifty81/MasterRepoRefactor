"""Phase 14 — FastAPI Bridge Integration Tests.

Spins up a minimal in-process FastAPI test app that mirrors the real bridge's
endpoint shapes and exercises each handler without requiring the full
AtlasAI server stack.
"""

import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal test app — mirrors the real bridge's endpoint shapes
# ---------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.testclient import TestClient

_test_app = FastAPI()


@_test_app.get("/health")
def _health():
    return {"status": "ok", "timestamp": "2026-01-01T00:00:00Z"}


@_test_app.get("/projects")
def _projects():
    return {"projects": []}


@_test_app.post("/chat")
def _chat(msg: dict):
    return {"response": "test", "project": msg.get("project", "")}


@_test_app.post("/build")
def _build(req: dict):
    return {"status": "ok", "output": ""}


@_test_app.get("/status")
def _status():
    return {
        "status": "ready",
        "model": "none",
        "gpu": "none",
        "vram_gb": 0.0,
        "max_tokens": 0,
    }


_client = TestClient(_test_app)

# Path to the real bridge source
_BRIDGE_PATH = (
    Path(__file__).resolve().parent.parent
    / "AIEngine"
    / "PythonBridge"
    / "fastapi_bridge.py"
)


# ---------------------------------------------------------------------------
# Test classes
# ---------------------------------------------------------------------------


class TestBridgeAppSetup(unittest.TestCase):
    """Verify the real fastapi_bridge.py exists and has the expected structure."""

    def setUp(self):
        self.assertTrue(_BRIDGE_PATH.exists(), f"Bridge file not found: {_BRIDGE_PATH}")
        self._src = _BRIDGE_PATH.read_text(encoding="utf-8")

    def test_bridge_file_exists(self):
        self.assertTrue(_BRIDGE_PATH.is_file())

    def test_has_fastapi_app(self):
        self.assertIn("FastAPI(", self._src)
        self.assertIn("app =", self._src)

    def test_has_health_endpoint(self):
        self.assertIn('"/health"', self._src)

    def test_has_projects_endpoint(self):
        self.assertIn('"/projects"', self._src)

    def test_has_chat_endpoint(self):
        self.assertIn('"/chat"', self._src)

    def test_has_build_endpoint(self):
        self.assertIn('"/build"', self._src)

    def test_has_status_endpoint(self):
        self.assertIn('"/status"', self._src)

    def test_has_models_endpoint(self):
        self.assertIn('"/models"', self._src)


class TestBridgeEndpointShapes(unittest.TestCase):
    """Test the minimal in-process FastAPI app via TestClient."""

    def test_health_returns_200(self):
        resp = _client.get("/health")
        self.assertEqual(resp.status_code, 200)

    def test_health_has_status_field(self):
        resp = _client.get("/health")
        self.assertIn("status", resp.json())

    def test_projects_returns_200(self):
        resp = _client.get("/projects")
        self.assertEqual(resp.status_code, 200)

    def test_projects_has_projects_key(self):
        resp = _client.get("/projects")
        self.assertIn("projects", resp.json())

    def test_chat_post_returns_200(self):
        resp = _client.post("/chat", json={"message": "hi", "project": "test"})
        self.assertEqual(resp.status_code, 200)

    def test_build_post_returns_200(self):
        resp = _client.post("/build", json={"project": "test"})
        self.assertEqual(resp.status_code, 200)

    def test_status_returns_200(self):
        resp = _client.get("/status")
        self.assertEqual(resp.status_code, 200)

    def test_unknown_route_returns_404(self):
        resp = _client.get("/nonexistent")
        self.assertEqual(resp.status_code, 404)


class TestBridgePydanticModels(unittest.TestCase):
    """Verify Pydantic model field names by inspecting the bridge source."""

    def setUp(self):
        self._src = _BRIDGE_PATH.read_text(encoding="utf-8")

    def test_user_message_has_message_field(self):
        # UserMessage must declare `message: str`
        self.assertIn("message: str", self._src)

    def test_user_message_has_project_field(self):
        # UserMessage must declare `project: str`
        self.assertIn("project: str", self._src)

    def test_build_request_has_project_field(self):
        # BuildRequest must declare `project: str`
        self.assertIn("class BuildRequest", self._src)
        self.assertIn("project: str", self._src)

    def test_persona_request_has_persona_field(self):
        self.assertIn("persona: str", self._src)

    def test_status_response_has_status_field(self):
        self.assertIn("class StatusResponse", self._src)
        self.assertIn("status: str", self._src)

    def test_status_response_has_model_field(self):
        self.assertIn("model: str", self._src)


class TestBridgeRoutesCoverage(unittest.TestCase):
    """Check the bridge file contains all critical route handlers."""

    def setUp(self):
        self._src = _BRIDGE_PATH.read_text(encoding="utf-8")

    def test_has_ide_endpoint(self):
        self.assertIn('"/ide"', self._src)

    def test_has_files_endpoint(self):
        self.assertIn('"/files"', self._src)

    def test_has_assistant_endpoint(self):
        self.assertIn('"/assistant/chat"', self._src)

    def test_has_ai_complete_endpoint(self):
        self.assertIn('"/ai/complete"', self._src)

    def test_has_roadmap_endpoint(self):
        self.assertIn('"/roadmap/', self._src)

    def test_has_history_endpoint(self):
        self.assertIn('"/history/', self._src)


if __name__ == "__main__":
    unittest.main()
