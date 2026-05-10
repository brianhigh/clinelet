#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Check if 'magick' is installed
if ! command -v magick >/dev/null 2>&1; then
    echo "Error: 'magick' (ImageMagick 7+) is not installed or not in PATH." >&2
    exit 1
fi

# Find a suitable font
font=$(magick -list font | awk -F': ' '/Font: [Oo]pen-?[Ss]ans/ {print $2; exit}')

# Define target image formats
formats=(pdf png jpg jpeg gif bmp tiff tif webp)

# Generate a test image for each format
for ext in pdf png jpg jpeg gif bmp tiff tif webp; do
    echo "Generating test_${ext}.${ext}..."
    
    # Base command options
    opts=(-background white -fill black -font "$font" -pointsize 18)
    
    # Apply format-specific fixes for Tesseract compatibility
    if [ "$ext" = "bmp" ]; then
        opts+=(-compress None)
    elif [ "$ext" = "tif" ] || [ "$ext" = "tiff" ]; then
        opts+=(-depth 8 -compress None)
    fi
    
    # Run the generation
    magick "${opts[@]}" label:"This is a test." "test_${ext}.${ext}"
done

echo "Done! All test images generated."

