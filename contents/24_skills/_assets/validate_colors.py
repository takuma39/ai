#!/usr/bin/env python3
"""前景色と背景色の WCAG 2.x コントラスト比を検証する。

使い方:
    python3 scripts/validate_colors.py "<前景HEX>" "<背景HEX>" [--large]

終了コード:
    0 = AA 合格 / 1 = AA 不合格 / 2 = 入力エラー
"""
from __future__ import annotations

import math
import re
import sys

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def parse_hex(value: str) -> tuple[int, int, int]:
    m = HEX_RE.fullmatch(value)
    if not m:
        raise ValueError(f"HEX カラーとして解釈できない: {value!r}（例: #1a1a1a, #fff）")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = luminance(parse_hex(fg)), luminance(parse_hex(bg))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    large = "--large" in argv
    if len(args) != 2:
        print(__doc__)
        return 2
    try:
        ratio = contrast(args[0], args[1])
    except ValueError as e:
        print(f"ERROR: {e}")
        return 2

    aa = 3.0 if large else 4.5
    aaa = 4.5 if large else 7.0
    # 表示は切り捨てる（WCAG は丸めない。4.495 を「4.50」と表示して FAIL と出さないため）
    shown = math.floor(ratio * 100) / 100
    print(f"contrast: {shown:.2f}:1 ({'大きい文字' if large else '通常テキスト'})")
    print(f"AA : {'PASS' if ratio >= aa else 'FAIL'}（基準 {aa}:1）")
    print(f"AAA: {'PASS' if ratio >= aaa else 'FAIL'}（基準 {aaa}:1）")
    if ratio < aa:
        print("→ 前景色を暗く、または背景色を明るくして再検証すること")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
