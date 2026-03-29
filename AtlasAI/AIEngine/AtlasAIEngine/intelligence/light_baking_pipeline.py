"""AtlasAI Phase 28B — Light Baking Pipeline.

Submits and processes lightmap bake jobs and light probe clusters, tracking
results and statistics for integration with the Atlas engine bake toolchain.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class BakeJob:
    """A single lightmap bake job submitted to the pipeline."""

    job_id: str
    mesh_name: str
    resolution: int = 512
    bounce_count: int = 3
    quality_preset: str = "Medium"   # Preview, Low, Medium, High, Ultra
    cancelled: bool = False
    completed: bool = False

    @property
    def is_pending(self) -> bool:
        return not self.completed and not self.cancelled

    @property
    def is_high_quality(self) -> bool:
        return self.quality_preset in ("High", "Ultra")


@dataclass
class ProbeCluster:
    """A cluster of light probes defined by world-space position and count."""

    cluster_id: str
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    probe_count: int = 8
    spacing: float = 2.0
    resolution: int = 32

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.position_x, self.position_y, self.position_z)

    @property
    def total_texels(self) -> int:
        return self.probe_count * self.resolution * self.resolution * 6


@dataclass
class BakeResult:
    """Result of a completed bake job."""

    job_id: str
    mesh_name: str
    elapsed_seconds: float = 0.0
    lightmap_path: str = ""
    success: bool = False
    error_message: str = ""
    texel_count: int = 0
    peak_memory_mb: float = 0.0
    warnings: list[str] = field(default_factory=list)

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def lightmap_size_kb(self) -> float:
        return self.texel_count * 4 / 1024.0


class LightBakingPipeline:
    """Submits and processes lightmap bake jobs and probe clusters."""

    def __init__(self) -> None:
        self._jobs: dict[str, BakeJob] = {}
        self._probe_clusters: dict[str, ProbeCluster] = {}
        self._results: dict[str, BakeResult] = {}
        self._next_job: int = 0
        self._next_cluster: int = 0
        self._total_bake_time: float = 0.0

    # ------------------------------------------------------------------
    # Job management
    # ------------------------------------------------------------------

    def submit_job(
        self,
        mesh_name: str,
        resolution: int = 512,
        bounce_count: int = 3,
        quality_preset: str = "Medium",
    ) -> BakeJob:
        job_id = f"job_{self._next_job:04d}"
        self._next_job += 1
        job = BakeJob(
            job_id=job_id,
            mesh_name=mesh_name,
            resolution=resolution,
            bounce_count=bounce_count,
            quality_preset=quality_preset,
        )
        self._jobs[job_id] = job
        logger.debug("Submitted bake job %s for mesh %s", job_id, mesh_name)
        return job

    def cancel_job(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job is None or job.completed:
            return False
        job.cancelled = True
        return True

    def get_job(self, job_id: str) -> Optional[BakeJob]:
        return self._jobs.get(job_id)

    def list_jobs(self) -> list[str]:
        return list(self._jobs.keys())

    # ------------------------------------------------------------------
    # Probe cluster management
    # ------------------------------------------------------------------

    def submit_probe_cluster(
        self,
        position_x: float = 0.0,
        position_y: float = 0.0,
        position_z: float = 0.0,
        probe_count: int = 8,
        spacing: float = 2.0,
        resolution: int = 32,
    ) -> ProbeCluster:
        cluster_id = f"cluster_{self._next_cluster:04d}"
        self._next_cluster += 1
        cluster = ProbeCluster(
            cluster_id=cluster_id,
            position_x=position_x,
            position_y=position_y,
            position_z=position_z,
            probe_count=probe_count,
            spacing=spacing,
            resolution=resolution,
        )
        self._probe_clusters[cluster_id] = cluster
        logger.debug("Submitted probe cluster %s with %d probes", cluster_id, probe_count)
        return cluster

    def get_cluster(self, cluster_id: str) -> Optional[ProbeCluster]:
        return self._probe_clusters.get(cluster_id)

    def list_clusters(self) -> list[str]:
        return list(self._probe_clusters.keys())

    def remove_cluster(self, cluster_id: str) -> bool:
        if cluster_id not in self._probe_clusters:
            return False
        del self._probe_clusters[cluster_id]
        return True

    # ------------------------------------------------------------------
    # Baking
    # ------------------------------------------------------------------

    def _bake_single(self, job: BakeJob) -> BakeResult:
        """Simulate baking a single job."""
        start = time.time()
        if job.cancelled:
            return BakeResult(
                job_id=job.job_id,
                mesh_name=job.mesh_name,
                success=False,
                error_message="Job was cancelled",
            )
        texel_count = job.resolution * job.resolution
        lightmap_path = f"LightMaps/{job.mesh_name}_{job.resolution}.exr"
        elapsed = time.time() - start
        job.completed = True
        return BakeResult(
            job_id=job.job_id,
            mesh_name=job.mesh_name,
            elapsed_seconds=elapsed,
            lightmap_path=lightmap_path,
            success=True,
            texel_count=texel_count,
            peak_memory_mb=texel_count * 4 / (1024 * 1024),
        )

    def bake_all(self) -> list[BakeResult]:
        """Process all pending bake jobs and return results."""
        results: list[BakeResult] = []
        for job in self._jobs.values():
            if job.is_pending:
                result = self._bake_single(job)
                self._results[job.job_id] = result
                self._total_bake_time += result.elapsed_seconds
                results.append(result)
        return results

    def get_result(self, job_id: str) -> Optional[BakeResult]:
        return self._results.get(job_id)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def pending_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.is_pending)

    @property
    def completed_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.completed)

    @property
    def total_bake_time(self) -> float:
        return self._total_bake_time

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        return {
            "total_jobs": len(self._jobs),
            "pending": self.pending_count,
            "completed": self.completed_count,
            "cancelled": sum(1 for j in self._jobs.values() if j.cancelled),
            "probe_clusters": len(self._probe_clusters),
            "total_bake_time_s": self._total_bake_time,
            "success_count": sum(1 for r in self._results.values() if r.success),
            "failure_count": sum(1 for r in self._results.values() if not r.success),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_manifest(self, output_path: str) -> bool:
        data = {
            "stats": self.get_stats(),
            "jobs": [
                {
                    "job_id": j.job_id,
                    "mesh_name": j.mesh_name,
                    "resolution": j.resolution,
                    "bounce_count": j.bounce_count,
                    "quality_preset": j.quality_preset,
                    "completed": j.completed,
                    "cancelled": j.cancelled,
                }
                for j in self._jobs.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save bake manifest: %s", exc)
            return False

    def clear(self) -> None:
        self._jobs.clear()
        self._probe_clusters.clear()
        self._results.clear()
        self._next_job = 0
        self._next_cluster = 0
        self._total_bake_time = 0.0
