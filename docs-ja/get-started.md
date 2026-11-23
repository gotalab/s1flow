---
description: コーディングエージェントに、自分のケースで Decision Model を比べてもらい、選んだものをアプリで動かします。先に CLI と s1flow の Skill を入れます。
translated_from: e7a58a57e6a9
---

# はじめる

s1flow は、コーディングエージェントに頼んで使います。何を判断したいかを、自分の言葉で伝えてください。

```text
Use s1flow to decide whether a new GitHub issue is a bug. Call the task is-bug,
collect 200 labeled issues, compare the models and show me the result.
```

エージェントがケースを集め、モデルを比べ、結果を見せます。選ぶのはあなたで、それをアプリが動かします。最初に頼む前に、エージェントには CLI と s1flow の Skill が要ります。

## CLI を入れる { #install-the-cli }

Python 3.13 以降が要ります。

```bash
uv tool install "s1flow[eval]"
```

## コーディングエージェントに Skill を追加する { #add-the-skill-to-your-coding-agent }

| エージェント | 方法 |
|---|---|
| Claude Code | `/plugin marketplace add gotalab/s1flow` のあと `/plugin install s1flow@s1flow` |
| Codex | `codex plugin marketplace add gotalab/s1flow` のあと、Plugins ディレクトリから s1flow を入れる |
| Cursor などのエージェント | `s1flow init --skill` が、Git のルートの `.agents/skills/` と `.claude/skills/` に Skill をコピーする |

プラグインは、エージェントのプラグイン管理で更新されます。`s1flow init --skill` はファイルをリポジトリにコピーするので、もう一度実行したときだけ変わります。

## エージェントに頼む { #ask-your-agent }

Skill を入れたら、上のように頼みます。エージェントは `s1flow init` を実行します。これは `s1flow/` フォルダを作るだけで、リポジトリのほかの部分には触れません。既定のラインナップに要るキーは `OPENROUTER_API_KEY` の一つで、issue を取ってくるにはサインイン済みの `gh` CLI が要ります。

そこからエージェントは、

1. タスク（`s1flow/tasks/is-bug/task.py`）を書きます。問い、ラベルの読み方、objective です。
2. ラベル付きのケースを集め、`s1flow cases check` で確かめます。
3. `s1flow run` で、ラインナップのすべてのモデルに聞きます。
4. `s1flow report` の比較を見せ、選ぶのはあなたに任せます。

比較は、モデルとプロンプトごとに、目標の正解率で判断のどれだけを自分で引き受けられるかを、信頼区間、レイテンシ、費用と一緒に示します。正解率だけでなくそれを見る理由は、[考え方](concepts.md)で説明しています。

## 選んで、ポリシーとして保存する { #choose-and-save-the-choice-as-a-policy }

モデルを選ぶと、エージェントが `s1flow adopt` を実行します。比較のときにホールドアウトしたケースで選んだものを試し、通ったときだけ保存します。結果が*ポリシー*です。モデル、問い、確信度のしきい値を持つ一つの JSON ファイルです。それを含むプルリクエストを出し、マージがリリースです。

## アプリで動かす { #run-it-in-your-app }

アプリに要るのは、httpx と pydantic だけに依存する本体のパッケージと、呼び出してよいモデルを並べた `connections.toml` です（[書き方](app.md#your-first-decision)）。

```bash
pip install s1flow
```

```python
from s1flow import Client, policies

client = Client(connections="connections.toml")
policy = policies.load(path="s1flow/policies/is-bug/v1.json", client=client)
decision = policy.decide({"text": "Crash on startup"})
decision.value, decision.probability   # True, 0.93
```

答えで何をするかは、あなたのコード次第です。そのまま実行するか、確率がポリシーの最低値より低ければ人に回します。正解が分かったら記録してください。次の比較のケースになります（[フィードバックと改善](feedback.md)）。

ラベルがまだありませんか？ [今日ポリシーを出して](app.md)、あとで評価することもできます。

## 次に読む { #next }

- [考え方](concepts.md)：s1flow が使う言葉と、任せる前に確かめる理由。
- [評価して比べる](evaluate.md)：エージェントの作業の裏にあるコマンド。
- [ベンチマーク](https://gotalab.github.io/s1flow/benchmarks/)：公開タスクでの比較の例（英語）。
