# 01. Claude Code の仕組み

> このリポジトリの入口。ここだけ読めば Claude Code の全体像が掴める状態を目指す。

## 収録予定

| ファイル | 内容 | 出典（`AI駆動開発.md` のセクション） | 状態 |
| --- | --- | --- | --- |
| [`00_what-is-claude-code.md`](00_what-is-claude-code.md) | 位置づけ、CLI / IDE / Web / Desktop の違い、他ツールとの比較 🆕 | § 6.1 Claude Code ベストプラクティス | レビュー中 |
| [`01_models.md`](01_models.md) | モデルとは何か、Fable 5 / Opus 5 / Sonnet 5 / Haiku 4.5 の使い分け、Adaptive Thinking、コスト感 🆕 | § 1.8 モデル別の得意領域 / 付録「モデル選択ガイド」 | レビュー中 |
| [`02_architecture.md`](02_architecture.md) | プロンプト入力から応答までの内部フロー（プロンプト → CLAUDE.md → skills → sub-agent → MCP → tool 実行 → 応答）をシーケンス図で 🆕 | —（新規執筆） | レビュー中 |
| [`03_claude-md.md`](03_claude-md.md) | CLAUDE.md の設計、階層読み込み、肥大化対策 | § 4.2 CLAUDE.md の設計 | レビュー中 |
| [`04_skills.md`](04_skills.md) | skills とは・活用方法・SKILL.md の書き方 | § AI駆動開発の仕組み「skills とは」/ § 4.3 Skills の設計 | レビュー中 |
| [`05_sub-agents.md`](05_sub-agents.md) | sub-agent とは・役割設計・モデル割り当て | § AI駆動開発の仕組み「sub-agent とは」/ § 4.3 Subagents の設計 | レビュー中 |
| [`06_hooks.md`](06_hooks.md) | hooks の種類（PreToolUse / PostToolUse / Stop 等）、強制力を持つルールの実装 🆕 | § 4.3 Hooks の設定（大幅加筆・実装例は全面修正） | レビュー中 |
| [`07_mcp-basics.md`](07_mcp-basics.md) | MCP とは（概念のみ。個別カタログは 02_mcp/ へ） | § AI駆動開発の仕組み「MCP とは」 | レビュー中 |
| [`08_combination-patterns.md`](08_combination-patterns.md) | skills と sub-agent の違い、4部品の組み合わせフロー、ユースケース5種 | § AI駆動開発の仕組み「skills と sub-agent の違い」「3要素を組み合わせた開発ユースケース」 | レビュー中 |
| [`09_directory-structure.md`](09_directory-structure.md) | .claude/ 配下のファイル構成、ユーザー / プロジェクト / エンタープライズの3階層 🆕 | —（新規執筆） | レビュー中 |
| [`10_context-management.md`](10_context-management.md) | コンテキストウィンドウ戦略、/compact、セッション分割 | § 4.4 コンテキスト管理戦略 | レビュー中 |

> 🆕 = `AI駆動開発.md` に記述がなく、新規執筆が必要な項目。

---

執筆時は [`../../構成.md`](../../構成.md) の共通テンプレートに従うこと。
