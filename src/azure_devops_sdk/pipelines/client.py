"""Spec-generated Git/Pipelines REST methods."""
from __future__ import annotations
from typing import Any
from uuid import UUID
from azure_devops_sdk._transport import ApiResponse, AdoTransport
from . import models

class PipelinesApi:
    def __init__(self, transport: AdoTransport) -> None:
        self._transport = transport

    def pipelines_create(self, *, project: str, body: models.CreatePipelineParameters, accept: str = 'application/json') -> ApiResponse[models.Pipeline]:
        "Pipelines_Create. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/pipelines', path_params={'project': project}, body=body, content_type='application/json', accept=accept, response_type=models.Pipeline, binary=False, service='pipelines', operation='pipelines_create', route_template='/{project}/_apis/pipelines')
    def pipelines_list(self, *, project: str, order_by: str | None = None, top: int | None = None, continuation_token: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.Pipeline]]:
        "Pipelines_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines', path_params={'project': project}, query={'orderBy': order_by, '$top': top, 'continuationToken': continuation_token}, content_type=None, accept=accept, response_type=list[models.Pipeline], binary=False, service='pipelines', operation='pipelines_list', route_template='/{project}/_apis/pipelines')
    def pipelines_get(self, *, project: str, pipeline_id: int, pipeline_version: int | None = None, accept: str = 'application/json') -> ApiResponse[models.Pipeline]:
        "Pipelines_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}', path_params={'project': project, 'pipelineId': pipeline_id}, query={'pipelineVersion': pipeline_version}, content_type=None, accept=accept, response_type=models.Pipeline, binary=False, service='pipelines', operation='pipelines_get', route_template='/{project}/_apis/pipelines/{pipelineId}')
    def preview_preview(self, *, project: str, pipeline_id: int, pipeline_version: int | None = None, body: models.RunPipelineParameters, accept: str = 'application/json') -> ApiResponse[models.PreviewRun]:
        "Preview_Preview. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/pipelines/{pipelineId}/preview', path_params={'project': project, 'pipelineId': pipeline_id}, query={'pipelineVersion': pipeline_version}, body=body, content_type='application/json', accept=accept, response_type=models.PreviewRun, binary=False, service='pipelines', operation='preview_preview', route_template='/{project}/_apis/pipelines/{pipelineId}/preview')
    def runs_list(self, *, project: str, pipeline_id: int, accept: str = 'application/json') -> ApiResponse[list[models.Run]]:
        "Runs_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}/runs', path_params={'project': project, 'pipelineId': pipeline_id}, content_type=None, accept=accept, response_type=list[models.Run], binary=False, service='pipelines', operation='runs_list', route_template='/{project}/_apis/pipelines/{pipelineId}/runs')
    def runs_run_pipeline(self, *, project: str, pipeline_id: int, pipeline_version: int | None = None, body: models.RunPipelineParameters, accept: str = 'application/json') -> ApiResponse[models.Run]:
        "Runs_Run Pipeline. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/pipelines/{pipelineId}/runs', path_params={'project': project, 'pipelineId': pipeline_id}, query={'pipelineVersion': pipeline_version}, body=body, content_type='application/json', accept=accept, response_type=models.Run, binary=False, service='pipelines', operation='runs_run_pipeline', route_template='/{project}/_apis/pipelines/{pipelineId}/runs')
    def runs_get(self, *, project: str, pipeline_id: int, run_id: int, accept: str = 'application/json') -> ApiResponse[models.Run]:
        "Runs_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}/runs/{runId}', path_params={'project': project, 'pipelineId': pipeline_id, 'runId': run_id}, content_type=None, accept=accept, response_type=models.Run, binary=False, service='pipelines', operation='runs_get', route_template='/{project}/_apis/pipelines/{pipelineId}/runs/{runId}')
    def artifacts_get(self, *, project: str, pipeline_id: int, run_id: int, artifact_name: str, expand: str | None = None, accept: str = 'application/json') -> ApiResponse[models.Artifact]:
        "Artifacts_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/artifacts', path_params={'project': project, 'pipelineId': pipeline_id, 'runId': run_id}, query={'artifactName': artifact_name, '$expand': expand}, content_type=None, accept=accept, response_type=models.Artifact, binary=False, service='pipelines', operation='artifacts_get', route_template='/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/artifacts')
    def logs_list(self, *, project: str, pipeline_id: int, run_id: int, expand: str | None = None, accept: str = 'application/json') -> ApiResponse[models.LogCollection]:
        "Logs_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/logs', path_params={'project': project, 'pipelineId': pipeline_id, 'runId': run_id}, query={'$expand': expand}, content_type=None, accept=accept, response_type=models.LogCollection, binary=False, service='pipelines', operation='logs_list', route_template='/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/logs')
    def logs_get(self, *, project: str, pipeline_id: int, run_id: int, log_id: int, expand: str | None = None, accept: str = 'application/json') -> ApiResponse[models.Log]:
        "Logs_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/logs/{logId}', path_params={'project': project, 'pipelineId': pipeline_id, 'runId': run_id, 'logId': log_id}, query={'$expand': expand}, content_type=None, accept=accept, response_type=models.Log, binary=False, service='pipelines', operation='logs_get', route_template='/{project}/_apis/pipelines/{pipelineId}/runs/{runId}/logs/{logId}')
