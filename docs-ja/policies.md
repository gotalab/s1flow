---
translated_from: d993fc68dae7
---

# ポリシー、証拠、リリース

ポリシーは、アプリが動かす仕様です。評価の記録がその隣に置かれ、`channels.json` が `current` のバージョン、つまりアプリが動かすものを示します。`adopt` は選んだ候補を新しいバージョンとして保存し、作業ツリーでそれを現在のものにします。その変更を含むプルリクエストがレビューで、マージがリリースです。
このページでは、この 3 つがどう組み合わさるかと、`adopt` が断るときを説明します。

## ファイル { #files }

```
policies/ticket-bug/v1.json             the PolicySpec your app runs
policies/ticket-bug/v1.evaluation.json  the evaluation and selection record, if there is one
policies/ticket-bug/channels.json       {"schema": "s1flow/channels@1", "channels": {"current": 3}}: the version that runs
policies/ticket-bug/history.jsonl       one line per switch of current, and per refused candidate: when, which version, who, why
```


## 証拠とリリース { #evidence-and-releases }

評価の記録は、ポリシーのダイジェストと、どう動かしたか・データセット・入力アダプタ・評価の約束事のフィンガープリントを指します。評価のコード、objective、制約、採点のコード、宣言した価格、ケースの分け方のどれかを変えると、古い候補一覧や採用の記録は使えなくなるので、採点し直してもう一度採用します。評価の記録がポリシーそのものを変えることはなく、本番の実行がそれを読むこともありません。

`adopt` は選んだ候補とあなたの理由を記録し、それを現在のものにします。古くなった証拠は受け付けず、候補がテスト用のケースで届かなければ何も書きません。`--force` を付けるとそれでも出せます。その場合、評価の記録には `forced` と付き、あなたの理由がその説明になります。`--force` が無視するのはホールドアウトのテストだけで、古い証拠は無視しません。このホールドアウトのテストが、ポリシーを出す前に s1flow が出す唯一の合否です。新しいバージョンを含むプルリクエストは、その結果を `vN.evaluation.json` と `history.jsonl` で見せます。マージするかは人が決めます。

保存した `vN.json` や `vN.evaluation.json` は、書き換えも、名前の変更も、削除もされません。`adopt` はバージョンを足すだけなので、アプリが動かしたバージョンは、出したときのままいつでも読み直せます。

評価していない、手で書いたポリシーは、本体のパッケージだけで `adopt --spec FILE --reason "..."` によって保存し、現在のものにできます。s1flow は、それに証拠が無いことを伝えます。

前に動いていたバージョンに戻すには、それを次のバージョンとして保存し直します。番号を付け直したその `vN.json` を `adopt --spec` に渡すと、評価なしで、まったく同じ仕様が戻ります。`s1flow adopt TASK CANDIDATE` にその候補を渡すと、今のタスク、問い、ケースでその候補を測り直します。新しいバージョンを採用したプルリクエストを revert しないでください。保存したバージョンが消えてしまいます。

`current` を指せるのは `adopt` だけで、そのたびに `policies/<task>/history.jsonl` に理由を足します（いつ、どのバージョン、その前のバージョン、誰が、なぜ、測った候補ならホールドアウトのテストの判定）。ホールドアウトのテストで届かずに断った候補にも 1 行残るので、通るまでテスト用のケースで候補を試し続けると、その跡が残ります。

```bash
s1flow adopt --spec spec.json --reason "hand-written first rule" --json
s1flow adopt ticket-bug decider@openrouter/short --reason "v2 misreads feature requests"
s1flow export ticket-bug --out policies.json
```

## 書き出しとデプロイ { #exporting-and-deploying }

書き出したポリシーのセットには、ポリシーとその中身のダイジェストが入り、評価のデータや認証情報は入りません。受け取るアプリは、自分の接続ファイルを用意します。ダイジェストは中身が変わっていないことを示すだけで、誰が承認したかは示しません。ポリシーは、アプリの普段の、信頼できるリリースの手順で出してください。ポリシーがリモートのコードを読み込んだり、パッケージを入れたりすることはできません。

## スキーマ { #schemas }

`schema/` にある公開の JSON Schema は、型から作られます（`scripts/write_schemas.py`）。ポリシー、書き出したポリシーのセット、判断のログ、判断と応答、ケース、実行、ケースの分け方、比較、評価の記録、履歴です。JSON Schema が確かめるのは構造だけです。フィールドをまたぐ確認、たとえば選択の問いで決めた正の選択肢がしきい値と合うか、や、接続ファイルに対するポリシーの確認には、`s1flow adopt --spec FILE --validate` を使います。
