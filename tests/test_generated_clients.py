from __future__ import annotations

import importlib
import inspect
import json
import re
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx
import pytest

from azure_devops_sdk._transport import AdoTransport


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT.parent / "vsts-rest-api-specs" / "specification"
SERVICE_SPECS = {
    "git": ("git", "git", 111),
    "pipelines": ("pipelines", "pipelines", 10),
    "core": ("core", "core", 18),
    "build": ("build", "build", 91),
    "policy": ("policy", "policy", 12),
    "task_agent": ("distributedTask", "taskAgent", 56),
}
API_CLASSES = {
    "git": "GitApi",
    "pipelines": "PipelinesApi",
    "core": "CoreApi",
    "build": "BuildApi",
    "policy": "PolicyApi",
    "task_agent": "TaskAgentApi",
}
MANIFEST = json.loads(
    (ROOT / "src/azure_devops_sdk/_spec_manifest.json").read_text(encoding="utf-8")
)
UUID_VALUE = "12345678-1234-5678-1234-567812345678"


def _source_operations(module: str) -> set[tuple[str, str, str]]:
    source_dir, source_name, _ = SERVICE_SPECS[module]
    source_file = SPECS / source_dir / "7.0" / f"{source_name}.json"
    spec = json.loads(source_file.read_text(encoding="utf-8-sig"))
    operations = set()
    for group in ("paths", "x-ms-paths"):
        for raw_path, path_item in spec.get(group, {}).items():
            for verb, operation in path_item.items():
                if verb.lower() in {"get", "post", "put", "patch", "delete", "head", "options"}:
                    operations.add((operation["operationId"], raw_path, verb.upper()))
    return operations


def _fake_value(parameter: dict[str, Any]) -> Any:
    annotation = parameter["type"]
    name = parameter["name"]
    if "bool" in annotation:
        return True
    if "int" in annotation:
        return 17
    if "UUID" in annotation:
        return UUID(UUID_VALUE)
    if "list[" in annotation:
        return ["alpha", "beta"]
    if name.lower().endswith("id") and "str" in annotation:
        return UUID_VALUE
    return "synthetic-value"


def _expected_wire_path(route: str, path_parameters: dict[str, Any]) -> str:
    for key, value in path_parameters.items():
        route = re.sub(r"\{" + re.escape(key) + r"\}", str(value), route, flags=re.IGNORECASE)
    return route


def _operation(module: str, operation_id: str) -> dict[str, Any]:
    return next(
        operation
        for operation in MANIFEST["modules"][module]["operations"]
        if operation["operationId"] == operation_id
    )


