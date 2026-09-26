---
title: "Skills の配布：Claude Code・claude.ai・API の違い"
status: draft
updated: 2026-09-26
source: 新規（AI駆動開発.md に対応セクションなし）
tags: ["skills", "distribution", "claude-ai", "api", "agent-skills"]
---

# Skills の配布：Claude Code・claude.ai・API の違い

> **この記事でわかること**：Skill を Claude Code 以外（claude.ai の画面、API）で使う方法と、環境ごとの違い。他人の Skill を入れるときの安全面は [`08_security-governance.md`](08_security-governance.md) に分けている。

## 結論

Skill は **同じ形式（SKILL.md のフォルダ）で複数の環境で使える**。ただし **環境間で自動同期はされない**。

| 環境 | 作り方 | 共有範囲（公式概要の記載・2026年9月時点） |
| --- | --- | --- |
| **Claude Code** | フォルダを `.claude/skills/` などに置く（アップロード不要） | 個人 / リポジトリ / プラグイン / 組織（→ [`00_how-skills-work.md`](00_how-skills-work.md)） |
| **claude.ai** | **ZIP を設定画面からアップロード** | **個人ごと**。組織への集中配布は、公式概要では「不可」とされている |
| **Claude API** | Skills API（`/v1/skills`）でアップロード。実行にはコード実行ツールが必要 | ワークスペース全体 |

> claude.ai まわりの管理機能（組織設定など）は変更が続いている。**組織で配る前に、管理画面とヘルプセンターで最新の可否を確認する。**

## 背景・課題

チームに Skill を広げようとすると、「誰がどこで使うのか」で詰まる。

| 場面 | 課題 |
| --- | --- |
| 開発者だけが使う | Git で足りるが、非エンジニアには届かない |
| 非エンジニアも使う | claude.ai へ個別にアップロードが必要 |
| プロダクトに組み込む | API 経由で、実行環境の制約を受ける |

## 具体的な方法

### 環境ごとの違い

| 観点 | Claude Code | claude.ai | Claude API |
| --- | --- | --- | --- |
| 置き方 | ファイルを置く | ZIP をアップロード | API でアップロード |
| ネットワーク | 既定ではローカルと同等（権限設定で制限し得る） | 設定により 完全／一部／なし | **なし** |
| パッケージ追加 | 可（グローバル導入は避ける） | 可（設定に依存） | **不可**（事前導入分のみ） |
| 事前構築 Skill（pptx / xlsx / docx / pdf） | **なし** | あり | あり |
| Claude Code 独自フィールド | 使える | 使えない | 使えない |
| 更新の反映 | 即時 | 再アップロード | バージョンを上げて更新 |

> 実行環境の制約は変わりやすい。**スクリプトを含む Skill は、配布先で動くか実際に試す。** 標準ライブラリだけで書くと移植しやすい。API でバージョンを省略すると最新版が使われる点は、[`08_security-governance.md`](08_security-governance.md) を参照。

### claude.ai にアップロードする

```mermaid
flowchart LR
    A["1. スキルのフォルダを用意"] --> B["2. ZIP に圧縮"]
    B --> C["3. 設定画面の Skills<br/>（Features）からアップロード"]
    C --> D["4. 有効化して<br/>言い換え依頼で発動確認"]

    style D fill:#dcfce7,stroke:#16a34a,color:#000
```

ZIP の中身は、**フォルダごと圧縮し、その直下に SKILL.md がある形**にする。

```text
company-glossary.zip
└── company-glossary/
    ├── SKILL.md
    └── references/
        └── terms.md
```

| 項目 | 内容 |
| --- | --- |
| 対象プラン | Pro / Max / Team / Enterprise（コード実行機能の有効化が前提） |
| 共有 | 個人単位。チーム全員が使うには、各人がアップロードする |

> 画面の名称・手順は変わりやすい。最新は [ヘルプセンター](https://support.claude.com/en/articles/12512198-creating-custom-skills) で確認する。

### Claude Code でチームに配る

| 方法 | 向いている場面 | 注意 |
| --- | --- | --- |
| **Git（`.claude/skills/`）** | 1つのリポジトリ内のチーム | レビュー・履歴・ロールバックができる。最初の選択肢 |
| **プラグイン** | 複数リポジトリ・組織横断で配りたい | `/plugin-name:skill-name` の名前空間で呼ぶ |
| **Enterprise（管理設定）** | 組織として全員に適用したい | 個人・プロジェクトの同名 Skill より優先される |

チーム運用は [`../23_team-workflow/01_shared-resources.md`](../23_team-workflow/01_shared-resources.md)、レビュー体制・バージョン固定は [`08_security-governance.md`](08_security-governance.md) を参照。

### オープン標準としての Skill

Skill の形式は **Agent Skills** というオープン仕様（[agentskills.io](https://agentskills.io/specification)）として公開されている。仕様の範囲で書けば、他の対応エージェントにも持ち出しやすい。

| 区分 | フィールド |
| --- | --- |
| 共通仕様 | `name` / `description` / `license` / `compatibility` / `metadata` |
| 共通仕様（実験的・実装差あり） | `allowed-tools` |
| Claude Code 独自 | `disable-model-invocation` / `context` / `agent` / `paths` / `hooks` など |

```bash
# 仕様への適合を検証する（公式の参照ライブラリ）
skills-ref validate ./company-glossary
```

| 持ち出し方針 | 内容 |
| --- | --- |
| **共通仕様の範囲で書く** | 移植性が高い。`${CLAUDE_SKILL_DIR}` や `context: fork` は使えない |
| **Claude Code 拡張を使う** | 機能は豊富。ただし Claude Code 専用になる |
| **両立させる** | 共通仕様で核を作り、固有機能は別の Skill に分ける |

## 実際のプロンプト例

```text
# 移植性の確認
.claude/skills/company-glossary/ を claude.ai にアップロードする想定で確認して。
- Claude Code 独自のフィールドや ${CLAUDE_SKILL_DIR} を使っていないか
- スクリプトが標準ライブラリだけで動くか
- name がディレクトリ名と一致しているか
問題があれば、共通仕様に直した差分を出して。

# ZIP の作成
.claude/skills/company-glossary/ を、claude.ai にアップロードできる ZIP にして。
ZIP 内は company-glossary/SKILL.md の構造にして、不要なファイル（.DS_Store など）は除いて。
```

## 注意点

> **claude.ai・API・Claude Code の Skill は互いに同期されない。** 原本は Git に置き、各環境へはそこから出す。手作業で個別に直すと、内容がずれる。

> **Claude Code 独自フィールドを含む Skill を持ち出すと、その機能は働かない。** 無視されるのか拒否されるのかは環境によるため、持ち出す前にアップロードして確認する。

> **配布したら、更新の責任者を決める。** 配りっぱなしの Skill は古くなる。担当・更新時期・廃止基準は [`08_security-governance.md`](08_security-governance.md) の運用施策に従う。

## 参考リンク

- [Agent Skills 概要 — Where Skills work / Limitations](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills 仕様](https://agentskills.io/specification)
- [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Claude Help Center — How to create custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Claude Code Skillsに入門しよう！（Zenn）— claude.ai の GUI で作る](https://zenn.dev/jackpotjack/articles/30de567059dd19)
- 前：[`06_invocation-control.md`](06_invocation-control.md) / 次：[`08_security-governance.md`](08_security-governance.md)
