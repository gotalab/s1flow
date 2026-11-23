---
translated_from: 0374ffd4aa92
---

# CLI、エージェント、CI

## CLI { #the-cli }

どのコマンドにも `--help` があります。機械で読める出力が要るときは `--json` を付けます。通知とエラーは stderr に出ます。終了コードは、0 が成功、1 がゲートを通らなかったか何かが見つかったとき、2 が使い方や設定の誤り、または実行できなかったときです。

## Agent Skill { #the-agent-skill }

Skill は、[はじめる](get-started.md#add-the-skill-to-your-coding-agent)のとおりに入れます。プラグインは Cursor のマニフェストも持ち、Agent Plugins の形式に従っているので、Cursor のチーム向けマーケットプレイスにインポートするチームにも向いています。`SKILL.md` は、6 つのリファレンス（collect、measure、ship、app、learn、setup）のうち、各段階でどれを読むかを示します。Skill は `plugin/skills/s1flow/` にあり、プラグインとパッケージの両方にこのフォルダが入っています。Skill は、ケース集め、比較、見直し、改善を同じ CLI で進めます。CLI とは別の実装ではありません。

「はじめる」の例のように頼むと、Skill は `github.py` スクリプトで issue を取ってきて、`cases check`、`run`、`report` を実行し、どの候補を選ぶかはあなたに任せます。

## GitHub Actions { #github-actions }

`decide/action.yml` は、本体のパッケージと明示的な `connections` の入力を使い、`answer`、`probability`、`below_min_probability`、`decision_id`、`policy` を出力します。評価用の Action はありません。`adopt` が、実行したその場所で、ホールドアウトしたテスト用のケースで候補を試します。その結果はプルリクエストに含まれます（[ポリシー、証拠、リリース](policies.md#evidence-and-releases)）。

入力はファイルと環境変数で渡し、シェルのコマンドに貼り込むことはありません。ワークフローは、選んだパッケージを最初に入れます。実行時にポリシーを読み込んでも、何かがインストールされることはありません。本番のワークフローでは、Action をリリースのタグかコミットの SHA に、パッケージをバージョンに固定してください。decide の Action を呼ぶワークフローの例は [examples/](https://github.com/gotalab/s1flow/tree/main/examples) にあります。
