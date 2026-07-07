# ADR-0004(api): ドメイン層のレイヤリングと命名規約

## ステータス

承認済み (2026-07-02、2026-07-07 rain/station 実装に伴いポート分割を追記)

## コンテキスト

ADR-0001 で外部データソースの抽象化(port / infrastructure)は決定したが、
`domain` 層の内部構造と命名規約は未定だった。

一般に `services/` や `model/` のような総称フォルダは、責務が曖昧になりやすい:

- 「service」は アプリケーション層(オーケストレーション)・ドメイン層(純粋な
  ドメインロジック)・インフラ層(ゲートウェイ)で別々の意味に多重使用され、
  意味が一意に定まらない
- 「model」は entity なのか value object なのかを曖昧にする
- いずれも分類に迷ったロジックの投棄場所になり、時間とともに肥大化する

## 決定

### feature 別パッケージ + 役割名。総称フォルダ(`services/` `model/`)は作らない

- `domain/` の下を feature 単位(`mesh/` `rain/` `station/`)で分割する
- **振る舞い(builder / resolver / policy 等)は feature 直下に、役割名で置く**
  (`MeshBuilder` `RainValueResolver`)。`*Service` 接尾辞・`service/` フォルダは
  使わない
- supporting なステレオタイプのみサブフォルダに分ける。フォルダ名は意味が一意な
  名詞系に限定する: `value_object/` `interface/`(`entity/` は後述の条件時のみ)
- 外部 I/O・キャッシュ・DTO 変換・複数ステップの調整を担う「ユースケース」は
  `domain` ではなく `application/` に置き、動詞ベースで命名する
  (`GetMesh` `GetTimeseries`)

### value object はリッチに、ドメインサービスは薄く(貧血ドメインモデルの回避)

- value object は **immutable かつ自己検証**とする(生成時に不変条件を強制。
  例: `TileId` は x/y をタイル数 `2^z` の範囲に強制、`RainValue` は負値を弾く)
- **単一オブジェクトの性質・振る舞いは、そのオブジェクトのメソッドに置く**
  (例: `TileId.from_coordinate()`)。これらを builder / resolver 側に吸い上げると
  value object がデータ袋化し、貧血ドメインモデルに陥る
- 固定グリッドは XYZ タイル準拠とし(ADR-0001)、セルサイズはタイル(z+緯度)から
  一意に導出できるため専用フィールドや km 固定マップは持たない(必要になった消費者側で
  算出する。YAGNI)。「2km より細かくしない」下限は `ZoomLevel.tile_zoom` の
  タイルズーム上限(緯度35°付近で1タイル≒2km となるズーム14)で担保する
- `MeshBuilder` / `RainValueResolver` 等のドメインサービスは、**複数オブジェクトに
  またがり単一オブジェクトに属せない横断ロジックに限定**し、薄く保つ
- ただしシリアライズ・DTO 変換・JSON スキーマは domain に持ち込まない
  (`application/` の責務。ドメインオブジェクトに HTTP/JSON を知らせない)

### ロジックの振り分けルール(上から順に判定し、該当した時点で確定)

1. 特定の value object 1個の性質か → その VO のメソッド/プロパティ
2. 単一エンティティ1個の状態変化か → そのエンティティのメソッド
3. 複数ドメインオブジェクトにまたがる純粋計算か → 振る舞いクラス(feature 直下)
4. 外部 I/O・キャッシュ・変換・調整か → `application/` または
   `interface`(port) / `infrastructure`

3 を最小限に保ち、1・2 を先に疑うことが、貧血ドメインモデルと総称フォルダの
肥大化の両方を防ぐ砦となる。

### entity は識別子テストを満たすまで導入しない

- 判定基準: **識別子(ID)を持ち、時間とともに状態が変わるか**。Yes なら entity、
  No(不変・値で等価)なら value object
- 本 API は「取得 → 計算 → 返す」の read 中心で可変な集約を持たず、現時点では
  `Station`(観測所)を含め全て value object 扱いで足りる。`Station` は読み取り
  専用の参照データとして VO とする
- 上記テストを満たす可変オブジェクトが登場した時点で初めて `entity/` を追加する

### ディレクトリ構成(想定)

```
app/
  domain/
    mesh/
      builder.py            # MeshBuilder(振る舞い・feature 直下)
      value_object/
        grid.py             # TileId, MeshGrid, MeshCell
        zoom.py             # ZoomLevel
    rain/
      resolver.py           # RainValueResolver
      value_object/
        value.py            # RainValue, Provenance, CellRainValue
    station/
      nearest.py            # NearestStationPolicy
      value_object/
        station.py          # Station(参照データ → VO)
    shared/
      interface/
        amedas_observation_provider.py  # AmedasObservationProvider(port)
        analyzed_rain_value_provider.py # AnalyzedRainValueProvider(port)
  application/
    get_mesh.py             # GetMesh(ユースケース)
    get_timeseries.py
```

補足:
- feature 固有の port が出てきたら、そのときだけ `mesh/interface/` のように
  feature 内に置く。横断 port(現状 `AmedasObservationProvider` /
  `AnalyzedRainValueProvider` の2つ)は `shared/interface/`
- 気象庁アメダス(観測所一覧の一括取得)と YOLP(タイル単位のオンデマンド取得)は
  呼び出し形状が根本的に異なる(バルク取得 vs 単発取得)ため、単一の
  `WeatherProvider` にまとめず提供元ごとに port を分ける。呼び出し側
  (application)は用途に応じて必要な port のみに依存できる
- サブフォルダは中身が 2 ファイル以上になる段階で切る。1 ファイルのために
  フォルダを作らない(過剰なネストの回避)。`shared/` も第2の受け皿になりやすい
  ため、本当に複数 feature で共有するものだけに限定する

### 不採用にした方式(検討の記録)

| 方式                          | 不採用理由                                                            |
| ----------------------------- | --------------------------------------------------------------------- |
| レイヤー別 + `services/` 一括 | 「service」が多層で多重使用され責務曖昧化・肥大化を招く               |
| feature 内に `service/` を新設 | 振る舞いは feature 直下に役割名で置けば足り、総称フォルダは不要        |
| `model/` にドメイン名詞を集約 | entity と value object を曖昧にする。ステレオタイプを一意に保てない    |
| entity/value_object を先行分離 | 現状 entity が存在しない。識別子テストを満たすまでは YAGNI            |

## 結果

- `domain` と `infrastructure` の間に `application/` 層を新設する
  (ユースケースの置き場)
- port(抽象インターフェース)は `interface/` に置く。横断 port は
  `domain/shared/interface/`、feature 固有は各 feature の `interface/`
- 実装・レビュー時は上記の振り分けルールに沿っているかを確認する。特に
  builder / resolver へロジックを足す際は、ルール 1・2(VO/エンティティの
  メソッド化)に先に当てはまらないかを必ず疑う
- value object は immutable・自己検証で実装し、貧血ドメインモデルを避ける
- ADR-0001 の「結果」に記した各種ドメインロジックは、本 ADR の構成に従って配置する

---

フォーマット参考: https://zenn.dev/maman/articles/f91a52bc06024d
