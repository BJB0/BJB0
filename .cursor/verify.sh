#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Lint GitHub Actions workflows"
actionlint -color .github/workflows/*.yml

echo "==> Refresh GitHub readme stats images (same as generate-stats workflow)"
mkdir -p assets
curl -fsSL \
  "https://github-readme-stats.vercel.app/api?username=BJB0&show_icons=true&theme=tokyonight&hide_border=true" \
  -o assets/github_stats.png
curl -fsSL \
  "https://github-readme-stats.vercel.app/api/top-langs/?username=BJB0&layout=compact&theme=tokyonight&hide_border=true" \
  -o assets/top_languages.png

for f in assets/github_stats.png assets/top_languages.png; do
  if [[ ! -s "$f" ]]; then
    echo "ERROR: missing or empty $f" >&2
    exit 1
  fi
  echo "OK: $f ($(wc -c <"$f") bytes)"
done

echo "==> README sanity check"
if [[ ! -s README.md ]]; then
  echo "ERROR: README.md is missing or empty" >&2
  exit 1
fi
grep -q 'BJB0' README.md || { echo "ERROR: README.md missing expected username" >&2; exit 1; }

echo "All verification checks passed."
