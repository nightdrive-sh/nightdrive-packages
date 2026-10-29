#!/bin/bash
# Puts wayvnc's patches, which live here beside the spec and not at a URL, in OUTDIR with the downloaded sources.
# Run by .copr/Makefile after spectool.
#   wayvnc/sources.sh SPEC OUTDIR
set -euo pipefail
cp "$(dirname "$1")"/*.patch "$2"/
