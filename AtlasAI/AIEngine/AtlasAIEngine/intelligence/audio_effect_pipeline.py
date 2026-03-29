"""AtlasAI Phase 27B — Audio Effect Pipeline.

Processes, transforms, and exports sound effect assets through a configurable
chain of DSP stages including EQ, compression, reverb, and normalization for
use in the game audio runtime.
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
class EQBand:
    """A single parametric EQ band."""

    band_id: str
    frequency_hz: float = 1000.0
    gain_db: float = 0.0
    q_factor: float = 1.0
    band_type: str = "Peak"      # Peak, LowShelf, HighShelf, LowCut, HighCut
    enabled: bool = True

    @property
    def is_boost(self) -> bool:
        return self.gain_db > 0.0

    @property
    def is_cut(self) -> bool:
        return self.gain_db < 0.0


@dataclass
class CompressorSettings:
    """Dynamic range compression parameters."""

    threshold_db: float = -12.0
    ratio: float = 4.0
    attack_ms: float = 5.0
    release_ms: float = 50.0
    knee_db: float = 3.0
    makeup_gain_db: float = 0.0
    enabled: bool = True

    @property
    def is_limiting(self) -> bool:
        return self.ratio >= 20.0


@dataclass
class ReverbSettings:
    """Convolution / algorithmic reverb parameters."""

    room_size: float = 0.5
    damping: float = 0.5
    wet_level: float = 0.2
    dry_level: float = 0.8
    pre_delay_ms: float = 10.0
    diffusion: float = 0.7
    algorithm: str = "Algorithmic"   # Algorithmic, Convolution
    ir_path: str = ""
    enabled: bool = True


@dataclass
class NormalisationSettings:
    """Loudness / peak normalisation target."""

    target_db: float = -6.0
    mode: str = "Peak"     # Peak, RMS, LUFS
    enabled: bool = True


@dataclass
class AudioEffectJob:
    """A single audio file to process through the pipeline."""

    job_id: str
    input_path: str
    output_path: str = ""
    sample_rate: int = 44100
    bit_depth: int = 16
    channels: int = 1
    trim_silence: bool = False
    trim_threshold_db: float = -60.0
    fade_in_ms: float = 0.0
    fade_out_ms: float = 0.0
    reverse: bool = False
    pitch_shift_semitones: float = 0.0

    @property
    def is_stereo(self) -> bool:
        return self.channels == 2

    @property
    def has_pitch_shift(self) -> bool:
        return abs(self.pitch_shift_semitones) > 0.001


@dataclass
class AudioProcessResult:
    """Result of processing a single audio effect job."""

    job_id: str
    success: bool = False
    input_path: str = ""
    output_path: str = ""
    duration_ms: float = 0.0
    peak_db: float = 0.0
    rms_db: float = 0.0
    sample_rate: int = 44100
    channels: int = 1
    error_message: str = ""
    processing_time_ms: float = 0.0
    warnings: list[str] = field(default_factory=list)

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def output_size_kb(self) -> float:
        return (self.duration_ms / 1000.0 * self.sample_rate *
                self.channels * 2) / 1024.0


class AudioEffectPipeline:
    """DSP pipeline for batch audio effect processing."""

    def __init__(self) -> None:
        self._jobs: dict[str, AudioEffectJob] = {}
        self._results: dict[str, AudioProcessResult] = {}
        self._eq_bands: dict[str, list[EQBand]] = {}         # job_id -> bands
        self._compressors: dict[str, CompressorSettings] = {}
        self._reverbs: dict[str, ReverbSettings] = {}
        self._normalisation: dict[str, NormalisationSettings] = {}
        self._next_job: int = 0
        self._next_band: int = 0
        self._next_lfo: int = 0

    # ------------------------------------------------------------------
    # Job management
    # ------------------------------------------------------------------

    def add_job(
        self,
        input_path: str,
        output_path: str = "",
        sample_rate: int = 44100,
        channels: int = 1,
    ) -> AudioEffectJob:
        job_id = f"job_{self._next_job:04d}"
        self._next_job += 1
        job = AudioEffectJob(
            job_id=job_id,
            input_path=input_path,
            output_path=output_path or input_path,
            sample_rate=sample_rate,
            channels=channels,
        )
        self._jobs[job_id] = job
        logger.debug("Added audio job %s: %s", job_id, input_path)
        return job

    def remove_job(self, job_id: str) -> bool:
        if job_id not in self._jobs:
            return False
        del self._jobs[job_id]
        self._results.pop(job_id, None)
        self._eq_bands.pop(job_id, None)
        self._compressors.pop(job_id, None)
        self._reverbs.pop(job_id, None)
        self._normalisation.pop(job_id, None)
        return True

    def get_job(self, job_id: str) -> Optional[AudioEffectJob]:
        return self._jobs.get(job_id)

    def get_job_count(self) -> int:
        return len(self._jobs)

    def get_all_job_ids(self) -> list[str]:
        return list(self._jobs.keys())

    # ------------------------------------------------------------------
    # DSP settings per job
    # ------------------------------------------------------------------

    def add_eq_band(
        self,
        job_id: str,
        frequency_hz: float = 1000.0,
        gain_db: float = 0.0,
        q_factor: float = 1.0,
        band_type: str = "Peak",
    ) -> Optional[EQBand]:
        if job_id not in self._jobs:
            return None
        band_id = f"band_{self._next_band:04d}"
        self._next_band += 1
        band = EQBand(
            band_id=band_id,
            frequency_hz=frequency_hz,
            gain_db=gain_db,
            q_factor=q_factor,
            band_type=band_type,
        )
        self._eq_bands.setdefault(job_id, []).append(band)
        return band

    def get_eq_bands(self, job_id: str) -> list[EQBand]:
        return list(self._eq_bands.get(job_id, []))

    def get_eq_band_count(self, job_id: str) -> int:
        return len(self._eq_bands.get(job_id, []))

    def remove_eq_band(self, job_id: str, band_id: str) -> bool:
        bands = self._eq_bands.get(job_id)
        if bands is None:
            return False
        before = len(bands)
        self._eq_bands[job_id] = [b for b in bands if b.band_id != band_id]
        return len(self._eq_bands[job_id]) < before

    def set_compressor(
        self,
        job_id: str,
        threshold_db: float = -12.0,
        ratio: float = 4.0,
        attack_ms: float = 5.0,
        release_ms: float = 50.0,
    ) -> Optional[CompressorSettings]:
        if job_id not in self._jobs:
            return None
        comp = CompressorSettings(
            threshold_db=threshold_db,
            ratio=ratio,
            attack_ms=attack_ms,
            release_ms=release_ms,
        )
        self._compressors[job_id] = comp
        return comp

    def get_compressor(self, job_id: str) -> Optional[CompressorSettings]:
        return self._compressors.get(job_id)

    def remove_compressor(self, job_id: str) -> bool:
        if job_id not in self._compressors:
            return False
        del self._compressors[job_id]
        return True

    def set_reverb(
        self,
        job_id: str,
        room_size: float = 0.5,
        wet_level: float = 0.2,
        algorithm: str = "Algorithmic",
    ) -> Optional[ReverbSettings]:
        if job_id not in self._jobs:
            return None
        reverb = ReverbSettings(
            room_size=room_size,
            wet_level=wet_level,
            dry_level=1.0 - wet_level,
            algorithm=algorithm,
        )
        self._reverbs[job_id] = reverb
        return reverb

    def get_reverb(self, job_id: str) -> Optional[ReverbSettings]:
        return self._reverbs.get(job_id)

    def remove_reverb(self, job_id: str) -> bool:
        if job_id not in self._reverbs:
            return False
        del self._reverbs[job_id]
        return True

    def set_normalisation(
        self,
        job_id: str,
        target_db: float = -6.0,
        mode: str = "Peak",
    ) -> Optional[NormalisationSettings]:
        if job_id not in self._jobs:
            return None
        norm = NormalisationSettings(target_db=target_db, mode=mode)
        self._normalisation[job_id] = norm
        return norm

    def get_normalisation(self, job_id: str) -> Optional[NormalisationSettings]:
        return self._normalisation.get(job_id)

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    def process_job(self, job_id: str) -> AudioProcessResult:
        start = time.time()
        job = self._jobs.get(job_id)
        if job is None:
            return AudioProcessResult(
                job_id=job_id,
                success=False,
                error_message=f"Job {job_id} not found",
            )

        result = AudioProcessResult(
            job_id=job_id,
            input_path=job.input_path,
            output_path=job.output_path,
            sample_rate=job.sample_rate,
            channels=job.channels,
            duration_ms=500.0,    # simulated duration
            peak_db=-3.0,
            rms_db=-12.0,
        )

        # Apply simulated DSP chain
        comp = self._compressors.get(job_id)
        if comp and comp.enabled:
            result.peak_db += comp.makeup_gain_db

        norm = self._normalisation.get(job_id)
        if norm and norm.enabled:
            result.peak_db = norm.target_db
            result.warnings.append(
                f"Normalised to {norm.target_db} dB ({norm.mode})"
            ) if norm.mode == "LUFS" else None

        eq_bands = self._eq_bands.get(job_id, [])
        if len(eq_bands) > 8:
            result.warnings.append("More than 8 EQ bands may impact performance")

        result.success = True
        result.processing_time_ms = (time.time() - start) * 1000
        self._results[job_id] = result
        return result

    def process_all(self) -> list[AudioProcessResult]:
        return [self.process_job(jid) for jid in self._jobs]

    def get_result(self, job_id: str) -> Optional[AudioProcessResult]:
        return self._results.get(job_id)

    def get_processed_count(self) -> int:
        return len(self._results)

    def get_success_count(self) -> int:
        return sum(1 for r in self._results.values() if r.success)

    def get_failure_count(self) -> int:
        return sum(1 for r in self._results.values() if not r.success)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_manifest(self, output_path: str) -> bool:
        data = {
            "job_count": self.get_job_count(),
            "processed_count": self.get_processed_count(),
            "success_count": self.get_success_count(),
            "jobs": [
                {
                    "job_id": j.job_id,
                    "input_path": j.input_path,
                    "output_path": j.output_path,
                    "sample_rate": j.sample_rate,
                    "channels": j.channels,
                    "eq_band_count": self.get_eq_band_count(j.job_id),
                    "has_compressor": j.job_id in self._compressors,
                    "has_reverb": j.job_id in self._reverbs,
                    "has_normalisation": j.job_id in self._normalisation,
                }
                for j in self._jobs.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save manifest: %s", exc)
            return False

    def clear(self) -> None:
        self._jobs.clear()
        self._results.clear()
        self._eq_bands.clear()
        self._compressors.clear()
        self._reverbs.clear()
        self._normalisation.clear()
        self._next_job = 0
        self._next_band = 0
