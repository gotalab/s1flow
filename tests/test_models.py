"""The line-up in s1flow.toml: what a spec may say, how it builds, and what `models --verify` finds (no network)."""

import asyncio

import pytest
from conftest import BENCH, cli, make_project

from s1flow import Client
from s1flow.core.errors import ConfigError, NotFound
from s1flow.client import BooleanAnswer, Capabilities, ChoiceAnswer, Response, ModelBuild, ScoreAnswer
from s1flow.eval import verify
from s1flow.project import Project
from s1flow.client.lineup import BUILTIN_LINEUP, Lineup
from s1flow.client.providers.typesafe import TypeSafeModel

BENCH_LINEUP = Project(BENCH).client().connections

BASE = """
default = ["a"]
[models.a]
provider = "gateway"
id = "x/a"
"""


def load(tmp_path, text):
    p = tmp_path / "s1flow.toml"
    p.write_text(text)
    lineup = Lineup.read(p)
    Client(connections=lineup).connections.check()
    return lineup


def test_reading_checks_the_shape_and_builds_nothing(tmp_path):
    """A line-up reads without building its models (an `llm` one needs LiteLLM); check() builds them all."""
    p = tmp_path / "s1flow.toml"
    p.write_text(BASE + '\n[models.b]\nprovider = "nope"\nid = "m"\n')
    lineup = Lineup.read(p)
    assert Client(connections=lineup).connections.build("a").id == "gateway:x/a"
    with pytest.raises(ConfigError, match="unknown provider"):
        Client(connections=lineup).connections.check()
    p.write_text(BASE + '\n[models.b]\nprovider = "gateway"\nid = "m"\ncolour = "red"\n')
    with pytest.raises(ConfigError, match="Extra inputs"):
        Lineup.read(p)


def test_the_repo_lineup_keeps_its_cache_ids():
    """A model's id is its cache key: moving the line-up to s1flow.toml must not change one."""
    want = {
        "jev": "typesafe:jev-latest",
        "jev:1.14": "typesafe:jev-1.14.0",
        "jev@openrouter:1.14": "openrouter:typesafe/jev-1.14",
        "jev@vercel:1.13": "gateway:typesafe-ai/jev-1.13.0",
        "jev@vercel": "gateway:typesafe-ai/jev",
        "mercury@openrouter": "openrouter:inception/mercury-decide:free",
        "clef": "cloudflare:clef",
        "luna@decisions": "openai-decisions:gpt-6-luna",
        "haiku-k5@vercel": "llm:vercel_ai_gateway/anthropic/claude-haiku-4.5#k5",
    }
    assert {n: BENCH_LINEUP.build(n).id for n in want} == want
    assert BENCH_LINEUP.build("mercury@openrouter").concurrency == 2
    assert BENCH_LINEUP.build("haiku-k5@vercel").capabilities.distribution == "sampled"
    assert BENCH_LINEUP.build("haiku@vercel").capabilities.distribution == "none"


def test_box_follows_the_version_not_the_name():
    takes_box = lambda n: "box" in BENCH_LINEUP.build(n).capabilities.question_types
    assert not takes_box("jev") and takes_box("jev:1.14")  # jev-latest is 1.13
    assert not takes_box("jev@openrouter") and not takes_box("jev@openrouter:1.13") and takes_box("jev@openrouter:1.14")
    assert BENCH_LINEUP.build("jev@openrouter:1.14").capabilities.image  # the model's, kept under the version's own
    # `models --verify` holds each version to its own claims
    assert verify.claims(BENCH_LINEUP.build("jev@openrouter:1.14").capabilities)["box"]
    assert not verify.claims(BENCH_LINEUP.build("jev@openrouter:1.13").capabilities)["box"]


VERSIONED = BASE + """
[models.v]
provider = "gateway"
id = "x/v-1"
capabilities.image = true
capabilities.context_tokens = 8000

[models.v.versions."1"]
id = "x/v-1"

[models.v.versions."2"]
id = "x/v-2"
capabilities.question_types = ["boolean", "choice", "score", "box"]
capabilities.image = false

[models.latest]
provider = "gateway"
id = "x/v"

[models.latest.versions."2"]
id = "x/v-2"
"""