def _operation_kwargs(operation: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    kwargs = {
        parameter["python_name"]: _fake_value(parameter)
        for parameter in operation["parameters"]
    }
    if operation["body"] is not None:
        kwargs["body"] = {"synthetic": True}
    kwargs.update(overrides)
    return kwargs


@pytest.mark.parametrize("module", SERVICE_SPECS)
def test_manifest_operations_match_source_operation_ids_raw_paths_and_verbs(module: str):
    source = _source_operations(module)
    manifest_ops = MANIFEST["modules"][module]["operations"]
    generated = {
        (op["operationId"], op["source_path"], op["method"])
        for op in manifest_ops
    }
    assert len(manifest_ops) == SERVICE_SPECS[module][2]
    assert generated == source
    assert sum(SERVICE_SPECS[name][2] for name in SERVICE_SPECS) == 298


@pytest.mark.parametrize(
    ("module", "operation"),
    [
        (module, operation)
        for module in SERVICE_SPECS
        for operation in MANIFEST["modules"][module]["operations"]
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_every_generated_method_sends_its_declared_request(module: str, operation: dict[str, Any]):
    api_module = importlib.import_module(f"azure_devops_sdk.{module}.client")
    api_class = getattr(api_module, API_CLASSES[module])
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(204, headers={"x-sweep": "ok"})

    transport = AdoTransport(
        "https://ado.example/collection",
        "synthetic-pat",
        transport=httpx.MockTransport(handler),
    )
    try:
        api = api_class(transport)
        method = getattr(api, operation["python_method"])
        signature = inspect.signature(method)
        parameters = {parameter["python_name"]: parameter for parameter in operation["parameters"]}
        expected_names = set(parameters) | {"accept"}
        if operation["body"] is not None:
            expected_names.add("body")
        assert set(signature.parameters) == expected_names
        for parameter in operation["parameters"]:
            assert (signature.parameters[parameter["python_name"]].default is inspect.Parameter.empty) == parameter["required"]

        kwargs = {
            parameter["python_name"]: _fake_value(parameter)
            for parameter in operation["parameters"]
        }
        # Keep optional path arguments present during the sweep, so every route
        # placeholder is exercised; JSON-compatible mappings are intentionally
        # accepted by the transport for generated body arguments.
        if operation["body"] is not None:
            kwargs["body"] = {"synthetic": True}
        api_response = method(**kwargs)

        assert api_response.status_code == 204
        assert len(captured) == 1
        request = captured[0]
        assert request.method == operation["method"]
        route = _expected_wire_path(
            operation["path"],
            {
                parameter["name"]: kwargs[parameter["python_name"]]
                for parameter in operation["parameters"]
                if parameter["in"] == "path"
            },
        )
        assert request.url.path == "/collection" + route
        assert request.url.params.get("api-version") == "7.0"
        for parameter in operation["parameters"]:
            value = kwargs[parameter["python_name"]]
            if parameter["in"] == "query":
                expected = ",".join(map(str, value)) if isinstance(value, list) else str(value).lower() if isinstance(value, bool) else str(value)
                assert request.url.params.get(parameter["name"]) == expected
        body = operation["body"]
        if body is None:
            assert request.content == b""
            assert "content-type" not in request.headers
        else:
            assert json.loads(request.content) == {"synthetic": True}
            assert request.headers["content-type"].split(";", 1)[0] == body["content_type"]
    finally:
        transport.close()


def test_core_project_uuid_and_team_project_path_parameters():
    from azure_devops_sdk.core.client import CoreApi

    captured = []
    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(lambda request: (captured.append(request) or httpx.Response(200, json=[{"id": UUID_VALUE, "name": "demo"}] if request.url.path.endswith("/_apis/projects") else {"id": UUID_VALUE, "name": "demo"}))),
    )
    try:
        api = CoreApi(transport)
        project = _operation("core", "Projects_List")
        project_method = getattr(api, project["python_method"])
        response = project_method(**_operation_kwargs(project))
        assert response.data[0].id == UUID(UUID_VALUE)
        assert "/_apis/projects" in captured[-1].url.path

        team = next(
            op for op in MANIFEST["modules"]["core"]["operations"]
            if op["operationId"] == "Teams_Get" and "/teams/{teamId}" in op["source_path"]
        )
        args = {p["python_name"]: UUID(UUID_VALUE) if p["name"] in {"projectId", "teamId"} else _fake_value(p) for p in team["parameters"]}
        getattr(api, team["python_method"])(**args)
        assert captured[-1].url.path.endswith(f"/projects/{UUID_VALUE}/teams/{UUID_VALUE}")
    finally:
        transport.close()


def test_build_definitions_list_queue_and_typed_build_ids():
    from azure_devops_sdk.build.client import BuildApi

    captured = []
    transport = AdoTransport(
        "https://ado.example", "synthetic-pat",
        transport=httpx.MockTransport(lambda request: (captured.append(request) or httpx.Response(200, json=[] if request.method == "GET" else {"id": 17, "definition": {"id": 3}}))),
    )
    try:
        api = BuildApi(transport)
        listing = _operation("build", "Definitions_List")
        getattr(api, listing["python_method"])(**_operation_kwargs(listing))
        assert captured[-1].method == "GET"
        assert "/_apis/build/definitions" in captured[-1].url.path

        queue = _operation("build", "Builds_Queue")
        queue_kwargs = _operation_kwargs(queue)
        queue_kwargs["body"] = {"definition": {"id": 3}, "parameters": "{}"}
        response = getattr(api, queue["python_method"])(**queue_kwargs)
        assert captured[-1].method == "POST"
        assert json.loads(captured[-1].content) == queue_kwargs["body"]
        assert response.data.id == 17

        build_get = _operation("build", "Builds_Get")
        build_id = next(p for p in build_get["parameters"] if p["name"] == "buildId")
        signature = inspect.signature(getattr(api, build_get["python_method"]))
        assert "int" in str(signature.parameters[build_id["python_name"]].annotation)
    finally:
        transport.close()


def test_policy_configuration_arbitrary_settings_revision_and_queries():
    from azure_devops_sdk.policy.client import PolicyApi

    captured = []
    transport = AdoTransport(
        "https://ado.example", "synthetic-pat",
        transport=httpx.MockTransport(lambda request: (captured.append(request) or httpx.Response(200, json=[] if "/revisions" in request.url.path else {"id": 9, "revision": 4, "settings": {"future": {"enabled": True}}}))),
    )
    try:
        api = PolicyApi(transport)
        create = _operation("policy", "Configurations_Create")
        body = {"type": {"id": UUID_VALUE}, "isEnabled": True, "settings": {"future": {"nested": [1, "x"]}}}
        response = getattr(api, create["python_method"])(**_operation_kwargs(create, body=body))
        assert json.loads(captured[-1].content) == body
        assert response.data.settings["future"]["enabled"] is True

        update = _operation("policy", "Configurations_Update")
        update_body = {"id": 9, "revision": 5, "settings": {"opaque": {"keep": True}}}
        getattr(api, update["python_method"])(**_operation_kwargs(update, body=update_body))
        assert json.loads(captured[-1].content) == update_body
        revisions = _operation("policy", "Revisions_List")
        revision_args = _operation_kwargs(revisions)
        getattr(api, revisions["python_method"])(**revision_args)
        assert "/revisions" in captured[-1].url.path
        assert captured[-1].url.params.get("api-version") == "7.0"
    finally:
        transport.close()


def test_task_agent_pool_queue_queries_and_variable_group_unknown_fields():
    from azure_devops_sdk.task_agent.client import TaskAgentApi

    captured = []
    transport = AdoTransport(
        "https://ado.example", "synthetic-pat",
        transport=httpx.MockTransport(lambda request: (captured.append(request) or httpx.Response(200, json=group_body if request.method == "POST" else []))),
    )
    try:
        api = TaskAgentApi(transport)
        for operation_id in ("Pools_Get Agent Pools By Ids", "Queues_Get Agent Queues By Ids"):
            operation = _operation("task_agent", operation_id)
            query_name = "poolIds" if operation_id.startswith("Pools_") else "queueIds"
            array_parameter = next(p for p in operation["parameters"] if p["name"] == query_name)
            kwargs = _operation_kwargs(operation, **{array_parameter["python_name"]: [3, 8]})
            getattr(api, operation["python_method"])(**kwargs)
            assert captured[-1].url.params.get(array_parameter["name"]) == "3,8"

        group_create = _operation("task_agent", "Variablegroups_Add")
        group_body = {"name": "synthetic", "variables": {"token": {"value": "x", "isSecret": True}}, "futureField": {"nested": True}}
        kwargs = _operation_kwargs(group_create, body=group_body)
        getattr(api, group_create["python_method"])(**kwargs)
        assert json.loads(captured[-1].content) == group_body

        scoped = _operation("task_agent", "Queues_Get Agent Queues")
        project = next(p for p in scoped["parameters"] if p["name"] == "project")
        getattr(api, scoped["python_method"])(**_operation_kwargs(scoped, **{project["python_name"]: None}))
        assert "/{project}/" not in captured[-1].url.path
    finally:
        transport.close()


def test_pipeline_preview_alias_and_unknown_yaml_configuration_fields_are_preserved():
    from azure_devops_sdk.pipelines.models import RunPipelineParameters
    from azure_devops_sdk.pipelines.client import PipelinesApi

    captured = []
    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(
            lambda request: (captured.append(request) or httpx.Response(204))
        ),
    )
    try:
        params = RunPipelineParameters.model_validate(
            {
                "previewRun": True,
                "resources": {
                    "repositories": {
                        "self": {
                            "repository": "repo-name",
                            "refName": "refs/heads/main",
                            "type": "git",
                            "futureSetting": {"enabled": True},
                        }
                    }
                },
                "yamlOverride": "steps: []",
            }
        )
        assert params.preview_run is True
        params.preview_run = False
        PipelinesApi(transport).preview_preview(
            project="project", pipeline_id=7, body=params
        )
        payload = json.loads(captured[0].content)
        assert payload["previewRun"] is False
        assert payload["resources"]["repositories"]["self"]["futureSetting"] == {"enabled": True}
        assert payload["yamlOverride"] == "steps: []"
    finally:
        transport.close()


def test_git_optional_project_json_patch_change_item_and_array_query():
    from azure_devops_sdk.git.models import JsonPatchDocument
    from azure_devops_sdk.git.client import GitApi

    requests = []
    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(
            lambda request: (requests.append(request) or httpx.Response(204))
        ),
    )
    api = GitApi(transport)
    try:
        api.commits_get_changes(
            repository_id=UUID_VALUE, commit_id="abc", project=None, top=5, skip=2
        )
        assert "/_apis/git/repositories/" in requests[0].url.path
        assert "/projects/" not in requests[0].url.path

        patch = JsonPatchDocument.model_validate(
            [{"op": "add", "path": "/description", "value": {"new": True}}]
        )
        api.pull_request_iteration_statuses_update(
            repository_id=UUID_VALUE,
            pull_request_id=9,
            iteration_id=2,
            body=patch,
        )
        assert requests[1].headers["content-type"] == "application/json-patch+json"
        assert json.loads(requests[1].content) == [
            {"op": "add", "path": "/description", "value": {"new": True}}
        ]

        item = {"changeType": "add", "item": {"path": "/new-file"}}
        api.pushes_create(repository_id=UUID_VALUE, body={"refUpdates": [], "commits": [{"changes": [item]}]})
        assert json.loads(requests[2].content)["commits"][0]["changes"][0] == item

        api.commits_get_commits(
            repository_id=UUID_VALUE,
            project="project",
            search_criteria_ids=["one", "two"],
        )
        assert requests[3].url.params.get("searchCriteria.ids") == "one,two"
    finally:
        transport.close()


