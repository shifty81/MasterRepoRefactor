"""Tests for Phase 14 — JSON schema validation of bridge protocol envelopes."""

import json
import unittest
from pathlib import Path

import jsonschema
from jsonschema import ValidationError, validate

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = REPO_ROOT / "Shared" / "ToolProtocol" / "schemas"


def _load(filename: str) -> dict:
    return json.loads((SCHEMAS_DIR / filename).read_text(encoding="utf-8"))


class TestBridgeRequestSchema(unittest.TestCase):
    _schema = None

    def setUp(self):
        self._schema = _load("bridge_request.schema.json")

    def test_valid_minimal_request(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": "ProjectService",
            "operation": "GetProjectInfo",
            "timestampUtc": "2024-01-01T00:00:00Z",
        }
        validate(instance=instance, schema=self._schema)

    def test_missing_required_field_session_id(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "service": "ProjectService",
            "operation": "GetProjectInfo",
            "timestampUtc": "2024-01-01T00:00:00Z",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)

    def test_wrong_type_service(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": 123,
            "operation": "GetProjectInfo",
            "timestampUtc": "2024-01-01T00:00:00Z",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)

    def test_with_optional_payload(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": "BuildService",
            "operation": "RunBuild",
            "timestampUtc": "2024-01-01T00:00:00Z",
            "payload": {"configuration": "Debug"},
        }
        validate(instance=instance, schema=self._schema)


class TestBridgeResponseSchema(unittest.TestCase):
    _schema = None

    def setUp(self):
        self._schema = _load("bridge_response.schema.json")

    def test_valid_minimal_response(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "success": True,
        }
        validate(instance=instance, schema=self._schema)

    def test_missing_success_raises(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)

    def test_error_response_with_error_code(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "success": False,
            "errorCode": "NOT_FOUND",
            "message": "Resource not found",
        }
        validate(instance=instance, schema=self._schema)

    def test_wrong_type_success_raises(self):
        instance = {
            "protocolVersion": "1.0",
            "requestId": "550e8400-e29b-41d4-a716-446655440000",
            "success": "yes",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)


class TestBridgeEventSchema(unittest.TestCase):
    _schema = None

    def setUp(self):
        self._schema = _load("bridge_event.schema.json")

    def test_valid_minimal_event(self):
        instance = {
            "protocolVersion": "1.0",
            "eventId": "550e8400-e29b-41d4-a716-446655440002",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": "BuildService",
            "eventType": "BuildProgress",
            "timestampUtc": "2024-01-01T00:00:00Z",
        }
        validate(instance=instance, schema=self._schema)

    def test_missing_event_type_raises(self):
        instance = {
            "protocolVersion": "1.0",
            "eventId": "550e8400-e29b-41d4-a716-446655440002",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": "BuildService",
            "timestampUtc": "2024-01-01T00:00:00Z",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)

    def test_with_optional_payload(self):
        instance = {
            "protocolVersion": "1.0",
            "eventId": "550e8400-e29b-41d4-a716-446655440002",
            "sessionId": "550e8400-e29b-41d4-a716-446655440001",
            "service": "EditorService",
            "eventType": "SelectionChanged",
            "timestampUtc": "2024-01-01T00:00:00Z",
            "payload": {"line": 42},
        }
        validate(instance=instance, schema=self._schema)


class TestSessionConnectSchema(unittest.TestCase):
    _schema = None

    def setUp(self):
        self._schema = _load("session_connect_request.schema.json")

    def test_valid_minimal_connect(self):
        instance = {
            "clientVersion": "0.14.0",
            "projectId": "my-project",
        }
        validate(instance=instance, schema=self._schema)

    def test_with_protocol_version(self):
        instance = {
            "protocolVersion": "1.0",
            "clientVersion": "0.14.0",
            "projectId": "my-project",
        }
        validate(instance=instance, schema=self._schema)

    def test_missing_client_version_raises(self):
        instance = {
            "projectId": "my-project",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)

    def test_missing_project_id_raises(self):
        instance = {
            "clientVersion": "0.14.0",
        }
        with self.assertRaises(ValidationError):
            validate(instance=instance, schema=self._schema)


class TestSchemaFilesExist(unittest.TestCase):
    def _check(self, filename: str):
        path = SCHEMAS_DIR / filename
        self.assertTrue(path.exists(), f"Schema file missing: {path}")

    def test_bridge_request_schema_exists(self):
        self._check("bridge_request.schema.json")

    def test_bridge_response_schema_exists(self):
        self._check("bridge_response.schema.json")

    def test_bridge_event_schema_exists(self):
        self._check("bridge_event.schema.json")

    def test_session_connect_request_schema_exists(self):
        self._check("session_connect_request.schema.json")

    def test_tool_action_request_schema_exists(self):
        self._check("tool_action_request.schema.json")


if __name__ == "__main__":
    unittest.main()
