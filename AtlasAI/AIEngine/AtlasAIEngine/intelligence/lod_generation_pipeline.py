"""AtlasAI Phase 24B — LOD Generation Pipeline.

Manages queued LOD mesh generation jobs, allowing the AI engine to schedule,
monitor, and validate automatic level-of-detail reductions for static meshes.
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
class LODSettings:
    """Per-LOD reduction settings."""

    target_reduction: float = 0.5     # fraction of tris to keep (0..1)
    screen_size_threshold: float = 0.1  # when this LOD activates
    weld_threshold: float = 0.0
    recalculate_normals: bool = True
    preserve_borders: bool = True
    preserve_uv_seams: bool = True
    max_deviation: float = 0.01
    simplification_mode: str = "quadric"  # quadric | edge_collapse | voxel


@dataclass
class LODResult:
    """The generated output for one LOD level."""

    lod_index: int = 0
    input_tri_count: int = 0
    output_tri_count: int = 0
    reduction_ratio: float = 0.0
    output_path: str = ""
    generation_time_ms: float = 0.0

    @property
    def actual_reduction(self) -> float:
        if self.input_tri_count == 0:
            return 0.0
        return 1.0 - (self.output_tri_count / self.input_tri_count)


@dataclass
class LODJob:
    """A single LOD generation task."""

    job_id: str
    source_mesh_path: str
    output_directory: str
    asset_name: str
    lod_count: int = 3
    status: str = "pending"           # pending | running | completed | failed | cancelled
    settings: list[LODSettings] = field(default_factory=list)
    results: list[LODResult] = field(default_factory=list)
    error_message: str = ""
    warnings: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    started_at: float = 0.0
    completed_at: float = 0.0
    tags: list[str] = field(default_factory=list)

    @property
    def is_done(self) -> bool:
        return self.status in ("completed", "failed", "cancelled")

    @property
    def duration_seconds(self) -> float:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return 0.0

    @property
    def output_paths(self) -> list[str]:
        return [r.output_path for r in self.results if r.output_path]


class LODGenerationPipeline:
    """Queue and manage LOD mesh generation jobs.

    Typical usage::

        pipeline = LODGenerationPipeline()
        job = pipeline.submit("/meshes/hero.fbx", "/out/hero", "hero_mesh", lod_count=4)
        pipeline.start_job(job.job_id)
        pipeline.complete_job(job.job_id, results=[LODResult(0, 1000, 1000), ...])
    """

    def __init__(self, pipeline_path: str = "") -> None:
        self._pipeline_path = pipeline_path
        self._jobs: dict[str, LODJob] = {}

    # ------------------------------------------------------------------
    # Job submission
    # ------------------------------------------------------------------

    def submit(
        self,
        source_mesh_path: str,
        output_directory: str,
        asset_name: str,
        lod_count: int = 3,
        settings: Optional[list[LODSettings]] = None,
        tags: Optional[list[str]] = None,
    ) -> LODJob:
        job_id = f"lod_{uuid.uuid4().hex[:12]}"
        # Build default settings if not provided
        if settings is None:
            settings = []
            for i in range(lod_count):
                reduction = min(0.9, 0.25 * (i + 1))
                threshold = max(0.01, 0.5 / (2 ** i))
                settings.append(LODSettings(
                    target_reduction=reduction,
                    screen_size_threshold=threshold,
                ))
        job = LODJob(
            job_id=job_id,
            source_mesh_path=source_mesh_path,
            output_directory=output_directory,
            asset_name=asset_name,
            lod_count=lod_count,
            settings=settings,
            tags=tags or [],
        )
        self._jobs[job_id] = job
        logger.debug("LODGenerationPipeline: submitted %s (%d LODs)", job_id, lod_count)
        return job

    def cancel_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.is_done:
            return False
        job.status = "cancelled"
        return True

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.status != "pending":
            return False
        job.status = "running"
        job.started_at = time.time()
        return True

    def complete_job(
        self,
        job_id: str,
        results: Optional[list[LODResult]] = None,
    ) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.status != "running":
            return False
        job.status = "completed"
        job.completed_at = time.time()
        job.results = results or []
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

    def get_job(self, job_id: str) -> Optional[LODJob]:
        return self._jobs.get(job_id)

    def get_all_jobs(self) -> list[LODJob]:
        return list(self._jobs.values())

    def get_pending_jobs(self) -> list[LODJob]:
        return [j for j in self._jobs.values() if j.status == "pending"]

    def get_running_jobs(self) -> list[LODJob]:
        return [j for j in self._jobs.values() if j.status == "running"]

    def get_completed_jobs(self) -> list[LODJob]:
        return [j for j in self._jobs.values() if j.status == "completed"]

    def get_failed_jobs(self) -> list[LODJob]:
        return [j for j in self._jobs.values() if j.status == "failed"]

    def get_jobs_by_tag(self, tag: str) -> list[LODJob]:
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
        count = 0
        for job in self._jobs.values():
            if job.status == "failed":
                job.status = "pending"
                job.error_message = ""
                job.started_at = 0.0
                job.completed_at = 0.0
                count += 1
        return count

    def get_average_lod_count(self) -> float:
        jobs = self.get_all_jobs()
        if not jobs:
            return 0.0
        return sum(j.lod_count for j in jobs) / len(jobs)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str = "") -> bool:
        target = path or self._pipeline_path
        if not target:
            logger.warning("LODGenerationPipeline.save: no path specified")
            return False
        try:
            records = []
            for job in self._jobs.values():
                records.append({
                    "job_id": job.job_id,
                    "source_mesh_path": job.source_mesh_path,
                    "output_directory": job.output_directory,
                    "asset_name": job.asset_name,
                    "lod_count": job.lod_count,
                    "status": job.status,
                    "error_message": job.error_message,
                    "warnings": job.warnings,
                    "created_at": job.created_at,
                    "started_at": job.started_at,
                    "completed_at": job.completed_at,
                    "tags": job.tags,
                    "settings": [
                        {
                            "target_reduction": s.target_reduction,
                            "screen_size_threshold": s.screen_size_threshold,
                            "weld_threshold": s.weld_threshold,
                            "recalculate_normals": s.recalculate_normals,
                            "preserve_borders": s.preserve_borders,
                            "preserve_uv_seams": s.preserve_uv_seams,
                            "max_deviation": s.max_deviation,
                            "simplification_mode": s.simplification_mode,
                        }
                        for s in job.settings
                    ],
                    "results": [
                        {
                            "lod_index": r.lod_index,
                            "input_tri_count": r.input_tri_count,
                            "output_tri_count": r.output_tri_count,
                            "reduction_ratio": r.reduction_ratio,
                            "output_path": r.output_path,
                            "generation_time_ms": r.generation_time_ms,
                        }
                        for r in job.results
                    ],
                })
            Path(target).write_text(
                json.dumps({"jobs": records}, indent=2), encoding="utf-8"
            )
            return True
        except Exception as exc:
            logger.error("LODGenerationPipeline.save error: %s", exc)
            return False

    def load(self, path: str = "") -> bool:
        target = path or self._pipeline_path
        if not target or not Path(target).exists():
            return False
        try:
            data = json.loads(Path(target).read_text(encoding="utf-8"))
            self._jobs.clear()
            for rec in data.get("jobs", []):
                settings = [
                    LODSettings(
                        target_reduction=s.get("target_reduction", 0.5),
                        screen_size_threshold=s.get("screen_size_threshold", 0.1),
                        weld_threshold=s.get("weld_threshold", 0.0),
                        recalculate_normals=s.get("recalculate_normals", True),
                        preserve_borders=s.get("preserve_borders", True),
                        preserve_uv_seams=s.get("preserve_uv_seams", True),
                        max_deviation=s.get("max_deviation", 0.01),
                        simplification_mode=s.get("simplification_mode", "quadric"),
                    )
                    for s in rec.get("settings", [])
                ]
                results = [
                    LODResult(
                        lod_index=r.get("lod_index", 0),
                        input_tri_count=r.get("input_tri_count", 0),
                        output_tri_count=r.get("output_tri_count", 0),
                        reduction_ratio=r.get("reduction_ratio", 0.0),
                        output_path=r.get("output_path", ""),
                        generation_time_ms=r.get("generation_time_ms", 0.0),
                    )
                    for r in rec.get("results", [])
                ]
                job = LODJob(
                    job_id=rec["job_id"],
                    source_mesh_path=rec["source_mesh_path"],
                    output_directory=rec["output_directory"],
                    asset_name=rec["asset_name"],
                    lod_count=rec.get("lod_count", 3),
                    status=rec.get("status", "pending"),
                    settings=settings,
                    results=results,
                    error_message=rec.get("error_message", ""),
                    warnings=rec.get("warnings", []),
                    created_at=rec.get("created_at", 0.0),
                    started_at=rec.get("started_at", 0.0),
                    completed_at=rec.get("completed_at", 0.0),
                    tags=rec.get("tags", []),
                )
                self._jobs[job.job_id] = job
            return True
        except Exception as exc:
            logger.error("LODGenerationPipeline.load error: %s", exc)
            return False

    def clear(self) -> None:
        self._jobs.clear()
