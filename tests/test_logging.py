from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from azure_devops_sdk._transport import AdoTransport
from azure_devops_sdk.core.client import CoreApi


LOGGER_NAME = "azure_devops_sdk.transport"
ROOT = Path(__file__).resolve().parents[1]


def _transport(handler):
    return AdoTransport(
        "https://ado.example/collection",
        "synthetic-pat",
        transport=httpx.MockTransport(handler),
    )


def _sdk_records(caplog):
    return [record for record in caplog.records if record.name == LOGGER_NAME]


def test_generated_success_emits_one_safe_completion_record(caplog):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    transport = _transport(lambda _: httpx.Response(200, json=[{"id": "12345678-1234-5678-1234-567812345678", "name": "demo"}]))
    try:
        result = CoreApi(transport).projects_list()
    finally:
        transport.close()

    assert result.data[0].name == "demo"
    records = _sdk_records(caplog)
    assert len(records) == 1
    record = records[0]
    assert record.levelno == logging.DEBUG
    assert record.event == "request.completed"
    assert record.getMessage() == "Azure DevOps request completed"
    assert record.sdk_service == "core"
    assert record.sdk_operation == "projects_list"
    assert record.http_method == "GET"
    assert record.route_template.rstrip("/") == "/_apis/projects"
    assert record.status_code == 200
    assert record.duration_ms >= 0
    assert record.outcome == "success"
    assert record.error_type is None
    assert not record.exc_info


@pytest.mark.parametrize("status", [401, 404, 429, 500])
def test_http_status_failures_are_logged_once_and_reraised(caplog, status):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    calls = []

    def handler(_):
        calls.append(None)
        response = httpx.Response(status, request=httpx.Request("GET", "https://ado.example/_apis/projects"))
        return response

    transport = _transport(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError) as raised:
            transport.request("GET", "/_apis/projects", service="core", operation="projects_list", route_template="/_apis/projects")
    finally:
        transport.close()

    assert len(calls) == 1
    records = _sdk_records(caplog)
    assert len(records) == 1
    record = records[0]
    assert record.event == "request.failed"
    assert record.getMessage() == "Azure DevOps request failed"
    assert record.sdk_service == "core"
    assert record.sdk_operation == "projects_list"
    assert record.http_method == "GET"
    assert record.route_template == "/_apis/projects"
    assert record.status_code == status
    assert record.outcome == "failure"
    assert record.error_type == "http_error"
    assert not record.exc_info


@pytest.mark.parametrize(
    ("error", "category"),
    [
        (httpx.TimeoutException("CANARY_TIMEOUT"), "timeout"),
        (httpx.ConnectError("CANARY_CONNECTION"), "connection_error"),
        (httpx.ReadError("CANARY_TRANSPORT"), "transport_error"),
        (ValueError("CANARY_REQUEST"), "request_error"),
        (RuntimeError("CANARY_UNEXPECTED"), "unexpected_error"),
    ],
)
def test_transport_exceptions_use_fixed_safe_categories_and_preserve_identity(caplog, error, category):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    calls = []

    def handler(_):
        calls.append(None)
        raise error

    transport = _transport(handler)
    try:
        with pytest.raises(type(error)) as raised:
            transport.request("GET", "/_apis/private/CANARY_PATH", query={"token": "CANARY_QUERY"}, service="core", operation="private_get", route_template="/_apis/private/{id}")
    finally:
        transport.close()

    assert raised.value is error
    assert len(calls) == 1
    records = _sdk_records(caplog)
    assert len(records) == 1
    record = records[0]
    assert record.event == "request.failed"
    assert record.getMessage() == "Azure DevOps request failed"
    assert record.error_type == category
    assert record.status_code is None
    assert record.route_template == "/_apis/private/{id}"
    assert not record.exc_info
    assert "CANARY" not in repr(record.__dict__)
    assert "CANARY" not in caplog.text


def test_invalid_json_and_validation_errors_are_redacted(caplog):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    responses = iter([
        httpx.Response(200, content=b'{"secret":"CANARY_BODY"'),
        httpx.Response(200, json={"secret": "CANARY_VALIDATION"}),
    ])
    transport = _transport(lambda _: next(responses))
    try:
        with pytest.raises(ValueError):
            transport.request("GET", "/invalid", response_type=dict)
        with pytest.raises(ValidationError):
            transport.request("GET", "/invalid", response_type=int)
    finally:
        transport.close()

    records = _sdk_records(caplog)
    assert [record.error_type for record in records] == ["invalid_json", "validation_error"]
    assert all(record.event == "request.failed" and not record.exc_info for record in records)
    assert "CANARY" not in repr([record.__dict__ for record in records])


def test_direct_transport_defaults_metadata_to_none_and_never_logs_wire_url_or_payload(caplog):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    transport = _transport(lambda _: httpx.Response(200, json={}))
    try:
        transport.request(
            "GET",
            "/literal/CANARY_PATH",
            query={"token": "CANARY_QUERY_VALUE"},
            body={"token": "CANARY_BODY"},
        )
    finally:
        transport.close()

    records = _sdk_records(caplog)
    assert len(records) == 1
    record = records[0]
    assert record.sdk_service is None
    assert record.sdk_operation is None
    assert record.route_template is None
    assert "CANARY" not in repr(record.__dict__)
    assert "ado.example" not in repr(record.__dict__)


@pytest.mark.parametrize("fails", [False, True])
def test_logging_handler_failures_do_not_change_request_result_or_exception(caplog, fails):
    class BrokenHandler(logging.Handler):
        def emit(self, record):
            raise RuntimeError("CANARY_LOG_HANDLER")

    logger = logging.getLogger(LOGGER_NAME)
    handler = BrokenHandler()
    logger.addHandler(handler)
    error = RuntimeError("CANARY_ORIGINAL")
    transport = _transport(lambda _: (_ for _ in ()).throw(error) if fails else httpx.Response(200, json={}))
    try:
        if fails:
            with pytest.raises(RuntimeError) as raised:
                transport.request("GET", "/safe")
            assert raised.value is error
        else:
            assert transport.request("GET", "/safe").status_code == 200
    finally:
        transport.close()
        logger.removeHandler(handler)


def test_package_import_and_transport_construction_do_not_configure_root_or_emit_output():
    script = """
import logging
before = (list(logging.root.handlers), logging.root.level)
import azure_devops_sdk
from azure_devops_sdk._transport import AdoTransport
import httpx
client = AdoTransport('https://ado.example', 'synthetic-pat', transport=httpx.MockTransport(lambda _: httpx.Response(204)))
client.close()
assert (list(logging.root.handlers), logging.root.level) == before
assert any(isinstance(handler, logging.NullHandler) for handler in logging.getLogger('azure_devops_sdk').handlers)
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    assert result.stderr == ""
