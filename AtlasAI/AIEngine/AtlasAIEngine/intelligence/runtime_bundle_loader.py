"""AtlasAI Phase 21D — Runtime Bundle Loader.

Discovers, validates, and loads runtime asset bundle manifests from the
NovaForge/Content directory tree.  Mirrors the C++ RuntimeBundleRegistry
for cross-boundary bundle management and level streaming support.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AssetRef:
    """Reference to a single asset within a bundle."""

    asset_id: str
    asset_type: str
    path: str


@dataclass
class BundleManifest:
    """Parsed representation of a runtime asset bundle manifest."""

    bundle_id: str
    name: str
    version: str
    manifest_path: str
    assets: list[AssetRef] = field(default_factory=list)
    estimated_size_bytes: int = 0
    required: bool = False

    @property
    def asset_count(self) -> int:
        return len(self.assets)


class RuntimeBundleLoader:
    """Discover, validate, and load runtime asset bundle manifests.

    Bundle manifests live under a root directory and are named
    ``bundle_manifest.json``.

    Example::

        loader = RuntimeBundleLoader("/repo/NovaForge/Content")
        packs = loader.discover()
        loader.load_bundle("level_01_bundle")
        manifest = loader.get_manifest("level_01_bundle")
        order = loader.get_required_bundles()
    """

    MANIFEST_FILENAME = "bundle_manifest.json"

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._manifests: dict[str, BundleManifest] = {}
        self._loaded: set[str] = set()

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[str]:
        """Walk *content_root* for all ``bundle_manifest.json`` files."""
        discovered: list[str] = []
        for manifest_file in self.content_root.rglob(self.MANIFEST_FILENAME):
            try:
                data = json.loads(manifest_file.read_text())
                manifest = self._parse_manifest(data, str(manifest_file))
                self._manifests[manifest.bundle_id] = manifest
                discovered.append(manifest.bundle_id)
            except Exception as exc:  # pragma: no cover
                logger.warning("RuntimeBundleLoader: skipping %s — %s",
                               manifest_file, exc)
        return discovered

    def register_manifest(self, data: dict,
                          manifest_path: str = "") -> BundleManifest:
        """Manually register a manifest from a pre-parsed dict."""
        manifest = self._parse_manifest(data, manifest_path)
        self._manifests[manifest.bundle_id] = manifest
        return manifest

    @staticmethod
    def _parse_manifest(data: dict, manifest_path: str) -> BundleManifest:
        assets = [
            AssetRef(
                asset_id=a["asset_id"],
                asset_type=a.get("asset_type", "Unknown"),
                path=a.get("path", ""),
            )
            for a in data.get("assets", [])
        ]
        return BundleManifest(
            bundle_id=data["bundle_id"],
            name=data.get("name", data["bundle_id"]),
            version=data.get("version", "1.0"),
            manifest_path=manifest_path,
            assets=assets,
            estimated_size_bytes=data.get("estimated_size_bytes", 0),
            required=data.get("required", False),
        )

    # ------------------------------------------------------------------
    # Loading / unloading
    # ------------------------------------------------------------------

    def load_bundle(self, bundle_id: str) -> bool:
        if bundle_id not in self._manifests:
            logger.warning("RuntimeBundleLoader: unknown bundle %s", bundle_id)
            return False
        self._loaded.add(bundle_id)
        logger.info("RuntimeBundleLoader: loaded %s", bundle_id)
        return True

    def unload_bundle(self, bundle_id: str) -> bool:
        if bundle_id in self._loaded:
            self._loaded.discard(bundle_id)
            return True
        return False

    def is_loaded(self, bundle_id: str) -> bool:
        return bundle_id in self._loaded

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    def get_loaded_bundle_ids(self) -> list[str]:
        return list(self._loaded)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_manifest(self, bundle_id: str) -> Optional[BundleManifest]:
        return self._manifests.get(bundle_id)

    def get_all_bundle_ids(self) -> list[str]:
        return list(self._manifests.keys())

    def get_registered_count(self) -> int:
        return len(self._manifests)

    def get_required_bundles(self) -> list[BundleManifest]:
        return [m for m in self._manifests.values() if m.required]

    def get_total_estimated_size(self) -> int:
        return sum(m.estimated_size_bytes for m in self._manifests.values())

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_manifest(self, bundle_id: str, path: str) -> bool:
        manifest = self._manifests.get(bundle_id)
        if manifest is None:
            return False
        try:
            data = {
                "bundle_id": manifest.bundle_id,
                "name": manifest.name,
                "version": manifest.version,
                "required": manifest.required,
                "estimated_size_bytes": manifest.estimated_size_bytes,
                "assets": [
                    {"asset_id": a.asset_id,
                     "asset_type": a.asset_type,
                     "path": a.path}
                    for a in manifest.assets
                ],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("RuntimeBundleLoader.export_manifest failed: %s", exc)
            return False

    def clear(self) -> None:
        self._manifests.clear()
        self._loaded.clear()
