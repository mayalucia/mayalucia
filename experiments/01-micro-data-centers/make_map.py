#!/usr/bin/env python3
"""
Interactive map: Himachal Pradesh — natural landscape + hydropower infrastructure.

Generates an HTML map showing:
- Clean terrain basemap (no roads, no city labels)
- DEM-derived river network with width proportional to catchment area
- Hydroelectric projects color-coded by basin, sized by capacity
- Natural landmarks: peaks, passes, lakes, glaciers, protected areas
- Mountain range labels
- Context panel with experiment framing

Usage:
    .venv/bin/python3 experiments/01-micro-data-centers/make_map.py
"""

import csv
import json
import os
import folium
from folium import IFrame
from folium.features import DivIcon
import branca.colormap as cm

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ── Load dam data ─────────────────────────────────────────────────────

def load_dams(csv_path):
    dams = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['lat'] = float(row['lat'])
            row['lon'] = float(row['lon'])
            row['capacity_mw'] = float(row['capacity_mw'])
            dams.append(row)
    return dams


# ── Color schemes ─────────────────────────────────────────────────────

BASIN_COLORS = {
    'Sutlej': '#e74c3c',   # red
    'Beas':   '#3498db',   # blue
    'Ravi':   '#2ecc71',   # green
    'Chenab': '#9b59b6',   # purple
    'Yamuna': '#f39c12',   # orange
}

STATUS_OPACITY = {
    'operational':        0.9,
    'under construction': 0.6,
    'proposed':           0.3,
}


def dam_radius(capacity_mw):
    """Circle radius proportional to sqrt(capacity)."""
    if capacity_mw <= 0:
        return 4
    return max(4, min(25, 3 + (capacity_mw ** 0.5) * 0.7))


# ── Natural landmarks ────────────────────────────────────────────────

# Mountain peaks (name, lat, lon, elevation_m)
PEAKS = [
    ("Reo Purgyil",         31.884,  78.733,  6816),
    ("Manirang",            31.953,  78.367,  6593),
    ("Mulkila",             32.545,  77.412,  6517),
    ("Indrasan",            32.213,  77.397,  6221),
    ("Shikar Beh",          32.436,  77.057,  6200),
    ("Kinnaur Kailash",     31.520,  78.363,  6050),
    ("Deo Tibba",           32.196,  77.383,  6001),
    ("Hanuman Tibba",       32.342,  77.041,  5982),
    ("Manimahesh Kailash",  32.352,  76.652,  5653),
    ("Shrikhand Mahadev",   31.659,  77.644,  5227),
    ("Friendship Peak",     32.396,  77.102,  5289),
]

# Mountain passes (name, lat, lon, elevation_m)
PASSES = [
    ("Rohtang Pass",       32.373,  77.248,  3978),
    ("Kunzum Pass",        32.416,  77.649,  4551),
    ("Baralacha La",       32.733,  77.433,  4890),
    ("Hampta Pass",        32.350,  77.217,  4270),
    ("Jalori Pass",        31.533,  77.367,  3120),
    ("Sach Pass",          33.006,  76.240,  4414),
    ("Chandrakhani Pass",  32.130,  77.200,  3660),
    ("Manirang Pass",      31.936,  78.344,  5550),
]

# Lakes (name, lat, lon, type)
LAKES = [
    ("Gobind Sagar",       31.417,  76.500,  "reservoir"),
    ("Chamera Lake",       32.597,  75.986,  "reservoir"),
    ("Pong Dam Lake",      32.017,  76.083,  "reservoir"),
    ("Chandratal",         32.476,  77.618,  "natural"),
    ("Suraj Tal",          32.750,  77.400,  "natural"),
    ("Manimahesh Lake",    32.390,  76.636,  "natural"),
    ("Prashar Lake",       31.754,  77.101,  "natural"),
    ("Bhrigu Lake",        32.370,  77.200,  "natural"),
    ("Beas Kund",          32.380,  77.100,  "natural"),
    ("Renuka Lake",        30.606,  77.455,  "natural"),
    ("Dal Lake",           32.247,  76.311,  "natural"),
]