def test_versions_have_names_and_their_own_capabilities(tmp_path):
    lineup = load(tmp_path, VERSIONED)
    assert lineup.probe_names() == ["a", "v", "latest", "v:1", "v:2", "latest:2"]
    v2 = lineup.resolved("v:2")
    assert v2.id == "x/v-2" and v2.versions is None and Client(connections=lineup).connections.build("v:2").id == "gateway:x/v-2"
    # each field the version gives replaces the model's; the rest stays the model's
    assert "box" in v2.capabilities.question_types and not v2.capabilities.image and v2.capabilities.context_tokens == 8000
    assert lineup.resolved("v") == lineup.resolved("v:1")  # `id` is version 1: the model as it is
    assert lineup.resolved("v:1").capabilities == lineup.spec("v").capabilities
    assert not lineup.spec("v").alias and lineup.spec("v").version == "1"
    assert lineup.spec("latest").alias and lineup.resolved("latest").id == "x/v"  # an alias runs as it is
    with pytest.raises(NotFound, match="v: no version 'x/v-2'; versions: 1, 2"):
        Client(connections=lineup).connections.build("v:x/v-2")  # the label, not the id


def test_a_label_is_a_free_name_and_the_id_is_the_providers_string(tmp_path):
    lineup = load(tmp_path, BASE + '\n[models.ds]\nprovider = "gateway"\nid = "deepseek/deepseek-v4.1"\n'
                  '[models.ds.versions."4.1-flash-2026-10-17"]\nid = "deepseek/DeepSeek-V4.1-Flash@2026-10-17"\n'
                  '[models.ds.versions.2026-10-17]\nid = "deepseek/deepseek-v4.1-20261017"\n')
    assert Client(connections=lineup).connections.build("ds:4.1-flash-2026-10-17").id == "gateway:deepseek/DeepSeek-V4.1-Flash@2026-10-17"  # sent verbatim
    assert lineup.resolved("ds:2026-10-17").id == "deepseek/deepseek-v4.1-20261017"


@pytest.mark.parametrize("versions", ['versions = ["x/v-1"]', '[models.v.versions."1:2"]\nid = "x"', '[models.v.versions.""]\nid = "x"',
                                      '[models.v.versions."1,2"]\nid = "x"', '[models.v.versions."1"]\nmodel = "x"'])
def test_a_version_that_does_not_fit_stops_loading(tmp_path, versions):
    with pytest.raises(ConfigError):
        load(tmp_path, BASE + f'\n[models.v]\nprovider = "gateway"\nid = "m"\n{versions}\n')


@pytest.mark.parametrize("extra, error", [
    ('\n[models.b]\nprovider = "nope"\nid = "m"\n', "unknown provider"),
    ('\n[models.b]\nprovider = "gateway"\nid = "m"\ncolour = "red"\n', "Extra inputs"),
    ('\n[models.b]\nprovider = "gateway"\nid = "m"\ncapabilities = { imgae = true }\n', "Extra inputs"),
    ('\n[models.b]\nprovider = "gateway"\nid = "m"\noptions = { per_minute = 3 }\n', "options do not fit"),
    ('\n[models.b]\nprovider = "llm"\nid = "m"\ncapabilities = { question_types = ["box"] }\n', "box_units"),
    ('\n[models.b]\nprovider = "llm"\nid = "m"\ncapabilities = { distribution = "native" }\n', "distribution follows"),
    ('\n[models."b:1"]\nprovider = "gateway"\nid = "m"\n', "model names"),
])
def test_a_spec_that_does_not_fit_stops_loading(tmp_path, extra, error):
    with pytest.raises(ConfigError, match=error):
        load(tmp_path, BASE + extra)


def test_default_must_name_known_models(tmp_path):
    with pytest.raises(ConfigError, match="not in the line-up"):
        load(tmp_path, BASE.replace('["a"]', '["a", "b"]'))


def test_versions_only_where_the_model_takes_them(tmp_path):
    lineup = load(tmp_path, BASE)
    with pytest.raises(ConfigError, match="declares no versions"):
        Client(connections=lineup).connections.build("a:v2")


def test_a_typesafe_compatible_server_caches_apart(tmp_path):
    lineup = load(tmp_path, BASE + '\n[models.mine]\nprovider = "typesafe"\nid = "jev-latest"\noptions = { base_url = "http://localhost:9000/v1", api_key_env = "MY_KEY" }\n')
    m = Client(connections=lineup).connections.build("mine")
    assert isinstance(m, TypeSafeModel)
    assert m.id == "typesafe:http://localhost:9000/v1:jev-latest" and m.api_key_env == "MY_KEY"


class Mine:
    """A provider of your own: anything with id, capabilities, concurrency and decide."""

    def __init__(self, b: ModelBuild):
        self.id = f"mine:{b.spec.id}"
        self.capabilities = b.spec.capabilities
        self.concurrency = b.spec.concurrency or 1
        self.options = b.spec.options

    async def decide(self, state, questions, *, options=None):
        raise NotImplementedError


def mine(b: ModelBuild) -> Mine:
    return Mine(b)


