#!/usr/bin/env bash

# Convert a markdown file to html and save in export_dir
# Set HTML title to first header in markdown file

export_dir='export'
mkdir -p "$export_dir"
base=$(basename "${1%.*}")
pandoc -s --lua-filter=scripts/header_to_file.lua --to html "$1" -o "${export_dir}/${base}.html"

