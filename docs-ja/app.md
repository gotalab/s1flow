---
translated_from: ccab62baf30c
---

# アプリで判断を動かす

このページでは、本体のパッケージだけを使い、何も無い状態から、アプリが呼び出す保存済みのポリシーを用意するところまで進みます。始めるのにラベルや評価は要りません。ラベル付きのケースがそろったら、[評価して比べる](evaluate.md)に進んでください。

## 実行用のパッケージを入れる { #install-the-runtime }

Python 3.13 以降が要ります。アプリに本体のパッケージを追加します。直接の依存は httpx と pydantic だけで、評価用のツールをインストールすることも import することもありません。

```bash
uv add s1flow   # or: pip install s1flow
```

## 最初の判断 { #your-first-decision }

どのモデルへの接続を許すかは、アプリが決めます。たとえば `connections.toml` は次のとおりです。

```toml
[models.triage]
provider = "typesafe"
id = "jev-1.14.0" # use a model ID your account has access to
```

プロバイダーの API キーを環境変数に入れます（この例では `TYPESAFE_API_KEY`）。外向きの通信にプロキシがキーを付けるサンドボックス（ネットワークシークレット）では、この変数を設定しないでください。そのとき s1flow は自分ではキーを送らず、401 や 403 が返ってきたら、キーが設定されていないと伝えます。どのファイルが信頼されるかと、SDK と CLI がそのファイルをどう見つけるかは、[接続ファイルとその探し方](connections.md)で説明しています。

このファイルは、ポリシーが名指しする接続を定義していなければなりません。評価から採用したポリシーは、`jev@openrouter` のようにプロジェクトのラインナップのモデルを名指しするので、そのモデルのエントリを `s1flow/s1flow.toml` からコピーしてください。

次に `bug.json` を書きます。評価のデータも、モデルの応答も、仮のスコアも要りません。

```json
{
  "schema": "s1flow/policy@2",
  "task": "ticket-bug",
  "version": 1,
  "connection": "triage",
  "model_id": "jev-1.14.0",
  "questions": {
    "bug": {
      "question": {"type": "boolean", "instructions": "Does this report describe a software defect?"},
      "rule": {"threshold": 0.5}
    }
  }
}
```

```bash
s1flow adopt --spec bug.json --connections connections.toml --validate --json
s1flow adopt --spec bug.json --root policies --connections connections.toml --reason "first rule" --json
s1flow decide --policy ticket-bug@v1 --path policies/ticket-bug/v1.json \
  --connections connections.toml --state '{"text":"Crash on startup"}' --json
```

`adopt --spec FILE --validate` は、仕様が正しいかと、接続ファイル（`--connections`、無ければプロジェクトの `s1flow.toml`）がその接続を定義し、そのモデル ID を許しているかを確かめます。モデルを呼ぶことも、何かを保存することもありません。`adopt --spec` は、ポリシーを変更できない新しいバージョンとして保存し、作った日時と作った SDK のバージョンを記録して、`current` にします。このとき、ポリシーを評価済みとして扱うことはありません。

`connections.toml` の隣に置く `app.py` では、アプリをどのディレクトリから起動しても同じように動くよう、ファイル自身の場所からパスを組み立てます。

```python
from pathlib import Path
from s1flow import Client, policies

APP = Path(__file__).resolve().parent
client = Client(connections=APP / "connections.toml")
policy = policies.load(path=APP / "policies/ticket-bug/v1.json", client=client,
                       log=APP / "decisions.jsonl", keep_state=True)
decision = policy.decide({"text": "Crash on startup"}, case_id="ticket-42")
print(decision.value, decision.probability, decision.decision_id)
policy.feedback(decision.decision_id, True)  # the correct answer, once you know it
```

`log=` は、判断と正解を残しておく場所です。ここに残した判断を測ったり、新しいケースにしたりできます。`log=` が無く、OpenTelemetry のトレーサープロバイダーも無いと、何も記録されません。最初の `decide` が警告を出し、`feedback` はエラーになります。

## ポリシーの API { #the-policy-api }

Python で `PolicySpec` を組み立てて、`DecisionPolicy(spec, client=client)` に渡すこともできます。非同期のコードでは `adecide` を使います。`decide` も `adecide` も、Task や Evaluation は読みません。

任意の `state_schema` は、JSON Schema の一部（オブジェクト・配列・スカラーの型、プロパティ、必須フィールド、追加のプロパティ）で入力の形を確かめます。完全な JSON Schema のバリデーターではありません。入力が合わなければ、リクエストを送る前に `DataError` になります。スキーマが無いと、本番の入力が評価した入力と同じ形であることを s1flow は保証できません。

