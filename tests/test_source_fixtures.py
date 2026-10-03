from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pytest

from azure_devops_sdk._transport import AdoTransport


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT.parent / "vsts-rest-api-specs" / "specification"


@pytest.fixture(scope="module", autouse=True)
def source_specs_available():
    if not SPECS.is_dir():
        pytest.skip(f"source spec repository is unavailable: {SPECS}")


def _example(path: str) -> dict[str, Any]:
    return json.loads((SPECS / path).read_text(encoding="utf-8-sig"))


def _response_body(path: str, status: str = "200") -> Any:
    return _example(path)["responses"][status]["body"]


def _transport(handler):
    return AdoTransport(
        "https://ado.example/collection",
        "synthetic-pat",
        transport=httpx.MockTransport(handler),
    )


def test_build_logs_list_envelope_is_typed_and_binary_alternative_stays_bytes():
    from azure_devops_sdk.build.client import BuildApi
    from azure_devops_sdk.build.models import BuildLog

    # The source operation declares an array response; Azure's standard
    # collection wrapper is also accepted by the transport.
    payload = {"count": 1, "value": [{"id": 1, "lineCount": 2}]}
    transport = _transport(lambda _: httpx.Response(200, json=payload))
    try:
        api = BuildApi(transport)
        logs = api.builds_get_build_logs(project="project", build_id=1)
        assert isinstance(logs.data, list)
        assert isinstance(logs.data[0], BuildLog)
        assert logs.data[0].line_count == 2

        binary_transport = _transport(
            lambda _: httpx.Response(
                200,
                content=b"\x00\xfflog archive",
                headers={"content-type": "application/octet-stream"},
            )
        )
        try:
            binary = BuildApi(binary_transport).builds_get_build_logs(
                project="project", build_id=1, accept="application/zip"
            )
            assert binary.data == b"\x00\xfflog archive"
            assert isinstance(binary.data, bytes)
        finally:
            binary_transport.close()
    finally:
        transport.close()


@pytest.mark.parametrize(
    ("module_name", "api_name", "model_name", "method_name", "kwargs"),
    [
        (
            "core",
            "CoreApi",
            "JsonPatchDocument",
            "projects_set_project_properties",
            {"project_id": "project"},
        ),
        (
            "build",
            "BuildApi",
            "JsonPatchDocument",
            "properties_update_build_properties",
            {"project": "project", "build_id": 1},
        ),
    ],
)
@pytest.mark.parametrize(
    "value", ["text", 23, True, [1, "two"], {"nested": [False]}, None]
)
def test_core_and_build_json_patch_documents_preserve_arbitrary_json_values(
    module_name: str,
    api_name: str,
    model_name: str,
    method_name: str,
    kwargs: dict[str, Any],
    value: Any,
):
    module = __import__(f"azure_devops_sdk.{module_name}.models", fromlist=[model_name])
    patch_type = getattr(module, model_name)
    operation = {"op": "add", "path": "/custom", "value": value, "from": "/source"}
    patch = patch_type.model_validate([operation])
    assert patch.model_dump(mode="json", by_alias=True) == [operation]

    client_module = __import__(f"azure_devops_sdk.{module_name}.client", fromlist=[api_name])
    api_type = getattr(client_module, api_name)
    requests: list[httpx.Request] = []
    transport = _transport(
        lambda request: (requests.append(request) or httpx.Response(204))
    )
    try:
        getattr(api_type(transport), method_name)(**kwargs, body=patch)
        request = requests[0]
        assert request.headers["content-type"].split(";", 1)[0] == "application/json-patch+json"
        assert json.loads(request.content) == [operation]
        assert isinstance(json.loads(request.content), list)
    finally:
        transport.close()


@pytest.mark.parametrize(
    "path",
    [
        "core/7.0/httpExamples/properties/GET__projects__project__properties.json",
        "core/7.0/httpExamples/properties/GET__projects__project__properties_keys-_propertyName_,_wildcard_.json",
    ],
)
def test_project_properties_source_responses_validate_and_values_round_trip(path: str):
    from azure_devops_sdk.core.client import CoreApi

    payload = _response_body(path)
    transport = _transport(lambda _: httpx.Response(200, json=payload))
    try:
        result = CoreApi(transport).projects_get_project_properties(project_id="project")
        assert len(result.data) == payload["count"]
        assert any(item.value == "Agile" for item in result.data) if path.endswith("properties.json") else True
    finally:
        transport.close()

    arbitrary = {"number": 17, "enabled": False, "nested": [None, {"x": "y"}]}
    returned = {"count": 1, "value": [{"name": "custom", "value": arbitrary}]}
    transport = _transport(lambda _: httpx.Response(200, json=returned))
    try:
        result = CoreApi(transport).projects_get_project_properties(project_id="project")
        assert result.data[0].value == arbitrary
    finally:
        transport.close()


