import os
from uuid import UUID

import httpx

from .models import AdoList, Project, Repository


class AdoClient:
    def __init__(self, base_url: str, pat: str, api_version: str = "7.0") -> None:
        self._http = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            auth=httpx.BasicAuth("", pat),
            params={"api-version": api_version},
        )

    def list_projects(self) -> list[Project]:

        r = self._http.get("_apis/projects")
        r.raise_for_status()

        projects = AdoList[Project].model_validate(r.json())
        return projects.value

    def list_repositories(self, project_id: UUID):

        r = self._http.get(f"{project_id}/_apis/git/repositories")
        r.raise_for_status()

        repos = AdoList[Repository].model_validate(r.json())
        return repos.value

    def close(self) -> None:
        self._http.close()
