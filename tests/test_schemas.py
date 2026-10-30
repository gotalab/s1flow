"""schema/*.json: generated from the types (scripts/write_schemas.py), and what s1flow stores and writes fits them."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import TypeAdapter, ValidationError

from s1flow.client import Client, Response
from s1flow.client.models import ModelSpec
from s1flow.core.errors import Rejected
from s1flow.eval.cases import Correction, FeedbackCase
from s1flow.eval.evalset import SplitFile
from s1flow.eval.comparison import Comparison
from s1flow.eval.policy import EvaluatedPolicy, EvaluationRecord
from s1flow.eval.records import PredictionRecord
from s1flow.policies.policy_set import PolicySet
from s1flow.policies.policy import DecisionPolicy
from s1flow.policies.log import Decision, Log
from s1flow.policies.file import PolicySpec, read_file
from s1flow.policies.history import Switch
from s1flow.questions import Choice

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
TYPES: dict[str, TypeAdapter | None] = {
    "comparison-2": TypeAdapter(Comparison),
    "policy-evaluation-3": TypeAdapter(EvaluationRecord), "run-2": TypeAdapter(PredictionRecord),
    "case-1": None,  # a row is the task's own: no type of s1flow's reads it whole
    "split-2": TypeAdapter(SplitFile), "policy-2": TypeAdapter(PolicySpec), "evaluated-policy-3": TypeAdapter(EvaluatedPolicy),
    "log-2": TypeAdapter(Log), "response-1": TypeAdapter(Response), "decision-2": TypeAdapter(Decision), "policy-set-2": TypeAdapter(PolicySet), "history-1": TypeAdapter(Switch),
}


def validator(name: str, part: str | None = None) -> Draft202012Validator:
    s = json.loads((SCHEMA / f"{name}.json").read_text())
    Draft202012Validator.check_schema(s)
    return Draft202012Validator({**s, "$ref": f"#/$defs/{part}"} if part else s)


def errors(v: Draft202012Validator, data) -> list[str]:
    return [e.message for e in v.iter_errors(data)]


def test_the_schemas_are_what_the_types_give():
    done = subprocess.run([sys.executable, str(ROOT / "scripts" / "write_schemas.py"), "--check"], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert {p.stem for p in SCHEMA.glob("*.json")} == set(TYPES)


@pytest.mark.parametrize("name", TYPES)
def test_each_schema_takes_its_valid_fixture_and_refuses_the_invalid_one(name):
    v, t = validator(name), TYPES[name]
    good = json.loads((SCHEMA / "fixtures" / f"{name}.valid.json").read_text())
    bad = json.loads((SCHEMA / "fixtures" / f"{name}.invalid.json").read_text())
    assert errors(v, good) == []
    assert errors(v, bad) != []
    if t is not None:  # and the type that reads it agrees
        t.validate_python(good)
        with pytest.raises(ValidationError):
            t.validate_python(bad)


def test_every_stored_policy_fits():
    from s1flow.eval.policy import Store
    import re

    files = sorted(p for p in (ROOT / "apps/bench/policies").glob("*/v*.json") if re.fullmatch(r"v\d+\.json", p.name))
    assert files
    runtime, evidence = validator("policy-2"), validator("policy-evaluation-3")
    store = Store(ROOT / "apps/bench/policies")
    for path in files:
        spec = json.loads(path.read_text())
        sidecar = path.with_name(path.stem + ".evaluation.json")
        assert errors(runtime, spec) == [], path
        assert errors(evidence, json.loads(sidecar.read_text())) == [], sidecar
        evaluated = store.read(spec["task"], version=spec["version"])
        assert evaluated.spec.digest == json.loads(sidecar.read_text())["policy_digest"]
        assert evaluated.evidence.execution_digest is None  # historical provenance is not invented


def task_files(pattern: str) -> list[Path]:
    return sorted(p for top in ("apps", "examples", "src") for p in (ROOT / top).rglob(pattern) if ".venv" not in p.parts)


def test_every_case_feedback_correction_and_split_fits():
    row, feedback, correction, split = validator("case-1"), validator("case-1", "feedback"), validator("case-1", "correction"), validator("split-2")
    rows = 0
    for f in task_files("data.jsonl") + task_files("cases.json"):
        text = f.read_text()
        for r in json.loads(text) if f.suffix == ".json" else [json.loads(x) for x in text.split("\n") if x.strip()]:  # as Cases reads them (U+2028 is in bodies)
            assert errors(row, r) == [], f
            rows += 1
    for name, v in (("feedback.jsonl", feedback), ("corrections.jsonl", correction)):
        for f in task_files(name):
            for line in f.read_text().split("\n"):
                assert line.strip() == "" or errors(v, json.loads(line)) == [], f
    for f in task_files("split.json"):
        assert errors(split, json.loads(f.read_text())) == [], f
    assert rows > 1000 and task_files("feedback.jsonl") and task_files("split.json")
    # $defs/feedback and $defs/correction are the types' own
    assert errors(feedback, json.loads(FeedbackCase(id="prod:1", state={}, label="a", at="t", policy="x@v1").model_dump_json())) == []
    assert errors(correction, {"id": "1", "verdict": "keep", "was": "a", "reason": "r", "by": "me", "at": "t"}) == []
    assert [f.alias or n for n, f in Correction.model_fields.items()] == list(json.loads((SCHEMA / "case-1.json").read_text())["$defs"]["correction"]["properties"])


def test_a_log_written_by_a_policy_fits(tmp_path):
    r = read_file(ROOT / "apps" / "bench" / "policies" / "gh-ruff-kind" / "v1.json")
    r = r.model_copy(update={"connection": "toy", "model_id": "t1"})
    from s1flow.client.lineup import Lineup
    client = Client(Lineup(default=["toy"], models={"toy": ModelSpec(provider="toy_provider:build", id="t1")}))
    log = tmp_path / "log.jsonl"
    loaded = DecisionPolicy(r, client=client, log=log, keep_state=True)
    d = loaded.decide({"title": "a bug in the formatter", "body": "x"}, case_id="#1")
    loaded.feedback(d.decision_id, "bug")
    refusing = r.with_question(Choice(instructions="refuse this", criteria=dict(r.question.criteria)))  # type: ignore[union-attr]
    with pytest.raises(Rejected):
        DecisionPolicy(refusing, client=client, log=log).decide({"title": "t", "body": "b"})
    lines = [json.loads(x) for x in log.read_text().splitlines()]
    assert [x["type"] for x in lines] == ["answered", "feedback", "failed"]
    v = validator("log-2")
    for x in lines:
        assert errors(v, x) == [], x
    assert errors(validator("decision-2"), json.loads(d.model_dump_json())) == []
    assert errors(validator("response-1"), json.loads(d.response.model_dump_json())) == []



def test_only_a_version_below_on_the_held_out_test_is_forced():
    record = json.loads((SCHEMA / "fixtures" / "policy-evaluation-3.valid.json").read_text())
    record["selection"]["forced"] = True
    for test, ok in (("below", True), ("kept", False), (None, False)):
        record["evidence"]["test"] = test
        if ok:
            assert EvaluationRecord.model_validate_json(json.dumps(record)).selection.forced
        else:
            with pytest.raises(ValidationError, match="only a version below is forced"):
                EvaluationRecord.model_validate_json(json.dumps(record))


@pytest.mark.parametrize("text", ["[]", "null", "{"])
def test_a_record_that_is_no_object_is_an_invalid_record(tmp_path, text):
    from s1flow.core.errors import ConfigError
    from s1flow.eval.policy import Store

    src = ROOT / "apps/bench/policies/nod-wake"
    (tmp_path / "nod-wake").mkdir()
    (tmp_path / "nod-wake" / "v1.json").write_text((src / "v1.json").read_text())
    (tmp_path / "nod-wake" / "v1.evaluation.json").write_text(text)
    with pytest.raises(ConfigError, match="invalid evaluation record"):
        Store(tmp_path).read("nod-wake", version=1)
