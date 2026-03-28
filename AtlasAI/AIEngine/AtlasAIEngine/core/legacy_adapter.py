"""legacy_adapter.py — MasterRepo legacy layout adapter for AtlasAI context.

Bridges AtlasAI to a pre-refactor MasterRepo that still uses the Arbiter naming
convention and the old flat folder structure (src/, tests/, docs/ at repo root).

Responsibilities:
- Detect whether a repo root uses the legacy layout.
- Translate legacy Arbiter.* tool-action names to modern AtlasAI equivalents.
- Resolve legacy source/test/doc paths and expose them as normalised SearchRoots.
- Load and validate the masterrepo.legacy.project.json manifest.
- Provide a bridge-compatible project info snapshot for AtlasAI consumers.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional
from core.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LEGACY_MANIFEST_REL = "Shared/ProjectManifests/masterrepo.legacy.project.json"

#: Maps legacy Arbiter.* action names to their modern equivalents.
LEGACY_ACTION_MAP: dict[str, str] = {
    "Arbiter.ValidateData":       "ValidateData",
    "Arbiter.RunPCGPreview":      "RunPCGPreview",
    "Arbiter.OpenScene":          "OpenScene",
    "Arbiter.FocusEntity":        "FocusEntity",
    "Arbiter.RegenerateSchemas":  "RegenerateSchemas",
}

#: Default search roots for a legacy MasterRepo layout.
LEGACY_DEFAULT_ROOTS: list[dict[str, str]] = [
    {"label": "Source",  "path": "src",   "kind": "source"},
    {"label": "Tests",   "path": "tests", "kind": "source"},
    {"label": "Docs",    "path": "docs",  "kind": "docs"},
    {"label": "Scripts", "path": "Scripts", "kind": "script"},
]


# ---------------------------------------------------------------------------
# Manifest model
# ---------------------------------------------------------------------------

class LegacyManifest:
    """Parsed representation of masterrepo.legacy.project.json."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    # -- Project info --------------------------------------------------------
    @property
    def project_id(self) -> str:
        return self._data.get("project", {}).get("id", "masterrepo-legacy")

    @property
    def display_name(self) -> str:
        return self._data.get("project", {}).get("displayName", "MasterRepo (Legacy)")

    @property
    def version(self) -> str:
        return self._data.get("project", {}).get("version", "0.1.0")

    # -- Legacy layout -------------------------------------------------------
    @property
    def legacy_enabled(self) -> bool:
        return bool(self._data.get("legacyLayout", {}).get("enabled", False))

    @property
    def legacy_naming_prefix(self) -> str:
        return str(self._data.get("legacyLayout", {}).get("legacyNamingPrefix", "Arbiter"))

    @property
    def legacy_source_root(self) -> str:
        return str(self._data.get("legacyLayout", {}).get("sourceRoot", "src"))

    @property
    def legacy_tests_root(self) -> str:
        return str(self._data.get("legacyLayout", {}).get("testsRoot", "tests"))

    @property
    def legacy_docs_root(self) -> str:
        return str(self._data.get("legacyLayout", {}).get("docsRoot", "docs"))

    # -- Bridge config -------------------------------------------------------
    @property
    def bridge_host(self) -> str:
        return str(self._data.get("bridge", {}).get("host", "localhost"))

    @property
    def rest_port(self) -> int:
        return int(self._data.get("bridge", {}).get("restPort", 57100))

    # -- Safety --------------------------------------------------------------
    @property
    def allowed_tool_actions(self) -> list[str]:
        return list(self._data.get("safetySettings", {}).get("allowedToolActions", []))

    @property
    def require_dry_run(self) -> bool:
        return bool(self._data.get("safetySettings", {}).get("requireDryRunByDefault", True))

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id":     self.project_id,
            "display_name":   self.display_name,
            "version":        self.version,
            "legacy_enabled": self.legacy_enabled,
            "naming_prefix":  self.legacy_naming_prefix,
            "bridge_host":    self.bridge_host,
            "rest_port":      self.rest_port,
        }


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class MasterRepoLegacyAdapter:
    """
    Provides AtlasAI with a normalised view of a legacy MasterRepo workspace.

    Usage::

        adapter = MasterRepoLegacyAdapter("/path/to/repo")
        info    = adapter.get_project_info()
        roots   = adapter.get_search_roots()
        modern  = adapter.translate_action("Arbiter.ValidateData")
    """

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self._manifest: Optional[LegacyManifest] = None
        self._load_manifest()

    # ------------------------------------------------------------------
    # Manifest loading
    # ------------------------------------------------------------------

    def _load_manifest(self) -> None:
        manifest_path = self.repo_root / LEGACY_MANIFEST_REL
        if not manifest_path.exists():
            logger.warning(
                "Legacy manifest not found at %s; using defaults.", manifest_path
            )
            self._manifest = LegacyManifest({})
            return
        try:
            with manifest_path.open(encoding="utf-8") as f:
                data = json.load(f)
            self._manifest = LegacyManifest(data)
            logger.debug("Loaded legacy manifest: %s", manifest_path)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load legacy manifest: %s", exc)
            self._manifest = LegacyManifest({})

    @property
    def manifest(self) -> LegacyManifest:
        assert self._manifest is not None
        return self._manifest

    # ------------------------------------------------------------------
    # Layout detection
    # ------------------------------------------------------------------

    def is_legacy_layout(self) -> bool:
        """Return True if the repo root contains the legacy flat layout."""
        if self.manifest.legacy_enabled:
            return True
        # Heuristic: legacy layout has src/ at the repo root
        return (self.repo_root / "src").is_dir()

    # ------------------------------------------------------------------
    # Project info
    # ------------------------------------------------------------------

    def get_project_info(self) -> dict[str, Any]:
        """Return a bridge-compatible project info dict."""
        return {
            "id":           self.manifest.project_id,
            "displayName":  self.manifest.display_name,
            "version":      self.manifest.version,
            "isLegacy":     self.is_legacy_layout(),
            "namingPrefix": self.manifest.legacy_naming_prefix,
        }

    # ------------------------------------------------------------------
    # Search roots
    # ------------------------------------------------------------------

    def get_search_roots(self) -> list[dict[str, str]]:
        """
        Return normalised search roots for this legacy layout.
        Falls back to defaults if the legacy roots don't exist on disk.
        """
        roots: list[dict[str, str]] = []

        # Legacy-layout paths
        legacy_roots = [
            {"label": "Legacy Source", "path": self.manifest.legacy_source_root,    "kind": "source"},
            {"label": "Legacy Tests",  "path": self.manifest.legacy_tests_root,     "kind": "source"},
            {"label": "Legacy Docs",   "path": self.manifest.legacy_docs_root,      "kind": "docs"},
        ]

        # Modern paths (from refactored layout, if they exist)
        modern_roots = [
            {"label": "Atlas",    "path": "Atlas",         "kind": "source"},
            {"label": "NovaForge","path": "NovaForge",     "kind": "source"},
            {"label": "Docs",     "path": "Docs",          "kind": "docs"},
            {"label": "Data",     "path": "NovaForge/Data","kind": "data"},
        ]

        for r in legacy_roots + modern_roots:
            full = self.repo_root / r["path"]
            if full.exists():
                roots.append(r)

        if not roots:
            logger.debug("No roots found on disk; returning defaults.")
            return LEGACY_DEFAULT_ROOTS

        return roots

    # ------------------------------------------------------------------
    # Action name translation
    # ------------------------------------------------------------------

    def translate_action(self, action_name: str) -> str:
        """
        Translate a legacy Arbiter.* action name to its modern equivalent.
        Returns the input unchanged if no translation is needed.
        """
        # Exact map lookup first
        if action_name in LEGACY_ACTION_MAP:
            return LEGACY_ACTION_MAP[action_name]

        # Strip any legacy prefix dynamically
        prefix = self.manifest.legacy_naming_prefix + "."
        if action_name.startswith(prefix):
            modern = action_name[len(prefix):]
            logger.debug("Translated legacy action '%s' → '%s'", action_name, modern)
            return modern

        return action_name

    # ------------------------------------------------------------------
    # Allowed actions
    # ------------------------------------------------------------------

    def get_allowed_tool_actions(self) -> list[str]:
        """Return the list of allowed tool actions from the manifest."""
        return self.manifest.allowed_tool_actions

    def is_action_allowed(self, action_name: str) -> bool:
        """
        Return True if the (possibly legacy-named) action is in the allowlist.
        Translates the name before checking.
        """
        modern = self.translate_action(action_name)
        allowed = self.get_allowed_tool_actions()
        return modern in allowed

    # ------------------------------------------------------------------
    # Dry-run guard
    # ------------------------------------------------------------------

    def requires_dry_run(self) -> bool:
        """Return True when the manifest mandates dry-run by default."""
        return self.manifest.require_dry_run