# Glaciers (name, lat, lon, note)
GLACIERS = [
    ("Bara Shigri",   32.270,  77.667,  "largest glacier in HP, ~28 km"),
    ("Parvati Glacier",     32.050,  77.450,  "source of Parvati River"),
    ("Beas Kund Glacier",   32.390,  77.090,  "source of Beas River"),
]

# Protected areas (name, lat, lon, note)
PROTECTED_AREAS = [
    ("Great Himalayan NP",  31.737,  77.543,  "UNESCO WHS, 754 sq km"),
    ("Pin Valley NP",       31.571,  77.587,  "cold desert, 675 sq km"),
]

# Mountain ranges — labels only, placed for readability
RANGES = [
    ("Pir Panjal",               32.35,   77.10),
    ("Dhauladhar",               32.25,   76.32),
    ("Great Himalayan Range",    31.75,   77.55),
    ("Zanskar Range",            32.00,   78.50),
]

# River width → color mapping (for DEM-derived rivers)
RIVER_STYLES = {
    'major':     {'color': '#1a5276', 'weight': 4, 'opacity': 0.9},
    'medium':    {'color': '#2471a3', 'weight': 3, 'opacity': 0.8},
    'tributary': {'color': '#5dade2', 'weight': 2, 'opacity': 0.6},
    'stream':    {'color': '#85c1e9', 'weight': 1, 'opacity': 0.4},
}


# ── Build map ─────────────────────────────────────────────────────────

