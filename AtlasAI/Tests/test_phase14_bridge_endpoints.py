"""Tests for Phase 14 — Bridge Endpoint envelope shapes (no HTTP calls)."""

import unittest
import uuid
from datetime import datetime, timezone


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _uuid() -> str:
    return str(uuid.uuid4())


class TestProjectServiceRequest(unittest.TestCase):
    def _build(self) -> dict:
        return {
            "protocolVersion": "1.0",
            "requestId": _uuid(),
            "sessionId": _uuid(),
            "service": "ProjectService",
            "operation": "GetProjectInfo",
            "timestampUtc": _timestamp(),
        }

    def test_required_fields_present(self):
        req = self._build()
        for field in ("protocolVersion", "requestId", "sessionId", "service", "operation", "timestampUtc"):
            self.assertIn(field, req, f"Missing required field: {field}")

    def test_service_value(self):
        self.assertEqual(self._build()["service"], "ProjectService")

    def test_operation_value(self):
        self.assertEqual(self._build()["operation"], "GetProjectInfo")

    def test_request_id_is_string(self):
        self.assertIsInstance(self._build()["requestId"], str)

    def test_session_id_is_string(self):
        self.assertIsInstance(self._build()["sessionId"], str)


class TestEditorServiceRequest(unittest.TestCase):
    def _build(self) -> dict:
        return {
            "protocolVersion": "1.0",
            "requestId": _uuid(),
            "sessionId": _uuid(),
            "service": "EditorService",
            "operation": "GetSelectionSnapshot",
            "timestampUtc": _timestamp(),
        }

    def test_required_fields_present(self):
        req = self._build()
        for field in ("protocolVersion", "requestId", "sessionId", "service", "operation", "timestampUtc"):
            self.assertIn(field, req, f"Missing required field: {field}")

    def test_service_value(self):
        self.assertEqual(self._build()["service"], "EditorService")

    def test_operation_value(self):
        self.assertEqual(self._build()["operation"], "GetSelectionSnapshot")

    def test_protocol_version(self):
        self.assertEqual(self._build()["protocolVersion"], "1.0")


class TestBuildServiceRequest(unittest.TestCase):
    def _build(self) -> dict:
        return {
            "protocolVersion": "1.0",
            "requestId": _uuid(),
            "sessionId": _uuid(),
            "service": "BuildService",
            "operation": "RunBuild",
            "timestampUtc": _timestamp(),
            "payload": {"configuration": "Debug", "platform": "x64"},
        }

    def test_required_fields_present(self):
        req = self._build()
        for field in ("protocolVersion", "requestId", "sessionId", "service", "operation", "timestampUtc"):
            self.assertIn(field, req, f"Missing required field: {field}")

    def test_service_value(self):
        self.assertEqual(self._build()["service"], "BuildService")

    def test_operation_value(self):
        self.assertEqual(self._build()["operation"], "RunBuild")

    def test_optional_payload_is_dict(self):
        req = self._build()
        self.assertIsInstance(req.get("payload"), dict)


class TestBridgeResponseShape(unittest.TestCase):
    def _build(self, success: bool = True) -> dict:
        return {
            "protocolVersion": "1.0",
            "requestId": _uuid(),
            "success": success,
        }

    def test_required_keys_present(self):
        resp = self._build()
        for key in ("protocolVersion", "requestId", "success"):
            self.assertIn(key, resp, f"Missing required key: {key}")

    def test_success_true(self):
        self.assertTrue(self._build(success=True)["success"])

    def test_success_false(self):
        self.assertFalse(self._build(success=False)["success"])

    def test_protocol_version_string(self):
        self.assertIsInstance(self._build()["protocolVersion"], str)

    def test_request_id_string(self):
        self.assertIsInstance(self._build()["requestId"], str)


class TestSessionConnectShape(unittest.TestCase):
    def _build(self) -> dict:
        return {
            "protocolVersion": "1.0",
            "clientName": "AtlasAI",
            "clientVersion": "0.14.0",
            "capabilities": ["liveViewport", "hotReload"],
        }

    def test_required_keys_present(self):
        req = self._build()
        for key in ("protocolVersion", "clientName", "clientVersion", "capabilities"):
            self.assertIn(key, req, f"Missing required key: {key}")

    def test_capabilities_is_list(self):
        self.assertIsInstance(self._build()["capabilities"], list)

    def test_client_version_string(self):
        self.assertIsInstance(self._build()["clientVersion"], str)

    def test_client_name_string(self):
        self.assertIsInstance(self._build()["clientName"], str)


if __name__ == "__main__":
    unittest.main()
