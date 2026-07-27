# -*- coding: utf-8 -*-
"""Kvintána — static map builder.

Fetches OpenStreetMap tiles around the club's address once, stitches them,
grades them into the site palette and writes assets/img/map-*.webp|jpg.

Why static rather than an <iframe>:
  · the default OSM style is bright and fights the dark design
  · no third-party frame, no cookies, nothing to fail at runtime
  · one polite fetch at build time instead of a tile request per visitor

Attribution to OpenStreetMap contributors is still required and is rendered
on the contact page next to the map.

    python3 tools/build_map.py        # needs network + ImageMagick
"""

import math
import os
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
CACHE = os.path.join(ROOT, "tools", ".tilecache")

ZOOM = 15
COLS, ROWS = 9, 6          # 2304 x 1536 px of tiles
TILE = 256
UA = "KvintanaSitePrototype/1.0 (static map build; +https://kvintana.cz)"


def deg2tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y


def fetch(z, x, y):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "%d-%d-%d.png" % (z, x, y))
    if os.path.exists(path):
        return path
    url = "https://tile.openstreetmap.org/%d/%d/%d.png" % (z, x, y)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
        f.write(r.read())
    time.sleep(0.12)          # stay well inside the tile usage policy
    return path


def main():
    lat, lon = SITE["lat"], SITE["lon"]
    fx, fy = deg2tile(lat, lon, ZOOM)
    x0 = int(fx) - COLS // 2
    y0 = int(fy) - ROWS // 2

    print("Fetching %d tiles at z%d …" % (COLS * ROWS, ZOOM))
    rows = []
    for ry in range(ROWS):
        cols = [fetch(ZOOM, x0 + rx, y0 + ry) for rx in range(COLS)]
        rows.append(cols)

    # pixel position of the marker inside the stitched sheet
    px = int((fx - x0) * TILE)
    py = int((fy - y0) * TILE)

    sheet = os.path.join(CACHE, "_sheet.png")
    args = ["magick", "montage"]
    for r in rows:
        args += r
    args += ["-tile", "%dx%d" % (COLS, ROWS), "-geometry", "+0+0", sheet]
    subprocess.run(args, check=True)

    # crop a 21:9 band centred on the marker
    cw, ch = 1800, 771
    cx = max(0, min(px - cw // 2, COLS * TILE - cw))
    cy = max(0, min(py - ch // 2, ROWS * TILE - ch))
    mx, my = px - cx, py - cy

    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, "map-siroky-dul")

    # grade to match the site, then drop an ember pin on the address
    pin = (
        "-fill '#e86a32' -stroke '#14100e' -strokewidth 2 "
        "-draw \"circle %d,%d %d,%d\" "
        "-fill none -stroke '#e86a32' -strokewidth 2 "
        "-draw \"circle %d,%d %d,%d\""
    ) % (mx, my, mx + 9, my, mx, my, mx + 26, my)

    cmd = (
        "magick '{sheet}' -crop {cw}x{ch}+{cx}+{cy} +repage "
        "-modulate 100,32,100 "
        "-sigmoidal-contrast 4,52% "
        "-fill '#1b1310' -colorize 64% "
        "-brightness-contrast -8x16 "
        "{pin} "
    ).format(sheet=sheet, cw=cw, ch=ch, cx=cx, cy=cy, pin=pin)

    for w in (1800, 1200, 800):
        subprocess.run(cmd + "-resize %dx -quality 82 '%s-%d.webp'" % (w, base, w),
                       shell=True, check=True)
    subprocess.run(cmd + "-resize 1200x -quality 82 '%s.jpg'" % base,
                   shell=True, check=True)
    print("Wrote %s-{1800,1200,800}.webp + .jpg" % base)


if __name__ == "__main__":
    main()
