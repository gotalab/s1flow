"""A project: one directory with s1flow.toml, tasks/, runs/, reports/, policies/ and .cache/.

    project = Project(place.project(None, required=True))  # the CLI finds the directory (core/place.py)
    project.client().connections.build("jev")  # the line-up (s1flow.toml) is the model-calling layer's (s1flow.client)

Tasks are loaded by `s1flow.eval.task.load(project, id)`. Nothing happens on import: s1flow.toml is read only when asked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from ..client import AsyncClient
from ..client.lineup import Lineup
from ..core import place
from ..core.errors import NotFound

if TYPE_CHECKING:
    from ..client._client import Connections


@dataclass(frozen=True)
class Project:
    root: Path
    connections: Path | None = None
    _client: list[AsyncClient] = field(default_factory=list, compare=False, repr=False)  # made once, on first use
    _lineup: list[Lineup] = field(default_factory=list, compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", place.absolute(self.root, "project"))
        if self.connections is not None:
            object.__setattr__(self, "connections", place.absolute(self.connections, "connections"))

    @property
    def tasks_dir(self) -> Path:
        return self.root / "tasks"

    @property
    def runs_dir(self) -> Path:
        return self.root / "runs"

    @property
    def policies_dir(self) -> Path:
        return self.root / "policies"

    @property
    def cache_dir(self) -> Path:
        return self.root / ".cache"  # the check Action keeps it in the Actions cache

    @property
    def config(self) -> Path:
        """Explicit connection configuration, otherwise this project's s1flow.toml."""
        return self.connections if self.connections is not None else self.root / place.CONFIG

    def client(self) -> AsyncClient:
        """The evaluation's client: the project's line-up, every model in it checked to build (Connections.check)."""
        if not self._client:
            c = AsyncClient(self.config, cache_dir=self.cache_dir)
            c.connections.check()
            self._client.append(c)
        return self._client[0]

    def declared_connections(self) -> Connections:
        """The line-up's names and specs, nothing built: what reading and ranking saved runs needs (no provider's extra)."""
        if self._client:
            return self._client[0].connections
        return AsyncClient(self.lineup(), cache_dir=self.cache_dir).connections  # unlike client(), no check()

    def lineup(self) -> Lineup:
        """s1flow.toml, read once and nothing built: what a report reads the models' prices from."""
        if self._client:
            return self._client[0].connections.lineup
        if not self._lineup:
            self._lineup.append(Lineup.read(self.config))
        return self._lineup[0]

    def task_ids(self) -> list[str]:
        return sorted(p.parent.name for p in self.tasks_dir.glob("*/task.py"))  # a task's directory is named its id

    def task_dir(self, task_id: str) -> Path:
        d = self.tasks_dir / task_id
        if not (d / "task.py").is_file():
            raise NotFound(f"no task {task_id!r}; the tasks: {', '.join(self.task_ids()) or 'none'} (in {self.tasks_dir})")
        return d
