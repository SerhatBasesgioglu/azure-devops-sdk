from __future__ import annotations

import json
from enum import Enum
from typing import Any
from uuid import UUID

import httpx
import pytest
from pydantic import BaseModel, Field, RootModel, ValidationError

from azure_devops_sdk._transport import AdoTransport, UNSET


def transport(handler, *, base_url="https://ado.example/tfs/TeamCollection"):
    return AdoTransport(base_url, "synthetic-pat", transport=httpx.MockTransport(handler))


def test_collection_prefix_query_encoding_and_auth_are_applied_once():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    client = transport(handler)
    client.request(
        "GET",
        "projects/{project}/branches/{branch}",
        path_params={"project": "Space #?/%", "branch": "feature/ü%"},
        query={"search.criteria": "x", "$top": 0, "enabled": False, "skip": None, "items": ["a", "b"]},
    )
    request = seen[0]
    assert request.url.raw_path.split(b"?", 1)[0] == b"/tfs/TeamCollection/projects/Space%20%23%3F%2F%25/branches/feature%2F%C3%BC%25"
    assert request.url.params.get("search.criteria") == "x"
    assert request.url.params.get("$top") == "0"
    assert request.url.params.get("enabled") == "false"
    assert request.url.params.get("items") == "a,b"
    assert request.url.params.get("api-version") == "7.0"
    assert request.headers["authorization"].startswith("Basic ")
    assert request.headers["host"] == "ado.example"
    client.close()


def test_optional_path_segment_and_custom_query_formats():
    seen = []
    client = transport(lambda r: (seen.append(r) or httpx.Response(200, json=[])))
    client.request("GET", "{project}/_apis/items", path_params={"project": None}, query={"ids": [1, 2]}, query_formats={"ids": "multi"})
    assert seen[0].url.path == "/tfs/TeamCollection/_apis/items"
    assert seen[0].url.params.get_list("ids") == ["1", "2"]
    client.close()


def test_dot_segment_path_parameter_is_not_emitted_as_traversal():
    seen = []
    client = transport(lambda r: (seen.append(r) or httpx.Response(200, json={})))
    client.request("GET", "projects/{project}", path_params={"project": ".."})
    assert seen[0].url.raw_path.split(b"?", 1)[0].endswith(b"/projects/%2E%2E")
    client.close()


def test_body_unset_explicit_null_and_json_patch_root_array():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(204)

    client = transport(handler)
    client.request("POST", "empty")
    client.request("POST", "null", body=None)

    class Patch(RootModel[list[dict[str, Any]]]):
        pass

    client.request("PATCH", "patch", body=Patch([{"op": "replace", "path": "/x", "value": None}]), content_type="application/json-patch+json")
    assert requests[0].content == b""
    assert requests[0].headers.get("content-type") is None
    assert requests[1].content == b"null"
    assert requests[2].headers["content-type"] == "application/json-patch+json"
    assert json.loads(requests[2].content) == [{"op": "replace", "path": "/x", "value": None}]
    client.close()


def test_typed_models_aliases_nested_values_and_explicit_nulls():
    class Nested(BaseModel):
        display_name: str = Field(alias="displayName")
        maybe: str | None = None

    class Model(BaseModel):
        nested: Nested
        optional: str | None = None

    captured = []

    def handler(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json={"nested": {"displayName": "Ada"}})

    client = transport(handler)
    result = client.request("POST", "typed", body=Model(nested=Nested(displayName="Ada")), response_type=Model)
    assert result.data.nested.display_name == "Ada"
    assert captured == [{"nested": {"displayName": "Ada"}}]
    client.request("POST", "mapping", body={"model": Model(nested=Nested(displayName="Ada")), "explicit": None})
    assert captured[1] == {"model": {"nested": {"displayName": "Ada"}}, "explicit": None}
    client.close()


def test_array_response_envelope_and_empty_response():
    responses = iter([
        httpx.Response(200, json={"count": 2, "value": [1, 2]}),
        httpx.Response(204),
    ])
    client = transport(lambda _: next(responses))
    assert client.request("GET", "array", response_type=list[int]).data == [1, 2]
    empty = client.request("GET", "empty", response_type=list[int])
    assert empty.data is None
    assert empty.content == b""
    client.close()


def test_exact_binary_upload_download_and_response_headers():
    upload = b"\x00\xffpayload"
    captured = []

    def handler(request):
        captured.append(request)
        return httpx.Response(200, content=upload, headers={"content-type": "application/octet-stream", "x-marker": "yes"})

    client = transport(handler)
    result = client.request("PUT", "upload", body=upload, binary=True)
    assert captured[0].content == upload
    assert captured[0].headers["content-type"] == "application/octet-stream"
    assert result.data == upload
    assert result.content == upload
    assert result.headers["x-marker"] == "yes"
    client.close()


def test_status_and_validation_errors_propagate_without_following_redirects():
    seen = []

    def handler(request):
        seen.append(request)
        if request.url.path.endswith("redirect"):
            return httpx.Response(302, headers={"location": "https://outside.example/"})
        if request.url.path.endswith("error"):
            return httpx.Response(500, json={"error": "failed"})
        return httpx.Response(200, json={"not": "an integer"})

    client = transport(handler)
    with pytest.raises(httpx.HTTPStatusError):
        client.request("GET", "error", response_type=int)
    with pytest.raises(ValidationError):
        client.request("GET", "typed", response_type=int)
    with pytest.raises(httpx.HTTPStatusError):
        client.request("GET", "redirect")
    assert len(seen) == 3
    assert seen[-1].url.path.endswith("redirect")
    client.close()


@pytest.mark.parametrize("route", ["https://evil.example/path", "//evil.example/path", "../escape", "x/{missing}"])
def test_rejects_external_traversal_and_unresolved_routes(route):
    client = transport(lambda _: httpx.Response(200))
    with pytest.raises(ValueError):
        client.request("GET", route)
    client.close()


def test_http_is_explicit_opt_in():
    with pytest.raises(ValueError, match="HTTPS"):
        AdoTransport("http://ado.example/collection", "synthetic-pat")
    client = AdoTransport("http://ado.example/collection", "synthetic-pat", allow_insecure_http=True, transport=httpx.MockTransport(lambda _: httpx.Response(200, json={})))
    client.close()


def test_enum_uuid_datetime_and_query_delimiters():
    class Flag(Enum):
        yes = "yes"

    captured = []
    client = transport(lambda r: (captured.append(r) or httpx.Response(200, json={})))
    client.request("GET", "q", query={"ids": [UUID("12345678-1234-5678-1234-567812345678"), Flag.yes], "space": ["a", "b"]}, query_formats={"space": "ssv"})
    assert captured[0].url.params.get("ids") == "12345678-1234-5678-1234-567812345678,yes"
    assert captured[0].url.params.get("space") == "a b"
    client.close()
