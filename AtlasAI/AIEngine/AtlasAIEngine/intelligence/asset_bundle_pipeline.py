"""AtlasAI Phase 39B — Asset Bundle Pipeline.

Manages asset bundle entries, patch records, and bundle manifests
for the AssetBundleComposerTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AssetBundleEntry:
    """An asset bundle definition."""
    bundle_id: str
    bundle_name: str
    platform: str = "PC"
    compression: str = "LZ4"
    patch_strategy: str = "Incremental"
    asset_ids: list = field(default_factory=list)
    state: str = "Draft"
    enabled: bool = True

    @property
    def is_ready(self) -> bool:
        return self.state == "Ready"

    @property
    def is_shipping(self) -> bool:
        return self.state == "Shipping"

    @property
    def asset_count(self) -> int:
        return len(self.asset_ids)

    @property
    def has_assets(self) -> bool:
        return bool(self.asset_ids)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_compressed(self) -> bool:
        return self.compression != "None"


@dataclass
class BundlePatchEntry:
    """A bundle patch record."""
    patch_id: str
    bundle_id: str
    strategy: str = "Incremental"
    base_version: str = ""
    target_version: str = ""
    patch_size_bytes: int = 0
    validated: bool = False

    @property
    def is_validated(self) -> bool:
        return self.validated

    @property
    def is_incremental(self) -> bool:
        return self.strategy == "Incremental"

    @property
    def has_versions(self) -> bool:
        return bool(self.base_version) and bool(self.target_version)

    @property
    def size_kb(self) -> float:
        return self.patch_size_bytes / 1024.0


@dataclass
class BundleManifestEntry:
    """A bundle manifest entry."""
    manifest_id: str
    bundle_id: str
    manifest_path: str = ""
    state: str = "Draft"
    asset_count: int = 0
    total_size_bytes: int = 0

    @property
    def is_ready(self) -> bool:
        return self.state == "Ready"

    @property
    def is_draft(self) -> bool:
        return self.state == "Draft"

    @property
    def has_path(self) -> bool:
        return bool(self.manifest_path)

    @property
    def size_mb(self) -> float:
        return self.total_size_bytes / 1048576.0


class AssetBundlePipeline:
    """Pipeline managing asset bundles, patches, and manifests."""

    def __init__(self) -> None:
        self._bundles: Dict[str, AssetBundleEntry] = {}
        self._patches: Dict[str, Dict[str, BundlePatchEntry]] = {}
        self._manifests: Dict[str, Dict[str, BundleManifestEntry]] = {}

    def add_bundle(self, entry: AssetBundleEntry) -> bool:
        if not entry.bundle_id:
            return False
        self._bundles[entry.bundle_id] = entry
        return True

    def get_bundle(self, bundle_id: str) -> Optional[AssetBundleEntry]:
        return self._bundles.get(bundle_id)

    def remove_bundle(self, bundle_id: str) -> bool:
        if bundle_id in self._bundles:
            del self._bundles[bundle_id]
            self._patches.pop(bundle_id, None)
            self._manifests.pop(bundle_id, None)
            return True
        return False

    def get_all_bundles(self) -> List[AssetBundleEntry]:
        return list(self._bundles.values())

    def add_patch(self, bundle_id: str, patch: BundlePatchEntry) -> bool:
        if bundle_id not in self._bundles:
            return False
        if bundle_id not in self._patches:
            self._patches[bundle_id] = {}
        self._patches[bundle_id][patch.patch_id] = patch
        return True

    def remove_patch(self, bundle_id: str, patch_id: str) -> bool:
        if bundle_id in self._patches and patch_id in self._patches[bundle_id]:
            del self._patches[bundle_id][patch_id]
            return True
        return False

    def get_patches_for_bundle(self, bundle_id: str) -> List[BundlePatchEntry]:
        return list(self._patches.get(bundle_id, {}).values())

    def add_manifest(self, bundle_id: str, manifest: BundleManifestEntry) -> bool:
        if bundle_id not in self._bundles:
            return False
        if bundle_id not in self._manifests:
            self._manifests[bundle_id] = {}
        self._manifests[bundle_id][manifest.manifest_id] = manifest
        return True

    def remove_manifest(self, bundle_id: str, manifest_id: str) -> bool:
        if bundle_id in self._manifests and manifest_id in self._manifests[bundle_id]:
            del self._manifests[bundle_id][manifest_id]
            return True
        return False

    def get_manifests_for_bundle(self, bundle_id: str) -> List[BundleManifestEntry]:
        return list(self._manifests.get(bundle_id, {}).values())

    def get_ready_bundles(self) -> List[AssetBundleEntry]:
        return [b for b in self._bundles.values() if b.is_ready]

    def get_shipping_bundles(self) -> List[AssetBundleEntry]:
        return [b for b in self._bundles.values() if b.is_shipping]

    def get_validated_patches(self) -> List[BundlePatchEntry]:
        result = []
        for patches in self._patches.values():
            result.extend(p for p in patches.values() if p.is_validated)
        return result

    def get_ready_manifests(self) -> List[BundleManifestEntry]:
        result = []
        for manifests in self._manifests.values():
            result.extend(m for m in manifests.values() if m.is_ready)
        return result

    def get_bundles_by_platform(self, platform: str) -> List[AssetBundleEntry]:
        return [b for b in self._bundles.values() if b.platform == platform]

    def validate(self, entry: AssetBundleEntry) -> bool:
        return bool(entry.bundle_id) and bool(entry.bundle_name)

    @property
    def bundle_count(self) -> int:
        return len(self._bundles)

    @property
    def is_empty(self) -> bool:
        return len(self._bundles) == 0

    def clear(self) -> None:
        self._bundles.clear()
        self._patches.clear()
        self._manifests.clear()
