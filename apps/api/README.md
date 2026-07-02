# apps/api

## 概要

- 気象庁「高解像度香水ナウキャスト」（非公式エンドポイント）から雨量データを取得
- mesh（領域指定でのメッシュ取得）とtimeseries（地点クリックでの時系列取得）を提供
- Next.js製BFF(`apps/web`)からのみアクセスされれる想定（共有シークレットで内部認証）
- ホスティング: Fly.io

## ディレクトリ構成

```
src/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

## セットアップ

`docs/local-development.md`を参照
