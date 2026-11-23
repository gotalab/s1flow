---
translated_from: bad67fd44e61
---

# フィードバックと改善

正解が分かったら判断ごとに記録し、本番でポリシーを測り、記録した判断を新しいケースにします。

## フィードバックを記録する { #record-feedback }

`case_id` は、チケットのような業務上の項目を指します。`decision_id` は、一つのポリシーが一つの入力について下した一つの判断を指します。フィードバックは、返ってきた判断 ID に対して記録します。issue が編集されたり、もう一度呼んだりすると、新しい ID になります。

```bash
s1flow feedback record ticket-bug@v1 DECISION_ID true --log decisions.jsonl \
  --path policies/ticket-bug/v1.json
s1flow feedback measure ticket-bug decisions.jsonl --json         # measures; --add also adds the cases
s1flow optimize ticket-bug --json                  # a new candidate; report and adopt as for any other
```

人がまとめて答えを直すとき（レビュー担当がスプレッドシートでラベルを直す、など）は、判断ごとに `record` するのではなく、一度に取り込みます。

```bash
s1flow feedback import ticket-bug@v1 labels.csv --log decisions.jsonl --path policies/ticket-bug/v1.json
```

ファイルは、ヘッダーに `decision_id` と `label` を持つ CSV（ほかの列は無視し、ラベルは `record` と同じように読みます）か、`{"decision_id": ..., "label": ...}` の JSON Lines です。先にすべての行を確かめます。問いの答えになっていないラベル、ログでは別のポリシーの判断、一つの判断に 2 つのラベル、のどれかがあれば取り込みを止め、何も書きません。ログに無い判断 ID は、別のログにあるかもしれないので、知らせを出したうえで記録します。

アプリは、どこに記録するかを指定しない限り何も記録しません。`policies.load(..., log=PATH)`（または `decide --log`）を渡すか、OpenTelemetry のトレーサープロバイダーを設定してください。どちらも無ければ、最初の `decide` が警告を出し、`feedback` はラベルを捨てずにエラーになります。

## 本番で測る { #measure-in-production }

測定では、不明な ID、食い違う答え、ポリシーのダイジェストが合わないもの、有効な入力に結び付けられないフィードバックを飛ばし、飛ばしたものをそれぞれ報告します。重複したイベントは一度だけ数え、あとからの訂正は同じ判断の履歴に残ります。`measure` は測って、足せるケースを数えるだけです。`--add` を付けると、それを `tasks/<task>/feedback.jsonl` に足します。判断の入力が新しいケースになるのは、その入力を記録していたときだけです。

本番での測定は、採用した目的の指標と判断のルールを使います。測れるのはフィードバックのある判断だけで、それが判断全体のどれだけかも報告します。ラベルがたくさんあっても、偏りなく集められたとは限りません。

## プロンプトを最適化する { #optimize-the-prompt }

`s1flow optimize` は実験的な機能です。オプションや保存する記録は、リリースの間で変わることがあります。

`s1flow optimize` は、task.py が指定する最適化器を動かします（テンプレートでは `optimizer=Gepa(budget=300, reflection=None)`）。GEPA は、学習用と検証用のケースで、代わりのスコア（半分は正しさ、半分は 1 − Brier スコア）を使ってより良いプロンプトを探します。テスト用のケースが渡されることはありません。s1flow はそのあと、最良のプロンプトを新しい候補としてすべてのケースで動かします。モデルの重みを学習することはなく、新しいプロンプトを勝手に本番に入れることもありません。`s1flow report` がほかの候補と比べ、選べば `s1flow adopt` が現在のものにします。`--budget`、`--reflection`、`--patience`、`--max-cost` で、1 回の実行の GEPA の設定を変えられます。

ほかの最適化器も同じように差し込めます。task.py に `name`、`settings()`、`run(problem)` を持つオブジェクトを置くか（`problem` はタスク、モデル、出発点の問い、学習用と検証用のケースを持ちます。`run` は `Found` を返します。問い、モデルの呼び出し、それ以外にかかった費用、そして `detail` に独自の情報です）、パッケージのファクトリーを `s1flow.optimizers` エントリーポイントグループに登録して、文字列で指定します（`optimizer="my-optimizer"`）。どの最適化器の結果も、同じ記録 `tasks/<task>/optimized/<variant>.json`（`s1flow/optimized@2`）に保存されます。
