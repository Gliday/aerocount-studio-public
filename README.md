# AeroCount Studio

A Python web app for planning oblique camera count (OCC) aerial wildlife surveys,
built as part of Save the Elephants' Aerial Survey Reform work in Kenya.

## What it does
- **Guided planner:** step-by-step OCC survey design
- **Survey geometry:** oblique camera footprint and strip-width calculations
- **Survey area:** upload a boundary (GeoJSON, KML, KMZ or CSV) and compute its geodesic area
- **Region & season:** 20-year rainfall climatology (Open-Meteo API) and solar elevation to plan flight windows
- **Cost comparison:** OCC image-interpretation effort vs rear-seat observer (RSO) survey costs
- **News & papers:** live feed of recent aerial-survey and detection research (OpenAlex API)
- **African parks:** reference data for key protected areas

## Built with
Python · Streamlit · pandas · NumPy · Altair · Pillow

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```

## Note
This is a showcase version of a private tool. Survey data, imagery,
background photos and the reference-paper library are not included.

Developed by Yuka Gliday