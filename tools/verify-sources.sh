#!/bin/bash
# Checks the sources spectool downloaded against <package>/sources.sha256 before the SRPM is made, so an upstream
# archive that was re-tagged or replaced stops the build instead of reaching users in the COPR's signed packages.
# Run by .copr/Makefile after spectool, before the package's sources.sh. A package without sources.sha256 isn't checked;
# one with it must list every downloaded Source: a new Source, or a version bumped without new sums, fails too.
#   tools/verify-sources.sh SPEC OUTDIR
# sources.sha256 is sha256sum's format ("SUM  FILE"; # comments). On a failure the sums of what was downloaded are
# printed: check them against an independent source (README › Updating a package) before they go in the file.
set -euo pipefail
spec=$1 out=$2
sums=$(dirname "$spec")/sources.sha256
[[ -f $sums ]] || exit 0

# spectool's "SourceN: URL" lines; a file spectool saves under the URL's last part (local Sources aren't downloaded)
list=$(spectool --list-files --sources "$spec")
failed=() got=()
while read -r _ url; do
  [[ $url == *://* ]] || continue
  file=${url##*/}
  want=$(awk -v f="$file" '$1 !~ /^#/ && $2 == f {print $1}' "$sums")
  sum=$(sha256sum "$out/$file" | cut -d' ' -f1)
  got+=("$sum  $file")
  if [[ -z $want ]]; then
    failed+=("$file: not in $sums")
  elif [[ $sum != "$want" ]]; then
    failed+=("$file: sha256 $sum, expected $want")
  fi
done <<<"$list"

if (( ${#failed[@]} )); then
  printf 'verify-sources: %s\n' "${failed[@]}" >&2
  echo "verify-sources: downloaded (check them before putting them in $sums):" >&2
  printf '  %s\n' "${got[@]}" >&2
  exit 1
fi
echo "verify-sources: ${#got[@]} sources match $sums"