def test_your_own_provider_by_import_path(tmp_path):
    lineup = load(tmp_path, BASE + '\n[models.own]\nprovider = "test_models:mine"\nid = "m1"\noptions.anything = 1\ncapabilities.image = true\n'
                                   '[models.own.versions.v2]\nid = "m2"\n')
    m = Client(connections=lineup).connections.build("own:v2")
    assert m.id == "mine:m2" and m.capabilities.image and m.options == {"anything": 1}


def test_optimize_reads_length_limits_from_capabilities():
    from s1flow.eval.gepa import DEFAULT_LIMITS, limits

    assert limits(BENCH_LINEUP.build("laya@vercel")) == (300, 60)
    assert limits(BENCH_LINEUP.build("jev")) == DEFAULT_LIMITS


# ---------- models --verify ----------


class TextOnly:
    """Reads text right; does not see images (answers the first option at chance)."""

    id, concurrency = "fake:text", 4

    def __init__(self, b=None):
        self.capabilities = Capabilities()

    async def decide(self, state, questions, *, options=None):
        text = " ".join(x for x in state if isinstance(x, str)) if isinstance(state, list) else str(state)
        out = {}
        for qid, q in questions.items():
            if q.type == "boolean":
                out[qid] = BooleanAnswer(probability=0.95 if "red" in text else 0.05)
            elif q.type == "score":
                out[qid] = ScoreAnswer(score=3.0 if "three" in text else 1.0)
            elif q.type == "choice":
                pick = next((k for k in q.criteria if k in text), "red")
                p = 0.97 if pick in text else 0.34
                out[qid] = ChoiceAnswer(choice=pick, probabilities={k: p if k == pick else (1 - p) / 2 for k in q.criteria})
        return Response(answers=out, answered_by="fake-1")


def test_verify_checks_every_claim(tmp_path):
    v = asyncio.run(verify.probe(make_project(tmp_path, {"textonly": TextOnly}).client(), "textonly"))
    assert {c: r.ok for c, r in v.checks.items()} == {
        "boolean": True, "choice": True, "score": True, "image": False, "images": False, "box": False,
    }
    assert v.answered_by == "fake-1" and v.checks["box"].detail == "not asked: image failed"
    assert verify.disagreements(Capabilities(), v) == ([], [])
    assert verify.disagreements(Capabilities(image=True), v) == (["image", "images"], [])
    assert verify.disagreements(Capabilities(question_types={"boolean"}), v) == ([], ["choice", "score"])


def test_verify_results_merge(tmp_path):
    p = make_project(tmp_path)
    ok = verify.Check(ok=True, detail="")
    verify.save(p, {"a": verify.Verification(at="t1", checks={"boolean": ok}), "b": verify.Verification(at="t1", checks={"boolean": ok})})
    verify.save(p, {"a": verify.Verification(at="t2", checks={"boolean": ok})})
    got = verify.read_verified(p)
    assert got["a"].at == "t2" and got["b"].at == "t1"


def test_the_line_up_init_writes_runs_on_one_key():
    """`init` copies the packaged line-up: a few models a newcomer can run with one key, each pinned to a version
    or serving one, and none of this repository's own notes (apps/bench/s1flow.toml is s1flow's own line-up)."""
    from s1flow.client.providers import needs

    lineup = Lineup.read(BUILTIN_LINEUP)
    Client(connections=lineup).connections.check()
    assert 2 <= len(lineup.models) <= 3 and lineup.default == list(lineup.models)
    assert {k for s in lineup.models.values() for k in needs(s).keys} == {"OPENROUTER_API_KEY"}
    assert not any(s.alias for s in lineup.models.values())
    text = BUILTIN_LINEUP.read_text()
    assert not any(x in text for x in ("DESIGN.md", "clef-proxy", "apps/bench", "note ="))


def test_verify_without_a_key_checks_nothing_and_records_nothing(tmp_path, monkeypatch):
    p = make_project(tmp_path, {"textonly": TextOnly})
    with p.config.open("a") as f:
        f.write('\n[models."kev@openrouter"]\nprovider = "openrouter"\nid = "jaredpalmer/kev-4b"\n')
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    got = cli("models", "--verify")
    assert got.exit_code == 0, got.output  # textonly does what it declares; kev is not asked, so not failed
    assert "kev@openrouter  not checked (no OPENROUTER_API_KEY): get one at https://openrouter.ai/keys" in got.output
    assert set(verify.read_verified(p)) == {"textonly"}
    verify.verified_path(p).unlink()
    got = cli("models", "--verify", "--models", "kev@openrouter")
    assert got.exit_code == 2 and "nothing checked" in got.output and not verify.verified_path(p).exists()
