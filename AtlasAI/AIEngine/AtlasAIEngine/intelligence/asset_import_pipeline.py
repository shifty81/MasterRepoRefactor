"""AtlasAI Phase 23B — Asset Import Pipeline.

Manages the staged import of raw source assets (FBX, PNG, WAV, etc.) into
engine-ready formats.  Tracks import jobs, per-asset settings, and results
so that the AI engine can monitor, retry, or batch-process content ingestion.
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ImportSettings:
    """Per-asset import settings."""

    generate_mipmaps: bool = True
    compress_textures: bool = True
    recalculate_normals: bool = False
    import_animations: bool = True
    import_materials: bool = True
    normalize_scale: float = 1.0
    lod_levels: int = 3
    collision_type: str = "none"     # none | simple | complex
    custom: dict = field(default_factory=dict)


@dataclass
class ImportJob:
    """Represents a single asset import task."""

    job_id: str
    source_path: str
    destination_path: str
    asset_type: str                   # Mesh | Texture | Audio | Animation | Material
    status: str = "pending"           # pending | running | completed | failed | cancelled
    settings: ImportSettings = field(default_factory=ImportSettings)
    error_message: str = ""
    warnings: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    started_at: float = 0.0
    completed_at: float = 0.0
    output_paths: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def is_done(self) -> bool:
        return self.status in ("completed", "failed", "cancelled")

    @property
    def duration_seconds(self) -> float:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return 0.0


class AssetImportPipeline:
    """Manages a queue of asset import jobs.

    Typical usage::

        pipeline = AssetImportPipeline()
        job = pipeline.submit("/raw/hero.fbx", "/content/hero", "Mesh")
        pipeline.start_job(job.job_id)
        pipeline.complete_job(job.job_id, ["/content/hero.mesh"])
        results = pipeline.get_completed_jobs()
    """

    def __init__(self, pipeline_path: str = "") -> None:
        self._pipeline_path = pipeline_path
        self._jobs: dict[str, ImportJob] = {}

    # ------------------------------------------------------------------
    # Job submission
    # ------------------------------------------------------------------

    def submit(
        self,
        source_path: str,
        destination_path: str,
        asset_type: str,
        settings: Optional[ImportSettings] = None,
        tags: Optional[list[str]] = None,
    ) -> ImportJob:
        """Create and enqueue a new import job."""
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        job = ImportJob(
            job_id=job_id,
            source_path=source_path,
            destination_path=destination_path,
            asset_type=asset_type,
            settings=settings or ImportSettings(),
            tags=tags or [],
        )
        self._jobs[job_id] = job
        logger.debug("AssetImportPipeline: submitted %s (%s)", job_id, asset_type)
        return job

    def cancel_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.is_done:
            return False
        job.status = "cancelled"
        return True

    # ------------------------------------------------------------------
    # Job lifecycle
    # ------------------------------------------------------------------

    def start_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.status != "pending":
            return False
        job.status = "running"
        job.started_at = time.time()
        return True

    def complete_job(
        self, job_id: str, output_paths: Optional[list[str]] = None
    ) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.status != "running":
            return False
        job.status = "completed"
        job.completed_at = time.time()
        job.output_paths = output_paths or []
        return True

    def fail_job(self, job_id: str, error_message: str = "") -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.status != "running":
            return False
        job.status = "failed"
        job.completed_at = time.time()
        job.error_message = error_message
        return True

    def add_warning(self, job_id: str, warning: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None:
            return False
        job.warnings.append(warning)
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_job(self, job_id: str) -> Optional[ImportJob]:
        return self._jobs.get(job_id)

    def get_all_jobs(self) -> list[ImportJob]:
        return list(self._jobs.values())

    def get_pending_jobs(self) -> list[ImportJob]:
        return [j for j in self._jobs.values() if j.status == "pending"]

    def get_running_jobs(self) -> list[ImportJob]:
        return [j for j in self._jobs.values() if j.status == "running"]

    def get_completed_jobs(self) -> list[ImportJob]:
        return [j for j in self._jobs.values() if j.status == "completed"]

    def get_failed_jobs(self) -> list[ImportJob]:
        return [j for j in self._jobs.values() if j.status == "failed"]

    def get_jobs_by_type(self, asset_type: str) -> list[ImportJob]:
        return [j for j in self._jobs.values() if j.asset_type == asset_type]

    def get_jobs_by_tag(self, tag: str) -> list[ImportJob]:
        return [j for j in self._jobs.values() if tag in j.tags]

    def get_job_count(self) -> int:
        return len(self._jobs)

    def get_pending_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.status == "pending")

    def get_completed_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.status == "completed")

    def get_failed_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.status == "failed")

    def retry_failed_jobs(self) -> int:
        """Reset all failed jobs back to pending for retry."""
        count = 0
        for job in self._jobs.values():
            if job.status == "failed":
                job.status = "pending"
                job.error_message = ""
                job.started_at = 0.0
                job.completed_at = 0.0
                count += 1
        return count

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str = "") -> bool:
        target = path or self._pipeline_path
        if not target:
            logger.warning("AssetImportPipeline.save: no path specified")
            return False
        try:
            records = []
            for job in self._jobs.values():
                records.append({
                    "job_id": job.job_id,
                    "source_path": job.source_path,
                    "destination_path": job.destination_path,
                    "asset_type": job.asset_type,
                    "status": job.status,
                    "error_message": job.error_message,
                    "warnings": job.warnings,
                    "created_at": job.created_at,
                    "started_at": job.started_at,
                    "completed_at": job.completed_at,
                    "output_paths": job.output_paths,
                    "tags": job.tags,
                    "settings": {
                        "generate_mipmaps": job.settings.generate_mipmaps,
                        "compress_textures": job.settings.compress_textures,
                        "recalculate_normals": job.settings.recalculate_normals,
                        "import_animations": job.settings.import_animations,
                        "import_materials": job.settings.import_materials,
                        "normalize_scale": job.settings.normalize_scale,
                        "lod_levels": job.settings.lod_levels,
                        "collision_type": job.settings.collision_type,
                        "custom": job.settings.custom,
                    },
                })
            Path(target).write_text(
                json.dumps({"jobs": records}, indent=2), encoding="utf-8"
            )
            return True
        except Exception as exc:
            logger.error("AssetImportPipeline.save error: %s", exc)
            return False

    def load(self, path: str = "") -> bool:
        target = path or self._pipeline_path
        if not target or not Path(target).exists():
            return False
        try:
            data = json.loads(Path(target).read_text(encoding="utf-8"))
            self._jobs.clear()
            for rec in data.get("jobs", []):
                s = rec.get("settings", {})
                settings = ImportSettings(
                    generate_mipmaps=s.get("generate_mipmaps", True),
                    compress_textures=s.get("compress_textures", True),
                    recalculate_normals=s.get("recalculate_normals", False),
                    import_animations=s.get("import_animations", True),
                    import_materials=s.get("import_materials", True),
                    normalize_scale=s.get("normalize_scale", 1.0),
                    lod_levels=s.get("lod_levels", 3),
                    collision_type=s.get("collision_type", "none"),
                    custom=s.get("custom", {}),
                )
                job = ImportJob(
                    job_id=rec["job_id"],
                    source_path=rec["source_path"],
                    destination_path=rec["destination_path"],
                    asset_type=rec["asset_type"],
                    status=rec.get("status", "pending"),
                    settings=settings,
                    error_message=rec.get("error_message", ""),
                    warnings=rec.get("warnings", []),
                    created_at=rec.get("created_at", 0.0),
                    started_at=rec.get("started_at", 0.0),
                    completed_at=rec.get("completed_at", 0.0),
                    output_paths=rec.get("output_paths", []),
                    tags=rec.get("tags", []),
                )
                self._jobs[job.job_id] = job
            return True
        except Exception as exc:
            logger.error("AssetImportPipeline.load error: %s", exc)
            return False

    def clear(self) -> None:
        self._jobs.clear()
