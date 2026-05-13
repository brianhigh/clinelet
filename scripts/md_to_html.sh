#!/usr/bin/env bash

# Convert a markdown file to html and save in export_dir
# Set HTML title to first header in markdown file

# Detect pandoc
if command -v pandoc >/dev/null 2>&1; then
    PD=(pandoc)
else
    echo "pandoc not found" >&2
    exit 1
fi

HTH='scripts/header_to_title.lua'
if [[ ! -f "$HTH" ]]; then 
    echo "$HTH not found" >&2
    exit 2
fi

export_dir='export'
mkdir -p "$export_dir"
base=$(basename "${1%.*}")
"$PD" -s --lua-filter="$HTH" --from markdown --to html "$1" -o "${export_dir}/${base}.html"





