#!/usr/bin/env bash
set -euo pipefail


# Detect ImageMagick
if command -v magick >/dev/null 2>&1; then
    IM=(magick)
elif command -v convert >/dev/null 2>&1 && convert -version 2>/dev/null | grep -q ImageMagick; then
    IM=(convert)
else
    echo "ImageMagick not found" >&2
    exit 1
fi

# Find a suitable font
font=$("$IM" -list font 2>/dev/null | awk -F': ' '/Font: .*Open-?Sans/ {print $2; exit}')
[[ -z "$font" && -f /System/Library/Fonts/Monaco.ttf ]] && font=/System/Library/Fonts/Monaco.ttf
[[ -z "$font" && -f /c/Windows/Fonts/verdana.ttf ]] && font=/c/Windows/Fonts/verdana.ttf

formats=(pdf png jpg jpeg gif bmp tiff tif webp)

for ext in "${formats[@]}"; do
    echo "Generating test_${ext}.${ext}..."

    opts=(-background white -fill black -pointsize 18)

    if [[ -n "$font" ]]; then
        opts+=(-font "$font")
    fi

    # Format-specific fixes
    if [[ "$ext" == "bmp" ]]; then
        opts+=(-compress None)
    elif [[ "$ext" == "tif" || "$ext" == "tiff" ]]; then
        opts+=(-depth 8 -compress None)
    fi

    "$IM" "${opts[@]}" label:"This is a ${ext} test." "test_${ext}.${ext}"
done

echo "Done! All test images generated."

