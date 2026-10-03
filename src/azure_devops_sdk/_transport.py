"""Shared synchronous HTTPX transport for the generated Azure DevOps SDK."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from types import UnionType
from typing import Any, Generic, TypeVar, Union, get_args, get_origin
from urllib.parse import quote, urlsplit
from uuid import UUID

import httpx
from pydantic import BaseModel, TypeAdapter

T = TypeVar("T")


class _Unset:
    __slots__ = ()


UNSET = _Unset()


@dataclass(frozen=True)
class ApiResponse(Generic[T]):
    data: T
    status_code: int
    headers: httpx.Headers
    content: bytes


def _wire_value(value: Any) -> str:
    if isinstance(value, Enum):
        return _wire_value(value.value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (UUID, datetime, date)):
        return str(value)
    return str(value)


def _quote_segment(value: Any) -> str:
    rendered = _wire_value(value)
    # urllib deliberately leaves dots unescaped, including a traversal segment.
    if rendered in {".", ".."}:
        return rendered.replace(".", "%2E")
    return quote(rendered, safe="")


def _json_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        # RootModel.model_dump() correctly produces its root array/scalar.
        return _json_value(value.model_dump(mode="json", by_alias=True, exclude_unset=True))
    if isinstance(value, Mapping):
        # Preserve explicit mapping nulls while converting nested model values.
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


class AdoTransport:
    """A small, synchronous, non-retrying Azure DevOps REST transport.

    HTTPS is required by default because HTTP Basic authentication exposes the
    PAT to the network. Set ``allow_insecure_http=True`` only for a deliberately
    trusted legacy server; this opt-in does not provide transport security.
    """

    _PLACEHOLDER = re.compile(r"\{([^{}]+)\}")

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
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) collection URL")
        if parsed.scheme != "https" and not allow_insecure_http:
            raise ValueError("HTTPS is required; set allow_insecure_http=True to explicitly permit HTTP")
        if parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValueError("base_url cannot contain credentials, a query, or a fragment")
        self.base_url = base_url.rstrip("/") + "/"
        self.api_version = api_version
        self._client = httpx.Client(
            base_url=self.base_url,
            auth=httpx.BasicAuth("", pat),
            timeout=timeout,
            transport=transport,
            follow_redirects=False,
        )

    def __enter__(self) -> AdoTransport:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _route(self, path: str, path_params: dict[str, Any] | None) -> str:
        parsed = urlsplit(path)
        if parsed.scheme or parsed.netloc or path.startswith("//"):
            raise ValueError("request path must be relative; external URLs are not allowed")
        if parsed.query or parsed.fragment:
            raise ValueError("query and fragment must be supplied separately from the request path")
        values = path_params or {}
        # Generated routes commonly begin with '/', but they are collection-
        # relative, not host-root-relative.
        parts = path.lstrip("/").split("/")
        output: list[str] = []
        for part in parts:
            matches = list(self._PLACEHOLDER.finditer(part))
            if not matches:
                if part == "..":
                    raise ValueError("parent traversal segments are not allowed")
                output.append(part)
                continue
            if len(matches) == 1 and matches[0].span() == (0, len(part)):
                name = matches[0].group(1)
                if name not in values:
                    raise ValueError(f"unresolved path placeholder {{{name}}}")
                value = values[name]
                if value is None:
                    continue
                output.append(_quote_segment(value))
                continue
            rendered = part
            for match in reversed(matches):
                name = match.group(1)
                if name not in values:
                    raise ValueError(f"unresolved path placeholder {{{name}}}")
                value = values[name]
                if value is None:
                    raise ValueError(f"path placeholder {{{name}}} cannot be None inside a segment")
                rendered = rendered[: match.start()] + _quote_segment(value) + rendered[match.end() :]
            output.append(rendered)
        result = "/".join(output)
        if self._PLACEHOLDER.search(result):
            raise ValueError("unresolved path placeholder")
        return result

    @staticmethod
    def _query_params(query: dict[str, Any] | None, formats: dict[str, str] | None) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = []
        delimiters = {"csv": ",", "ssv": " ", "tsv": "\t", "pipes": "|"}
        for key, value in (query or {}).items():
            if value is None:
                continue
            if isinstance(value, (list, tuple, set)):
                fmt = (formats or {}).get(key, "csv")
                if fmt == "multi":
                    result.extend((key, _wire_value(item)) for item in value if item is not None)
                    continue
                if fmt not in delimiters:
                    raise ValueError(f"unsupported query collection format {fmt!r} for {key!r}")
                value = delimiters[fmt].join(_wire_value(item) for item in value if item is not None)
            result.append((key, _wire_value(value)))
        return result

    def request(
        self,
        method: str,
        path: str,
        *,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        query_formats: dict[str, str] | None = None,
        body: Any = UNSET,
        content_type: str | None = None,
        accept: str = "application/json",
        response_type: Any = Any,
        binary: bool = False,
    ) -> ApiResponse[Any]:
        route = self._route(path, path_params)
        params = self._query_params(query, query_formats)
        # The transport owns api-version: caller-provided values cannot override it.
        params = [(key, value) for key, value in params if key != "api-version"]
        params.append(("api-version", self.api_version))
        headers = {"Accept": accept}
        request_kwargs: dict[str, Any] = {"params": params, "headers": headers}
        if body is not UNSET:
            if content_type and content_type.lower().split(";", 1)[0].strip() == "application/json-patch+json":
                request_kwargs["content"] = json.dumps(_json_value(body), separators=(",", ":")).encode("utf-8")
                headers["Content-Type"] = content_type
            elif isinstance(body, bytes):
                request_kwargs["content"] = body
                headers["Content-Type"] = content_type or "application/octet-stream"
            elif content_type and content_type.lower().split(";", 1)[0].strip() != "application/json":
                request_kwargs["content"] = body if isinstance(body, (str, bytes)) else json.dumps(_json_value(body)).encode()
                headers["Content-Type"] = content_type
            else:
                request_kwargs["content"] = json.dumps(_json_value(body), separators=(",", ":")).encode("utf-8")
                headers["Content-Type"] = content_type or "application/json"

        response = self._client.request(method, route, **request_kwargs)
        response.raise_for_status()
        content = response.content
        if not content:
            data: Any = None
        else:
            media_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            accept_is_json = "json" in accept.lower() or "+json" in accept.lower()
            if binary or not accept_is_json or (media_type and "json" not in media_type and "+json" not in media_type):
                data = content
            else:
                parsed_data = response.json()
                def has_list_branch(annotation: Any) -> bool:
                    origin = get_origin(annotation)
                    if origin is list:
                        return True
                    if origin in {UnionType, Union}:
                        return any(has_list_branch(branch) for branch in get_args(annotation))
                    return False

                if has_list_branch(response_type) and isinstance(parsed_data, dict) and isinstance(parsed_data.get("value"), list):
                    parsed_data = parsed_data["value"]
                data = parsed_data if response_type is Any else TypeAdapter(response_type).validate_python(parsed_data)
        return ApiResponse(data=data, status_code=response.status_code, headers=response.headers, content=content)
