# 24. Skills 実践ガイド

> Skills を「作る・書く・試す・配る」。入口編（[`../01_claude-code/04_skills.md`](../01_claude-code/04_skills.md)）の先を扱う深掘りシリーズ。

## 想定読者と読み方

| 目的 | 読む記事 |
| --- | --- |
| 仕組みだけ知りたい | `00` → `01` |
| まず1つ作りたい | `00` → `02` → `03`（作ったら `05` で確かめる） |
| 検証を組み込んだ Skill を作りたい | `04` |
| 作ったが呼び出されない・指示に従わない | `02` → `05` |
| 手動実行・引数・fork など Claude Code の機能を使いたい | `06` |
| チームや別環境へ配りたい | `07` → `08` |
| 他人の Skill を入れる・組織で運用する | `08` |

## 収録ファイル

| ファイル | 内容 | 出典（`AI駆動開発.md` のセクション） | 状態 |
| --- | --- | --- | --- |
| [`00_how-skills-work.md`](00_how-skills-work.md) | 3層ロード（Progressive Disclosure）と置き場所・共有範囲、他の部品との使い分け 🆕 | —（新規執筆） | 執筆中 |
| [`01_skill-anatomy.md`](01_skill-anatomy.md) | ディレクトリ構成、frontmatter の制約、命名、本文の書き方、参照は1階層まで 🆕 | —（新規執筆） | 執筆中 |
| [`02_writing-description.md`](02_writing-description.md) | 呼び出し条件としての description。3点セット、否定条件、改善サイクル 🆕 | —（新規執筆） | 執筆中 |
| [`03_practice-glossary.md`](03_practice-glossary.md) | 実践1：社内用語集 Skill を作る（references の分け方） 🆕 | —（新規執筆） | 執筆中 |
| [`04_practice-ui-guidelines.md`](04_practice-ui-guidelines.md) | 実践2：UI ガイドライン Skill と、scripts による機械検証 🆕 | —（新規執筆） | 執筆中 |
| [`05_testing-troubleshooting.md`](05_testing-troubleshooting.md) | 呼び出し・機能・比較の3テスト、評価駆動、症状別の切り分け 🆕 | —（新規執筆） | 執筆中 |
| [`06_invocation-control.md`](06_invocation-control.md) | Claude Code 固有：呼び出し制御・引数・動的コンテキスト・fork・paths 🆕 | —（新規執筆） | 執筆中 |
| [`07_distribution.md`](07_distribution.md) | claude.ai / API / Claude Code の違いと配布方法、オープン標準としての移植性 🆕 | —（新規執筆） | 執筆中 |
| [`08_security-governance.md`](08_security-governance.md) | 攻撃経路と3層の守り（入口の監査・実行時の権限・運用ガバナンス）、CI での lint と回帰評価 🆕 | —（新規執筆） | 執筆中 |

> 🆕 = `AI駆動開発.md` に記述がなく、新規執筆した項目。

## 社内共有用 PDF「Skills 入門」（A4 縦・13ページ）

社内で共有する、単体で読める入門資料。**Skills とは（P2）→ 使い方の例（P3〜4）→ 細かい説明（P5〜7）→ 応用（P8〜10）→ 社内での共有と注意（P11〜12）→ 付録（P13）** の順で、はじめての人が P2〜4 だけで最初の Skill を作れるようにしている。記事の要約ではなく、早見表・コピペ用プロンプト・チェックリストも含む（読み物は上の9本）。

| 項目 | 内容 |
| --- | --- |
| 成果物 | [`_pdf/skills-guide.pdf`](_pdf/skills-guide.pdf)（配布用） |
| **添削用（1枚の md）** | [`_pdf/guide.md`](_pdf/guide.md)：PDF の全文。`## P○` が PDF の1ページに対応する。直接書き換えて添削する |
| 原本（レイアウト） | [`_pdf/guide.html`](_pdf/guide.html)（HTML）と `_pdf/figures/*.mmd`（Mermaid の図） |
| 再生成 | `contents/24_skills/_pdf/build.sh`（Node.js と Google Chrome が必要。`--pdf-only` で図の書き出しを省略） |

> **記事を直したら PDF も直す。** PDF は記事から自動生成していない。数値・設定名・仕様を変えたときは `guide.md` と `guide.html` の両方を更新して再生成する。`guide.md` の添削結果を `guide.html` へ反映する工程は手作業（1ページに収まる分量の確認を含む）。

## 既存記事との棲み分け

| 内容 | 置き場所 |
| --- | --- |
| Skills とは何か・基本形（入口） | [`../01_claude-code/04_skills.md`](../01_claude-code/04_skills.md) |
| Skills × MCP の呼び出し規約 | [`../05_prompt-engineering/03_skills-integration.md`](../05_prompt-engineering/03_skills-integration.md) |
| チームでの共有・運用 | [`../23_team-workflow/01_shared-resources.md`](../23_team-workflow/01_shared-resources.md) |
| **Skills の作り方・テスト・配布（本セクション）** | `24_skills/` |

---

執筆時は [`../../構成.md`](../../構成.md) の共通テンプレートに従うこと。
`_assets/` の中身（いずれも標準ライブラリのみ・動作確認済み）：
- `validate_colors.py`：`04_practice-ui-guidelines.md` で使うコントラスト検証スクリプトの全文
- `lint_skills.py`：`08_security-governance.md` で使う Skill の簡易 lint（CI 用）
