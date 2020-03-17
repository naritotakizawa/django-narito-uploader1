## 必要なもののインストール

frontendディレクトリ内で、次コマンド

```
npm install
```

## テスト

Rest Framework側のテスト(manage.pyと同じ階層で)

```
coverage run --source='nuploader1/' manage.py test
coverage report -m --skip-covered
```


Vue側のテスト(frontendディレクトリ内で)

```
npx vue-cli-service test:unit
```

## ビルド

Vueファイル等を変更し、それを本番環境に反映するにはビルドが必要です。

frontendディレクトリ内で次コマンド

```
npm run build
```