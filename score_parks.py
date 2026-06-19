"""Score every candidate park: pop-within-100mi + distance to downtown + base rubric."""
import math
import numpy as np
import pandas as pd
from pathlib import Path
from candidates import PARKS, METROS
from pop_within_radius import load_county_pop, pop_within, haversine_miles

OUT = Path(__file__).parent / "data"
counties = load_county_pop()
metro_dict = {m[0]: (m[1], m[2]) for m in METROS}

rows = []
for metro, name, lat, lng, acres, notes in PARKS:
    pop, n_cty = pop_within(lat, lng, 100, counties)
    dlat, dlng = metro_dict[metro]
    dist_dt = haversine_miles(lat, lng, dlat, dlng)
    rows.append({
        "Metro": metro,
        "Park": name,
        "Lat": lat,
        "Lng": lng,
        "Acres": acres,
        "Pop_100mi": pop,
        "Counties_100mi": n_cty,
        "Miles_to_Downtown": round(dist_dt, 1),
        "Notes": notes,
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "parks_with_pop.csv", index=False)
print(f"Scored {len(df)} parks across {df['Metro'].nunique()} metros")
print()
print("Top 10 by Pop_100mi:")
print(df.nlargest(10, "Pop_100mi")[["Metro", "Park", "Pop_100mi", "Miles_to_Downtown"]].to_string(index=False))
print()
print("Pop_100mi range:")
print(df["Pop_100mi"].describe().astype(int))