def test_targets_list_source_response_preserves_string_and_object_demands():
    from azure_devops_sdk.task_agent.client import TaskAgentApi

    payload = _response_body(
        "distributedTask/7.0/httpExamples/targets/GET__distributedtask_DeploymentTargets__LastRequest_.json"
    )
    transport = _transport(lambda _: httpx.Response(200, json=payload))
    try:
        result = TaskAgentApi(transport).targets_list(
            project="project", deployment_group_id=22, expand="LastCompletedRequest"
        )
        demands = result.data[0].agent.last_completed_request.demands
        assert demands == payload["value"][0]["agent"]["lastCompletedRequest"]["demands"]
        assert all(isinstance(demand, str) for demand in demands)
    finally:
        transport.close()

    object_demands = [{"name": "Agent.Version", "operator": "gtVersion", "value": "1.0"}]
    synthetic = {"count": 1, "value": [{"id": 5, "agent": {"lastCompletedRequest": {"demands": object_demands}}}]}
    transport = _transport(lambda _: httpx.Response(200, json=synthetic))
    try:
        result = TaskAgentApi(transport).targets_list(
            project="project", deployment_group_id=22
        )
        demands = result.data[0].agent.last_completed_request.demands
        assert [demand.model_dump(mode="json", by_alias=True) for demand in demands] == object_demands
    finally:
        transport.close()


def test_targets_get_preserves_public_key_base64_strings_exactly():
    from azure_devops_sdk.task_agent.client import TaskAgentApi

    payload = _response_body(
        "distributedTask/7.0/httpExamples/targets/GET__distributedtask_DeploymentTargets__Id_.json"
    )
    expected_key = payload["agent"]["authorization"]["publicKey"]
    transport = _transport(lambda _: httpx.Response(200, json=payload))
    try:
        result = TaskAgentApi(transport).targets_get(
            project="project", deployment_group_id=22, target_id=5
        )
        key = result.data.agent.authorization.public_key
        assert key.exponent == expected_key["exponent"] == "AQAB"
        assert key.modulus == expected_key["modulus"]
        assert isinstance(key.modulus, str)
    finally:
        transport.close()


def test_policy_settings_and_task_agent_json_objects_allow_arbitrary_keys():
    from azure_devops_sdk.policy.models import PolicyConfiguration
    from azure_devops_sdk.task_agent.models import InputValue

    settings = {"item23": {"custom": 1}, "type": {"custom": 1}}
    policy = PolicyConfiguration.model_validate({"settings": settings})
    assert policy.settings == settings
    assert policy.model_dump(mode="json", by_alias=True)["settings"] == settings

    # TaskAgent's agentData is an untyped object field, unlike the JObject
    # wrapper whose `item` and `type` names are structural metadata.
    task_agent = InputValue.model_validate({"data": settings})
    assert task_agent.data == settings
    assert task_agent.model_dump(mode="json", by_alias=True)["data"] == settings


@pytest.mark.parametrize(
    "path",
    [
        f"policy/7.0/httpExamples/Configurations/POST__policy_configurations{suffix}.json"
        for suffix in ("", "2", "3", "4", "5", "6", "7")
    ],
)
def test_policy_configuration_public_create_responses_preserve_naive_dates(path: str):
    from azure_devops_sdk.policy.client import PolicyApi

    payload = _response_body(path)
    transport = _transport(lambda _: httpx.Response(200, json=payload))
    try:
        result = PolicyApi(transport).configurations_create(
            project="project", body={"type": {"id": "synthetic"}, "settings": {}}
        )
        created_date = result.data.created_date
        source_date = payload["createdDate"]
        assert isinstance(created_date, datetime)
        if "Z" not in source_date and "+" not in source_date and not source_date.endswith("-00:00"):
            assert created_date.tzinfo is None
        assert created_date.strftime("%Y-%m-%d") == source_date.split("T")[0]
    finally:
        transport.close()


def test_policy_configuration_timezone_aware_dates_remain_aware():
    from azure_devops_sdk.policy.models import PolicyConfiguration

    policy = PolicyConfiguration.model_validate({"createdDate": "2024-02-03T04:05:06Z"})
    assert policy.created_date is not None
    assert policy.created_date.utcoffset() is not None
