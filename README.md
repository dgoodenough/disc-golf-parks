# Disc Golf Tournament Host Park Analysis

A data-driven ranking of U.S. parks best positioned to host a **USDGC-equivalent
major** disc golf tournament — a metro-based, large-spectator event, distinct
from the smaller-town majors (DDO/Emporia, etc.).

It scores **103 candidate parks across 30 metros** on an eight-dimension rubric
and produces two rankings, a formatted Excel workbook, and an interactive
Leaflet map.

## Two rankings: Blue Sky vs. Classic

This is a **blue-sky** exercise — the goal is identifying where a major *could*
work, not just where the existing disc golf community already turns out. A major
in LA / NYC / Miami would *plant the flag* in those markets rather than follow
existing turnout.

- **Blue Sky Total** *(primary)* — the DG-Community penalty is removed, so a weak
  local scene can't drag an otherwise-iconic park below zero on that axis.
  Positive DG bonuses are still kept.
- **Classic Total** — the original methodology, with the full DG-Community
  penalty applied.

## The rubric

Each dimension scores −3 to +3; the dimensions are summed for the Total.

| Dimension | What it measures |
|---|---|
| **Size** | Park acreage (`<50` → `140+`) |
| **Amenities** | Paths → bathrooms → buildings → notable / large structures |
| **Centrality** | Straight-line distance to downtown, with manual transit overrides |
| **Parking** | None → players-only → VIP fans → GA fans |
| **DG Community** | Metro UDisc Health (higher of Variety or Availability) |
| **Population** | People in counties whose centroid is within 100 mi of the park |
| **History** | Narrative hook / age (+) vs. contaminated land, cemetery (−) |
| **Beauty** | Waterfront, tree variety, vistas (+) vs. highway-adjacent, golf course (−) |

**Calibration anchors:** Winthrop / USDGC = 8 (what a "good" major looks like),
European Open (The Beast) = 7. Small-town majors (DDO/Emporia, Harmony Bends)
intentionally score negative — the rubric targets metro events.

## How it works

```
candidates.py        103 parks (metro, name, lat/lng, acres, notes) + metro downtown coords
rubric.py            scoring logic, per-metro DG_COMMUNITY, PARK_OVERRIDES
pop_within_radius.py population within a radius via county centroids (2024 Census)
score_parks.py       quick scorer → data/parks_with_pop.csv
build.py             builds the ranked Excel workbook (5 sheets)
build_viz.py         builds parks.json + parks_viz.html (Leaflet map + sortable table)
```

The workbook has five sheets: **Blue Sky Rankings**, **Classic Rankings**,
**By Metro** (within-metro comparison), **Criteria** (the rubric reference), and
**Reference Anchors** (Winthrop / EO / DDO, for sanity-checking the scale).

## Running it

```bash
pip install -r requirements.txt
python build.py        # → "Disc Golf Tournament Parks - 2026 Refresh.xlsx"
python build_viz.py    # → parks.json + parks_viz.html
```

## Data sources & caveats

- **Population** — U.S. Census Bureau 2024 county population estimates
  (`co-est2024-alldata`) + 2024 county Gazetteer centroids. Both public domain.
- **Acreage** — city park systems, Wikipedia, TPL ParkServe. Cross-check before
  any production use.
- **Amenities / History / Beauty** are judgment calls — treat scores as starting
  points, not gospel.
- **Centrality** uses straight-line distance with manual overrides; it doesn't
  fully capture last-mile transit quality.

## License

[MIT](LICENSE).
