from __future__ import annotations
import math, datetime as dt
def solar_elevation_deg(lat_deg, lon_deg, when_utc):
    if when_utc.tzinfo is None: when_utc = when_utc.replace(tzinfo=dt.timezone.utc)
    when_utc = when_utc.astimezone(dt.timezone.utc)
    doy = when_utc.timetuple().tm_yday
    hour = when_utc.hour + when_utc.minute/60.0 + when_utc.second/3600.0
    g = 2.0*math.pi/365.0*(doy-1+(hour-12.0)/24.0)
    eq = 229.18*(0.000075+0.001868*math.cos(g)-0.032077*math.sin(g)-0.014615*math.cos(2*g)-0.040849*math.sin(2*g))
    decl = (0.006918-0.399912*math.cos(g)+0.070257*math.sin(g)-0.006758*math.cos(2*g)
            +0.000907*math.sin(2*g)-0.002697*math.cos(3*g)+0.00148*math.sin(3*g))
    tst = hour*60.0 + eq + 4.0*lon_deg
    ha = tst/4.0 - 180.0
    lat = math.radians(lat_deg); ha_r = math.radians(ha)
    cz = math.sin(lat)*math.sin(decl)+math.cos(lat)*math.cos(decl)*math.cos(ha_r)
    cz = max(-1.0, min(1.0, cz))
    return 90.0 - math.degrees(math.acos(cz))
def light_quality(e, low=25.0, high=60.0):
    if e < 0: return "night"
    if e < low: return "long-shadow risk"
    if e > high: return "glare risk"
    return "good"
