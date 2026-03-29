"""AtlasAI Phase 24B — Texture Atlas Packer.

Bins individual textures into power-of-two atlas sheets, tracks UV mappings
per region, and integrates with the asset import pipeline for batch workflows.
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AtlasRegion:
    """UV region for a single packed texture within a sheet."""

    region_id: str
    source_path: str
    sheet_id: str
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    rotated: bool = False
    padding: int = 1

    @property
    def uv_x(self) -> float:
        """Normalised UV left edge (0..1)."""
        return self.x / max(1, self._sheet_width)

    @property
    def uv_y(self) -> float:
        """Normalised UV top edge (0..1)."""
        return self.y / max(1, self._sheet_height)

    @property
    def uv_width(self) -> float:
        return self.width / max(1, self._sheet_width)

    @property
    def uv_height(self) -> float:
        return self.height / max(1, self._sheet_height)

    # Internal; set by AtlasSheet after assignment
    _sheet_width: int = field(default=1, repr=False)
    _sheet_height: int = field(default=1, repr=False)


@dataclass
class AtlasSheet:
    """A single output atlas texture sheet."""

    sheet_id: str
    name: str
    width: int = 2048
    height: int = 2048
    max_size: int = 4096
    regions: list[AtlasRegion] = field(default_factory=list)
    output_path: str = ""
    padding: int = 1

    @property
    def region_count(self) -> int:
        return len(self.regions)

    @property
    def fill_ratio(self) -> float:
        used = sum(r.width * r.height for r in self.regions)
        total = max(1, self.width * self.height)
        return used / total

    def find_region(self, region_id: str) -> Optional[AtlasRegion]:
        for r in self.regions:
            if r.region_id == region_id:
                return r
        return None


class TextureAtlasPacker:
    """Pack individual textures into power-of-two atlas sheets.

    Typical usage::

        packer = TextureAtlasPacker()
        sheet = packer.create_sheet("ui_atlas", 2048, 2048)
        region = packer.pack_texture(sheet.sheet_id, "/textures/icon_a.png", 64, 64)
        packer.save("/out/ui_atlas.json")
    """

    def __init__(self) -> None:
        self._sheets: dict[str, AtlasSheet] = {}
        self._regions: dict[str, AtlasRegion] = {}
        self._next_sheet = 0
        self._next_region = 0

    # ------------------------------------------------------------------
    # Sheet management
    # ------------------------------------------------------------------

    def create_sheet(
        self,
        name: str,
        width: int = 2048,
        height: int = 2048,
        max_size: int = 4096,
        padding: int = 1,
    ) -> AtlasSheet:
        sid = f"sheet_{self._next_sheet:04d}"
        self._next_sheet += 1
        sheet = AtlasSheet(
            sheet_id=sid,
            name=name,
            width=width,
            height=height,
            max_size=max_size,
            padding=padding,
        )
        self._sheets[sid] = sheet
        logger.debug("TextureAtlasPacker: created sheet %s (%dx%d)", sid, width, height)
        return sheet

    def remove_sheet(self, sheet_id: str) -> bool:
        if sheet_id not in self._sheets:
            return False
        for r in self._sheets[sheet_id].regions:
            self._regions.pop(r.region_id, None)
        del self._sheets[sheet_id]
        return True

    def get_sheet(self, sheet_id: str) -> Optional[AtlasSheet]:
        return self._sheets.get(sheet_id)

    def get_sheet_by_name(self, name: str) -> Optional[AtlasSheet]:
        for s in self._sheets.values():
            if s.name == name:
                return s
        return None

    def get_sheet_count(self) -> int:
        return len(self._sheets)

    def get_all_sheet_ids(self) -> list[str]:
        return list(self._sheets.keys())

    # ------------------------------------------------------------------
    # Packing
    # ------------------------------------------------------------------

    @staticmethod
    def _next_power_of_two(n: int) -> int:
        if n <= 0:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def pack_texture(
        self,
        sheet_id: str,
        source_path: str,
        tex_width: int,
        tex_height: int,
        padding: int = -1,
    ) -> Optional[AtlasRegion]:
        """Place a texture in the sheet using a simple shelf-first fit."""
        sheet = self._sheets.get(sheet_id)
        if sheet is None:
            logger.warning("TextureAtlasPacker.pack_texture: sheet %s not found", sheet_id)
            return None

        pad = padding if padding >= 0 else sheet.padding
        rw = tex_width + 2 * pad
        rh = tex_height + 2 * pad

        # Find free position (naive shelf algorithm)
        pos = self._find_free_position(sheet, rw, rh)
        if pos is None:
            logger.warning(
                "TextureAtlasPacker.pack_texture: no room for %dx%d in %s",
                tex_width,
                tex_height,
                sheet_id,
            )
            return None

        rid = f"region_{self._next_region:06d}"
        self._next_region += 1
        region = AtlasRegion(
            region_id=rid,
            source_path=source_path,
            sheet_id=sheet_id,
            x=pos[0] + pad,
            y=pos[1] + pad,
            width=tex_width,
            height=tex_height,
            padding=pad,
            _sheet_width=sheet.width,
            _sheet_height=sheet.height,
        )
        sheet.regions.append(region)
        self._regions[rid] = region
        return region

    def _find_free_position(
        self, sheet: AtlasSheet, rw: int, rh: int
    ) -> Optional[tuple[int, int]]:
        """Simple shelf bin-packing (top-left placement, row-by-row)."""
        occupied = [(r.x - r.padding, r.y - r.padding,
                     r.width + 2 * r.padding, r.height + 2 * r.padding)
                    for r in sheet.regions]
        x, y, row_h = 0, 0, 0
        for ox, oy, ow, oh in occupied:
            far_x = ox + ow
            far_y = oy + oh
            if far_x > x:
                x = far_x
                row_h = max(row_h, oh)
            if x + rw > sheet.width:
                x = 0
                y += row_h
                row_h = 0
        if x + rw > sheet.width:
            x = 0
            y += row_h
        if y + rh > sheet.height:
            return None
        return (x, y)

    def remove_region(self, region_id: str) -> bool:
        region = self._regions.get(region_id)
        if region is None:
            return False
        sheet = self._sheets.get(region.sheet_id)
        if sheet:
            sheet.regions = [r for r in sheet.regions if r.region_id != region_id]
        del self._regions[region_id]
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_region(self, region_id: str) -> Optional[AtlasRegion]:
        return self._regions.get(region_id)

    def find_region_by_source(self, source_path: str) -> Optional[AtlasRegion]:
        for r in self._regions.values():
            if r.source_path == source_path:
                return r
        return None

    def get_region_count(self) -> int:
        return len(self._regions)

    def get_total_fill_ratio(self) -> float:
        if not self._sheets:
            return 0.0
        return sum(s.fill_ratio for s in self._sheets.values()) / len(self._sheets)

    # ------------------------------------------------------------------
    # Resize / grow
    # ------------------------------------------------------------------

    def resize_sheet(self, sheet_id: str, new_width: int, new_height: int) -> bool:
        sheet = self._sheets.get(sheet_id)
        if sheet is None:
            return False
        if new_width > sheet.max_size or new_height > sheet.max_size:
            return False
        sheet.width = new_width
        sheet.height = new_height
        for r in sheet.regions:
            r._sheet_width = new_width
            r._sheet_height = new_height
        return True

    def grow_sheet(self, sheet_id: str) -> bool:
        """Double the sheet size up to max_size."""
        sheet = self._sheets.get(sheet_id)
        if sheet is None:
            return False
        new_w = min(sheet.width * 2, sheet.max_size)
        new_h = min(sheet.height * 2, sheet.max_size)
        if new_w == sheet.width and new_h == sheet.height:
            return False
        return self.resize_sheet(sheet_id, new_w, new_h)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> bool:
        try:
            out: dict = {"sheets": {}}
            for sid, sheet in self._sheets.items():
                out["sheets"][sid] = {
                    "sheet_id": sheet.sheet_id,
                    "name": sheet.name,
                    "width": sheet.width,
                    "height": sheet.height,
                    "max_size": sheet.max_size,
                    "padding": sheet.padding,
                    "output_path": sheet.output_path,
                    "regions": [
                        {
                            "region_id": r.region_id,
                            "source_path": r.source_path,
                            "sheet_id": r.sheet_id,
                            "x": r.x,
                            "y": r.y,
                            "width": r.width,
                            "height": r.height,
                            "rotated": r.rotated,
                            "padding": r.padding,
                        }
                        for r in sheet.regions
                    ],
                }
            Path(path).write_text(json.dumps(out, indent=2), encoding="utf-8")
            return True
        except Exception as exc:
            logger.error("TextureAtlasPacker.save error: %s", exc)
            return False

    def load(self, path: str) -> bool:
        if not Path(path).exists():
            return False
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self._sheets.clear()
            self._regions.clear()
            for sid, srec in data.get("sheets", {}).items():
                sheet = AtlasSheet(
                    sheet_id=srec["sheet_id"],
                    name=srec["name"],
                    width=srec["width"],
                    height=srec["height"],
                    max_size=srec.get("max_size", 4096),
                    padding=srec.get("padding", 1),
                    output_path=srec.get("output_path", ""),
                )
                for rrec in srec.get("regions", []):
                    r = AtlasRegion(
                        region_id=rrec["region_id"],
                        source_path=rrec["source_path"],
                        sheet_id=rrec["sheet_id"],
                        x=rrec["x"],
                        y=rrec["y"],
                        width=rrec["width"],
                        height=rrec["height"],
                        rotated=rrec.get("rotated", False),
                        padding=rrec.get("padding", 1),
                        _sheet_width=srec["width"],
                        _sheet_height=srec["height"],
                    )
                    sheet.regions.append(r)
                    self._regions[r.region_id] = r
                self._sheets[sid] = sheet
            return True
        except Exception as exc:
            logger.error("TextureAtlasPacker.load error: %s", exc)
            return False

    def clear(self) -> None:
        self._sheets.clear()
        self._regions.clear()
