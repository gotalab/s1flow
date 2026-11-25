---
translated_from: ecb25f85cfc2
---

# フィードバックと改善

正解が分かったら判断ごとに記録し、本番でポリシーを測り、記録した判断を新しいケースにします。

## フィードバックを記録する { #record-feedback }

`case_id` はチケットのような業務上の項目を指します。`decision_id` は一つのポリシーが一つの入力について下した一つの判断を指します。フィードバックは返ってきた判断 ID に対して記録します。issue が編集されたときや、もう一度呼び出したときは、新しい ID になります。

```bash
s1flow feedback record ticket-bug@v1 DECISION_ID true --log decisions.jsonl \
  --path policies/ticket-bug/v1.json
s1flow feedback measure ticket-bug decisions.jsonl --json         # measures; --add also adds the cases
```

レビュー担当がスプレッドシートでラベルを直すときのように、人がまとめて答えを直すときは、判断ごとに `record` せず、一度にインポートします。

```bash
s1flow feedback import ticket-bug@v1 labels.csv --log decisions.jsonl --path policies/ticket-bug/v1.json
```

ファイルは、ヘッダーに `decision_id` と `label` を持つ CSV（ほかの列は無視し、ラベルは `record` と同じように読みます）か、`{"decision_id": ..., "label": ...}` の JSON Lines です。インポートの前に、すべての行を確かめます。問いの答えになっていないラベル、ログ上では別のポリシーが下した判断、2 つのラベルが付いた判断のどれかがあれば、インポートを止め、何も書きません。ログに無い判断 ID は、別のログにあるかもしれないので、通知を出したうえで記録します。

アプリは、記録先を指定しない限り何も記録しません。`policies.load(..., log=PATH)`（または `decide --log`）を渡すか、OpenTelemetry のトレーサープロバイダーを設定してください。どちらも無ければ、最初の `decide` が警告を出し、`feedback` はラベルを捨てずにエラーになります。

## 本番で測る { #measure-in-production }

測定では、不明な ID、食い違う答え、ポリシーのダイジェストが合わないもの、有効な入力に結び付けられないフィードバックを飛ばし、飛ばしたものをそれぞれ報告します。重複したイベントは一度だけ数え、あとからの訂正は同じ判断の履歴に残ります。`measure` は測って、足せるケースを数えるだけです。`--add` を付けると、そのケースを `tasks/<task>/feedback.jsonl` に足します。判断の入力が新しいケースになるのは、その入力を記録していたときだけです。

本番での測定には採用した objective と判断のルールを使います。測定が表すのはフィードバックのある判断だけで、それが判断全体のどれだけに当たるかも報告します。ラベルがたくさんあっても、偏りなく集められたとは限りません。

## 問いを改善する { #improve-the-question }

s1flow の Skill を入れたコーディングエージェントは、人がするのと同じやり方で問いを改善します。そのとき、ラベル付きケースの 3 つの分割（学習用、検証用、テスト用）に、それぞれ別の役目を持たせます。

```bash
s1flow report ticket-bug --split train --out work    # the mistakes to write from: work/questions/<variant>.md
s1flow cases check ticket-bug                        # names a variant that repeats a train case's text
s1flow run ticket-bug --models jev/plain,jev/scope   # the variants it wrote in task.py
s1flow report ticket-bug --split val                 # pick among them on cases their writer never read
s1flow adopt ticket-bug jev/plain --reason "..."     # the held-out test, read once, for the pick
```

各バリアントは学習用のケースだけから書きます。今の問いが間違えたケースと、0.9 未満で答えたケースのすべてを、モデルの上位の答えと一緒に読みます（`--split train --out`）。選ぶのは検証用のケースだけで行い、`adopt` は、それまで何も読んでいないテスト用のケースで、選んだものを確かめます。s1flow 自身の比較では、学習用と検証用の間違いをすべて読んで書いた問いは、そのケースでは良い値でしたが、テスト用のケースではそうなりませんでした。学習用から書いて検証用で選んだ問いは、テスト用のケースでも良い値を保ちました。学習用の言葉（あるケースの文、一つの学習用ケースで見つけたキーワードや例）を借りたバリアントは、そのケースにしか合いません。検証用やテスト用のケースが学習用と似た言い回しだと、この問題はその値に表れません。`cases check` は、学習用ケースの 6 語以上を続けてそのまま使うバリアントを挙げ、Skill は新しいエージェントに、借りた言葉を一つずつ探させます。`report` は、バリアントが、測っているそのケースから書かれたかもしれないことを注記します。その場合、そこでの値は高めに出ます。手順は Skill の `references/improve.md` にあります。
