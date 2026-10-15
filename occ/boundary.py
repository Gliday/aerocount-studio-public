"""
occ/boundary.py
Parse a survey-area boundary from common GIS formats and compute its area.
Supports GeoJSON (.geojson/.json), KML (.kml), KMZ (.kmz) and a coordinate
CSV/TXT (lat,lng). Area via the spherical-polygon (geodesic) formula — no
geopandas/shapely dependency. Returns rings as lists of (lat, lng) degrees.
"""
from __future__ import annotations
import io
import json
import math
import zipfile
import xml.etree.ElementTree as ET

R = 6371008.8  # mean Earth radius (m)


def _ring_area_km2(coords):
    n = len(coords)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        lat1, lng1 = coords[i]
        lat2, lng2 = coords[(i + 1) % n]
        s += math.radians(lng2 - lng1) * (2 + math.sin(math.radians(lat1)) + math.sin(math.radians(lat2)))
    return abs(s * R * R / 2.0) / 1e6


def area_km2(rings):
    return sum(_ring_area_km2(r) for r in rings)


# ---- format parsers ----------------------------------------------------------
def _rings_from_geojson_geom(geom):
    rings, t, c = [], geom.get("type"), geom.get("coordinates")
    if not c:
        return rings
    if t == "Polygon":                         # coordinates: [ring][pt][lng,lat]
        rings.append([(pt[1], pt[0]) for pt in c[0]])
    elif t == "MultiPolygon":
        for poly in c:
            rings.append([(pt[1], pt[0]) for pt in poly[0]])
    return rings


def parse_geojson(text):
    obj = json.loads(text)
    rings = []
    if obj.get("type") == "FeatureCollection":
        for f in obj.get("features", []):
            rings += _rings_from_geojson_geom(f.get("geometry", {}) or {})
    elif obj.get("type") == "Feature":
        rings += _rings_from_geojson_geom(obj.get("geometry", {}) or {})
    else:
        rings += _rings_from_geojson_geom(obj)
    return rings


def parse_kml_text(text):
    try:
        root = ET.fromstring(text)
    except Exception:
        return []
    rings = []
    for el in root.iter():
        if el.tag.endswith("coordinates") and el.text:
            pts = []
            for tok in el.text.split():
                parts = tok.split(",")
                if len(parts) >= 2:
                    try:
                        pts.append((float(parts[1]), float(parts[0])))  # lat, lng
                    except ValueError:
                        pass
            if len(pts) >= 3:
                rings.append(pts)
    return rings


def parse_kmz(data_bytes):
    try:
        with zipfile.ZipFile(io.BytesIO(data_bytes)) as z:
            names = z.namelist()
            name = "doc.kml" if "doc.kml" in names else next(
                (n for n in names if n.lower().endswith(".kml")), None)
            if not name:
                return []
            return parse_kml_text(z.read(name).decode("utf-8", "ignore"))
    except Exception:
        return []


def parse_coord_csv(data_bytes):
    import pandas as pd
    df = pd.read_csv(io.BytesIO(data_bytes))
    cols = {c.lower().strip(): c for c in df.columns}
    latc = next((cols[k] for k in cols if k in ("lat", "latitude", "y")), None)
    lngc = next((cols[k] for k in cols if k in ("lng", "lon", "long", "longitude", "x")), None)
    if latc and lngc:
        pts = list(zip(df[latc].astype(float), df[lngc].astype(float)))
    else:                                      # fall back to first two columns as lat,lng
        pts = list(zip(df.iloc[:, 0].astype(float), df.iloc[:, 1].astype(float)))
    return [pts] if len(pts) >= 3 else []


def parse_boundary(filename, data_bytes):
    """Return (rings, area_km2). rings = list of [(lat, lng), ...]."""
    ext = filename.lower().rsplit(".", 1)[-1]
    if ext in ("geojson", "json"):
        rings = parse_geojson(data_bytes.decode("utf-8", "ignore"))
    elif ext == "kml":
        rings = parse_kml_text(data_bytes.decode("utf-8", "ignore"))
    elif ext == "kmz":
        rings = parse_kmz(data_bytes)
    elif ext in ("csv", "txt"):
        rings = parse_coord_csv(data_bytes)
    else:
        rings = []
    return rings, area_km2(rings)
