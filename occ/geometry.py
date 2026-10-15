from __future__ import annotations
import math
from dataclasses import dataclass, asdict

def gsd_nadir_cm(sensor_w_mm, hagl_m, focal_mm, image_w_px):
    return 100.0 * sensor_w_mm * hagl_m / (focal_mm * image_w_px)

def footprint_width_m(hagl_m, sensor_w_mm, focal_mm):
    return hagl_m * sensor_w_mm / focal_mm

def along_track_per_frame_m(hagl_m, sensor_h_mm, focal_mm):
    return hagl_m * sensor_h_mm / focal_mm

def field_of_view_deg(sensor_dim_mm, focal_mm):
    return math.degrees(2.0 * math.atan(sensor_dim_mm / (2.0 * focal_mm)))

@dataclass
class ObliqueResult:
    fov_deg: float; near_range_m: float; far_range_m: float; strip_width_m: float
    gsd_near_cm: float; gsd_far_cm: float; valid: bool
    def as_dict(self): return asdict(self)

def oblique_geometry(hagl_m, focal_mm, sensor_h_mm, sensor_w_mm, image_w_px, depression_deg):
    phi = field_of_view_deg(sensor_h_mm, focal_mm); half = phi/2.0
    near_ang = depression_deg + half; far_ang = depression_deg - half
    if far_ang <= 0.5:
        return ObliqueResult(phi, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), False)
    near = hagl_m/math.tan(math.radians(near_ang)); far = hagl_m/math.tan(math.radians(far_ang))
    slant_near = hagl_m/math.sin(math.radians(near_ang)); slant_far = hagl_m/math.sin(math.radians(far_ang))
    gsd_near = 100.0*sensor_w_mm*slant_near/(focal_mm*image_w_px)
    gsd_far = 100.0*sensor_w_mm*slant_far/(focal_mm*image_w_px)
    return ObliqueResult(phi, near, far, far-near, gsd_near, gsd_far, True)

def capture_interval_s(along_track_m, overlap, groundspeed_ms):
    if groundspeed_ms <= 0: return float("nan")
    return along_track_m*(1.0-overlap)/groundspeed_ms

def sampling_fraction(strip_width_m, transect_spacing_m):
    if transect_spacing_m <= 0: return float("nan")
    return strip_width_m/transect_spacing_m

def total_images(block_area_km2, transect_spacing_m, along_track_m, overlap):
    advance = along_track_m*(1.0-overlap)
    if transect_spacing_m <= 0 or advance <= 0: return 0
    return int(round(block_area_km2*1_000_000.0/(transect_spacing_m*advance)))
