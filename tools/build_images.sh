#!/bin/bash
# Kvintána — asset pipeline
# Grades the original photos into the "Ember & Night" look and emits
# responsive WebP (+ a JPG fallback) into assets/img/.
#
# Requires ImageMagick 7 (`brew install imagemagick`).
# Usage:  sh tools/build_images.sh

set -euo pipefail

SRC="${SRC:-$HOME/www/kvintana/www/img/gallery}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/assets/img"
WIDTHS=(2000 1200 800 400)

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

emit() {
  local src="$1" name="$2"
  local native
  native=$(magick identify -format '%w' "$src")

  grade "$src" > /tmp/kv-graded.miff

  for w in "${WIDTHS[@]}"; do
    # never upscale past the native resolution
    [ "$w" -gt "$native" ] && continue
    magick /tmp/kv-graded.miff -resize "${w}x" -quality 78 -define webp:method=6 \
      "$OUT/${name}-${w}.webp"
  done

  # smallest available width, so tiny sources still get one file
  if ! ls "$OUT/${name}"-*.webp >/dev/null 2>&1; then
    magick /tmp/kv-graded.miff -quality 78 "$OUT/${name}-${native}.webp"
  fi

  # JPG fallback at a middling width
  local fb=1200
  [ "$fb" -gt "$native" ] && fb="$native"
  magick /tmp/kv-graded.miff -resize "${fb}x" -quality 80 "$OUT/${name}.jpg"

  echo "  ${name}  (native ${native}px)"
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

rm -f /tmp/kv-graded.miff
echo "Done. $(ls "$OUT" | wc -l | tr -d ' ') files."
