---
description: 繰り返す判断を自分のデータで確かめてから、Decision Model に任せる。
translated_from: c74ebfb939ec
hide:
  - navigation
  - toc
---

# 繰り返す判断を自分のデータで確かめてから、Decision Model に任せる { .hero-title }

自動化には小さな分かれ道がたくさんあります。エージェントがそのまま実行するか人に確認するか、このチケットをどのチームに回すか、このメッセージに返信が要るか。Decision Model は、こうした型の決まった問いに、確率付きで素早く答えます。s1flow は、必要な正解率を保ったまま判断のどれだけをモデルに任せられるかを、あなた自身のケースで測ります。アプリはモデルが確信している答えをそのまま使い、残りは人に回します。人の答えは新しいケースになります。
{ .hero-lead }

[はじめる](get-started.md){ .md-button .md-button--primary } [しくみ](concepts.md){ .md-button }

<figure class="flow" markdown>
![コーディングエージェントが s1flow の Skill を使って、ラベル付きのケースを集め、そのケースで Decision Model を測ります。あなたは信頼できるモデルを選び、アプリは測ったとおりにそのモデルで判断します。確信度のしきい値を超えた答えはそのまま使い、残りは人に回し、人の答えは新しいケースになります。](../images/how-it-works.svg#only-light)
![](../images/how-it-works-dark.svg#only-dark)
</figure>

<div class="entries" markdown>

- [**はじめる**](get-started.md)
  CLI を入れ、コーディングエージェントに Skill を追加して、最初の比較を頼みます。
- [**考え方**](concepts.md)
  Decision Model、ケース、objective、しきい値、ポリシーと、s1flow が任せる前に確かめる理由。
- [**評価して比べる**](evaluate.md)
  ラベル付きのケースを集め、判断に合った objective でモデルとプロンプトを比べます。
- [**アプリで判断を動かす**](app.md)
  選んだポリシーを読み込み、測ったとおりに判断します。
- [**フィードバックと改善**](feedback.md)
  正解を記録して本番で測り、新しいケースにします。
- [**ベンチマーク**](https://gotalab.github.io/s1flow/benchmarks/)
  公開タスクで Decision Model を測った、日付付きのスナップショット（英語）。各タスクは、答えの使い道に合った指標で測っています。

</div>
