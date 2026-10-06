#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v actionlint >/dev/null 2>&1; then
  curl -sSfL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash | bash
  sudo mv -f actionlint /usr/local/bin/actionlint
  sudo chmod +x /usr/local/bin/actionlint
fi

mkdir -p assets output
