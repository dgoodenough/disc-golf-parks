"""Generate parks.json and viz.html (Leaflet map + sortable table)."""
import json
from pathlib import Path
from candidates import PARKS, METROS
from pop_within_radius import load_county_pop, pop_within, haversine_miles
from rubric import score_park

OUT = Path(__file__).parent
counties = load_county_pop()
metro_dt = {m[0]: (m[1], m[2]) for m in METROS}

parks = []
for metro, name, lat, lng, acres, notes in PARKS:
    pop, _ = pop_within(lat, lng, 100, counties)
    dlat, dlng = metro_dt[metro]
    dist_dt = haversine_miles(lat, lng, dlat, dlng)
    s = score_park(metro, name, acres, pop, dist_dt)
    blue_sky = s["Total"] - s["DG_Community"] + max(0, s["DG_Community"])
    parks.append({
        "metro": metro, "park": name, "lat": lat, "lng": lng,
        "acres": acres, "pop": pop, "miles": round(dist_dt, 1),
        "size": s["Size"], "amen": s["Amenities"], "cent": s["Centrality"],
        "park_": s["Parking"], "dg": s["DG_Community"], "popS": s["Population"],
        "hist": s["History"], "beauty": s["Beauty"],
        "total": s["Total"], "blueSky": blue_sky, "notes": notes,
    })
parks.sort(key=lambda p: (-p["blueSky"], p["metro"]))