`DecisionRule` には、`threshold`（はい／いいえの問い、または正の選択肢がある選択の問い）と `min_probability` を設定できます。
`Decision.below_min_probability` は、最低確率が設定されていなければ `None`、答えの確率が最低確率より低ければ `True`、それ以外は `False` です。答えが正しいことや、その行動が許されることを意味するものではありません。その先どうするかはアプリが決めます（[s1flow がアプリに任せること](#what-s1flow-leaves-to-your-app)を参照）。

## s1flow がアプリに任せること { #what-s1flow-leaves-to-your-app }

s1flow が持つのは、変えると評価で測ったものが変わるもの（モデルに送るリクエスト、モデルのバージョン、しきい値に対する答えの読み方、渡したタイムアウトを守ること）と、あとで正解を記録するのに要るもの（判断 ID、ログ、フィードバック）だけです。判断の周りにあるものはすべて、あなたのコードかエージェントのフレームワークが持ちます。それを変えても、その判断について測った数字は変わらないからです。

- **答えで何をするか。** s1flow は判断を返します。アプリがその判断で何をするか、それが許されるかは、あなたのコードが決めます。
- **確信のない答えをどこに回すか。** `below_min_probability` が `True` なら、答えの確率は最低確率を下回っています。人に回すか、大きなモデルに回すか、既定の値にするかは、あなたのコードが決めます。
- **呼び出しが失敗したときのフォールバック。** 失敗した呼び出しや、[タイムアウト](#time-limit)を過ぎた呼び出しは `ProviderError` になります。s1flow は別のモデルに切り替えません。別のモデルは別に測るべきものだからです。
- **順番、分岐、ループ。** どの判断を、どの順で、何回動かすかは、あなたのコードかフレームワークが決めます。その中で `policy.decide` を呼んでください。
- **スコアの組み合わせ。** 複数のスコアの重み付け、並べ替え、選び方は、あなた自身の計算です。

s1flow の動かし方は 2 つあります。一つは Python アプリの中のライブラリとして動かす方法で、本番ではこちらを使います。もう一つは CLI として動かす方法で、CI、GitHub Actions、スクリプト、フックなど、ときどき実行する処理に使います。CLI は呼ぶたびに新しいプロセスを起動して新しい接続を開くので、数百ミリ秒余計にかかります。そのため、人やループが待っている判断には向きません。s1flow は自前のサーバーを持ちません。HTTP で判断を返したいときは、Web フレームワークで `policy.decide` をラップしてください。

## エラー { #errors }

プロバイダーが不正な応答を返すと、s1flow は判断を返さずに `ProviderError` を出します。モデルが問いへの回答を拒否したときは、Client からは `Refusal`、ポリシーの実行では `Rejected` が返ります。設定の誤り、不正な入力、対応していない機能は、それぞれ `S1flowError` の別のサブクラスになります。

## タイムアウト { #time-limit }

プロバイダーがレート制限をかけたとき（429）、サーバー側で失敗したとき、タイムアウトしたときは、リトライします。最初の呼び出しを含めて最大 4 回試し、その間に 0.5 秒、1 秒、2 秒待ちます。1 回の試行には最大 60 秒かかることがあるので、タイムアウトが無いと、一つの判断に何分もかかることがあります。人が答えを待っているときは、判断に秒数でタイムアウトを指定してください。

```python
from s1flow import ProviderError

try:
    decision = policy.decide(state, case_id="ticket-42", timeout=1.5)
except ProviderError:
    ...  # no decision in time, or the call failed: send the case to a person or a fallback
```

このタイムアウトはリトライと待ち時間を含めた呼び出し全体にかかります。時間を過ぎると、s1flow は呼び出しを取り消して `TimedOut`（`ProviderError` の一種）を出します。そのため、失敗した呼び出しでフォールバックするコードは、遅れた呼び出しでも同じようにフォールバックします。ログには、ほかの失敗と区別して、`TimedOut: ...` というエラー付きの `failed` として残ります。`adecide` も同じ `timeout` を取ります。タイムアウトが無ければ、判断にはリトライにかかるだけの時間がかかります。

## 画像、音声、動画、PDF と入力のログ { #images-audio-video-pdfs-and-logged-input }

メディアは、ポリシーを動かす前にコードで準備した値として渡します。リスト形式の state の最上位の要素として、`media.prepare("audio", data)`（または `"image"`、`"video"`、`"pdf"`）を渡します。入力の JSON によって、実行時にファイルや URL を取ってこさせることはできません。CLI では、`--image`、`--audio`、`--video`、`--pdf PATH` で指定したローカルのファイルを読み込みます。画像には `s1flow[images]` が要ります。音声は WAV か MP3、動画は MP4 で、ファイルのバイトのまま送ります。画像はリサイズして再エンコードします。入力は、頼んだとき（`keep_state=True` か `--keep-state`）だけ記録します。

## モデルを直接呼ぶ { #call-a-model-directly }

保存したポリシーやしきい値が要らないときは、`Client` か `AsyncClient` を使います。この場合も評価は要りません。

```python
from s1flow import Client
from s1flow.client import ModelSpec
from s1flow.questions import Boolean

response = Client().responses.create(
    model=ModelSpec(provider="typesafe", id="jev-1.14.0"),
    state={"text": "Crash on startup"},
    questions={"bug": Boolean(instructions="Does this report describe a software defect?")},
)
print(response.answers["bug"].probability)
```

この `ModelSpec` は自分のコードに書いたものなので、この例に接続ファイルは要りません。シェルからは、`s1flow decide --model liquid:d1.2 --state '"Crash on startup"' --boolean "Does this report describe a software defect?"` が、プロジェクト無しで同じことをします。`provider:id` は、組み込みのプロバイダーと、そのプロバイダーに送る id を示します。モデルを別名で指すときは、アプリが許可したモデルの一覧を渡します。

```python
response = Client(connections="connections.toml").responses.create(
    model="triage",
    state={"text": "Crash on startup"},
    questions={"bug": Boolean(instructions="Does this report describe a software defect?")},
)
```

Client は、プロバイダーが対応している範囲で、はい／いいえ（`boolean`）、選択、スコア、ボックスの問いと、一つのリクエストでの複数の問いに対応します。評価はこの 4 つの型すべてを比べます。ポリシーはこのどれかの型の問いを一つ持ちます。

対応するモデルがあれば、state から値を抽出する問い（`Text`、`Number`、`Date`）や、state に書かれていない数値を推定する問い（`RangeEstimate`、`min` と `max` の間）も聞けます。Liquid の d1.2 と d1.2-ultra は、Liquid 自身の API で 4 つすべてに対応し、ほかの問いと同じ呼び出しで聞けます。OpenRouter 経由では、Clairic が 4 つすべて、Schematron がテキスト・数値・日付、Perplexity の Decider v1.3 と ScaleDown Extract がテキストに対応しています。抽出の答えの `value` は、モデルが何も見つけなければ `None` です。モデルが返せば `p_null`、`confidence`、`span` も付きます。推定の答えには `p10` と `p90` が付きます。`span` は、送ったテキストの中での文字の位置です（Liquid の `span` は、テキストの state のときだけ残ります）。JSON の state では、キーを並べ替えてインデント 1 で書き出したテキストの中での位置になります。問いの指示だけでなく名前も読むモデルがあるので、問いには抽出するものに合った名前を付けてください（`q` ではなく `order_number`）。OpenRouter はこれらの問いを別の経路で提供するので、一つのリクエストで聞けるのは、これらの問いかほかの 4 つの型のどちらかです。評価もこれらの問いを比べられ（[評価して比べる](evaluate.md)）、ポリシーもほかの型と同じようにこれらの問いを一つ持てます。

ボックスの答えの `box` は、対象が画像に写っていないとモデルが答えたときは `None` です。モデルが返せば、対象が写っている確率 `found` も付きます（Liquid の d1.2 は返します）。いつもボックスを返すモデル（jev）は、写っていないとは答えられません。対象が写っていないとモデルが答えたとき、ボックスのポリシーの判断は `None` になります。対象が写っていないケースには、`feedback record ... false` でラベルを付けます。

`Boxes` は、写っている対象一つひとつのボックスを聞き、写っていなければボックスは返りません。答えには、`confidence` と `found` 付きの各ボックスが入った `boxes`、モデルが問いの `max` で打ち切ったときの `at_least`、各スロットの `presence` が入ります。Liquid の d1.2 と d1.2-ultra が対応しています。評価でも比べられ、ポリシーも一つ持てます（`feedback record` にはボックスを JSON で渡し、無いときは `none` を渡します）。

`MultiChoice` は、当てはまる選択肢をすべて聞きます。一つも当てはまらないこともあります。答えには `choices` と、選択肢ごとの確率を入れた `probabilities` が入ります（確率の合計は 1 になりません）。Liquid の d1.2 と d1.2-ultra が対応しています。評価でも比べられ、ポリシーも一つ持てます（`feedback record ... late,damage`、無いときは `none`）。

どの呼び出しも各 JSON オブジェクトのキーを並べ替えて state を送ります。そのため、キーの順番だけが違う評価のケースと本番の呼び出しは、同じリクエストを送ります。リストの順番はそのままです。
