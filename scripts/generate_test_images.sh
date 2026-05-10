#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Check if 'magick' is installed
if ! command -v magick >/dev/null 2>&1; then
    echo "Error: 'magick' (ImageMagick 7+) is not installed or not in PATH." >&2
    exit 1
fi

# Define target image formats
formats=(pdf png jpg jpeg gif bmp tiff tif webp)

# Generate a test image for each format
for ext in "${formats[@]}"; do
    echo "Generating test_${ext}.${ext}..."
    if ! magick -background white \
                -fill black \
                -font "Open-Sans-Regular" \
                -pointsize 18 \
                label:"This is a test." \
                "test_${ext}.${ext}" 2>/dev/null; then
        echo "Warning: Failed to create test_${ext}.${ext} (format might not be supported by your ImageMagick build)." >&2
    fi
done

echo "Done! All test images generated."

