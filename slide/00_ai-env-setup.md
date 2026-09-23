---
deck: 00_ai-env-setup
title: AIに書かせる前にやること
source: contents/01_claude-code/（02_architecture, 03_claude-md, 09_directory-structure） + contents/00_overview/03_design-doc-structure.md
audience: Claude Code を使い始めたが、思ったほど速くなっていないエンジニア
duration: 8            # 5〜10分（LT枠）
takeaway: AIに最初に渡っているのは CLAUDE.md だけ。ここを整える工程を1つ挟むと、以降の出力が安定する。
scope: 基礎編（CLAUDE.md と .claude/ を作るところまで）。skills / hooks / sub-agent / MCP は発展編（01_claude-code デッキ）
style: 図中心・線画ベースの図解・文字は最小限・濃色背景
status: draft
updated: 2026-08-31
---

# AIに書かせる前にやること

<!-- 尺: 本編10枚。表紙10秒 + 各50秒 ≒ 約8分。図は9点で、Canva の asset_ids 上限10まで1枠空いている -->
<!-- 図: Mermaid 10点（Canva の asset_ids 上限ちょうど）。`./render-figures.sh 00_ai-env-setup` で _assets/ に書き出す -->

## 導入

### S01 ｜ AIに書かせる前にやること

`type: title` ｜ `visual: none`

AIに書かせる前にやること — 手戻りを減らす環境のつくりかた

<!-- note: 表紙。冒頭で「今日は基礎編です。skills や hooks の話はしません」と範囲を宣言する -->

## 1. 課題

### S02 ｜ 速くなった分が、手戻りに消える

`type: compare` ｜ `visual: mermaid`

書く時間は確かに減ります。減った分がそのまま手戻りに消えていく、という状態が起きます。

[figure: 手戻りが発生するまでのシーケンス]

```mermaid
sequenceDiagram
    autonumber
    participant D as 開発者
    participant AI as AI
    participant R as レビュア
    D->>AI: 実装を依頼
    AI-->>D: 動くコード（前提はズレている）
    D->>R: PR を出す
    R-->>D: 「この前提が違う」
    Note over D,R: ここで手戻り
    D->>AI: 前提を伝え直して再依頼
    AI-->>D: 作り直したコード
    Note over D,AI: 書く時間は減った<br/>減った分が手戻りに消えた
```

<!-- note: 「速くならない」ではなく「手戻りに消える」と言い切る。ここで聞き手を当事者にする -->

## 2. 原因

### S03 ｜ AIは渡された情報しか見ていない

`type: message` ｜ `visual: mermaid`

AIはプロジェクトを見渡してはいません。渡された範囲だけで判断します。足りないのは性能ではなく、渡している情報のほうです。

[figure: AIに渡っている情報と、渡っていない情報]

```mermaid
flowchart TB
    subgraph ALL["プロジェクトの全情報"]
        direction TB
        subgraph READ["AI に渡っている情報"]
            A["開いているファイル"]
            B["直前の会話"]
        end
        C["仕様書"]
        D["命名規約"]
        E["過去の決定理由"]
    end
    READ --> OUT["AI はこの内側だけで判断する"]
    classDef miss fill:#1e2430,stroke:#3d4757,color:#6b7684,stroke-dasharray:4 3
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff
    class C,D,E miss
    class OUT hi
```

<!-- note: ここが転換点。「もっと良いモデルを待つ」という発想を切る -->

## 3. 結論

### S04 ｜ 工程を1つ挟むだけでいい

`type: message` ｜ `visual: mermaid`

新しい方法論を覚え直す必要はありません。実装に入る前に、AIに渡すものを決める工程を1つ挟みます。

[figure: ★このデッキの主役。開発フロー全体と、増える1工程]

```mermaid
flowchart LR
    A[要件定義] --> B[基本設計] --> C[詳細設計] --> X[["AI 環境設定"]]
    X --> D[実装] --> E[レビュー] --> F[テスト] --> G[運用]
    N["ここだけが新しい"] -.-> X
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff,font-weight:bold
    classDef dim fill:#1e2430,stroke:#3d4757,color:#8b95a5
    classDef note fill:none,stroke:none,color:#ff6b35
    class X hi
    class A,B,C,D,E,F,G dim
    class N note
```

