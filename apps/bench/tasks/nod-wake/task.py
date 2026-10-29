"""nod: does the agent have to wake for this message?

The `next` question with P(wake), on the 80 labelled cases in cases.json. In the miss / false-alarm table,
a missed `must` is the failure that matters.
"""

from s1flow.objectives import Coverage, ExpectedLoss
from s1flow.eval import KindParams, Task
from s1flow.questions import Choice

HISTORY_LINES = 6
ROLE = "あなたはユーザーの調べもの・予定・連絡・買い物・作業などを手伝っているAIエージェント。チャットでユーザーの最新の発言(user)を受け取った。agent はその直前のあなたの発言、earlier はそれより前のやりとり（古い順）。"


def state(row):
    lines = row["history"][-HISTORY_LINES:]
    last = lines[-1] if lines else None
    agent = last["text"] if last and last["role"] == "agent" else "(なし。ユーザーから話しかけてきた)"
    rest = lines[:-1] if last and last["role"] == "agent" else lines
    earlier = [f"{'あなた' if l['role'] == 'agent' else 'ユーザー'}: {l['text']}" for l in rest]
    return {"earlier": earlier, "agent": agent, "user": row["user"].strip()} if earlier else {"agent": agent, "user": row["user"].strip()}


task = Task(
    id="nod-wake",
    cases="cases.json",
    state=state,
    question_id="next",
    question=Choice(
        instructions=ROLE + "ユーザーの発言(user)を受けて、あなたはどうするべきか。",
        criteria={
            "wake": "起きて対応する。返事をする、または作業をする（始める・続ける・変える・やめる・調べる・確かめる）必要がある。質問、依頼、許可（「OK」「お願い」）、訂正、方針の変更や中止、相談、不満、提案への同意で予定や作業が変わる。進行中の作業に関わる発言。",
            "stamp": "スタンプだけで足りる。返事も作業も要らない。お礼、相づち、感想、雑談、冗談、「あとで読む」、「そのままでいい」、会話の締め。",
            "ignore": "反応不要。意味のない入力や誤入力、発言の途中で続きが来そう、あなた宛てではない。",
        },
    ),
    kind_params=KindParams(positive="wake"),
    label=lambda r: {"must": True, "sleep": False}.get(r["label"]),  # either: no wrong answer
    # A missed must drops work; a needless wake costs one LLM call.
    objective=Coverage(target_accuracy=0.95), tiebreak=[ExpectedLoss(fn=10, fp=1)],
    variants={
        # Laya rejects option descriptions of ~100 Japanese characters; this one fits every model.
        "short": Choice(
            instructions=ROLE + "ユーザーの発言(user)を受けて、あなたはどうするべきか。",
            criteria={
                "wake": "返事か作業が要る。質問、依頼、許可、訂正、方針の変更や中止、不満、相談。",
                "stamp": "スタンプで足りる。お礼、相づち、感想、雑談、冗談、会話の締め。",
                "ignore": "反応不要。誤入力、続きが来そうな途中の発言、あなた宛てではない。",
            },
        ),
    },
    source="cases.json",
)
