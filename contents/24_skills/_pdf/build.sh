#!/usr/bin/env bash
# Skills 実践ガイド（A4縦PDF）をビルドする。
#   ./build.sh            # 図の書き出し + PDF 生成
#   ./build.sh --pdf-only # 図はそのまま、PDF だけ再生成
# 必要なもの: Node.js（npx）、Google Chrome（macOS）
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" != "--pdf-only" ]]; then
  for f in figures/*.mmd; do
    npx -y @mermaid-js/mermaid-cli@latest -i "$f" -o "${f%.mmd}.png" \
      -c mermaid-print.json -b white -s 3 --quiet
    echo "  figure: ${f%.mmd}.png"
  done
fi

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="skills-guide.pdf" "file://$PWD/guide.html" >/dev/null 2>&1
echo "✅ skills-guide.pdf"
