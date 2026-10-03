from __future__ import annotations

import importlib
from pathlib import Path

import httpx


ROOT = Path(__file__).resolve().parents[1]


def test_public_package_imports_without_environment_configuration(monkeypatch):
    for name in ("ADO_URL", "ADO_ORG", "ADO_PAT"):
        monkeypatch.delenv(name, raising=False)

    package = importlib.import_module("azure_devops_sdk")
    git = importlib.import_module("azure_devops_sdk.git")
    pipelines = importlib.import_module("azure_devops_sdk.pipelines")
    core = importlib.import_module("azure_devops_sdk.core")
    build = importlib.import_module("azure_devops_sdk.build")
    policy = importlib.import_module("azure_devops_sdk.policy")
    task_agent = importlib.import_module("azure_devops_sdk.task_agent")
    git_models = importlib.import_module("azure_devops_sdk.git.models")
    pipeline_models = importlib.import_module("azure_devops_sdk.pipelines.models")
    core_models = importlib.import_module("azure_devops_sdk.core.models")
    build_models = importlib.import_module("azure_devops_sdk.build.models")
    policy_models = importlib.import_module("azure_devops_sdk.policy.models")
    task_agent_models = importlib.import_module("azure_devops_sdk.task_agent.models")

    assert package.AdoClient
    assert git.GitApi
    assert pipelines.PipelinesApi
    assert git_models.GitRepository
    assert pipeline_models.Pipeline
    assert core.CoreApi
    assert build.BuildApi
    assert policy.PolicyApi
    assert task_agent.TaskAgentApi
    assert core_models.TeamProjectReference
    assert build_models.Build
    assert policy_models.PolicyConfiguration
    assert task_agent_models.TaskAgentPool


def test_ado_client_composes_services_over_an_injected_offline_transport():
    from azure_devops_sdk import AdoClient
    from azure_devops_sdk.git import GitApi
    from azure_devops_sdk.pipelines import PipelinesApi
    from azure_devops_sdk.core import CoreApi
    from azure_devops_sdk.build import BuildApi
    from azure_devops_sdk.policy import PolicyApi
    from azure_devops_sdk.task_agent import TaskAgentApi

    client = AdoClient(
        "https://ado.example/collection",
        "synthetic-pat",
        transport=httpx.MockTransport(lambda _: httpx.Response(204)),
    )
    try:
        assert isinstance(client.git, GitApi)
        assert isinstance(client.pipelines, PipelinesApi)
        assert isinstance(client.core, CoreApi)
        assert isinstance(client.build, BuildApi)
        assert isinstance(client.policy, PolicyApi)
        assert isinstance(client.task_agent, TaskAgentApi)
        assert client.git._transport is client.pipelines._transport
        assert all(
            service._transport is client.git._transport
            for service in (client.core, client.build, client.policy, client.task_agent)
        )
    finally:
        client.close()


def test_generated_package_is_authoritative_not_legacy_generated_folder():
    package = ROOT / "src/azure_devops_sdk"
    assert not (package / "generated").exists()
    assert (package / "_spec_manifest.json").is_file()
    manifest = __import__("json").loads((package / "_spec_manifest.json").read_text())
    assert sum(module["operation_count"] for module in manifest["modules"].values()) == 298
    assert set(manifest["modules"]) == {"git", "pipelines", "core", "build", "policy", "task_agent"}
    assert not (package / "runtime.py").exists()
    assert not (package / "models.py").exists()
    assert not (ROOT / "main.py").exists()
