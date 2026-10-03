from __future__ import annotations

from uuid import UUID

from .models import AdoList, Project, Repository
from .runtime import AdoTransport


class AdoClient:
    def __init__(self, base_url: str, pat: str, api_version: str = "7.0") -> None:
        self._transport = AdoTransport(base_url, pat, api_version)
        # Generated clients are supplied by the SDK generator. Import locally so
        # the transport and the legacy convenience methods remain usable when a
        # generated API surface is not yet present.
        from .generated.git_api import GitApi
        from .generated.pipelines_api import PipelinesApi

        self.git = GitApi(self._transport)
        self.pipelines = PipelinesApi(self._transport)

    def list_projects(self) -> list[Project]:

        response = self._transport.request("GET", "_apis/projects", response_type=AdoList[Project])
        return response.data.value

    def list_repositories(self, project_id: UUID):

        response = self._transport.request(
            "GET",
            "{project_id}/_apis/git/repositories",
            path_params={"project_id": project_id},
            response_type=AdoList[Repository],
        )
        return response.data.value

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> AdoClient:
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()
