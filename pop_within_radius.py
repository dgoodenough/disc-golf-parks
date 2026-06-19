"""Compute US population within a radius of a lat/lng point using county centroids."""
import pandas as pd
import math
from pathlib import Path

DATA = Path(__file__).parent / "data"

def load_county_pop():
    pop = pd.read_csv(DATA / "co-est2024-alldata.csv", encoding="latin-1")
    pop = pop[pop["SUMLEV"] == 50].copy()
    pop["GEOID"] = pop["STATE"] * 1000 + pop["COUNTY"]
    gaz = pd.read_csv(DATA / "gaz" / "2024_Gaz_counties_national.txt", sep="\t")
    gaz.columns = [c.strip() for c in gaz.columns]
    merged = pop.merge(gaz[["GEOID", "INTPTLAT", "INTPTLONG"]], on="GEOID", how="inner")
    return merged[["GEOID", "STNAME", "CTYNAME", "POPESTIMATE2024", "INTPTLAT", "INTPTLONG"]]

def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3958.7613
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def pop_within(lat, lng, miles, counties_df):
    R = 3958.7613
    lat_r = math.radians(lat)
    lng_r = math.radians(lng)
    clat = counties_df["INTPTLAT"].to_numpy()
    clng = counties_df["INTPTLONG"].to_numpy()
    import numpy as np
    clat_r = np.radians(clat)
    clng_r = np.radians(clng)
    dlat = clat_r - lat_r
    dlng = clng_r - lng_r
    a = np.sin(dlat/2)**2 + math.cos(lat_r)*np.cos(clat_r)*np.sin(dlng/2)**2
    dist = 2 * R * np.arcsin(np.sqrt(a))
    mask = dist <= miles
    return int(counties_df.loc[mask, "POPESTIMATE2024"].sum()), int(mask.sum())

if __name__ == "__main__":
    counties = load_county_pop()
    print(f"Loaded {len(counties)} counties, total pop: {counties['POPESTIMATE2024'].sum():,}")
    tests = [
        ("Forest Park, St Louis", 38.6357, -90.2845),
        ("Grant Park, Chicago", 41.8757, -87.6189),
        ("Central Park, NYC", 40.7829, -73.9654),
        ("Denver City Park", 39.7461, -104.9486),
        ("Zilker Park, Austin", 30.2669, -97.7729),
    ]
    for name, lat, lng in tests:
        pop, n = pop_within(lat, lng, 100, counties)
        print(f"{name:30s} {pop:>12,}  ({n} counties)")
