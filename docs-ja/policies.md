---
translated_from: d993fc68dae7
---

# ポリシー、証拠、リリース

ポリシーは、アプリが動かす仕様です。その隣に評価の記録が置かれ、`channels.json` が `current` のバージョン、つまりアプリが動かすバージョンを示します。`adopt` は選んだ候補を新しいバージョンとして保存し、作業ツリーでそのバージョンを `current` にします。この変更を含むプルリクエストでレビューし、マージした時点でリリースになります。
このページでは、この 3 つがどう組み合わさるかと、`adopt` が断るのはどんなときかを説明します。

## ファイル { #files }

```
policies/ticket-bug/v1.json             the PolicySpec your app runs
policies/ticket-bug/v1.evaluation.json  the evaluation and selection record, if there is one
policies/ticket-bug/channels.json       {"schema": "s1flow/channels@1", "channels": {"current": 3}}: the version that runs
policies/ticket-bug/history.jsonl       one line per switch of current, and per refused candidate: when, which version, who, why
```

## 証拠とリリース { #evidence-and-releases }

評価の記録は、ポリシーのダイジェストと、実行のしかた、データセット、入力アダプタ、評価の契約（evaluation contract）それぞれのフィンガープリントを指します。評価のコード、objective、制約、採点のコード、宣言した価格、ケースの分割のどれかを変えると、古い候補一覧や採用の記録は使えなくなるので、採点し直してもう一度採用します。評価の記録がポリシーそのものを変えることはなく、本番の実行が評価の記録を読むこともありません。

`adopt` は選んだ候補とあなたの理由を記録し、その候補を `current` にします。古くなった証拠は受け付けません。候補がテスト用のケースで基準に届かなければ、何も書きません。`--force` を付けると、それでもリリースできます。その場合、評価の記録には `forced` と付き、あなたの理由がその説明になります。`--force` が無視するのはホールドアウトのテストだけで、古い証拠は無視しません。このホールドアウトのテストが、ポリシーをリリースする前に s1flow が出す唯一の合否判定です。新しいバージョンを含むプルリクエストでは、`vN.evaluation.json` と `history.jsonl` で結果を確かめられます。マージするかどうかは人が決めます。

保存した `vN.json` や `vN.evaluation.json` は、書き換えも、名前の変更も、削除もされません。`adopt` はバージョンを足すだけなので、アプリが動かしたバージョンは、リリースしたときのままいつでも読み直せます。

評価していない、手で書いたポリシーも、本体のパッケージだけで `adopt --spec FILE --reason "..."` によって保存し、`current` にできます。そのとき s1flow は、このポリシーには証拠が無いと伝えます。

前に動いていたバージョンに戻すには、そのバージョンを次のバージョンとして保存し直します。番号を付け直した `vN.json` を `adopt --spec` に渡すと、評価なしで、まったく同じ仕様が戻ります。`s1flow adopt TASK CANDIDATE` にそのバージョンの候補を渡すと、今のタスク、問い、ケースでその候補を測り直します。新しいバージョンを採用したプルリクエストは revert しないでください。保存したバージョンが消えてしまいます。

`current` を切り替えられるのは `adopt` だけです。切り替えるたびに、`policies/<task>/history.jsonl` に理由を 1 行足します（いつ、どのバージョン、その前のバージョン、誰が、なぜ、測った候補ならホールドアウトのテストの判定）。ホールドアウトのテストで基準を下回って断った候補にも 1 行残るので、通るまでテスト用のケースで候補を試し続けると、その跡が残ります。

```bash
s1flow adopt --spec spec.json --reason "hand-written first rule" --json
s1flow adopt ticket-bug decider@openrouter/short --reason "v2 misreads feature requests"
s1flow export ticket-bug --out policies.json
```

## エクスポートとデプロイ { #exporting-and-deploying }

エクスポートしたポリシーのセットには、ポリシーとその中身のダイジェストが入り、評価のデータや認証情報は入りません。受け取るアプリは、自分の接続ファイルを用意します。ダイジェストが示すのは中身が変わっていないことだけで、誰が承認したかは示しません。ポリシーは、アプリのいつもの信頼できるリリース手順でリリースしてください。ポリシーがリモートのコードを読み込んだり、パッケージを入れたりすることはできません。

## スキーマ { #schemas }

`schema/` にある公開の JSON Schema は、型から生成されます（`scripts/write_schemas.py`）。対象は、ポリシー、エクスポートしたポリシーのセット、判断のログ、判断と応答、ケース、実行、ケースの分割、比較、評価の記録、履歴です。JSON Schema が確かめるのは構造だけです。フィールドをまたぐ確認（たとえば、選択の問いで決めた正の選択肢がしきい値と合うか）と、接続ファイルに対するポリシーの確認には、`s1flow adopt --spec FILE --validate` を使います。