def build_map(dams):
    # Center on Kullu district
    m = folium.Map(
        location=[31.8, 77.1],
        zoom_start=8,
        tiles=None,
        control_scale=True,
    )

    # ── Clean terrain basemaps (no roads, no city labels) ──────────

    # OpenTopoMap — topographic with contours, minimal road noise
    folium.TileLayer(
        'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        name='Topographic',
        attr='OpenTopoMap contributors',
        max_zoom=17,
    ).add_to(m)

    # ESRI World Terrain — simple physical terrain, no labels
    folium.TileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/'
        'World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
        name='Terrain (clean)',
        attr='Esri, USGS, NOAA',
        max_zoom=13,
    ).add_to(m)

    # ESRI World Imagery — satellite, no auth required
    folium.TileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/'
        'World_Imagery/MapServer/tile/{z}/{y}/{x}',
        name='Satellite',
        attr='Esri, Maxar, Earthstar Geographics',
    ).add_to(m)

    # CartoDB Positron (no labels variant) — very clean light basemap
    folium.TileLayer(
        'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
        name='Light (no labels)',
        attr='CartoDB',
        max_zoom=20,
    ).add_to(m)

    # ── DEM-derived river network ──────────────────────────────────

    rivers_path = os.path.join(DATA, "rivers.geojson")
    if os.path.exists(rivers_path):
        with open(rivers_path) as f:
            rivers_geojson = json.load(f)

        # Group by river class for separate layers with different styles
        for river_class in ['major', 'medium', 'tributary', 'stream']:
            features = [feat for feat in rivers_geojson['features']
                        if feat['properties']['class'] == river_class]
            if not features:
                continue

            style = RIVER_STYLES[river_class]
            n_segments = len(features)
            n_pixels = sum(f['properties']['n_pixels'] for f in features)
            km_approx = n_pixels * 0.090  # ~90m per pixel

            layer_name = f"Rivers — {river_class} ({n_segments} segments, ~{km_approx:.0f} km)"
            # Show major and medium by default, tributaries on toggle
            show = river_class in ('major', 'medium', 'tributary')

            fg = folium.FeatureGroup(name=layer_name, show=show)

            for feat in features:
                coords = feat['geometry']['coordinates']
                # folium wants (lat, lon) not (lon, lat)
                latlngs = [[c[1], c[0]] for c in coords]
                folium.PolyLine(
                    locations=latlngs,
                    color=style['color'],
                    weight=style['weight'],
                    opacity=style['opacity'],
                ).add_to(fg)

            fg.add_to(m)

    # ── Dam layers per basin ───────────────────────────────────────

    basin_stats = {}
    for dam in dams:
        basin = dam['basin']
        if basin not in basin_stats:
            basin_stats[basin] = {'count': 0, 'total_mw': 0,
                                  'operational_mw': 0, 'count_operational': 0}
        basin_stats[basin]['count'] += 1
        basin_stats[basin]['total_mw'] += dam['capacity_mw']
        if dam['status'] == 'operational':
            basin_stats[basin]['operational_mw'] += dam['capacity_mw']
            basin_stats[basin]['count_operational'] += 1

    for basin_name in BASIN_COLORS:
        basin_dams = [d for d in dams if d['basin'] == basin_name]
        if not basin_dams:
            continue

        stats = basin_stats[basin_name]
        layer_name = (f"{basin_name} basin — "
                      f"{stats['count']} projects, "
                      f"{stats['total_mw']:.0f} MW")

        fg = folium.FeatureGroup(name=layer_name, show=True)

        for dam in basin_dams:
            color = BASIN_COLORS[basin_name]
            opacity = STATUS_OPACITY.get(dam['status'], 0.5)
            radius = dam_radius(dam['capacity_mw'])

            popup_html = f"""
            <div style="font-family: sans-serif; width: 260px;">
                <h4 style="margin: 0 0 6px 0; color: {color};">{dam['name']}</h4>
                <table style="font-size: 12px; border-collapse: collapse;">
                    <tr><td style="padding: 2px 8px 2px 0; font-weight: bold;">River</td>
                        <td>{dam['river']}</td></tr>
                    <tr><td style="padding: 2px 8px 2px 0; font-weight: bold;">Type</td>
                        <td>{dam['type']}</td></tr>
                    <tr><td style="padding: 2px 8px 2px 0; font-weight: bold;">Capacity</td>
                        <td>{dam['capacity_mw']:.0f} MW</td></tr>
                    <tr><td style="padding: 2px 8px 2px 0; font-weight: bold;">Status</td>
                        <td>{dam['status']}</td></tr>
                    <tr><td style="padding: 2px 8px 2px 0; font-weight: bold;">Operator</td>
                        <td>{dam['operator']}</td></tr>
                </table>
            </div>
            """
            folium.CircleMarker(
                location=[dam['lat'], dam['lon']],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=opacity,
                opacity=opacity,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{dam['name']} ({dam['capacity_mw']:.0f} MW)",
            ).add_to(fg)

        fg.add_to(m)

    # ── Natural landmarks ──────────────────────────────────────────

    # Mountain peaks
    fg_peaks = folium.FeatureGroup(name='Mountain peaks', show=True)
    for name, lat, lon, elev in PEAKS:
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(0, 0),
                html=f'<div style="font-size:10px; color:#4a2810; '
                     f'font-weight:bold; white-space:nowrap; '
                     f'text-shadow: 1px 1px 2px white, -1px -1px 2px white, '
                     f'1px -1px 2px white, -1px 1px 2px white;">'
                     f'&#9650; {name} ({elev}m)</div>',
            ),
            tooltip=f"{name} — {elev}m",
        ).add_to(fg_peaks)
    fg_peaks.add_to(m)

    # Mountain passes
    fg_passes = folium.FeatureGroup(name='Mountain passes', show=True)
    for name, lat, lon, elev in PASSES:
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(0, 0),
                html=f'<div style="font-size:9px; color:#6c3483; '
                     f'white-space:nowrap; '
                     f'text-shadow: 1px 1px 2px white, -1px -1px 2px white, '
                     f'1px -1px 2px white, -1px 1px 2px white;">'
                     f'&#10006; {name} ({elev}m)</div>',
            ),
            tooltip=f"{name} — {elev}m",
        ).add_to(fg_passes)
    fg_passes.add_to(m)

    # Lakes
    fg_lakes = folium.FeatureGroup(name='Lakes & water bodies', show=True)
    for name, lat, lon, lake_type in LAKES:
        color = '#2e86c1' if lake_type == 'natural' else '#1b4f72'
        radius = 6 if lake_type == 'reservoir' else 4
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color='#85c1e9',
            fill_opacity=0.7,
            opacity=0.9,
            tooltip=f"{name} ({lake_type})",
        ).add_to(fg_lakes)
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(-8, 0),
                html=f'<div style="font-size:9px; color:#1b4f72; '
                     f'white-space:nowrap; '
                     f'text-shadow: 1px 1px 2px white, -1px -1px 2px white, '
                     f'1px -1px 2px white, -1px 1px 2px white;">'
                     f'{name}</div>',
            ),
        ).add_to(fg_lakes)
    fg_lakes.add_to(m)

    # Glaciers
    fg_glaciers = folium.FeatureGroup(name='Glaciers', show=True)
    for name, lat, lon, note in GLACIERS:
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(0, 0),
                html=f'<div style="font-size:9px; color:#1abc9c; '
                     f'font-style:italic; white-space:nowrap; '
                     f'text-shadow: 1px 1px 2px white, -1px -1px 2px white, '
                     f'1px -1px 2px white, -1px 1px 2px white;">'
                     f'&#9724; {name}</div>',
            ),
            tooltip=f"{name} — {note}",
        ).add_to(fg_glaciers)
    fg_glaciers.add_to(m)

    # Protected areas (shown as translucent circles)
    fg_protected = folium.FeatureGroup(name='Protected areas', show=True)
    for name, lat, lon, note in PROTECTED_AREAS:
        folium.Circle(
            location=[lat, lon],
            radius=15000,  # ~15km radius for visibility
            color='#27ae60',
            fill=True,
            fill_color='#27ae60',
            fill_opacity=0.08,
            opacity=0.4,
            dash_array='5,8',
            tooltip=f"{name} — {note}",
        ).add_to(fg_protected)
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(0, 0),
                html=f'<div style="font-size:10px; color:#1e8449; '
                     f'font-weight:bold; white-space:nowrap; '
                     f'text-shadow: 1px 1px 2px white, -1px -1px 2px white, '
                     f'1px -1px 2px white, -1px 1px 2px white;">'
                     f'{name}</div>',
            ),
        ).add_to(fg_protected)
    fg_protected.add_to(m)

    # Mountain range labels (large, angled text)
    fg_ranges = folium.FeatureGroup(name='Mountain ranges', show=True)
    for name, lat, lon in RANGES:
        folium.Marker(
            location=[lat, lon],
            icon=DivIcon(
                icon_size=(0, 0),
                icon_anchor=(0, 0),
                html=f'<div style="font-size:13px; color:rgba(90,60,30,0.7); '
                     f'font-weight:bold; font-style:italic; '
                     f'letter-spacing:3px; white-space:nowrap; '
                     f'transform: rotate(-15deg); '
                     f'text-shadow: 1px 1px 3px rgba(255,255,255,0.8), '
                     f'-1px -1px 3px rgba(255,255,255,0.8);">'
                     f'{name.upper()}</div>',
            ),
        ).add_to(fg_ranges)
    fg_ranges.add_to(m)

    # ── Context panel (bottom-left) ────────────────────────────────

    total_mw = sum(d['capacity_mw'] for d in dams)
    total_op = sum(d['capacity_mw'] for d in dams if d['status'] == 'operational')
    total_uc = sum(d['capacity_mw'] for d in dams if d['status'] == 'under construction')
    total_pr = sum(d['capacity_mw'] for d in dams if d['status'] == 'proposed')

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px;
        left: 10px;
        width: 340px;
        background: rgba(255,255,255,0.92);
        border: 2px solid #333;
        border-radius: 8px;
        padding: 14px;
        font-family: sans-serif;
        font-size: 12px;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        max-height: 90vh;
        overflow-y: auto;
    ">
        <h3 style="margin: 0 0 8px 0; font-size: 14px;">
            Himachal Pradesh — Landscape &amp; Hydropower
        </h3>

        <p style="margin: 0 0 8px 0; font-size: 11px; color: #555;">
            {len(dams)} projects mapped &mdash;
            {total_op:.0f} MW operational,
            {total_uc:.0f} MW under construction,
            {total_pr:.0f} MW proposed
        </p>

        <table style="font-size: 11px; border-collapse: collapse; width: 100%; margin-bottom: 10px;">
            <tr style="border-bottom: 1px solid #ddd;">
                <th style="text-align: left; padding: 3px;">Basin</th>
                <th style="text-align: right; padding: 3px;">Projects</th>
                <th style="text-align: right; padding: 3px;">MW</th>
            </tr>
    """
    for basin_name in ['Sutlej', 'Beas', 'Ravi', 'Chenab', 'Yamuna']:
        if basin_name in basin_stats:
            s = basin_stats[basin_name]
            color = BASIN_COLORS[basin_name]
            legend_html += f"""
            <tr>
                <td style="padding: 3px;">
                    <span style="color: {color}; font-size: 16px;">&#9679;</span>
                    {basin_name}
                </td>
                <td style="text-align: right; padding: 3px;">{s['count']}</td>
                <td style="text-align: right; padding: 3px;">{s['total_mw']:.0f}</td>
            </tr>
            """

    legend_html += """
        </table>

        <div style="font-size: 11px; margin-bottom: 8px;">
            <b>Hydropower circles</b>: size = capacity,
            opacity: solid = operational,
            semi = under construction,
            faint = proposed
        </div>

        <div style="font-size: 11px; margin-bottom: 8px;">
            <b>Rivers</b> (from SRTM DEM, D8 flow routing):<br>
            <span style="color: #1a5276;">&#9644;</span> major &nbsp;
            <span style="color: #2471a3;">&#9644;</span> medium &nbsp;
            <span style="color: #5dade2;">&#9644;</span> tributary &nbsp;
            <span style="color: #85c1e9;">&#9644;</span> stream
        </div>

        <div style="font-size: 11px; margin-bottom: 8px;">
            <span style="color: #4a2810;">&#9650;</span> peaks &nbsp;
            <span style="color: #6c3483;">&#10006;</span> passes &nbsp;
            <span style="color: #1b4f72;">&#9679;</span> lakes &nbsp;
            <span style="color: #1abc9c;">&#9724;</span> glaciers &nbsp;
            <span style="color: #27ae60;">&#9675;</span> protected areas
        </div>

        <hr style="margin: 8px 0; border: none; border-top: 1px solid #ccc;">

        <h4 style="margin: 0 0 6px 0; font-size: 12px; color: #c0392b;">
            Experiment: Micro-Data-Centers
        </h4>
        <p style="margin: 0; font-size: 11px; color: #555; line-height: 1.4;">
            Can a network of micro-data-centers, distributed along a
            mountain river &mdash; powered by micro-hydro and solar,
            cooled by glacial water &mdash; provide meaningful
            computation within ecological limits?
            <br><br>
            This map shows the natural landscape of Himachal Pradesh
            overlaid with industrial hydropower infrastructure that has
            transformed its rivers. Every blue line was computed from
            the DEM &mdash; the rivers these dams tap.
        </p>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)

    return m


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    csv_path = os.path.join(HERE, 'dams.csv')
    dams = load_dams(csv_path)
    print(f"Loaded {len(dams)} dams from {csv_path}")

    m = build_map(dams)

    out_path = os.path.join(HERE, 'map.html')
    m.save(out_path)
    print(f"Saved interactive map: {out_path}")
    print(f"Open in browser: file://{out_path}")
