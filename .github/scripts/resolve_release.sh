#!/usr/bin/env bash
# Read-only preflight. Never creates a tag, release, or asset.
set -euo pipefail
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT must point to the step output file}"

tags="$(git tag --list)"
if [[ -z "$tags" ]]; then
  echo "No release tags exist; skipping automatic publication."
  echo "publish=false" >> "$GITHUB_OUTPUT"
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    echo "No release published: this repository has no release tag." >> "$GITHUB_STEP_SUMMARY"
  fi
  exit 0
fi

# Retain the existing latest-reachable-tag policy. Other git errors must fail.
version="$(git describe --tags --abbrev=0)"
if [[ ! "$version" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+([.+-][A-Za-z0-9.-]+)?$ ]]; then
  echo "Invalid release version tag." >&2
  exit 1
fi
notes="docs/release_notes/release_notes_${version#v}.md"
if [[ ! -f "$notes" ]]; then
  echo "Release notes for the selected tag are missing." >&2
  exit 1
fi
printf 'publish=true\nversion=%s\n' "$version" >> "$GITHUB_OUTPUT"
