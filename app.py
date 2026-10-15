"""
OCC AeroCount Studio  —  Streamlit decision-support app
Run:  python -m streamlit run app.py

Sidebar-navigated conservation-tech UI: Overview · Guided Planner · Survey
Geometry · Region & Season · Cost · Correction Factors · Export · Parks · News
· About/Methods. All scientific logic lives in occ/ (unchanged); this file is
UI/UX only. Weather © Open-Meteo (CC BY 4.0); articles © OpenAlex.
"""
import os, io, base64
import datetime as dt
import pandas as pd
import altair as alt
import streamlit as st
from PIL import Image

from occ import geometry as geo
from occ import solar
from occ import cost as costmod
from occ import regions as reg
from occ import climate as clim
from occ import parks as parkmod
from occ import articles as art
from occ import library as lib
from occ import presets as pre
from occ import survey as surv
from occ import boundary as bnd

# ---- paths ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def _first_existing(*paths):
    for p in paths:
        if p and os.path.exists(p): return p
    return None
def _first_dir(*names):
    for n in names:
        p = os.path.join(BASE_DIR, n)
        if os.path.isdir(p): return p
    return None
BG_DIR = _first_dir("BG_IMAGES", "assets")
PAPERS_DIR = _first_dir("PAPERS_DIR", "Research Papers") or os.path.join(BASE_DIR, "PAPERS_DIR")
LOGO = _first_existing(os.path.join(BASE_DIR, "logo.png"), os.path.join(BASE_DIR, "assets", "logo.png"),
                       os.path.join(BG_DIR or "", "logo.png"))
HAS_LOGO = LOGO is not None
def _bg_candidates():
    if not BG_DIR: return []
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [os.path.join(BG_DIR, f) for f in sorted(os.listdir(BG_DIR))
            if f.lower().endswith(exts) and "logo" not in f.lower()]
BG_IMAGES = _bg_candidates()

st.set_page_config(page_title="OCC AeroCount Studio", page_icon=LOGO if HAS_LOGO else "•",
                   layout="wide", initial_sidebar_state="expanded")

