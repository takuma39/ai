`slide/` の原稿を Canva プレゼンに変換します。

対象ファイル: $ARGUMENTS

## ⚠️ 実行前の確認

**人間のレビューを通していない原稿を流さないこと。** 対象ファイルの frontmatter が `status: review` 以上であることを確認する。`draft` の場合は、ユーザーに確認してから進める。

## 実行手順

### ステップ1: 原稿をパースする

| 原稿の記法 | Canva の引数 |
| --- | --- |
| frontmatter `title` | `topic`（150字以内） |
| frontmatter `audience` | `audience` |
| frontmatter `style` | `style` |
| frontmatter `duration` + 枚数 | `length` |
| `### SNN ｜ タイトル` | `presentation_outlines[].title`（`SNN ｜ ` を除去） |
| 直後の平文・箇条書き | `presentation_outlines[].description` |

**送らないもの**：`##` チャプター見出し / `` `type:` `` 行 / `<!-- note: -->` / `[figure: ...]`

### ステップ2: 手作業に回すものを一覧化する

パース時に次を収集し、**ユーザーに申し送りとして提示する**。

- `visual: mermaid` のスライド → 図を Canva へ登録する（下記）
- `visual: manual` のスライド → **Canva 上で手作業**が必要なもの（プロンプト全文・コード断片・QR）

### 図の登録手順

1. 未レンダリングの図があれば `./slide/render-figures.sh <deck>` を実行する
2. `slide/_assets/` に**未 push の変更がないか確認**する。あればユーザーに commit & push を依頼する（**push していない図は raw URL が 404 になる**）
3. 各図について `upload-asset-from-url` を呼ぶ

```
url:  https://raw.githubusercontent.com/takuma39/ai/master/slide/_assets/<deck>/<SNN>.png
name: <deck>-<SNN>
```

4. 返ってきた `asset_ids` を**スライド順に並べて** `generate-design-structured` へ渡す（**最大10枚**）

> **⚠️ 使えるのはこのリポジトリの raw URL だけ。** 図を新たにホスティングサービスへアップロードしてはならない。リポジトリが非公開になっている場合、または図に公開できない情報が含まれる場合は、この経路を使わず**ユーザーに手動アップロードを依頼する**。

> `asset_ids` は**最大10枚**。超えていたら流す前に報告して止める。

### ステップ3: アウトラインのレビューを依頼する

**`request-outline-review` を必ず先に呼ぶ。** ユーザーがウィジェット上で承認するまで `generate-design-structured` を呼んではならない（Canva MCP の必須要件）。

ユーザーが構成の変更を求めた場合は、原稿 md を修正してから `request-outline-review` を呼び直す。

### ステップ4: デッキを生成する

承認後に `generate-design-structured` を `design_type: presentation` で呼ぶ。

### ステップ5: 生成後の確認と申し送り

1. 生成されたデッキの URL を報告する
2. ステップ2で集めた**手作業リスト**を再掲する
3. `slide/README.md` の「状態」列を `完了` に、原稿の frontmatter を `status: published` に更新する

## 注意事項

- **`description` は Canva 側の AI に書き換えられる。** 生成後、コマンド・設定キー・バージョン番号が本文に混ざっていないか確認し、混ざっていたら原稿側を `visual: manual` に直す
- `verbatim: true` は `doc` 専用。presentation では効かない
- ブランドキットを使うかどうかは、`list-brand-kits` を提示してユーザーに選ばせる
- 結果は必ず日本語で報告すること