@pytest.mark.parametrize("value", ["a primitive", 42, True, ["one", 2]])
def test_json_patch_operation_accepts_arbitrary_json_values(value: Any):
    from azure_devops_sdk.git.models import JsonPatchDocument

    patch = JsonPatchDocument.model_validate(
        [{"op": "replace", "path": "/value", "value": value}]
    )
    assert patch.model_dump(mode="json", by_alias=True) == [
        {"op": "replace", "path": "/value", "value": value}
    ]


def test_git_binary_upload_accepts_bytes_and_sends_raw_octet_stream():
    from azure_devops_sdk.git.client import GitApi

    captured = []
    payload = b"\x00\xffstreamed attachment"
    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(
            lambda request: (captured.append(request) or httpx.Response(200, json={}))
        ),
    )
    try:
        method = GitApi(transport).pull_request_attachments_create
        body_parameter = inspect.signature(method).parameters["body"]
        assert body_parameter.annotation in (bytes, "bytes")
        method(
            file_name="attachment.bin",
            repository_id=UUID_VALUE,
            pull_request_id=3,
            body=payload,
        )
        assert captured[0].content == payload
        assert captured[0].headers["content-type"] == "application/octet-stream"
    finally:
        transport.close()


@pytest.mark.parametrize(
    ("method_name", "kwargs"),
    [
        ("items_get", {"repository_id": UUID_VALUE, "path": "/readme.md", "project": "project"}),
        ("trees_get", {"repository_id": UUID_VALUE, "sha1": "tree-sha", "project": "project"}),
        ("blobs_get_blob", {"repository_id": UUID_VALUE, "sha1": "blob-sha", "project": "project"}),
    ],
)
def test_git_json_negotiation_for_binary_capable_reads_parses_json(method_name: str, kwargs: dict[str, Any]):
    from azure_devops_sdk.git.client import GitApi

    from azure_devops_sdk.git.models import GitBlobRef, GitItem, GitTreeRef

    response_models = {
        "items_get": (GitItem, {"path": "/readme.md", "objectId": "item-sha"}),
        "trees_get": (
            GitTreeRef,
            {"objectId": "tree-sha", "treeEntries": [{"relativePath": "readme.md"}]},
        ),
        "blobs_get_blob": (GitBlobRef, {"objectId": "blob-sha", "size": 2}),
    }
    expected_model, payload = response_models[method_name]
    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json=payload)
        ),
    )
    try:
        response = getattr(GitApi(transport), method_name)(**kwargs, accept="application/json")
        assert isinstance(response.data, expected_model)
        if method_name == "items_get":
            assert response.data.path == "/readme.md"
            assert response.data.object_id == "item-sha"
        elif method_name == "trees_get":
            assert response.data.object_id == "tree-sha"
            assert response.data.tree_entries[0].relative_path == "readme.md"
        else:
            assert response.data.object_id == "blob-sha"
            assert response.data.size == 2
    finally:
        transport.close()


