---
translated_from: 0374ffd4aa92
---

# CLI、エージェント、CI

## CLI { #the-cli }

どのコマンドにも `--help` があります。機械で読める出力には `--json` を付けます。知らせとエラーは stderr に出ます。終了コードの 0 は成功、1 はゲートを通らなかったか何かが見つかった、2 は使い方・設定の誤りか動かせなかった、です。

## Agent Skill { #the-agent-skill }

Skill は、[はじめる](get-started.md#add-the-skill-to-your-coding-agent)のとおりに入れます。プラグインは Cursor のマニフェストも持ち、Agent Plugins の形式に従っているので、Cursor のチーム向けマーケットプレイスに取り込むチームにも使えます。`SKILL.md` は、6 つのリファレンス（collect、measure、ship、app、learn、setup）のどれを各段階で読むかを示します。Skill は `plugin/skills/s1flow/` にあり、プラグインとパッケージの両方がこれを持っています。Skill は、ケース集め、比較、見直し、改善を同じ CLI で進めます。別の実装ではありません。

「はじめる」の例のような頼み方をすると、Skill は `github.py` スクリプトで issue を取ってきて、`cases check`、`run`、`report` を実行し、どの候補を選ぶかはあなたに任せます。

## GitHub Actions { #github-actions }

`decide/action.yml` は、本体のパッケージと明示的な `connections` の入力を使い、`answer`、`probability`、`below_min_probability`、`decision_id`、`policy` を出力します。評価用の Action はありません。`adopt` は、実行した場所で、ホールドアウトしたテスト用のケースで候補を試し、プルリクエストがその結果を運びます（[ポリシー、証拠、リリース](policies.md#evidence-and-releases)）。

入力はファイルと環境変数で渡し、シェルのコマンドに貼り込むことはありません。ワークフローは、選んだパッケージを最初に入れます。実行時にポリシーを読み込んでも、何かを入れることはありません。本番のワークフローでは、Action をリリースのタグかコミットの SHA に、パッケージをバージョンに固定してください。decide の Action を呼ぶワークフローの例は [examples/](https://github.com/gotalab/s1flow/tree/main/examples) にあります。
