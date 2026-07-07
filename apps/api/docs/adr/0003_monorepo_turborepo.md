# ADR-0003: モノレポ構成とツール選定(Turborepo + pnpm)

## コンテキスト

Next.js(BFF込み)とFastAPIを、単一リポジトリで管理したい。将来的にアプリケーションが
増える可能性(管理画面など)も見据え、拡張しやすいディレクトリ構成にしておきたい。

## 決定

- ディレクトリ構成: `apps/*` `packages/*`
- モノレポ管理ツール: Turborepo
- パッケージマネージャー: pnpm

理由:

**apps/ packages/ 構成**

- Turborepo公式スキャフォールド(`create-turbo`)の標準命名であり、情報・実例が探しやすい
- 将来アプリケーションが増えた場合(例: `apps/admin`)も、同列に自然に配置できる
- `packages/shared-types` のような共有コードを置く前提があり、
  「実行可能なもの(apps)」と「共有される部品(packages)」の対比構造に意味がある

**Turborepo**

- タスク実行のキャッシュ・並列実行により、開発体験・CI速度が向上する
- Next.js + FastAPI というモノレポの実例(OSSテンプレート等)が既に存在し、
  Pythonプロジェクトも `package.json` 経由のラッパースクリプトで統合可能

**pnpm**

- シンボリックリンク方式により、モノレポ内の重複依存によるディスク容量・速度の
  悪化を防げる
- Turborepoとの相性が良く、追加設定なしで統合できる
- Phantom Dependency(package.jsonに書いていない依存が動いてしまう問題)を
  構造的に防止できる

除外した選択肢:

- `frontend/` `backend/` 構成: アプリケーションがこの2つのまま増えない前提であれば
  問題ないが、将来の拡張(管理画面等)を見据えると、モノレポツールの標準命名に
  合わせておく方が一貫性がある
- npm workspaces: 機能的には十分だが、Turborepoとの統合における実績・情報量で
  pnpmに劣る

## 結果

- チームがnpmに慣れている場合、pnpm特有のコマンド・挙動(`workspace:*`記法、
  ビルドスクリプトの承認 `pnpm approve-builds` 等)への学習コストが発生する
- `apps/api`(FastAPI)は Turborepo のネイティブ対象ではないため、
  `package.json` に `dev` / `build` / `test` スクリプトを手動で用意し、
  Pythonコマンドを呼び出すラッパーとして機能させる
- Node.js/pnpmのバージョン管理には Volta を使用する
  (Corepackとの併用は競合の原因になるため行わない)
