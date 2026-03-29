"""AtlasAI Phase 20D — Content Pack Loader.

Discovers, validates, and loads content pack manifests from the
NovaForge/Content directory tree.  Works alongside the C++ side
ContentPackRegistry to keep the runtime content state synchronised
with the on-disk packs.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ContentPackManifest:
    """Parsed representation of a content pack manifest file."""

    pack_id: str
    name: str
    version: str
    manifest_path: str
    assets: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def asset_count(self) -> int:
        return len(self.assets)


class ContentPackLoader:
    """Discover, validate, and load content pack manifests.

    Content packs live under a root directory (e.g. ``NovaForge/Content``).
    Each pack has a ``pack_manifest.json`` file that lists its assets and
    declares dependencies on other packs.

    Example::

        loader = ContentPackLoader("/repo/NovaForge/Content")
        packs = loader.discover()
        loader.load_pack("solar_system_pack_v1")
        manifest = loader.get_manifest("solar_system_pack_v1")
    """

    MANIFEST_FILENAME = "pack_manifest.json"

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._manifests: dict[str, ContentPackManifest] = {}
        self._loaded: set[str] = set()

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[str]:
        """Walk *content_root* and register all ``pack_manifest.json`` files.
        Returns list of discovered pack IDs."""
        discovered: list[str] = []
        for manifest_file in self.content_root.rglob(self.MANIFEST_FILENAME):
            try:
                data = json.loads(manifest_file.read_text())
                manifest = self._parse_manifest(data, str(manifest_file))
                self._manifests[manifest.pack_id] = manifest
                discovered.append(manifest.pack_id)
                logger.debug("ContentPackLoader: discovered pack %s", manifest.pack_id)
            except Exception as exc:  # pragma: no cover
                logger.warning("ContentPackLoader: skipping %s — %s", manifest_file, exc)
        return discovered

    def register_manifest(self, data: dict, manifest_path: str = "") -> ContentPackManifest:
        """Manually register a manifest from a pre-parsed dict."""
        manifest = self._parse_manifest(data, manifest_path)
        self._manifests[manifest.pack_id] = manifest
        return manifest

    @staticmethod
    def _parse_manifest(data: dict, manifest_path: str) -> ContentPackManifest:
        return ContentPackManifest(
            pack_id=data["pack_id"],
            name=data.get("name", data["pack_id"]),
            version=data.get("version", "1.0"),
            manifest_path=manifest_path,
            assets=list(data.get("assets", [])),
            dependencies=list(data.get("dependencies", [])),
            metadata=dict(data.get("metadata", {})),
        )

    # ------------------------------------------------------------------
    # Loading / unloading
    # ------------------------------------------------------------------

    def load_pack(self, pack_id: str) -> bool:
        """Mark a pack as loaded.  Returns False if not registered."""
        if pack_id not in self._manifests:
            logger.warning("ContentPackLoader: unknown pack %s", pack_id)
            return False
        self._loaded.add(pack_id)
        logger.info("ContentPackLoader: loaded pack %s", pack_id)
        return True

    def unload_pack(self, pack_id: str) -> bool:
        """Mark a pack as unloaded.  Returns False if it wasn't loaded."""
        if pack_id in self._loaded:
            self._loaded.discard(pack_id)
            logger.info("ContentPackLoader: unloaded pack %s", pack_id)
            return True
        return False

    def is_loaded(self, pack_id: str) -> bool:
        return pack_id in self._loaded

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_manifest(self, pack_id: str) -> Optional[ContentPackManifest]:
        return self._manifests.get(pack_id)

    def get_all_pack_ids(self) -> list[str]:
        return list(self._manifests.keys())

    def get_registered_count(self) -> int:
        return len(self._manifests)

    # ------------------------------------------------------------------
    # Dependency resolution
    # ------------------------------------------------------------------

    def get_load_order(self, pack_id: str) -> list[str]:
        """Return a topologically sorted load order for *pack_id* and its deps."""
        order: list[str] = []
        visited: set[str] = set()

        def _visit(pid: str) -> None:
            if pid in visited:
                return
            visited.add(pid)
            manifest = self._manifests.get(pid)
            if manifest:
                for dep in manifest.dependencies:
                    _visit(dep)
            order.append(pid)

        _visit(pack_id)
        return order

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def export_manifest(self, pack_id: str, path: str) -> bool:
        """Write a pack manifest back to *path*.  Returns True on success."""
        manifest = self._manifests.get(pack_id)
        if manifest is None:
            return False
        try:
            data = {
                "pack_id": manifest.pack_id,
                "name": manifest.name,
                "version": manifest.version,
                "assets": manifest.assets,
                "dependencies": manifest.dependencies,
                "metadata": manifest.metadata,
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("ContentPackLoader.export_manifest failed: %s", exc)
            return False

    def clear(self) -> None:
        self._manifests.clear()
        self._loaded.clear()
