from __future__ import annotations

import httpx

from ._transport import AdoTransport


class AdoClient:
    def __init__(
        self,
        base_url: str,
        pat: str,
        api_version: str = "7.0",
        *,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 30.0,
        allow_insecure_http: bool = False,
    ) -> None:
        self._transport = AdoTransport(
            base_url,
            pat,
            api_version,
            transport=transport,
            timeout=timeout,
            allow_insecure_http=allow_insecure_http,
        )
        from .git import GitApi
        from .pipelines import PipelinesApi
        from .core import CoreApi
        from .build import BuildApi
        from .policy import PolicyApi
        from .task_agent import TaskAgentApi

        self.git = GitApi(self._transport)
        self.pipelines = PipelinesApi(self._transport)
        self.core = CoreApi(self._transport)
        self.build = BuildApi(self._transport)
        self.policy = PolicyApi(self._transport)
        self.task_agent = TaskAgentApi(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> AdoClient:
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()
