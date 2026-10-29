"""s1flow: run small model-backed decisions in your app and CI, then evaluate and improve them on your own data.

    s1flow.client     call any decision model: Client, AsyncClient, Response (no policy, no evaluation stack)
    s1flow.questions  the question types: Boolean, Choice, Score, Box
    s1flow.policies   load a policy and decide (light: no evaluation stack)
    s1flow.objectives what a task chooses by
    s1flow.core       what every part shares: errors, where a project is, its .env files
    s1flow.eval       tasks, runs, metrics, choosing, checking, optimizing, feedback
    s1flow.project    where a project lives and its directories
"""

from .client import AsyncClient, Client, Response
from .core.errors import ConfigError, DataError, NotFound, ProviderError, Rejected, S1flowError, Unsupported

__all__ = [
    "AsyncClient", "Client", "ConfigError", "DataError", "Response", "NotFound", "ProviderError", "Rejected", "S1flowError", "Unsupported",
]