def test_git_x_ms_path_parameters_array_envelope_and_binary_response_headers():
    from azure_devops_sdk.git.client import GitApi

    captured = []
    blob = b"\x00\xffgenerated-sdk"

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.url.path.endswith("/blobs") or request.url.path.endswith("/blobs/sha"):
            return httpx.Response(200, content=blob, headers={"content-type": "application/octet-stream", "x-artifact": "present"})
        if request.url.path.endswith("/commits") and request.url.params.get("pushId") is None:
            return httpx.Response(200, json=[{"commitId": "c1"}])
        return httpx.Response(200, json={"count": 1, "value": []})

    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(handler),
    )
    api = GitApi(transport)
    try:
        api.items_get(repository_id=UUID_VALUE, path="/src/a b", project="project")
        assert captured[0].url.params.get("path") == "/src/a b"

        commits = api.commits_get_commits(repository_id=UUID_VALUE, project="project")
        assert commits.data[0].model_dump(by_alias=True)["commitId"] == "c1"
        enveloped = api.commits_get_push_commits(repository_id=UUID_VALUE, push_id=12, project="project")
        assert enveloped.data == []

        uploaded = api.blobs_get_blobs_zip(
            repository_id=UUID_VALUE,
            project="project",
            filename="archive.zip",
            body=["blob-one", "blob-two"],
        )
        assert uploaded.data == blob
        assert json.loads(captured[-1].content) == ["blob-one", "blob-two"]
        assert captured[-1].headers["content-type"] == "application/json"
        assert captured[-1].headers["accept"] == "application/zip"

        downloaded = api.blobs_get_blob(repository_id=UUID_VALUE, sha1="sha", project="project")
        assert downloaded.data == blob
        assert downloaded.content == blob
        assert downloaded.headers["x-artifact"] == "present"
        assert captured[-1].headers["accept"] == "application/json"
        downloaded_binary = api.blobs_get_blob(
            repository_id=UUID_VALUE,
            sha1="sha",
            project="project",
            accept="application/zip",
        )
        assert downloaded_binary.data == blob
        assert downloaded_binary.content == blob
        assert downloaded_binary.headers["x-artifact"] == "present"
        assert captured[-1].headers["accept"] == "application/zip"
    finally:
        transport.close()


def test_git_repository_alias_survives_fetch_modify_and_update():
    from azure_devops_sdk.git.client import GitApi

    captured = []
    response_body = {
        "id": UUID_VALUE,
        "name": "repo",
        "defaultBranch": "refs/heads/old",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.method == "GET":
            return httpx.Response(200, json=response_body)
        return httpx.Response(200, json=json.loads(request.content))

    transport = AdoTransport(
        "https://ado.example",
        "synthetic-pat",
        transport=httpx.MockTransport(handler),
    )
    try:
        api = GitApi(transport)
        repository = api.repositories_get_repository(repository_id=UUID_VALUE).data
        assert repository.default_branch == "refs/heads/old"
        repository.default_branch = "refs/heads/new"

        api.repositories_update(repository_id=UUID_VALUE, body=repository)

        updated_payload = json.loads(captured[-1].content)
        assert updated_payload["defaultBranch"] == "refs/heads/new"
        assert "default_branch" not in updated_payload
    finally:
        transport.close()