<!-- note: 一番時間を使うスライド。指で「ここだけ」と示す -->
<!-- note: ★「AI環境設定」は一般的な用語ではない。「この発表ではこう呼びます」と断ってから使う -->
<!-- note: 世の中では「コンテキストエンジニアリング」と呼ばれている領域だと補足すると位置づけが伝わる -->

## 4. AI環境設定とは

### S05 ｜ AIはどの順番で読んでいるか

`type: message` ｜ `visual: mermaid`

プロンプトを送った瞬間、AIはコードを見ていません。最初に読まれるのはプロジェクトのルールです。

[figure: プロンプトから出力までに何が読まれるか]

```mermaid
sequenceDiagram
    participant U as あなた
    participant CC as Claude Code
    participant CM as CLAUDE.md
    participant DOT as .claude/
    participant M as モデル
    U->>CC: プロンプト
    CC->>CM: 毎回かならず読む
    CM-->>CC: プロジェクトのルール
    CC->>DOT: 必要なときだけ読む
    DOT-->>CC: Skills / Sub Agent / Hooks
    CC->>M: まとめて渡す
    M-->>U: 出力
    Note over CM,DOT: CLAUDE.md は毎回<br/>.claude/ は必要なときだけ
```

<!-- note: ★このスライドで「なぜ CLAUDE.md が効くのか」が腑に落ちる。急がない -->
<!-- note: 「コードを読むのはこのあと」と一言添える。最初の判断材料は CLAUDE.md だけ -->

### S06 ｜ CLAUDE.md と .claude/

`type: compare` ｜ `visual: mermaid`

ルート直下に置く2つです。片方は毎回読まれる指示書、もう片方は必要なときだけ開く道具箱です。

[figure: 2つのファイルの役割と、読まれるタイミング]

```mermaid
flowchart TB
    subgraph ROOT["プロジェクトルート直下（場所は固定）"]
        direction LR
        CM["CLAUDE.md<br/>命名規約・使う技術・禁止事項"]
        DIR[".claude/<br/>Skills / Sub Agent / Hooks"]
    end
    CM --> R1["毎ターン全文が渡る<br/>→ 短く保つ"]
    DIR --> R2["必要なときだけ開かれる<br/>→ 量は気にしなくていい"]
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff,font-weight:bold
    classDef sub fill:#1e2430,stroke:#3d4757,color:#e8eaed
    class CM hi
    class DIR,R1,R2 sub
```

<!-- fig: CLAUDE.md を強調。「今日は CLAUDE.md まで」の範囲を示すため .claude/ は控えめに -->
<!-- note: 「.claude/ の中身は発展編で」と明示して深追いを避ける -->

## 5. 具体的にやること

### S07 ｜ 用意するのは3つ

`type: message` ｜ `visual: mermaid`

ルールを書く。AIが参照できるデータを置く。検証手段を用意する。この3つです。

[figure: AI環境設定で用意する3つ]

```mermaid
flowchart TB
    R["AI 環境設定で用意するもの"] --> P1["① ルールを書く<br/>CLAUDE.md"] & P2["② 参照データを置く<br/>仕様書・設計書"] & P3["③ 検証手段を用意する<br/>テスト"]
    P1 --> D1["毎回渡る前提になる"]
    P2 --> D2["実装時に読ませる材料になる"]
    P3 --> D3["与えると精度が上がる"]
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff,font-weight:bold
    classDef sub fill:#1e2430,stroke:#3d4757,color:#a8b2c1
    class P1,P2,P3 hi
    class D1,D2,D3 sub
```

<!-- fig: ③ は断定しない。「必ず上がる」ではなく「上がる」トーンで -->
<!-- note: ②は「AIが実装時に参照できるデータを置く」と言う。仕様書を書くのはAIのためではないが、置き方は AI のために決める -->
<!-- note: ③は言い切らない。「絶対ではないが、検証手段を渡して実装させると精度が上がる」と言う -->

