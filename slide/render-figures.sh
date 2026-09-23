#!/usr/bin/env bash
# スライド原稿の ```mermaid ブロックを PNG に書き出す。
#   ./render-figures.sh 00_overview        # 1デッキ
#   ./render-figures.sh                    # 全デッキ
# 出力: slide/_assets/<deck>/<SNN>.png（Canva へは手動でアップロードする）
set -euo pipefail
cd "$(dirname "$0")"

render_one() {
  local deck="$1" md="$1.md" out="_assets/$1"
  [[ -f "$md" ]] || { echo "❌ $md がない"; return 1; }
  mkdir -p "$out"

  python3 - "$md" "$out" <<'PY'
import re, sys, pathlib
md, out = sys.argv[1], pathlib.Path(sys.argv[2])
src = pathlib.Path(md).read_text(encoding="utf-8")
# 「### SNN ｜ ...」で分割し、各スライド内の mermaid ブロックを取り出す
n = 0
for m in re.finditer(r'^### (\S+) ｜ (.+?)$(.*?)(?=^### |\Z)', src, re.M | re.S):
    sid, title, body = m.group(1), m.group(2), m.group(3)
    for i, fig in enumerate(re.findall(r'```mermaid\n(.*?)\n```', body, re.S)):
        name = sid if i == 0 else f"{sid}-{i+1}"
        (out / f"{name}.mmd").write_text(fig + "\n", encoding="utf-8")
        print(f"  {name}.mmd  ({title})")
        n += 1
print(f"抽出: {n} 点")
PY

  local cfg=_mermaid.json
  local ok=0 ng=0
  for f in "$out"/*.mmd; do
    [[ -e "$f" ]] || continue
    if npx -y @mermaid-js/mermaid-cli@latest \
         -i "$f" -o "${f%.mmd}.png" \
         -c "$cfg" -b "#151a23" -s 3 --quiet >/dev/null 2>&1; then
      ok=$((ok+1))
    else
      echo "  ❌ 構文エラー: $f"; ng=$((ng+1))
    fi
  done
  echo "✅ $deck: $ok 点を書き出し / エラー $ng 点"
}

if [[ $# -ge 1 ]]; then
  render_one "$1"
else
  for f in [0-9]*.md; do render_one "${f%.md}"; done
fi

echo
echo "→ git add slide/_assets/ && git commit && git push してから /slide-to-canva を実行してください。"
echo "  （Canva は GitHub の raw URL から図を取得します。push していないと 404 になります）"
