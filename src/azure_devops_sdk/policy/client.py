"""Spec-generated Git/Pipelines REST methods."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from azure_devops_sdk._transport import ApiResponse, AdoTransport
from . import models


class PolicyApi:
    def __init__(self, transport: AdoTransport) -> None:
        self._transport = transport

    def configurations_create(
        self,
        *,
        project: str,
        body: models.PolicyConfiguration,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyConfiguration]:
        "Configurations_Create. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/policy/configurations',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.PolicyConfiguration,
            binary=False,
            service='policy',
            operation='configurations_create',
            route_template='/{project}/_apis/policy/configurations',
        )

    def configurations_list(
        self,
        *,
        project: str,
        scope: str | None = None,
        top: int | None = None,
        continuation_token: str | None = None,
        policy_type: str | UUID | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.PolicyConfiguration]]:
        "Configurations_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/configurations',
            path_params={
                'project': project,
            },
            query={
                'scope': scope,
                '$top': top,
                'continuationToken': continuation_token,
                'policyType': policy_type,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.PolicyConfiguration],
            binary=False,
            service='policy',
            operation='configurations_list',
            route_template='/{project}/_apis/policy/configurations',
        )

    def configurations_delete(
        self,
        *,
        project: str,
        configuration_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Configurations_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/policy/configurations/{configurationId}',
            path_params={
                'project': project,
                'configurationId': configuration_id,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='policy',
            operation='configurations_delete',
            route_template='/{project}/_apis/policy/configurations/{configurationId}',
        )

    def configurations_get(
        self,
        *,
        project: str,
        configuration_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyConfiguration]:
        "Configurations_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/configurations/{configurationId}',
            path_params={
                'project': project,
                'configurationId': configuration_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PolicyConfiguration,
            binary=False,
            service='policy',
            operation='configurations_get',
            route_template='/{project}/_apis/policy/configurations/{configurationId}',
        )

    def configurations_update(
        self,
        *,
        project: str,
        configuration_id: int,
        body: models.PolicyConfiguration,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyConfiguration]:
        "Configurations_Update. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/policy/configurations/{configurationId}',
            path_params={
                'project': project,
                'configurationId': configuration_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.PolicyConfiguration,
            binary=False,
            service='policy',
            operation='configurations_update',
            route_template='/{project}/_apis/policy/configurations/{configurationId}',
        )

    def revisions_list(
        self,
        *,
        project: str,
        configuration_id: int,
        top: int | None = None,
        skip: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.PolicyConfiguration]]:
        "Revisions_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/configurations/{configurationId}/revisions',
            path_params={
                'project': project,
                'configurationId': configuration_id,
            },
            query={
                '$top': top,
                '$skip': skip,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.PolicyConfiguration],
            binary=False,
            service='policy',
            operation='revisions_list',
            route_template='/{project}/_apis/policy/configurations/{configurationId}/revisions',
        )

    def revisions_get(
        self,
        *,
        project: str,
        configuration_id: int,
        revision_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyConfiguration]:
        "Revisions_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/configurations/{configurationId}/revisions/{revisionId}',
            path_params={
                'project': project,
                'configurationId': configuration_id,
                'revisionId': revision_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PolicyConfiguration,
            binary=False,
            service='policy',
            operation='revisions_get',
            route_template='/{project}/_apis/policy/configurations/{configurationId}/revisions/{revisionId}',
        )

    def evaluations_list(
        self,
        *,
        project: str,
        artifact_id: str,
        include_not_applicable: bool | None = None,
        top: int | None = None,
        skip: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.PolicyEvaluationRecord]]:
        "Evaluations_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/evaluations',
            path_params={
                'project': project,
            },
            query={
                'artifactId': artifact_id,
                'includeNotApplicable': include_not_applicable,
                '$top': top,
                '$skip': skip,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.PolicyEvaluationRecord],
            binary=False,
            service='policy',
            operation='evaluations_list',
            route_template='/{project}/_apis/policy/evaluations',
        )

    def evaluations_get(
        self,
        *,
        project: str,
        evaluation_id: str | UUID,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyEvaluationRecord]:
        "Evaluations_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/evaluations/{evaluationId}',
            path_params={
                'project': project,
                'evaluationId': evaluation_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PolicyEvaluationRecord,
            binary=False,
            service='policy',
            operation='evaluations_get',
            route_template='/{project}/_apis/policy/evaluations/{evaluationId}',
        )

    def evaluations_requeue_policy_evaluation(
        self,
        *,
        project: str,
        evaluation_id: str | UUID,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyEvaluationRecord]:
        "Evaluations_Requeue Policy Evaluation. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/policy/evaluations/{evaluationId}',
            path_params={
                'project': project,
                'evaluationId': evaluation_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PolicyEvaluationRecord,
            binary=False,
            service='policy',
            operation='evaluations_requeue_policy_evaluation',
            route_template='/{project}/_apis/policy/evaluations/{evaluationId}',
        )

    def types_list(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.PolicyType]]:
        "Types_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/types',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.PolicyType],
            binary=False,
            service='policy',
            operation='types_list',
            route_template='/{project}/_apis/policy/types',
        )

    def types_get(
        self,
        *,
        project: str,
        type_id: str | UUID,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PolicyType]:
        "Types_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/policy/types/{typeId}',
            path_params={
                'project': project,
                'typeId': type_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PolicyType,
            binary=False,
            service='policy',
            operation='types_get',
            route_template='/{project}/_apis/policy/types/{typeId}',
        )