# ---- palette (STE brand + forest/sand per brief) ----------------------------
WETLANDS, SAVANNAH, EMBER = "#28414F", "#FFBF19", "#EE6D22"
FOREST, SAND, WORDMARK, IVORY, STONE = "#33513F", "#EADFC6", "#4F6571", "#FEFCF5", "#D6DAD3"
GOOD = "#3E8E5E"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family:'Inter',system-ui,sans-serif; }
.stApp { background:#FEFCF5; }
header[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1200px; padding-top:1.6rem; padding-bottom:4rem; }
section[data-testid="stSidebar"] { background:#28414F; }
section[data-testid="stSidebar"] * { color:#EDEFEA !important; }
section[data-testid="stSidebar"] [role="radiogroup"] label { padding:.15rem 0; }
section[data-testid="stSidebar"] .stRadio > label { color:#B9C6CB !important; font-weight:600; letter-spacing:.1em; text-transform:uppercase; font-size:.7rem; }
h1,h2,h3,h4 { font-family:'Fraunces',Georgia,serif !important; color:#28414F; letter-spacing:-.01em; }
.eyebrow { letter-spacing:.16em; text-transform:uppercase; font-size:.7rem; font-weight:600; color:#4F6571; margin-bottom:.1rem; }
.sec-title { font-family:'Fraunces',serif; font-size:1.6rem; color:#28414F; margin:.05rem 0 .1rem; }
.sec-sub { color:#4F6571; font-size:.95rem; margin-bottom:.9rem; }
[data-testid="stMetric"] { background:#fff; border:1px solid #ECEFEA; border-radius:16px; padding:1rem 1.15rem;
   box-shadow:0 1px 2px rgba(27,42,50,.04), 0 14px 30px -26px rgba(27,42,50,.45); }
[data-testid="stMetricValue"] { color:#28414F; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }
[data-testid="stMetricLabel"] { color:#4F6571; }
.stButton>button, .stDownloadButton>button { background:#28414F; color:#fff; border:0; border-radius:12px; padding:.5rem 1.1rem; font-weight:600; }
.stButton>button:hover, .stDownloadButton>button:hover { background:#FFBF19; color:#28414F; }
[data-testid="stExpander"] { border:1px solid #ECEFEA; border-radius:14px; background:#fff; }
[data-testid="stDataFrame"] { border:1px solid #ECEFEA; border-radius:14px; overflow:hidden; }
.card { background:#fff; border:1px solid #ECEFEA; border-radius:16px; padding:1.2rem 1.3rem; height:100%;
   box-shadow:0 1px 2px rgba(27,42,50,.04), 0 16px 32px -28px rgba(27,42,50,.4); }
.card h4 { margin:.1rem 0 .3rem; font-size:1.05rem; }
.card p { color:#4F6571; font-size:.88rem; margin:0; line-height:1.5; }
.interp { background:#F4F1E8; border-left:4px solid #33513F; padding:.75rem .95rem; border-radius:8px;
   color:#3a4a44; font-size:.9rem; line-height:1.55; margin:.4rem 0; }
.badge { font-size:.72rem; font-weight:600; padding:.15rem .6rem; border-radius:99px; }
.b-exc{background:#E7F0EA;color:#2F6B45;} .b-good{background:#FFF6DB;color:#8A6A00;} .b-marg{background:#FCEBDD;color:#9E4A17;}
.hero { background:radial-gradient(120% 130% at 88% -30%, rgba(255,191,25,.22), transparent 55%), linear-gradient(180deg,#FEFCF5,#F5F1E6);
   border:1px solid #ECEFEA; border-radius:22px; padding:1.6rem 1.8rem; margin-bottom:1.3rem; }
.hero h1 { margin:0; font-size:2rem; color:#28414F; }
.hero p { color:#4F6571; margin:.35rem 0 0; font-size:1rem; max-width:640px; }
.stepbar { display:flex; gap:.5rem; margin:.2rem 0 1.2rem; flex-wrap:wrap; }
.step { flex:1; min-width:110px; border-radius:12px; padding:.55rem .7rem; border:1px solid #ECEFEA; background:#fff; font-size:.85rem; }
.step .n { font-family:ui-monospace,monospace; font-weight:700; margin-right:.4rem; }
.step.active { background:#28414F; color:#fff; } .step.active .n { color:#FFBF19; }
.step.done { background:#EFF4EE; border-color:#CDE3D2; } .step.done .n { color:#2F6B45; }
</style>
""", unsafe_allow_html=True)

# ---- photographic background ------------------------------------------------
@st.cache_data(show_spinner=False)
def _bg_uri(path, max_w=1600, quality=60):
    try:
        im = Image.open(path).convert("RGB")
        if im.width > max_w: im = im.resize((max_w, round(im.height*max_w/im.width)))
        buf = io.BytesIO(); im.save(buf, format="JPEG", quality=quality)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None
_bg1 = _bg_uri(BG_IMAGES[0]) if len(BG_IMAGES) > 0 else None
_bg2 = _bg_uri(BG_IMAGES[1]) if len(BG_IMAGES) > 1 else None
_css = ""
if _bg1: _css += (".stApp{background:linear-gradient(rgba(254,252,245,.93),rgba(254,252,245,.95)),"
                  f"url('{_bg1}');background-size:cover;background-attachment:fixed;background-position:center;}}")
if _bg2: _css += (".hero{background:linear-gradient(90deg,rgba(254,252,245,.96) 30%,rgba(254,252,245,.55) 100%),"
                  f"url('{_bg2}');background-size:cover;background-position:center;}}")
if _css: st.markdown(f"<style>{_css}</style>", unsafe_allow_html=True)

# ---- UI helpers -------------------------------------------------------------
def eyebrow(t): st.markdown(f"<div class='eyebrow'>{t}</div>", unsafe_allow_html=True)
def section_header(title, sub=""):
    st.markdown(f"<div class='sec-title'>{title}</div>" + (f"<div class='sec-sub'>{sub}</div>" if sub else ""),
                unsafe_allow_html=True)
def card(title, body):
    return f"<div class='card'><h4>{title}</h4><p>{body}</p></div>"
def interp(text): st.markdown(f"<div class='interp'>{text}</div>", unsafe_allow_html=True)
def badge(text, kind): return f"<span class='badge b-{kind}'>{text}</span>"
def alt_theme(c):
    return c.configure_view(strokeWidth=0).configure_axis(grid=True, gridColor="#EEF1EC",
        labelColor="#4F6571", titleColor="#4F6571").configure_legend(labelColor="#4F6571", titleColor="#4F6571")

@st.cache_data(ttl=3600, show_spinner=False)
def cached_climatology(lat, lng): return clim.monthly_climatology(lat, lng)
@st.cache_data(ttl=3600, show_spinner=False)
def cached_forecast(lat, lng): return clim.forecast_16day(lat, lng)
@st.cache_data(ttl=3600, show_spinner=False)
def cached_articles(q, n, d): return art.fetch_articles(q, n, d)

def plan_geometry(p):
    if p["mode"] == "Near-vertical":
        strip = geo.footprint_width_m(p["hagl"], p["sensor_w"], p["focal"])
        gsd = geo.gsd_nadir_cm(p["sensor_w"], p["hagl"], p["focal"], p["img_w"])
        return strip, gsd, gsd, 1
    ob = geo.oblique_geometry(p["hagl"], p["focal"], p["sensor_h"], p["sensor_w"], p["img_w"], p["depression"])
    if not ob.valid: return float("nan"), float("nan"), float("nan"), 2
    return ob.strip_width_m, ob.gsd_near_cm, ob.gsd_far_cm, 2

def build_report(p):
    strip, gn, gf, cams = plan_geometry(p)
    strata = "\n".join(f"  - {s.get('name','?')}: {s.get('area_km2',0)} km2, {s.get('spacing_m',0)} m spacing"
                       for s in p.get("strata", []))
    return (f"OCC AEROCOUNT — SURVEY PLAN\n===========================\n"
            f"Survey : {p.get('name','')}\nRegion : {p.get('region','')}\nPreset : {p.get('preset','')}\n"
            f"Aircraft: {p.get('aircraft','')}\n\n"
            f"FLIGHT & CAMERA\n  HAGL {p['hagl']} m | Speed {p['speed_ms']} m/s | Interval {p['interval_s']} s\n"
            f"  Mode {p['mode']} | Depression {p.get('depression','-')} deg | Focal {p['focal']} mm\n"
            f"  Strip {strip:.0f} m | GSD near-far {gn:.1f}-{gf:.1f} cm/px\n\n"
            f"STRATIFICATION\n{strata}\n\nOUTPUT\n  Total images: {p.get('total_images',0):,}\n\n"
            f"ASSUMPTIONS/LIMITS\n  Oblique GSD/strip are planning estimates; validate with ground-marker "
            f"calibration (Lamprey method). Pair sampling fraction with Jolly II for estimate + variance.\n"
            f"  Climate window from 20-year rainfall climatology (Open-Meteo, CC BY 4.0).\n")


# =============================================================================
# GUIDED PLANNER (wizard)
# =============================================================================
WSTEPS = ["Setup", "Aircraft & camera", "Stratification", "Season & light", "Effort & cost", "Review"]

def _init_plan():
    if "plan" not in st.session_state:
        base = dict(pre.PRESETS["Custom — Samburu default"])
        base.update({"name": "Untitled survey", "region": reg.region_names()[0],
                     "preset": "Custom — Samburu default", "interp_s": 20.0, "interp_rate": 15.0,
                     "aircraft_rate": 800.0, "flight_hours": 6.0, "rso_obs": 2, "rso_rate": 25.0, "total_images": 0})
        st.session_state.plan = base
    st.session_state.setdefault("wiz_step", 1)

def _stepbar(cur):
    html = "<div class='stepbar'>"
    for i, s in enumerate(WSTEPS, 1):
        cls = "active" if i == cur else ("done" if i < cur else "")
        html += f"<div class='step {cls}'><span class='n'>{i}</span>{s}</div>"
    st.markdown(html + "</div>", unsafe_allow_html=True)

def render_guided():
    _init_plan(); p = st.session_state.plan; step = st.session_state.wiz_step
    st.markdown(f"<div class='hero'><h1>{p['name'] or 'New survey plan'}</h1>"
                f"<p>Guided OCC survey planning · {p['region']}</p></div>", unsafe_allow_html=True)
    _stepbar(step)
    if step == 1:
        section_header("1 · Setup", "Name the survey, pick the region, and choose a starting configuration.")
        p["name"] = st.text_input("Survey name", p["name"])
        rn = reg.region_names(); p["region"] = st.selectbox("Region", rn, index=rn.index(p["region"]) if p["region"] in rn else 0)
        names = pre.preset_names()
        choice = st.selectbox("Configuration preset", names, index=names.index(p["preset"]) if p["preset"] in names else 0,
                              help="Presets reproduce published survey setups (Lamprey 2020/2021/2025; Delplanque 2024).")
        if choice != p["preset"]:
            keep = {k: p[k] for k in ("name", "region", "interp_s", "interp_rate", "aircraft_rate", "flight_hours", "rso_obs", "rso_rate")}
            newp = dict(pre.PRESETS[choice]); newp["preset"] = choice; newp.update(keep); newp["total_images"] = 0
            st.session_state.plan = newp; st.rerun()
        st.info(pre.PRESETS[choice]["source"])
    elif step == 2:
        section_header("2 · Aircraft & camera", "Flight and camera parameters — outputs update live.")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            p["hagl"] = st.slider("HAGL — height above ground (m)", 50, 2000, int(p["hagl"]), 10, help="OCC typically 90–200 m (300–650 ft).")
            p["speed_ms"] = st.slider("Groundspeed (m/s)", 20, 120, int(p["speed_ms"]), 1, help="Survey aircraft ~45–55 m/s (85–105 kn).")
            p["interval_s"] = st.slider("Frame interval (s)", 1.0, 6.0, float(p["interval_s"]), 0.5, help="2 s is standard for overlapping OCC coverage.")
            p["mode"] = st.radio("Camera mode", ["Near-vertical", "Oblique"], index=0 if p["mode"] == "Near-vertical" else 1, horizontal=True)
            if p["mode"] == "Oblique":
                p["depression"] = st.slider("Depression angle (° below horizontal)", 5, 80, int(p["depression"]), 1, help="OCC ~33–53° (i.e. 36.5–57° from vertical).")
        with c2:
            p["focal"] = st.number_input("Focal length (mm)", 8.0, 400.0, float(p["focal"]), 1.0, help="35–42 mm gives ~150 m strip at survey height.")
            with st.expander("Sensor / image (advanced)"):
                p["sensor_w"] = st.number_input("Sensor width (mm)", 5.0, 60.0, float(p["sensor_w"]), 0.1)
                p["sensor_h"] = st.number_input("Sensor height (mm)", 5.0, 60.0, float(p["sensor_h"]), 0.1)
                p["img_w"] = st.number_input("Image width (px)", 1000, 20000, int(p["img_w"]), 1)
                p["img_h"] = st.number_input("Image height (px)", 1000, 20000, int(p["img_h"]), 1)
        strip, gn, gf, cams = plan_geometry(p)
        st.divider()
        if strip != strip:
            st.warning("Far edge doesn't meet the ground at this depression angle — increase it.")
        else:
            m = st.columns(3)
            m[0].metric("Strip width (per side)", f"{strip:.0f} m")
            m[1].metric("GSD near→far", f"{gn:.1f}→{gf:.1f} cm/px")
            m[2].metric("Cameras assumed", f"{cams}")
            txt, kind = surv.resolving_power(gn); st.markdown(badge(txt, kind), unsafe_allow_html=True)
    elif step == 3:
        section_header("3 · Stratification", "Edit strata, upload a CSV, or import a survey-area boundary.")
        up = st.file_uploader("Upload strata CSV (name, area_km2, spacing_m)", type=["csv"])
        if up is not None:
            try:
                df = pd.read_csv(up); p["strata"] = df[["name", "area_km2", "spacing_m"]].to_dict("records")
                st.success(f"Loaded {len(p['strata'])} strata.")
            except Exception as e:
                st.error(f"Need columns name, area_km2, spacing_m. {e}")
        with st.expander("Or define the survey area from a boundary / GIS file (GeoJSON, KML, KMZ, coordinate CSV)"):
            bup = st.file_uploader("Boundary file", type=["geojson", "json", "kml", "kmz", "csv"], key="bnd_up")
            if bup is not None:
                try:
                    rings, area = bnd.parse_boundary(bup.name, bup.getvalue())
                    if not rings: st.error("No polygon/coordinates found.")
                    else:
                        st.metric("Computed survey area", f"{area:,.0f} km²")
                        outer = rings[0]
                        try:
                            import pydeck as pdk
                            poly = [[ln, la] for (la, ln) in outer]
                            mlat = sum(la for la, _ in outer)/len(outer); mlng = sum(ln for _, ln in outer)/len(outer)
                            st.pydeck_chart(pdk.Deck(map_style=None,
                                initial_view_state=pdk.ViewState(latitude=mlat, longitude=mlng, zoom=7),
                                layers=[pdk.Layer("PolygonLayer", data=[{"polygon": poly}], get_polygon="polygon",
                                    get_fill_color=[255, 191, 25, 60], get_line_color=[40, 65, 79], line_width_min_pixels=2)]))
                        except Exception:
                            st.map(pd.DataFrame([{"lat": la, "lon": ln} for la, ln in outer]))
                        stem = bup.name.rsplit(".", 1)[0][:40]
                        if st.button("➕ Add boundary as a stratum"):
                            p["strata"].append({"name": stem, "area_km2": round(area), "spacing_m": 2000})
                            st.success(f"Added '{stem}'."); st.rerun()
                except Exception as e:
                    st.error(f"Couldn't parse boundary. {e}")
        edited = st.data_editor(pd.DataFrame(p["strata"]), num_rows="dynamic", use_container_width=True, hide_index=True)
        p["strata"] = edited.dropna(how="all").to_dict("records")
        strip, gn, gf, cams = plan_geometry(p)
        if strip == strip and p["strata"]:
            rows, tot = surv.survey_totals(p["strata"], strip, p["speed_ms"], p["interval_s"], cams)
            p["total_images"] = tot["images"]
            st.dataframe(pd.DataFrame([{"Stratum": r.get("name", ""), "Area (km²)": r.get("area_km2", 0),
                "Spacing (m)": r.get("spacing_m", 0), "Line (km)": round(r["line_km"]),
                "Sampling (%)": round(r["sampling_pct"], 1), "Images": f"{r['images']:,}"} for r in rows]),
                use_container_width=True, hide_index=True)
            m = st.columns(3)
            m[0].metric("Total area", f"{tot['area_km2']:,.0f} km²"); m[1].metric("Transect line", f"{tot['line_km']:,.0f} km")
            m[2].metric("Total images", f"{tot['images']:,}")
        else:
            st.info("Add strata and a valid camera geometry to see the design.")
    elif step == 4:
        section_header("4 · Season & light", "When to fly — dry-season window and today's good-light hours.")
        _region_climate(reg.get_region(p["region"]))
    elif step == 5:
        section_header("5 · Effort & cost", "OCC interpretation vs an equivalent RSO survey.")
        _cost_block(p.get("total_images", 0), p, store=True)
    else:
        section_header("6 · Review", "Your survey plan — download and take it to the flight team.")
        report = build_report(p); st.code(report, language="text")
        st.download_button("⬇ Download plan (.txt)", data=report,
                           file_name=f"{p['name'].replace(' ','_')}_plan.txt", mime="text/plain")
    st.divider()
    b1, b2, _ = st.columns([1, 1, 4])
    if b1.button("← Back", disabled=(step == 1), use_container_width=True):
        st.session_state.wiz_step -= 1; st.rerun()
    if b2.button("Next →", disabled=(step == len(WSTEPS)), use_container_width=True):
        st.session_state.wiz_step += 1; st.rerun()


# ---- shared blocks ----------------------------------------------------------
def _region_climate(r):
    st.markdown(f"<div class='card'><div class='eyebrow'>Selected region</div>"
                f"<h4 style='margin:.1rem 0'>{r['name']}</h4>"
                f"<p>{r['country']} · {r['ecosystem']} · {r['lat']:.2f}, {r['lng']:.2f}</p></div>", unsafe_allow_html=True)
    st.write("")
    try:
        clim_df = cached_climatology(r["lat"], r["lng"])
        long = clim_df.reset_index().melt("Month", var_name="Series", value_name="mm")
        ch = alt.Chart(long).mark_bar().encode(
            x=alt.X("Month:N", sort=list(clim_df.index), title=None), xOffset="Series:N",
            y=alt.Y("mm:Q", title="Rainfall (mm)"),
            color=alt.Color("Series:N", scale=alt.Scale(range=[STONE, WETLANDS]), legend=alt.Legend(orient="top")))
        st.altair_chart(alt_theme(ch), use_container_width=True)
        best = clim.best_survey_months(clim_df)
        st.success(f"**Best survey window: {', '.join(best)}** — driest months.")
        interp(f"Rainfall drives both detectability and animal distribution. The driest months "
               f"({', '.join(best)}) concentrate animals near water and thin the vegetation, so counts are more complete.")
        with st.expander("16-day forecast (flight-window outlook)"):
            try:
                st.dataframe(clim.daily_forecast_table(cached_forecast(r["lat"], r["lng"])),
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Forecast needs internet. ({e})")
    except Exception as e:
        st.warning(f"Climate data needs internet. ({e})")
    eyebrow("Good-light window — today (UTC)")
    today = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    rows = []
    for h in range(24):
        e = solar.solar_elevation_deg(r["lat"], r["lng"], today + dt.timedelta(hours=h))
        if e > 0: rows.append({"Hour": h, "Elevation": round(e, 1), "Light": solar.light_quality(e)})
    ldf = pd.DataFrame(rows)
    if len(ldf):
        ch = alt.Chart(ldf).mark_bar(cornerRadius=3).encode(
            x=alt.X("Hour:O", title="Hour (UTC)"), y=alt.Y("Elevation:Q", title="Sun °"),
            color=alt.Color("Light:N", scale=alt.Scale(domain=["good", "long-shadow risk", "glare risk"],
                range=[GOOD, EMBER, SAVANNAH]), legend=alt.Legend(orient="top")))
        st.altair_chart(alt_theme(ch), use_container_width=True)
        st.caption("Target 25°–60° sun elevation: below = long shadows, above = glare.")

def _cost_block(imgs, store_target=None, store=False):
    st.metric("Planned / entered images", f"{imgs:,}")
    src = store_target if store else {}
    c1, c2 = st.columns(2, gap="large")
    with c1:
        it = st.number_input("Interpretation time / image (s)", 0.0, 600.0, float(src.get("interp_s", 20.0)), 1.0, key="cst_it",
                             help="Manual OCC ≈ 15–30 s/image; SADL-OCC pipelines cut this sharply.")
        ir = st.number_input("Interpreter rate (/hr)", 0.0, 10000.0, float(src.get("interp_rate", 15.0)), 1.0, key="cst_ir")
        ar = st.number_input("Aircraft cost (/hr)", 0.0, 10000.0, float(src.get("aircraft_rate", 800.0)), 10.0, key="cst_ar")
    with c2:
        fh = st.number_input("Survey flight hours", 0.0, 500.0, float(src.get("flight_hours", 6.0)), 0.5, key="cst_fh")
        ob = st.number_input("RSO observers", 0, 8, int(src.get("rso_obs", 2)), 1, key="cst_ob")
        rr = st.number_input("RSO observer rate (/hr)", 0.0, 10000.0, float(src.get("rso_rate", 25.0)), 1.0, key="cst_rr")
    if store:
        store_target.update({"interp_s": it, "interp_rate": ir, "aircraft_rate": ar, "flight_hours": fh, "rso_obs": ob, "rso_rate": rr})
    res = costmod.compare_costs(imgs, it, 0, ir, ar, fh, ob, rr)
    st.write("")
    a, b, c = st.columns(3)
    a.metric("OCC interpretation hrs", f"{res.occ_interp_hours:.1f}")
    b.metric("OCC total cost", f"{res.occ_cost:,.0f}")
    c.metric("RSO total cost", f"{res.rso_cost:,.0f}")
    comp = pd.DataFrame({
        "Method": ["OCC", "OCC", "RSO", "RSO"],
        "Component": ["Interpretation", "Aircraft", "Observers", "Aircraft"],
        "Cost": [res.occ_interp_hours*ir, fh*ar, ob*fh*rr, fh*ar]})
    ch = alt.Chart(comp).mark_bar(cornerRadius=6).encode(
        x=alt.X("Method:N", title=None), y=alt.Y("Cost:Q", title="Cost"),
        color=alt.Color("Component:N", scale=alt.Scale(range=[FOREST, WETLANDS, SAVANNAH, STONE]), legend=alt.Legend(orient="top")))
    st.altair_chart(alt_theme(ch), use_container_width=True)
    pct = (res.saving / max(res.rso_cost, res.occ_cost, 1)) * 100
    if res.cheaper == "OCC":
        st.success(f"**OCC is ~{pct:.0f}% cheaper** here (saving {res.saving:,.0f}).")
        interp("OCC appears more cost-efficient under these assumptions mainly because it avoids paying "
               "multiple observers for the whole flight; its main cost is image interpretation, which scales "
               "with image volume rather than air-time. A cheaper aircraft (no observers to seat) reinforces this.")
    else:
        st.warning(f"**RSO is ~{pct:.0f}% cheaper** here (by {res.saving:,.0f}).")
        interp("RSO wins at this scale because the interpretation workload for OCC is high relative to a short "
               "flight. OCC typically overtakes RSO as survey area — and thus the value of a complete, "
               "re-checkable photographic record — grows.")


# =============================================================================
# SECTIONS
# =============================================================================
def render_overview():
    st.markdown("<div class='hero'><h1>OCC AeroCount Studio</h1>"
                "<p>A decision-support tool for planning Oblique Camera Count aerial wildlife surveys across "
                "Africa — geometry, season, effort, cost and count-correction in one place.</p></div>", unsafe_allow_html=True)
    section_header("What this tool does")
    c = st.columns(3, gap="medium")
    cards = [("Plan survey geometry", "Near-vertical and oblique footprint, strip width, GSD and capture interval."),
             ("Estimate image volume", "Stratified image counts from area, spacing and cadence — before you fly."),
             ("Find the right window", "Dry-season timing and good-light hours from 20-year climate data."),
             ("Compare OCC vs RSO", "Side-by-side cost with interpretation, aircraft and observer components."),
             ("Correct historical counts", "Published detection factors to re-scale legacy RSO estimates."),
             ("Export a plan", "A clean, copyable planning summary for the flight team and stakeholders.")]
    for i, (t, b) in enumerate(cards):
        with c[i % 3]:
            st.markdown(card(t, b), unsafe_allow_html=True); st.write("")
    section_header("How to use this tool")
    st.markdown("1. **Guided Planner** — walk through Setup → Camera → Stratification → Season → Cost → Review, and download a plan.\n"
                "2. Or jump to a single tool in the sidebar (**Survey Geometry**, **Region & Season**, **Cost**, **Correction Factors**).\n"
                "3. Use **Export / Summary** to produce a shareable planning report.\n"
                "4. See **About / Methods** for assumptions and scientific caveats.")
    st.caption("Weather data by Open-Meteo.com, licensed CC BY 4.0. Research feed via OpenAlex. "
               "Presets grounded in Lamprey et al. (2020, 2021, 2025) and Delplanque et al. (2024).")

def render_geometry():
    section_header("Survey Geometry", "Design the camera footprint and image volume for one block.")
    c1, c2, c3 = st.columns(3)
    with c1:
        hagl = st.slider("HAGL (m)", 50, 2000, 350, 10, help="Height above ground.")
        speed = st.slider("Groundspeed (m/s)", 20, 120, 58, 1)
        interval = st.slider("Frame interval (s)", 1.0, 6.0, 2.0, 0.5)
        spacing = st.number_input("Transect spacing (m)", 100, 20000, 2000, 100, help="Distance between adjacent transects.")
        block = st.number_input("Block area (km²)", 1, 100000, 1000, 10)
    with c2:
        sensor_w = st.number_input("Sensor width (mm)", 5.0, 60.0, 35.9, 0.1)
        sensor_h = st.number_input("Sensor height (mm)", 5.0, 60.0, 23.9, 0.1)
        img_w = st.number_input("Image width (px)", 1000, 20000, 7008, 1)
        focal = st.number_input("Focal length (mm)", 8.0, 400.0, 50.0, 1.0)
    with c3:
        mode = st.radio("Camera mode", ["Near-vertical", "Oblique"], horizontal=True)
        depression = st.slider("Depression angle (°)", 5, 80, 35, 1, disabled=(mode == "Near-vertical"))
    p = {"mode": mode, "hagl": hagl, "sensor_w": sensor_w, "sensor_h": sensor_h, "img_w": img_w,
         "focal": focal, "depression": depression}
    strip, gn, gf, cams = plan_geometry(p)
    st.divider()
    if strip != strip:
        st.error("Far edge doesn't meet the ground — increase the depression angle."); return
    along = geo.along_track_per_frame_m(hagl, sensor_h, focal)
    images = int(cams * (block / (spacing/1000)) * 1000 / max(speed*interval, 1e-6))
    sampling = cams * strip / spacing * 100
    m = st.columns(4)
    m[0].metric("Strip width /side", f"{strip:.0f} m")
    m[1].metric("GSD near→far", f"{gn:.1f}→{gf:.1f} cm/px")
    m[2].metric("Sampling fraction", f"{sampling:.1f} %")
    m[3].metric("Estimated images", f"{images:,}")
    txt, kind = surv.resolving_power(gn); st.markdown(badge(txt, kind), unsafe_allow_html=True)
    # interpretation + warnings
    interp(f"Estimated image count: <b>{images:,} images</b>. At {speed} m/s and a {interval:.0f}s interval "
           f"({'two cameras' if cams==2 else 'one camera'}), each frame resolves ground at {gn:.1f}–{gf:.1f} cm/px. "
           f"A GSD under ~6 cm resolves small antelope; coarser than ~15 cm limits you to large species.")
    if gn > 15: st.warning("GSD is coarse (>15 cm/px) — only large species will be reliably identified. Consider lower HAGL or longer focal length.")
    if sampling > 100: st.warning("Sampling fraction exceeds 100% — transect spacing is narrower than the imaged strip (heavy overlap). Widen spacing.")
    if sampling < 3: st.warning("Sampling fraction is very low (<3%) — estimates will have wide confidence limits. Consider tighter spacing in core blocks.")
    if images > 500000: st.warning(f"{images:,} images is a very large dataset — plan storage and annotation capacity (or a SADL-OCC pipeline) before committing.")
    # charts: strip & images vs HAGL
    st.write("")
    eyebrow("How outputs change with flight height")
    hs = list(range(100, 801, 50)); rowsg = []
    for h in hs:
        pp = dict(p); pp["hagl"] = h
        s2, g2, _, c2n = plan_geometry(pp)
        if s2 == s2:
            im2 = int(c2n * (block/(spacing/1000)) * 1000 / max(speed*interval, 1e-6))
            rowsg.append({"HAGL (m)": h, "Strip width (m)": round(s2), "GSD near (cm)": round(g2, 1)})
    if rowsg:
        gdf = pd.DataFrame(rowsg)
        cc = st.columns(2)
        with cc[0]:
            ch = alt.Chart(gdf).mark_line(point=True, color=WETLANDS).encode(
                x="HAGL (m):Q", y=alt.Y("Strip width (m):Q"))
            st.altair_chart(alt_theme(ch).properties(title="Strip width vs HAGL"), use_container_width=True)
        with cc[1]:
            ch = alt.Chart(gdf).mark_line(point=True, color=EMBER).encode(
                x="HAGL (m):Q", y=alt.Y("GSD near (cm):Q"))
            st.altair_chart(alt_theme(ch).properties(title="Near-edge GSD vs HAGL"), use_container_width=True)
    st.caption("Oblique GSD/strip are planning estimates — validate the real strip with ground-marker calibration (Lamprey method).")

def render_region():
    section_header("Region & Season Planner", "Choose where and when to fly, from live climate data.")
    r = reg.get_region(st.selectbox("Region", reg.region_names()))
    _region_climate(r)

def render_cost():
    section_header("OCC vs RSO Cost Comparison", "Is a camera survey cheaper than observers, at your scale?")
    imgs = st.number_input("Total images (from your survey design)", 0, 5_000_000, 4000, 100,
                           help="Bring this from Survey Geometry or the Guided Planner.")
    _cost_block(imgs)

def render_correction():
    section_header("Correction Factor Calculator", "Re-scale observer counts for the animals cameras show were missed.")
    interp("A <b>correction factor (Cd)</b> scales a raw count up to account for animals that were present but "
           "not detected. It is the inverse of the probability of detection: <b>Cd = 1 / P<sub>d</sub></b>. "
           "Multiply a historical RSO count by Cd to get the OCC-adjusted estimate.")
    st.markdown("**Formula:**  OCC-adjusted estimate = RSO count × Cd")
    c1, c2 = st.columns(2)
    opts = ["Custom"] + [f"{s} ({src})" for s, _, _, src in pre.CORRECTION_FACTORS]
    pick = c1.selectbox("Species / source", opts)
    if pick == "Custom":
        cd = c2.number_input("Correction factor Cd", 1.0, 10.0, 1.5, 0.01)
        pd_ = 100.0 / cd
    else:
        row = pre.CORRECTION_FACTORS[opts.index(pick) - 1]
        cd, pd_ = row[2], row[1]
        c2.metric("Published Cd", f"{cd:.2f}"); c2.caption(f"Detection {pd_:.0f}% · {row[3]}")
    rso = st.number_input("Historical RSO count", 0, 10_000_000, 58313, 100)
    adj = rso * cd; missed = adj - rso
    m = st.columns(3)
    m[0].metric("RSO count", f"{rso:,}"); m[1].metric("Correction factor", f"{cd:.2f}"); m[2].metric("OCC-adjusted", f"{adj:,.0f}")
    interp(f"If historical RSO counts were <b>{rso:,}</b> and the correction factor is <b>{cd:.2f}</b>, the "
           f"OCC-adjusted estimate is <b>{adj:,.0f}</b> — the observers likely missed about {missed:,.0f} animals "
           f"(~{(1-pd_/100)*100:.0f}% of the true number).")
    with st.expander("Published detection & correction factors (apply cautiously — site/season specific)"):
        st.dataframe(pd.DataFrame([{"Species": s, "Detection Pd (%)": p, "Correction Cd": c, "Source": src}
                                   for s, p, c, src in pre.CORRECTION_FACTORS]), use_container_width=True, hide_index=True)

def render_export():
    section_header("Export / Summary Report", "A clean, copyable planning summary.")
    if "plan" not in st.session_state:
        st.info("Run the **Guided Planner** first — this report summarises that plan."); return
    p = st.session_state.plan
    report = build_report(p)
    st.code(report, language="text")
    st.download_button("⬇ Download plan (.txt)", data=report,
                       file_name=f"{p.get('name','survey').replace(' ','_')}_plan.txt", mime="text/plain")
    st.caption("Copy the text above, or download it. Cost figures reflect the last values entered on the Effort & cost step.")

def render_methods():
    section_header("About / Methods", "Assumptions and scientific caveats — read before presenting results.")
    st.markdown(
        "**Oblique GSD & strip width are planning estimates.** The near/far ground-sampling-distance and strip "
        "width are computed from flight height, focal length, sensor size and camera angle. In practice the true "
        "strip is set by **ground-marker calibration** (the Lamprey method): flying an array of marks at known "
        "spacing and regressing visible marks against height. Always calibrate before operational counting.\n\n"
        "**Population estimates need Jolly II.** The sampling fraction here supports design only. Turn transect "
        "counts into a population estimate and variance with **Jolly's (1969) Method II** for unequal sample units.\n\n"
        "**Season window** uses a **20-year monthly rainfall climatology** (Open-Meteo archive). The driest tertile "
        "of months is flagged as the recommended survey window; a seasonal-forecast layer can refine this.\n\n"
        "**Correction factors** (Cd = 1/Pd) come from double-observer re-interpretation in published studies "
        "(Lamprey et al. 2020; Lamprey 2025). They are species-, site- and season-specific — apply with judgement.\n\n"
        "**Data sources.** Weather © Open-Meteo.com (CC BY 4.0). Research feed via OpenAlex. Park areas are "
        "approximate. Presets reproduce Lamprey et al. (2020 Tsavo & Murchison; 2021 viewing-angle; 2025 KAZA) "
        "and Delplanque et al. (2024 Comoé).")

def render_news():
    section_header("News & Papers", "Newest related research via OpenAlex, plus your local library.")
    q = st.text_input("Search topic", art.DEFAULT_QUERY); n = st.slider("How many", 5, 50, 20)
    try:
        with st.spinner("Fetching latest articles…"):
            items = cached_articles(q, n, 1095)
        if not items: st.info("No results — try broader terms.")
        for a in items:
            with st.container(border=True):
                st.markdown(f"**{a['title']}**")
                meta = " · ".join(x for x in [a["date"], a["authors"], a["venue"]] if x)
                if meta: st.caption(meta)
                if a["abstract"]: st.write(a["abstract"])
                links = [f"[DOI]({a['doi']})"] if a["doi"] else []
                if a["oa_url"]: links.append(f"[Open access PDF]({a['oa_url']})")
                if links: st.markdown(" · ".join(links))
    except Exception as e:
        st.warning(f"Couldn't reach OpenAlex (needs internet). ({e})")
    st.divider(); section_header("Your research library")
    folder = st.text_input("Papers folder", PAPERS_DIR); pdfs = lib.list_pdfs(folder)
    if not pdfs: st.info("No PDFs found in that folder.")
    else:
        st.dataframe(pd.DataFrame([{"Paper": p["name"], "Size (MB)": p["size_mb"], "Modified": p["modified"]} for p in pdfs]),
                     use_container_width=True, hide_index=True)
        pick = st.selectbox("Open a paper", [p["name"] for p in pdfs]); chosen = next(p for p in pdfs if p["name"] == pick)
        try:
            st.download_button("Download / open selected PDF", data=lib.read_pdf_bytes(chosen["path"]),
                               file_name=chosen["name"], mime="application/pdf")
        except Exception as e:
            st.warning(f"Couldn't read that file. ({e})")

def render_parks():
    section_header("African Parks", "Location, area and key species.")
    p = parkmod.get_park(st.selectbox("Park / landscape", parkmod.park_names()))
    c1, c2 = st.columns([2, 1], gap="large")
    with c1: st.map(pd.DataFrame({"lat": [p["lat"]], "lon": [p["lng"]]}), zoom=6)
    with c2:
        st.metric("Area", f"{p['area_km2']:,} km²"); st.metric("Area", f"{p['area_km2']*1_000_000:,} m²"); st.metric("Country", p["country"])
    eyebrow("Key species"); st.markdown(" ".join(badge(s, "good") for s in p["species"]), unsafe_allow_html=True)
    st.divider(); section_header("All parks — overview")
    st.dataframe(pd.DataFrame([{"Park": x["name"], "Country": x["country"], "Area (km²)": x["area_km2"],
                                "Key species": ", ".join(x["species"][:4])} for x in parkmod.PARKS]),
                 use_container_width=True, hide_index=True)
    st.map(pd.DataFrame([{"lat": x["lat"], "lon": x["lng"]} for x in parkmod.PARKS]), zoom=2)
    st.caption("Areas approximate — verify before publication.")


# =============================================================================
# SIDEBAR NAV + DISPATCH
# =============================================================================
if HAS_LOGO:
    try: st.logo(LOGO)
    except Exception: pass
    _lc = st.sidebar.columns([1, 2, 1])
    _lc[1].image(LOGO, width=160)
st.sidebar.markdown("<div style='font-family:Fraunces,serif;font-size:1.25rem;font-weight:600'>OCC AeroCount Studio</div>"
                    "<div style='font-size:.8rem;opacity:.8'>Aerial survey planning</div>", unsafe_allow_html=True)
st.sidebar.write("")
PLAN = st.sidebar.radio("Plan", ["Overview", "Guided Planner", "Survey Geometry", "Region & Season",
                                 "OCC vs RSO Cost", "Correction Factors", "Export / Summary"])
LEARN = st.sidebar.radio("Explore", ["— (stay on Plan) —", "News & Papers", "African Parks", "About / Methods"])
st.sidebar.write(""); st.sidebar.caption("Weather © Open-Meteo (CC BY 4.0)\nArticles © OpenAlex")

page = LEARN if LEARN != "— (stay on Plan) —" else PLAN
DISPATCH = {
    "Overview": render_overview, "Guided Planner": render_guided, "Survey Geometry": render_geometry,
    "Region & Season": render_region, "OCC vs RSO Cost": render_cost, "Correction Factors": render_correction,
    "Export / Summary": render_export, "News & Papers": render_news, "African Parks": render_parks,
    "About / Methods": render_methods,
}
DISPATCH[page]()