html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>US Disc Golf Tournament Host Parks</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; font-size: 13px; color: #222; }
  #app { display: grid; grid-template-columns: 1fr 1fr; height: 100vh; }
  #map { height: 100vh; }
  #side { overflow: hidden; display: flex; flex-direction: column; border-left: 1px solid #ddd; }
  header { padding: 12px 16px; background: #1F4E78; color: white; display: flex; align-items: center; gap: 16px; }
  header h1 { margin: 0; font-size: 16px; font-weight: 600; }
  header .stats { font-size: 12px; opacity: 0.85; }
  .controls { padding: 8px 16px; background: #f7f7f7; border-bottom: 1px solid #ddd; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .controls input, .controls select { padding: 4px 8px; font-size: 12px; border: 1px solid #ccc; border-radius: 3px; }
  .controls label { font-size: 12px; color: #555; }
  .legend { display: flex; align-items: center; gap: 4px; margin-left: auto; }
  .legend span { display: inline-block; width: 14px; height: 14px; border-radius: 50%; border: 1px solid #333; }
  .table-wrap { overflow: auto; flex: 1; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  thead { position: sticky; top: 0; background: #1F4E78; color: white; z-index: 1; }
  th { padding: 6px 6px; text-align: center; cursor: pointer; user-select: none; font-weight: 600; white-space: nowrap; }
  th.sorted-asc::after { content: " ▲"; }
  th.sorted-desc::after { content: " ▼"; }
  th:hover { background: #2c5e8c; }
  td { padding: 4px 6px; border-bottom: 1px solid #eee; text-align: center; white-space: nowrap; }
  td.park, td.metro { text-align: left; }
  tr.hi { background: #FFF3B0 !important; }
  tr:nth-child(even) td { background: #fafafa; }
  tr:hover td { background: #e9f1fa; cursor: pointer; }
  tr.hi:hover td { background: #FFE873 !important; }
  .total-cell { font-weight: 700; }
  .dim-pos-3 { background: #63BE7B !important; color: #073; }
  .dim-pos-2 { background: #A0D89C !important; }
  .dim-pos-1 { background: #DCEFC9 !important; }
  .dim-zero { color: #999; }
  .dim-neg-1 { background: #FFE7CC !important; }
  .dim-neg-2 { background: #FFC080 !important; }
  .dim-neg-3 { background: #F8696B !important; color: #500; }
  .popup-title { font-weight: 700; margin-bottom: 4px; font-size: 13px; }
  .popup-row { font-size: 11px; color: #555; }
  .popup-total { font-weight: 700; font-size: 14px; margin-top: 4px; color: #1F4E78; }
</style>
</head>
<body>
<div id="app">
  <div id="map"></div>
  <div id="side">
    <header>
      <h1>US Disc Golf Tournament Host Parks</h1>
      <div class="stats" id="stats"></div>
    </header>
    <div class="controls">
      <input id="filter" placeholder="Filter park or metro..." style="width:200px">
      <label>Sort: <select id="sortBy">
        <option value="blueSky">Blue Sky Total</option>
        <option value="total">Classic Total</option>
        <option value="size">Size</option>
        <option value="amen">Amenities</option>
        <option value="cent">Centrality</option>
        <option value="park_">Parking</option>
        <option value="dg">DG Community</option>
        <option value="popS">Population</option>
        <option value="hist">History</option>
        <option value="beauty">Beauty</option>
        <option value="pop">Pop within 100mi</option>
        <option value="acres">Acres</option>
        <option value="miles">Miles to Downtown</option>
      </select></label>
      <div class="legend">
        <span style="background:#F8696B"></span>
        <span style="background:#FFEB84"></span>
        <span style="background:#63BE7B"></span>
        <span style="font-size:11px;margin-left:4px">low &rarr; high Blue Sky Total</span>
      </div>
    </div>
    <div class="table-wrap">
      <table id="tbl">
        <thead><tr id="thead"></tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const PARKS = __DATA__;
const COLUMNS = [
  {k:"blueSky", label:"BS",    title:"Blue Sky Total",   dim:true, tot:true},
  {k:"total",   label:"CL",    title:"Classic Total",    dim:true, tot:true},
  {k:"metro",   label:"Metro", title:"Metro",            cls:"metro"},
  {k:"park",    label:"Park",  title:"Park",             cls:"park"},
  {k:"size",    label:"Sz",    title:"Size",             dim:true},
  {k:"amen",    label:"Am",    title:"Amenities",        dim:true},
  {k:"cent",    label:"Ct",    title:"Centrality",       dim:true},
  {k:"park_",   label:"Pk",    title:"Parking",          dim:true},
  {k:"dg",      label:"DG",    title:"DG Community",     dim:true},
  {k:"popS",    label:"Po",    title:"Population score", dim:true},
  {k:"hist",    label:"Hi",    title:"History",          dim:true},
  {k:"beauty",  label:"Be",    title:"Beauty",           dim:true},
  {k:"acres",   label:"Ac",    title:"Acres",            num:true},
  {k:"pop",     label:"Pop",   title:"Pop within 100mi", num:true, fmt:n=>n.toLocaleString()},
  {k:"miles",   label:"Mi",    title:"Miles to downtown",num:true},
];

let sortKey = "blueSky";
let sortDir = -1;
let filter = "";
let selectedIdx = -1;

const dimClass = (v) => {
  if (v === 3) return "dim-pos-3";
  if (v === 2) return "dim-pos-2";
  if (v === 1) return "dim-pos-1";
  if (v === 0) return "dim-zero";
  if (v === -1) return "dim-neg-1";
  if (v === -2) return "dim-neg-2";
  if (v <= -3) return "dim-neg-3";
  if (v >= 13) return "dim-pos-3";
  if (v >= 10) return "dim-pos-2";
  if (v >= 7)  return "dim-pos-1";
  return "";
};
const totalClass = (v, max, min) => {
  const t = (v - min) / (max - min);
  if (t >= 0.8) return "dim-pos-3";
  if (t >= 0.6) return "dim-pos-2";
  if (t >= 0.4) return "dim-pos-1";
  if (t >= 0.2) return "dim-neg-1";
  return "dim-neg-2";
};
const totalColor = (v, max, min) => {
  const t = (v - min) / (max - min);
  if (t >= 0.7) return "#63BE7B";
  if (t >= 0.4) return "#FFEB84";
  return "#F8696B";
};

const buildThead = () => {
  document.getElementById("thead").innerHTML = COLUMNS.map(c =>
    `<th data-k="${c.k}" title="${c.title}">${c.label}</th>`).join("");
  document.querySelectorAll("th").forEach(th => {
    th.onclick = () => {
      const k = th.dataset.k;
      if (sortKey === k) sortDir *= -1;
      else { sortKey = k; sortDir = (k==="metro"||k==="park") ? 1 : -1; }
      document.getElementById("sortBy").value = COLUMNS.find(c=>c.k===k) ? k : sortKey;
      render();
    };
  });
};

const filtered = () => {
  const f = filter.toLowerCase().trim();
  let rows = PARKS.slice();
  if (f) rows = rows.filter(p => p.park.toLowerCase().includes(f) || p.metro.toLowerCase().includes(f));
  rows.sort((a,b) => {
    const va = a[sortKey], vb = b[sortKey];
    if (typeof va === "string") return va.localeCompare(vb) * sortDir;
    return (va - vb) * sortDir;
  });
  return rows;
};

let markers = {};
const map = L.map("map", {minZoom: 3, maxZoom: 13}).setView([39, -96], 4);
L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
  attribution: "&copy; OpenStreetMap &copy; CARTO",
  subdomains: "abcd", maxZoom: 19
}).addTo(map);

const max_total = Math.max(...PARKS.map(p => p.blueSky));
const min_total = Math.min(...PARKS.map(p => p.blueSky));
PARKS.forEach((p, i) => {
  const r = 5 + (p.blueSky - min_total) / Math.max(1, max_total - min_total) * 8;
  const m = L.circleMarker([p.lat, p.lng], {
    radius: r,
    fillColor: totalColor(p.blueSky, max_total, min_total),
    color: "#333", weight: 1, fillOpacity: 0.85
  });
  m.bindPopup(() => `
    <div class="popup-title">${p.park}</div>
    <div class="popup-row">${p.metro} &middot; ${p.acres} ac &middot; ${p.miles} mi to downtown</div>
    <div class="popup-row">Pop within 100mi: ${p.pop.toLocaleString()}</div>
    <div class="popup-total">Blue Sky: ${p.blueSky} &middot; Classic: ${p.total}</div>
    <div class="popup-row">Size ${p.size} | Amen ${p.amen} | Cent ${p.cent} | Park ${p.park_} | DG ${p.dg} | Pop ${p.popS} | Hist ${p.hist} | Beauty ${p.beauty}</div>
    <div class="popup-row" style="margin-top:4px;color:#666;font-style:italic">${p.notes||""}</div>
  `);
  m.on("click", () => {
    selectedIdx = i;
    render();
    const row = document.querySelector(`tr[data-i="${i}"]`);
    if (row) row.scrollIntoView({behavior:"smooth", block:"center"});
  });
  m.addTo(map);
  markers[i] = m;
});

const render = () => {
  const rows = filtered();
  document.getElementById("stats").textContent = `${rows.length} of ${PARKS.length} parks`;
  document.querySelectorAll("th").forEach(th => {
    th.classList.remove("sorted-asc","sorted-desc");
    if (th.dataset.k === sortKey) th.classList.add(sortDir === 1 ? "sorted-asc" : "sorted-desc");
  });
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = rows.map(p => {
    const i = PARKS.indexOf(p);
    return `<tr data-i="${i}" class="${i===selectedIdx?'hi':''}">` + COLUMNS.map(c => {
      const v = p[c.k];
      let cls = c.cls || "";
      if (c.tot) cls += " total-cell " + totalClass(v, max_total, min_total);
      else if (c.dim) cls += " " + dimClass(v);
      const txt = c.fmt ? c.fmt(v) : v;
      return `<td class="${cls}">${txt}</td>`;
    }).join("") + "</tr>";
  }).join("");
  tbody.querySelectorAll("tr").forEach(tr => {
    tr.onclick = () => {
      const i = parseInt(tr.dataset.i);
      selectedIdx = i;
      const p = PARKS[i];
      map.flyTo([p.lat, p.lng], 11, {duration: 0.6});
      markers[i].openPopup();
      render();
    };
  });
};

document.getElementById("filter").oninput = (e) => { filter = e.target.value; render(); };
document.getElementById("sortBy").onchange = (e) => {
  sortKey = e.target.value;
  sortDir = (sortKey==="metro"||sortKey==="park") ? 1 : -1;
  render();
};

buildThead();
render();
</script>
</body>
</html>"""

html = html.replace("__DATA__", json.dumps(parks, separators=(",", ":")))
(OUT / "parks.json").write_text(json.dumps(parks, indent=2))
out_html = OUT / "parks_viz.html"
out_html.write_text(html, encoding="utf-8")
print(f"Wrote: {out_html}")
print(f"Parks: {len(parks)}")
