from __future__ import annotations
import datetime as dt, requests, pandas as pd
ARCHIVE="https://archive-api.open-meteo.com/v1/archive"
FORECAST="https://api.open-meteo.com/v1/forecast"
MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
TIMEOUT=25
def monthly_climatology(lat,lng,years=20):
    end=dt.date.today(); start=end.replace(year=end.year-years)
    p={"latitude":lat,"longitude":lng,"start_date":start.isoformat(),"end_date":end.isoformat(),
       "daily":"precipitation_sum","timezone":"auto"}
    r=requests.get(ARCHIVE,params=p,timeout=TIMEOUT); r.raise_for_status()
    d=r.json()["daily"]
    df=pd.DataFrame({"date":pd.to_datetime(d["time"]),"rain":d["precipitation_sum"]}).dropna()
    df["month"]=df["date"].dt.month; df["year"]=df["date"].dt.year
    mt=df.groupby(["year","month"])["rain"].sum().reset_index()
    base=mt.groupby("month")["rain"].mean()
    cut=pd.Timestamp(end)-pd.DateOffset(months=12)
    rec=df[df["date"]>=cut].groupby("month")["rain"].sum()
    out=pd.DataFrame({"month":range(1,13)})
    out["Month"]=out["month"].map(lambda m:MONTHS[m-1])
    out["Baseline (mm)"]=out["month"].map(base).round(1)
    out["Last 12 mo (mm)"]=out["month"].map(rec).round(1)
    return out.set_index("Month")[["Baseline (mm)","Last 12 mo (mm)"]]
def best_survey_months(clim):
    b=clim["Baseline (mm)"].dropna().sort_values(); n=max(1,len(b)//3)
    return list(b.index[:n])
def forecast_16day(lat,lng):
    p={"latitude":lat,"longitude":lng,"hourly":"cloud_cover,precipitation_probability",
       "daily":"precipitation_probability_max,sunrise,sunset","forecast_days":16,"timezone":"auto"}
    r=requests.get(FORECAST,params=p,timeout=TIMEOUT); r.raise_for_status(); return r.json()
def daily_forecast_table(fc):
    d=fc["daily"]; h=fc["hourly"]
    hh=pd.DataFrame({"time":pd.to_datetime(h["time"]),"cloud":h["cloud_cover"]})
    hh["date"]=hh["time"].dt.date
    day=hh[(hh["time"].dt.hour>=8)&(hh["time"].dt.hour<=17)]
    cbd=day.groupby("date")["cloud"].mean().round(0)
    out=pd.DataFrame({"Date":pd.to_datetime(d["time"]).date,"Rain prob (%)":d["precipitation_probability_max"],
        "Sunrise":[t[-5:] for t in d["sunrise"]],"Sunset":[t[-5:] for t in d["sunset"]]})
    out["Daytime cloud (%)"]=out["Date"].map(cbd).values
    return out
