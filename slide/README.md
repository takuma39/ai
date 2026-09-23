# slide — 勉強会スライド原稿

`contents/` の記事から派生させた、登壇用スライドの**原稿**を置くディレクトリ。

このディレクトリの md は最終成果物ではない。**Canva MCP に渡すための中間形式**である。

```mermaid
flowchart LR
    A["AI駆動開発.md<br/>（蓄積）"] --> B["contents/<br/>（記事）"]
    B --> C["slide/*.md<br/>（原稿）"]
    C --> D["人間のレビュー"]
    D --> E["Canva MCP<br/>generate-design-structured"]
    E --> F["Canva プレゼン"]
```

> **原稿は「抜粋 + 誘導」で作る。記事の要約ではない。** 詳細は [`../.claude/skills/slide-standards.md`](../.claude/skills/slide-standards.md) を唯一の規約とする。

---

## デッキ一覧

`contents/` の1ディレクトリ = 1デッキ。ファイル名も揃える。

> **例外：`00_ai-env-setup`。** 「AI環境設定をどう作るか」は `00_overview/`（課題・フロー・ディレクトリ）と `01_claude-code/`（コンテキストの読まれ方・CLAUDE.md）にまたがる。**基礎編**として1デッキに束ね、`01_claude-code` デッキを**発展編**（skills / sub-agent / hooks / MCP）に振り分けた。

| # | デッキ | 元 | 尺 | 優先 | 状態 |
| --- | --- | --- | --- | --- | --- |
| 00 | [`00_ai-env-setup.md`](00_ai-env-setup.md)<br/>「AIに書かせる前にやること」 | `01_claude-code/` + `00_overview/` | **8分** | **S** | レビュー中 |
| 01 | [`01_claude-code.md`](01_claude-code.md)<br/>「Claude Code の5つの設定」 | `01_claude-code/` | **18分** | **S** | レビュー中 |
| 02 | `02_mcp.md` | `02_mcp/` | 30分 | **S** | 未着手 |
| 03 | `03_rag.md` | `03_rag/` | 15分 | B | 未着手 |
| 04 | `04_multi-agent.md` | `04_multi-agent/` | 30分 | A | 未着手 |
| 05 | `05_prompt-engineering.md` | `05_prompt-engineering/` | 30分 | A | 未着手 |
| 10 | `10_requirements.md` | `10_requirements/` | 30分 | A | 未着手 |
| 11 | `11_design.md` | `11_design/` | 30分 | B | 未着手 |
| 12 | `12_ui-ux.md` | `12_ui-ux/` | 30分 | B | 未着手 |
| 13 | `13_implementation.md` | `13_implementation/` | 30分 | **S** | 未着手 |
| 14 | `14_code-review.md` | `14_code-review/` | 15分 | A | 未着手 |
| 15 | `15_test.md` | `15_test/` | 30分 | **S** | 未着手 |
| 20 | `20_github-claude.md` | `20_github-claude/` | 30分 | A | 未着手 |
| 21 | `21_cicd-ops.md` | `21_cicd-ops/` | 30分 | B | 未着手 |
| 22 | `22_security.md` | `22_security/` | 40分 | **S** | 未着手 |
| 23 | `23_team-workflow.md` | `23_team-workflow/` | 30分 | A | 未着手 |

**優先度**：**S** = 単体で登壇1回分の価値がある / A = 需要は確実にある / B = 連続開催の後半向け

> **尺は登壇枠に合わせて決める。** 5〜10分（LT）は本編10〜12枚、30〜40分は本編20〜25枚。骨格そのものが変わるので、先に尺を決めてから原稿を書く。

> **`02_mcp` だけ 1:1 にしない。** 元が18ファイル・7.2万字あり、1デッキに入らない。**「MCP の選び方」という総論**にし、個別 MCP は Appendix と `contents/` 誘導に回す。

---

## 作り方

```bash
# 1. 原稿を生成する（図は Mermaid で書かれる）
/make-slide 00_ai-env-setup

# 2. 図を PNG に書き出す
./slide/render-figures.sh 00_ai-env-setup   # → slide/_assets/00_ai-env-setup/*.png

# 2.5 図を push する（raw URL から Canva が取得するため必須）
git add slide/_assets/ && git commit -m "docs(slide): 図を更新" && git push

# 3. 人間がレビュー（← ここは必ず人間が通す）
#    VS Code のプレビューで Mermaid 図がそのまま見える

# 4. Canva へ流す
/slide-to-canva slide/00_ai-env-setup.md
```

### ディレクトリ

| パス | 中身 |
| --- | --- |
| `NN_*.md` | デッキ原稿（Mermaid ソース込み） |
| `_assets/<deck>/` | 書き出した図（`.mmd` と `.png`）。**Canva へは手動アップロード** |
| `_mermaid.json` | 全デッキ共通の配色・フォント設定 |
| `render-figures.sh` | 図の書き出しスクリプト |

> **Canva へ渡す前に必ず人間がチェックする。** `description` は Canva 側の AI に書き換えられるため、**表記が壊れて困る情報が平文に残っていないか**を人の目で確認する工程を飛ばさない。

> **図は GitHub の raw URL 経由で Canva に入れる。** `upload-asset-from-url` は公開 HTTPS URL しか受け付けないが、このリポジトリは公開しているので **`_assets/` を push すればその raw URL がそのまま使える**。**push を忘れると 404 になる**ので、Canva へ流す前に必ず push する。

---

## 状態の定義

| 状態 | 意味 |
| --- | --- |
| 未着手 | ファイル未作成 |
| 執筆中 | 原稿を書いている |
| レビュー中 | 人間のチェック待ち |
| 完了 | Canva デッキを生成済み |
