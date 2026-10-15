"""
occ/presets.py
Survey configuration presets grounded in published OCC studies, and the
published RSO/total-count-vs-camera detection probabilities / Jolly II
correction factors. Depression = angle below horizontal.
Sources: Ngene et al. 2017; Lamprey et al. 2020; Lamprey 2021; Delplanque
et al. 2024; Lamprey 2025 (synthesised in the ASR literature review, 2026).
"""

PRESETS = {
    "Custom — Samburu default": {
        "aircraft": "Generic (Sony A7 IV, 50 mm)",
        "hagl": 350, "speed_ms": 58, "interval_s": 2.0,
        "sensor_w": 35.9, "sensor_h": 23.9, "img_w": 7008, "img_h": 4672,
        "focal": 50.0, "mode": "Oblique", "depression": 35, "overlap": 20,
        "strata": [{"name": "Samburu NR", "area_km2": 165, "spacing_m": 2000}],
        "source": "Generic full-frame starting point — edit freely.",
    },
    "Tsavo OCC (TS1) — Lamprey et al. 2020": {
        "aircraft": "Cessna 206",
        "hagl": 107, "speed_ms": 46, "interval_s": 2.0,
        "sensor_w": 23.5, "sensor_h": 15.6, "img_w": 6016, "img_h": 4000,
        "focal": 42.0, "mode": "Oblique", "depression": 33, "overlap": 46,
        "strata": [
            {"name": "Tsavo Core", "area_km2": 9560, "spacing_m": 2500},
            {"name": "Outer blocks (N/NW/S/E)", "area_km2": 24171, "spacing_m": 5000},
        ],
        "source": ("Lamprey et al. 2020, Biol. Conserv. 108243 — Nikon D3200 24 MP, 42 mm, "
                   "57° from vertical, 350 ft HAGL, ISO ≤400, ≤1/1000 s, 2 s, 89 kn; ~150 m strip/side."),
    },
    "Murchison OCC — Lamprey et al. 2020": {
        "aircraft": "Cessna 210",
        "hagl": 152, "speed_ms": 54, "interval_s": 2.0,
        "sensor_w": 23.5, "sensor_h": 15.6, "img_w": 6016, "img_h": 4000,
        "focal": 35.0, "mode": "Oblique", "depression": 45, "overlap": 46,
        "strata": [
            {"name": "Block 1 (high density)", "area_km2": 1000, "spacing_m": 2500},
            {"name": "Rest of MFPA", "area_km2": 4037, "spacing_m": 5000},
        ],
        "source": ("Lamprey et al. 2020, RSE&C 6(4):529 — Nikon D3200, 35 mm, 45°, 500 ft HAGL, "
                   "ISO ≥800, ≥1/1000 s, 2 s, 105 kn; MFPA 5037 km². Per-stratum areas approximate."),
    },
    "Comoé SADL-OCC — Delplanque et al. 2024": {
        "aircraft": "Cessna 206",
        "hagl": 91, "speed_ms": 49, "interval_s": 2.0,
        "sensor_w": 23.5, "sensor_h": 15.6, "img_w": 6000, "img_h": 4000,
        "focal": 35.0, "mode": "Oblique", "depression": 53, "overlap": 46,
        "strata": [{"name": "Comoé NP (approx)", "area_km2": 11500, "spacing_m": 2500}],
        "source": ("Delplanque et al. 2024, Ecol. Informatics 82:102679 — Nikon D5600 24 MP, "
                   "35 mm, 36.5° from vertical, ~91 m HAGL, ≥1/2000 s, 2 s; 150 m strip/side; "
                   "HerdNet SADL pipeline. 190,686 images (148,239 on-transect). Strip validated by SWC."),
    },
    "KAZA OCC — Lamprey 2025": {
        "aircraft": "Cessna 210-class (V5-IIM/WOT/LJB)",
        "hagl": 91, "speed_ms": 49, "interval_s": 2.0,
        "sensor_w": 35.9, "sensor_h": 23.9, "img_w": 7008, "img_h": 4672,
        "focal": 40.0, "mode": "Oblique", "depression": 39, "overlap": 46,
        "strata": [{"name": "KAZA survey block (edit area)", "area_km2": 100000, "spacing_m": 5000}],
        "source": ("Lamprey 2025, KAZA OCC-RSO Output 3 — Sony Alpha 7 IV 33 MP full-frame, ~300 ft "
                   "HAGL; frame edges 62 m (inner) to 219 m (outer) from nadir. 2022 survey: ~250,000 "
                   "images over 43 blocks. Depression derived from published frame edges; edit block area."),
    },
    "Tsavo viewing-angle (600 ft) — Lamprey 2021": {
        "aircraft": "Cessna 182 / 206 (twin-transect)",
        "hagl": 183, "speed_ms": 49, "interval_s": 2.0,
        "sensor_w": 23.5, "sensor_h": 15.6, "img_w": 6016, "img_h": 4000,
        "focal": 35.0, "mode": "Oblique", "depression": 45, "overlap": 46,
        "strata": [{"name": "Voi Test Area", "area_km2": 500, "spacing_m": 1000}],
        "source": ("Lamprey 2021, Tsavo vertical-vs-oblique trial — Nikon D3300 oblique, 600 ft "
                   "HAGL (GPS-DEM/HTF), twin-transect 195–200 m apart, 435 m combined footprint. "
                   "Oblique detected up to 7–11× more animals than vertical under canopy."),
    },
}

# Detection probability (Pd, %) and Jolly II correction factor (Cd = 1/Pd).
# Apply cautiously — species/site/season specific.
CORRECTION_FACTORS = [
    ("Elephant", 96.3, 1.04, "Tsavo OCC 2020"),
    ("Buffalo", 92.6, 1.08, "Tsavo OCC 2020"),
    ("Giraffe", 90.9, 1.10, "Tsavo OCC 2020"),
    ("Zebra", 78.2, 1.28, "Tsavo OCC 2020"),
    ("Hartebeest", 72.7, 1.38, "Tsavo OCC 2020"),
    ("Eland", 81.3, 1.23, "Tsavo OCC 2020"),
    ("Oryx", 45.4, 2.20, "Tsavo OCC 2020"),
    ("Waterbuck", 60.7, 1.65, "Tsavo OCC 2020"),
    ("Impala", 82.0, 1.22, "Tsavo OCC 2020"),
    ("Grant's gazelle", 38.1, 2.62, "Tsavo OCC 2020"),
    ("Thomson's gazelle", 20.8, 4.80, "Tsavo OCC 2020"),
    ("All antelopes", 67.1, 1.49, "Tsavo OCC 2020"),
    ("Uganda kob", 55.0, 1.81, "Murchison 2020"),
    ("Hartebeest (MFPA)", 80.0, 1.25, "Murchison 2020"),
    ("Waterbuck (MFPA)", 49.0, 2.03, "Murchison 2020"),
    ("Elephant (KAZA)", 89.7, 1.115, "KAZA 2025"),
    ("Giraffe (KAZA)", 87.7, 1.14, "KAZA 2025"),
]

# Total-Count-vs-OCC non-detection (Tsavo 2017 total count vs OCC; Lamprey 2020):
# elephant 27% missed, buffalo 33%, giraffe 57%, carcasses 85%.
TOTAL_COUNT_MISS = [
    ("Elephant", 27, 1.37), ("Buffalo", 33, 1.49), ("Giraffe", 57, 2.33), ("Carcasses", 85, 6.67),
]


def preset_names():
    return list(PRESETS.keys())