## 6. ディレクトリの例

### S08 ｜ 小規模の場合

`type: message` ｜ `visual: mermaid`

機能数が少ないうちは、この形で足ります。設計書は3種類、AI環境設定はルート直下に置きます。

[figure: 小規模プロジェクトのディレクトリ]

```mermaid
flowchart TB
    ROOT["プロジェクトルート/"]
    ROOT --> CM["CLAUDE.md"]
    ROOT --> DOT[".claude/"]
    ROOT --> DOCS["docs/"]
    ROOT --> SRC["src/"]
    DOCS --> S1["spec/<br/>要件定義<br/>SPEC.md"]
    DOCS --> S2["basic_design/<br/>基本設計<br/>BASIC_DESIGN.md"]
    DOCS --> S3["detail_design/<br/>詳細設計<br/>DETAIL_DESIGN.md"]
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff,font-weight:bold
    classDef doc fill:#1e2430,stroke:#3d4757,color:#a8b2c1
    class CM,DOT hi
    class DOCS,S1,S2,S3,SRC doc
```

<!-- note: ★ファイル名は description に書かない。Canva のAIにリライトされて壊れる。必ず図で出す -->
<!-- note: 「AI環境設定は設計書ではないので docs/ の下に入れない」を口頭で言う -->

### S09 ｜ 大規模の場合

`type: message` ｜ `visual: mermaid`

機能が増えたら機能別に分けます。3種類の設計書すべてを同じように分け、実装のモジュール名と揃えます。

[figure: 大規模プロジェクトの全体構成。3種類とも機能別に分ける]

```mermaid
flowchart LR
    ROOT["プロジェクトルート/"] --> CM["CLAUDE.md"]
    ROOT --> DOT[".claude/"]
    ROOT --> DOCS["docs/"]
    ROOT --> SRC["src/<br/>├─ auth/<br/>└─ payment/"]
    DOCS --> SP["spec/　要件定義<br/>├─ auth/<br/>└─ payment/"]
    DOCS --> BD["basic_design/　基本設計<br/>├─ auth/<br/>└─ payment/"]
    DOCS --> DD["detail_design/　詳細設計<br/>├─ auth/<br/>└─ payment/"]
    classDef hi fill:#1e2430,stroke:#ff6b35,stroke-width:3px,color:#ff6b35
    classDef root fill:#1e2430,stroke:#3d4757,color:#e8eaed
    class SP,BD,DD,SRC hi
    class ROOT,CM,DOT,DOCS root
```

<!-- fig: オレンジ枠の4つで同じ名前（auth / payment）が並んでいることが見えればよい。枠線で揃え、塗りつぶさない -->
<!-- note: ★spec だけではない。基本設計も詳細設計も同じように分ける、と口頭で必ず言う -->
<!-- note: 「最初からこれを作らない。読み切れなくなってから分ける」と一言添える -->

## 7. まとめ

### S10 ｜ まとめ

`type: message` ｜ `visual: mermaid`

AIに最初に渡っているのはプロジェクトのルールだけです。そこを整える工程を1つ挟めば、前提が揃った状態から始められます。

[figure: 今日の流れの再掲。課題から打ち手まで1本の線にする]

```mermaid
flowchart LR
    A["手戻りに<br/>時間が消える"] --> B["AI に前提が<br/>渡っていない"] --> C["AI 環境設定"]
    C --> D1["① ルールを書く"]
    C --> D2["② 参照データを置く"]
    C --> D3["③ 検証手段を用意する"]
    D1 --> E["前提が揃った状態から始まる"]
    D2 --> E
    D3 --> E
    classDef ng fill:#1e2430,stroke:#3d4757,color:#8b95a5
    classDef hi fill:#ff6b35,stroke:#ff6b35,color:#fff,font-weight:bold
    classDef sub fill:#1e2430,stroke:#3d4757,color:#e8eaed
    class A,B ng
    class C,E hi
    class D1,D2,D3 sub
```

<!-- note: 図の左から右へ指でなぞりながら話す。ここで新しい情報を足さない -->
