#!/bin/bash
# Kvintána — asset pipeline
# Grades the original photos into the "Ember & Night" look and emits
# responsive AVIF + WebP (+ a JPG fallback) into assets/img/.
#
# Idempotent: existing outputs are kept, only missing files are generated —
# so adding a format (or a photo) never re-encodes the rest.
#
# Requires ImageMagick 7 with AVIF support (`brew install imagemagick`).
# Usage:  sh tools/build_images.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${SRC:-$ROOT/photos/original}"
OUT="$ROOT/assets/img"
WIDTHS=(2000 1200 800 400)
TMP=/tmp/kv-graded.miff

mkdir -p "$OUT"

# The grade: pull saturation back, gentle S-curve, warm the reds / cool-down the
# blues, then a thin ember cast. Keeps firelight glowing without wrecking the
# daylight photos.
grade() {
  magick "$1" \
    -auto-orient \
    -strip \
    -modulate 100,86,100 \
    -sigmoidal-contrast 3.5,48% \
    -channel R -evaluate multiply 1.05 \
    -channel B -evaluate multiply 0.93 +channel \
    -fill '#2E1608' -colorize 7% \
    miff:-
}

# Grade lazily: only when this photo actually has something to emit.
graded() {
  [ -s "$TMP" ] || grade "$CUR" > "$TMP"
  echo "$TMP"
}

# AVIF q50 lands visually next to WebP q78 at ~60% of the bytes.
enc() { # <width> <ext> <outfile>
  case "$2" in
    webp) magick "$(graded)" -resize "$1x" -quality 78 -define webp:method=6 "$3" ;;
    avif) magick "$(graded)" -resize "$1x" -quality 50 "$3" ;;
  esac
}

emit() {
  local name="$2" native made=0
  CUR="$1"
  rm -f "$TMP"
  native=$(magick identify -format '%w' "$CUR")

  for w in "${WIDTHS[@]}"; do
    # never upscale past the native resolution
    [ "$w" -gt "$native" ] && continue
    for ext in avif webp; do
      [ -f "$OUT/${name}-${w}.${ext}" ] && continue
      enc "$w" "$ext" "$OUT/${name}-${w}.${ext}"
      made=$((made + 1))
    done
  done

  # smallest available width, so tiny sources still get one file per format
  for ext in avif webp; do
    if ! ls "$OUT/${name}"-*."$ext" >/dev/null 2>&1; then
      enc "$native" "$ext" "$OUT/${name}-${native}.${ext}"
      made=$((made + 1))
    fi
  done

  # JPG fallback at a middling width
  local fb=1200
  [ "$fb" -gt "$native" ] && fb="$native"
  if [ ! -f "$OUT/${name}.jpg" ]; then
    magick "$(graded)" -resize "${fb}x" -quality 80 "$OUT/${name}.jpg"
    made=$((made + 1))
  fi

  [ "$made" -gt 0 ] && echo "  ${name}  (native ${native}px, +${made} files)"
  return 0
}

echo "Grading photos → $OUT"

for dir in "$SRC"/*/; do
  album=$(basename "$dir")
  [ "$album" = "admin" ] && continue
  for f in "$dir"*.jpg; do
    [ -e "$f" ] || continue
    emit "$f" "g${album}-$(basename "$f" .jpg)"
  done
done

# loose files at the gallery root
for f in "$SRC"/*.jpg; do
  [ -e "$f" ] || continue
  emit "$f" "g0-$(basename "$f" .jpg)"
done

rm -f "$TMP"
echo "Done. $(ls "$OUT" | wc -l | tr -d ' ') files."
