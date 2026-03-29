"""AtlasAI Phase 23B — Shader Permutation Cache.

Tracks compiled shader permutations keyed by feature-flag combinations so
that the engine avoids redundant recompilations when switching render paths.
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ShaderVariant:
    """Represents a single compiled shader variant."""

    variant_id: str
    shader_name: str
    defines: list[str] = field(default_factory=list)
    stage: str = "vertex"          # vertex | fragment | compute | geometry
    profile: str = "sm_6_0"
    source_hash: str = ""
    compiled_hash: str = ""
    compile_time: float = field(default_factory=time.time)
    size_bytes: int = 0
    compile_duration_ms: float = 0.0

    @property
    def age_seconds(self) -> float:
        return time.time() - self.compile_time

    @property
    def define_key(self) -> str:
        """Canonical sorted defines string for lookup."""
        return ";".join(sorted(self.defines))


class ShaderPermutationCache:
    """Cache for compiled shader permutations.

    Variants are indexed by ``(shader_name, sorted_defines, stage)``.

    Typical usage::

        cache = ShaderPermutationCache()
        variant = cache.register("MyShader", ["USE_NORMAL_MAP", "ALPHA_TEST"],
                                  stage="fragment",
                                  source_hash=h)
        if cache.is_valid("MyShader", ["USE_NORMAL_MAP", "ALPHA_TEST"],
                           stage="fragment", source_hash=h):
            bytecode = cache.get_compiled_hash(variant.variant_id)
    """

    def __init__(self, cache_path: str = "") -> None:
        self._cache_path: str = cache_path
        self._variants: dict[str, ShaderVariant] = {}

    # ------------------------------------------------------------------
    # Registration & lookup
    # ------------------------------------------------------------------

    @staticmethod
    def _make_key(shader_name: str, defines: list[str], stage: str) -> str:
        key_str = f"{shader_name}|{';'.join(sorted(defines))}|{stage}"
        return hashlib.sha256(key_str.encode()).hexdigest()[:16]

    def register(
        self,
        shader_name: str,
        defines: list[str],
        stage: str = "vertex",
        profile: str = "sm_6_0",
        source_hash: str = "",
        compiled_hash: str = "",
        size_bytes: int = 0,
        compile_duration_ms: float = 0.0,
    ) -> ShaderVariant:
        """Register or update a compiled shader variant."""
        key = self._make_key(shader_name, defines, stage)
        vid = f"sv_{key}"
        variant = ShaderVariant(
            variant_id=vid,
            shader_name=shader_name,
            defines=list(defines),
            stage=stage,
            profile=profile,
            source_hash=source_hash,
            compiled_hash=compiled_hash,
            compile_time=time.time(),
            size_bytes=size_bytes,
            compile_duration_ms=compile_duration_ms,
        )
        self._variants[vid] = variant
        logger.debug("ShaderPermutationCache: registered %s", vid)
        return variant

    def is_cached(self, shader_name: str, defines: list[str], stage: str = "vertex") -> bool:
        """Return True if this permutation is in the cache."""
        key = self._make_key(shader_name, defines, stage)
        return f"sv_{key}" in self._variants

    def is_valid(
        self,
        shader_name: str,
        defines: list[str],
        stage: str = "vertex",
        source_hash: str = "",
    ) -> bool:
        """Return True if cached and the source hash still matches."""
        key = self._make_key(shader_name, defines, stage)
        vid = f"sv_{key}"
        if vid not in self._variants:
            return False
        return self._variants[vid].source_hash == source_hash

    def get_variant(self, variant_id: str) -> Optional[ShaderVariant]:
        return self._variants.get(variant_id)

    def get_variant_by_key(
        self, shader_name: str, defines: list[str], stage: str = "vertex"
    ) -> Optional[ShaderVariant]:
        key = self._make_key(shader_name, defines, stage)
        return self._variants.get(f"sv_{key}")

    def get_compiled_hash(self, variant_id: str) -> str:
        v = self._variants.get(variant_id)
        return v.compiled_hash if v else ""

    # ------------------------------------------------------------------
    # Invalidation
    # ------------------------------------------------------------------

    def invalidate(
        self, shader_name: str, defines: list[str], stage: str = "vertex"
    ) -> bool:
        key = self._make_key(shader_name, defines, stage)
        vid = f"sv_{key}"
        if vid not in self._variants:
            return False
        del self._variants[vid]
        logger.debug("ShaderPermutationCache: invalidated %s", vid)
        return True

    def invalidate_shader(self, shader_name: str) -> int:
        """Invalidate all variants for a given shader name."""
        to_del = [
            vid for vid, v in self._variants.items()
            if v.shader_name == shader_name
        ]
        for vid in to_del:
            del self._variants[vid]
        return len(to_del)

    def evict_stale(self, max_age_seconds: float = 3600.0) -> int:
        stale = [
            vid for vid, v in self._variants.items()
            if v.age_seconds > max_age_seconds
        ]
        for vid in stale:
            del self._variants[vid]
        return len(stale)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_all_variant_ids(self) -> list[str]:
        return list(self._variants.keys())

    def get_variants_for_shader(self, shader_name: str) -> list[ShaderVariant]:
        return [v for v in self._variants.values() if v.shader_name == shader_name]

    def get_variants_by_stage(self, stage: str) -> list[ShaderVariant]:
        return [v for v in self._variants.values() if v.stage == stage]

    def get_variant_count(self) -> int:
        return len(self._variants)

    def get_total_size_bytes(self) -> int:
        return sum(v.size_bytes for v in self._variants.values())

    def get_stale_variants(self, max_age_seconds: float = 3600.0) -> list[ShaderVariant]:
        return [v for v in self._variants.values() if v.age_seconds > max_age_seconds]

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str = "") -> bool:
        target = path or self._cache_path
        if not target:
            logger.warning("ShaderPermutationCache.save: no path specified")
            return False
        try:
            data: dict = {"variants": {}}
            for vid, v in self._variants.items():
                data["variants"][vid] = {
                    "variant_id": v.variant_id,
                    "shader_name": v.shader_name,
                    "defines": v.defines,
                    "stage": v.stage,
                    "profile": v.profile,
                    "source_hash": v.source_hash,
                    "compiled_hash": v.compiled_hash,
                    "compile_time": v.compile_time,
                    "size_bytes": v.size_bytes,
                    "compile_duration_ms": v.compile_duration_ms,
                }
            Path(target).write_text(
                json.dumps(data, indent=2), encoding="utf-8"
            )
            return True
        except Exception as exc:
            logger.error("ShaderPermutationCache.save error: %s", exc)
            return False

    def load(self, path: str = "") -> bool:
        target = path or self._cache_path
        if not target or not Path(target).exists():
            return False
        try:
            data = json.loads(Path(target).read_text(encoding="utf-8"))
            self._variants.clear()
            for vid, rec in data.get("variants", {}).items():
                v = ShaderVariant(
                    variant_id=rec["variant_id"],
                    shader_name=rec["shader_name"],
                    defines=rec.get("defines", []),
                    stage=rec.get("stage", "vertex"),
                    profile=rec.get("profile", "sm_6_0"),
                    source_hash=rec.get("source_hash", ""),
                    compiled_hash=rec.get("compiled_hash", ""),
                    compile_time=rec.get("compile_time", 0.0),
                    size_bytes=rec.get("size_bytes", 0),
                    compile_duration_ms=rec.get("compile_duration_ms", 0.0),
                )
                self._variants[vid] = v
            return True
        except Exception as exc:
            logger.error("ShaderPermutationCache.load error: %s", exc)
            return False

    def clear(self) -> None:
        self._variants.clear()
