#!/bin/bash
# Puts Hyprland's backported patches, which live here beside the spec and not at a URL, in OUTDIR with the downloaded
# sources. Run by .copr/Makefile after spectool.
#   hyprland/sources.sh SPEC OUTDIR
set -euo pipefail
cp "$(dirname "$1")"/*.patch "$2"/
