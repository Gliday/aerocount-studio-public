"""
occ/survey.py
Stratified OCC survey-design maths. Given per-stratum area and transect spacing,
plus the aircraft/camera-derived strip width and frame cadence, estimate transect
line length, image volume and sampling fraction. Two-sided (left+right camera)
by default for OCC, matching the twin-camera setups in Lamprey et al. 2020.
"""
from __future__ import annotations


def stratum_metrics(area_km2: float, spacing_m: float, strip_m: float,
                    speed_ms: float, interval_s: float, cameras: int = 2) -> dict:
    if spacing_m <= 0:
        return {"line_km": 0.0, "images": 0, "sampling_pct": 0.0}
    line_km = area_km2 / (spacing_m / 1000.0)
    advance = max(speed_ms * interval_s, 1e-6)          # metres between frames
    images = int(cameras * line_km * 1000.0 / advance)
    sampling = cameras * strip_m / spacing_m * 100.0    # both sides of aircraft
    return {"line_km": line_km, "images": images, "sampling_pct": sampling}


def survey_totals(strata: list[dict], strip_m: float, speed_ms: float,
                  interval_s: float, cameras: int = 2):
    rows, area, line, imgs = [], 0.0, 0.0, 0
    for s in strata:
        m = stratum_metrics(s.get("area_km2", 0), s.get("spacing_m", 0),
                            strip_m, speed_ms, interval_s, cameras)
        rows.append({**s, **m})
        area += s.get("area_km2", 0)
        line += m["line_km"]
        imgs += m["images"]
    return rows, {"area_km2": area, "line_km": line, "images": imgs}


def resolving_power(gsd_cm: float):
    """Classify what the ground-sampling-distance can resolve (per Lamprey 2020,
    who require < 6 cm to resolve oribi/small antelope)."""
    if gsd_cm <= 6:
        return "Resolves small antelope (oribi, gazelle)", "exc"
    if gsd_cm <= 15:
        return "Medium–large ungulates only", "good"
    return "Large species only", "marg"
