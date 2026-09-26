#!/usr/bin/env python3
"""Skill ディレクトリの簡易 lint（CI 用）。標準ライブラリのみ。

使い方:
    python3 lint_skills.py .claude/skills

終了コード: 0 = ERROR なし / 1 = ERROR あり
  ERROR : name とディレクトリ名の不一致、不可視文字（隠し指示の疑い）
  WARN  : description が frontmatter に無い、500行超、読み込み時シェル実行（!`...`）
  NOTE  : allowed-tools あり、scripts/ あり（人間のレビュー対象）
"""
import re
import sys
import unicodedata
from pathlib import Path


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fm[k.strip()] = v.strip()
    return fm


def invisible(text: str) -> list[str]:
    # Cf（書式制御）と Co（私用領域）。タグ文字・ゼロ幅文字・双方向制御などを含む
    return sorted({f"U+{ord(c):04X}" for c in text
                   if unicodedata.category(c) in ("Cf", "Co") and c != "﻿"})


def main(root: str) -> int:
    errors = 0
    for skill_md in sorted(Path(root).glob("*/SKILL.md")):
        d = skill_md.parent
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        out = []
        if fm.get("name") and fm["name"] != d.name:
            out.append(("ERROR", f"name '{fm['name']}' がディレクトリ名と不一致"))
        if not fm.get("description"):
            out.append(("WARN", "description が frontmatter に無い（標準仕様では必須）"))
        for f in [skill_md, *[p for p in d.rglob("*") if p.is_file() and p != skill_md]]:
            try:
                bad = invisible(f.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue  # バイナリは対象外
            if bad:
                out.append(("ERROR", f"{f.relative_to(d)} に不可視文字 {', '.join(bad)}"))
        if text.count("\n") > 500:
            out.append(("WARN", "SKILL.md が500行超"))
        if "!`" in text or "```!" in text:
            out.append(("WARN", "読み込み時シェル実行（!`...`）を含む"))
        if "allowed-tools" in fm:
            out.append(("NOTE", f"allowed-tools: {fm['allowed-tools']}"))
        if (d / "scripts").is_dir():
            out.append(("NOTE", "scripts/ あり（中身を人間がレビューすること）"))
        for level, msg in out:
            print(f"[{level}] {d.name}: {msg}")
            errors += level == "ERROR"
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ".claude/skills"))
