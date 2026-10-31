"""`Client` and `AsyncClient`: call any decision model, with no policy and no evaluation.

    client = Client(connections="connections.toml")     # explicit application-owned connection configuration
    d = client.responses.create(model="jev", state={"title": ...}, questions={"bug": Boolean(instructions="...")})
    d.answers["bug"].probability, d.answered_by, d.usage.cost_usd, d.latency_ms
    d = await AsyncClient(connections="connections.toml").responses.create(...)      # the same, awaited
    client.connections.list()                                # the line-up's names and what each declares

One call is one request: no threshold (a policy reads its answer, the evaluation caches). `model` is a name of the line-up (`jev`, or `jev:1.14` for a version), a
`ModelSpec`, or a `DecisionModel` you built. Keys come from the environment (`TYPESAFE_API_KEY`, ...).
"""

from __future__ import annotations

import builtins
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError

from ..core import place
from ..core.errors import ConfigError, DataError, NotFound, ProviderError, invalid
from . import loop
from .answers import Response
from .lineup import Lineup
from .models import DecisionModel, ModelSpec
from .providers import build_one
from .providers.contract import validate_response
from .questions import Question, Questions
from .state import State

ModelRef = str | ModelSpec | DecisionModel
_QUESTIONS: TypeAdapter[Questions] = TypeAdapter(Questions)


class ConnectionInfo(BaseModel):
    """One model of the line-up, as s1flow.toml declares it (nothing is built to list it)."""

    model_config = ConfigDict(frozen=True)
    name: str
    spec: ModelSpec
    default: bool  # in the line-up's `default`


class Connections:
    """Explicit named connections, read on first use from a path fixed at construction."""

    def __init__(self, source: str | Path | Lineup | None, cache_dir: Path | None):
        if source is not None and not isinstance(source, (str, Path, Lineup)):
            raise ConfigError("connections must be a TOML path or Lineup; pass a model to responses.create(model=...) instead")
        self._source = source if isinstance(source, Lineup) else place.absolute(source, "connections") if source is not None else None
        self._cache_dir = place.absolute(cache_dir, "cache_dir") if cache_dir is not None else None
        if isinstance(self._source, Lineup):
            self._source = self._source.model_copy(deep=True)
        self._lineup: Lineup | None = None

    @property
    def path(self) -> Path | None:
        """The configuration file, when known; None for an in-memory declaration."""
        return self._source._path if isinstance(self._source, Lineup) else self._source

    @property
    def lineup(self) -> Lineup:
        if self._source is None:
            raise ConfigError("no connections configured; pass connections=PATH (or a Lineup) to Client/AsyncClient, "
                              "or pass a ModelSpec/DecisionModel directly to responses.create(model=...)")
        if self._lineup is None:
            self._lineup = self._source if isinstance(self._source, Lineup) else Lineup.read(self._source)
        return self._lineup

    def list(self, *, default_only: bool = False) -> list[ConnectionInfo]:
        """Every model, in s1flow.toml's order; with `default_only`, those in `default`, in its order."""
        lu = self.lineup
        names = lu.default if default_only else list(lu.models)
        return [ConnectionInfo(name=n, spec=lu.models[n], default=n in lu.default) for n in names]

    def retrieve(self, name: str) -> ConnectionInfo:
        """One model by its name (`jev:<version>` gives jev's entry; `resolved` gives the model at that version)."""
        base = name.partition(":")[0]
        lu = self.lineup
        return ConnectionInfo(name=base, spec=lu.spec(base), default=base in lu.default)

    def resolved(self, name: str) -> ModelSpec:
        """What `jev` or `jev:1.14` sends: the model at that version, its capabilities over the model's (ModelSpec.at)."""
        return self.lineup.resolved(name)

    def names(self, *, versions: bool = False) -> builtins.list[str]:
        """Every name; with `versions`, also `name:<version>` for each version a spec lists."""
        return self.lineup.probe_names() if versions else list(self.lineup.models)

    def build(self, model: str | ModelSpec, *, name: str | None = None) -> DecisionModel:
        """A new model object: its `id`, `capabilities` and `concurrency`, and `decide` to call it. A `ModelSpec`
        is built alone (it cannot refer to another model of a line-up); `name` is the line-up's name it came
        from (a policy's candidate, `jev:1.14`), whose name without the version its provider sees, default the spec's id."""
        if isinstance(model, str):
            name, model = model.partition(":")[0], self.resolved(model)
        return build_one(name.partition(":")[0] if name else model.id, model, self._cache_dir)

    def check(self) -> None:
        """Build every model and each version it lists: a spec its provider cannot build is a ConfigError."""
        try:
            for name in self.names(versions=True):
                self.build(name)
        except (ConfigError, NotFound) as e:
            raise ConfigError(f"{self.path or 'connections'}: {e}") from None


def validate_questions(questions: Mapping[str, Question | dict[str, Any]]) -> Questions:
    try:
        return _QUESTIONS.validate_python(dict(questions))
    except ValidationError as e:
        raise DataError(f"questions: {invalid(e)}") from None


class AsyncResponses:
    def __init__(self, connections: Connections):
        self._connections = connections
        self._built: dict[str, DecisionModel] = {}

    def _model(self, model: ModelRef) -> DecisionModel:
        if isinstance(model, str):
            key = f"name:{model}"
        elif isinstance(model, ModelSpec):
            key = f"spec:{model.model_dump_json()}"
        elif isinstance(model, DecisionModel):
            return model
        else:
            raise ConfigError(f"model is a name of the line-up, a ModelSpec or a DecisionModel, not {type(model).__name__}")
        if key not in self._built:  # one object per model, so a model's own pacing holds across calls
            self._built[key] = self._connections.build(model)
        return self._built[key]

    async def create(
        self, *, model: ModelRef, state: State, questions: Mapping[str, Question | dict[str, Any]], options: dict[str, Any] | None = None,
    ) -> Response:
        """Ask `model` every question about `state` in one call. A question the model declined is a `Refusal`;
        a type or an image the model does not take raises `Unsupported` before the call, a failed call `ProviderError`."""
        qs = validate_questions(questions)
        m = self._model(model)
        try:
            d = await m.decide(state, qs, options=options)
        except (AttributeError, KeyError, TypeError, ValueError, ValidationError) as e:
            raise ProviderError(f"{m.id} returned a malformed response outside the contract: {e}") from e
        return validate_response(d, qs, m.id)


class Responses:
    def __init__(self, inner: AsyncResponses):
        self._inner = inner

    def create(
        self, *, model: ModelRef, state: State, questions: Mapping[str, Question | dict[str, Any]], options: dict[str, Any] | None = None,
    ) -> Response:
        """`AsyncClient.responses.create`, blocking until the answers (or the error) are in."""
        return loop.run(self._inner.create(model=model, state=state, questions=questions, options=options))


class AsyncClient:
    """Calls decision models from an event loop. `connections`: an explicit TOML path or Lineup.
    No project discovery, environment configuration lookup or dotenv loading. Without connections,
    pass a ModelSpec or DecisionModel directly. Relative paths are fixed at construction."""

    def __init__(self, connections: str | Path | Lineup | None = None, *, cache_dir: Path | None = None):
        self.connections = Connections(connections, cache_dir)
        self.responses = AsyncResponses(self.connections)


class Client:
    """`AsyncClient` for code that blocks: each call runs on one background event loop (client/loop.py)."""

    def __init__(self, connections: str | Path | Lineup | None = None, *, cache_dir: Path | None = None):
        self.aio = AsyncClient(connections, cache_dir=cache_dir)
        self.connections = self.aio.connections
        self.responses = Responses(self.aio.responses)
