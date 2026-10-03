"""Spec-generated Git/Pipelines REST methods."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from azure_devops_sdk._transport import ApiResponse, AdoTransport
from . import models


class BuildApi:
    def __init__(self, transport: AdoTransport) -> None:
        self._transport = transport

    def controllers_list(
        self,
        *,
        name: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildController]]:
        "Controllers_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/_apis/build/controllers',
            query={
                'name': name,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildController],
            binary=False,
            service='build',
            operation='controllers_list',
            route_template='/_apis/build/controllers',
        )

    def controllers_get(
        self,
        *,
        controller_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildController]:
        "Controllers_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/_apis/build/controllers/{controllerId}',
            path_params={
                'controllerId': controller_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildController,
            binary=False,
            service='build',
            operation='controllers_get',
            route_template='/_apis/build/controllers/{controllerId}',
        )

    def resource_usage_get(
        self,
        *,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildResourceUsage]:
        "Resource Usage_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/_apis/build/resourceusage',
            content_type=None,
            accept=accept,
            response_type=models.BuildResourceUsage,
            binary=False,
            service='build',
            operation='resource_usage_get',
            route_template='/_apis/build/resourceusage',
        )

    def history_get(
        self,
        *,
        days_to_lookback: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildRetentionHistory]:
        "History_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/_apis/build/retention/history',
            query={
                'daysToLookback': days_to_lookback,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildRetentionHistory,
            binary=False,
            service='build',
            operation='history_get',
            route_template='/_apis/build/retention/history',
        )

    def badge_get(
        self,
        *,
        project: str | UUID,
        definition_id: int,
        branch_name: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[str]:
        "Badge_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/_apis/public/build/definitions/{project}/{definitionId}/badge',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'branchName': branch_name,
            },
            content_type=None,
            accept=accept,
            response_type=str,
            binary=False,
            service='build',
            operation='badge_get',
            route_template='/_apis/public/build/definitions/{project}/{definitionId}/badge',
        )

    def authorizedresources_authorize_project_resources(
        self,
        *,
        project: str,
        body: list[models.DefinitionResourceReference],
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.DefinitionResourceReference]]:
        "Authorizedresources_Authorize Project Resources. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/authorizedresources',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[models.DefinitionResourceReference],
            binary=False,
            service='build',
            operation='authorizedresources_authorize_project_resources',
            route_template='/{project}/_apis/build/authorizedresources',
        )

    def authorizedresources_list(
        self,
        *,
        project: str,
        type: str | None = None,
        id: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.DefinitionResourceReference]]:
        "Authorizedresources_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/authorizedresources',
            path_params={
                'project': project,
            },
            query={
                'type': type,
                'id': id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.DefinitionResourceReference],
            binary=False,
            service='build',
            operation='authorizedresources_list',
            route_template='/{project}/_apis/build/authorizedresources',
        )

    def builds_list(
        self,
        *,
        project: str,
        definitions: str | None = None,
        queues: str | None = None,
        build_number: str | None = None,
        min_time: str | None = None,
        max_time: str | None = None,
        requested_for: str | None = None,
        reason_filter: str | None = None,
        status_filter: str | None = None,
        result_filter: str | None = None,
        tag_filters: str | None = None,
        properties: str | None = None,
        top: int | None = None,
        continuation_token: str | None = None,
        max_builds_per_definition: int | None = None,
        deleted_filter: str | None = None,
        query_order: str | None = None,
        branch_name: str | None = None,
        build_ids: str | None = None,
        repository_id: str | None = None,
        repository_type: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Build]]:
        "Builds_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds',
            path_params={
                'project': project,
            },
            query={
                'definitions': definitions,
                'queues': queues,
                'buildNumber': build_number,
                'minTime': min_time,
                'maxTime': max_time,
                'requestedFor': requested_for,
                'reasonFilter': reason_filter,
                'statusFilter': status_filter,
                'resultFilter': result_filter,
                'tagFilters': tag_filters,
                'properties': properties,
                '$top': top,
                'continuationToken': continuation_token,
                'maxBuildsPerDefinition': max_builds_per_definition,
                'deletedFilter': deleted_filter,
                'queryOrder': query_order,
                'branchName': branch_name,
                'buildIds': build_ids,
                'repositoryId': repository_id,
                'repositoryType': repository_type,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.Build],
            binary=False,
            service='build',
            operation='builds_list',
            route_template='/{project}/_apis/build/builds',
        )

    def builds_queue(
        self,
        *,
        project: str,
        ignore_warnings: bool | None = None,
        check_in_ticket: str | None = None,
        source_build_id: int | None = None,
        definition_id: int | None = None,
        body: models.Build,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Build]:
        "Builds_Queue. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/builds',
            path_params={
                'project': project,
            },
            query={
                'ignoreWarnings': ignore_warnings,
                'checkInTicket': check_in_ticket,
                'sourceBuildId': source_build_id,
                'definitionId': definition_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.Build,
            binary=False,
            service='build',
            operation='builds_queue',
            route_template='/{project}/_apis/build/builds',
        )

    def builds_update_builds(
        self,
        *,
        project: str,
        body: list[models.Build],
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Build]]:
        "Builds_Update Builds. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/builds',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[models.Build],
            binary=False,
            service='build',
            operation='builds_update_builds',
            route_template='/{project}/_apis/build/builds',
        )

    def builds_delete(
        self,
        *,
        project: str,
        build_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Builds_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/builds/{buildId}',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='builds_delete',
            route_template='/{project}/_apis/build/builds/{buildId}',
        )

    def builds_get(
        self,
        *,
        project: str,
        build_id: int,
        property_filters: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Build]:
        "Builds_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'propertyFilters': property_filters,
            },
            content_type=None,
            accept=accept,
            response_type=models.Build,
            binary=False,
            service='build',
            operation='builds_get',
            route_template='/{project}/_apis/build/builds/{buildId}',
        )

    def builds_update_build(
        self,
        *,
        project: str,
        build_id: int,
        retry: bool | None = None,
        body: models.Build,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Build]:
        "Builds_Update Build. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/builds/{buildId}',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'retry': retry,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.Build,
            binary=False,
            service='build',
            operation='builds_update_build',
            route_template='/{project}/_apis/build/builds/{buildId}',
        )

    def attachments_get(
        self,
        *,
        project: str,
        build_id: int,
        timeline_id: str | UUID,
        record_id: str | UUID,
        type: str,
        name: str,
        accept: str = 'application/octet-stream',
    ) -> ApiResponse[bytes]:
        "Attachments_Get. Use accept='application/octet-stream' for the default binary representation; pass another accepted media type for alternate representations."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/{timelineId}/{recordId}/attachments/{type}/{name}',
            path_params={
                'project': project,
                'buildId': build_id,
                'timelineId': timeline_id,
                'recordId': record_id,
                'type': type,
                'name': name,
            },
            content_type=None,
            accept=accept,
            response_type=bytes,
            binary=True,
            service='build',
            operation='attachments_get',
            route_template='/{project}/_apis/build/builds/{buildId}/{timelineId}/{recordId}/attachments/{type}/{name}',
        )

    def artifacts_create(
        self,
        *,
        project: str,
        build_id: int,
        body: models.BuildArtifact,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildArtifact]:
        "Artifacts_Create. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/builds/{buildId}/artifacts',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.BuildArtifact,
            binary=False,
            service='build',
            operation='artifacts_create',
            route_template='/{project}/_apis/build/builds/{buildId}/artifacts',
        )

    def artifacts_list(
        self,
        *,
        project: str,
        build_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildArtifact]]:
        "Artifacts_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/artifacts',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildArtifact],
            binary=False,
            service='build',
            operation='artifacts_list',
            route_template='/{project}/_apis/build/builds/{buildId}/artifacts',
        )

    def attachments_list(
        self,
        *,
        project: str,
        build_id: int,
        type: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Attachment]]:
        "Attachments_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/attachments/{type}',
            path_params={
                'project': project,
                'buildId': build_id,
                'type': type,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.Attachment],
            binary=False,
            service='build',
            operation='attachments_list',
            route_template='/{project}/_apis/build/builds/{buildId}/attachments/{type}',
        )

    def builds_get_build_changes(
        self,
        *,
        project: str,
        build_id: int,
        continuation_token: str | None = None,
        top: int | None = None,
        include_source_change: bool | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Change]]:
        "Builds_Get Build Changes. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/changes',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'continuationToken': continuation_token,
                '$top': top,
                'includeSourceChange': include_source_change,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.Change],
            binary=False,
            service='build',
            operation='builds_get_build_changes',
            route_template='/{project}/_apis/build/builds/{buildId}/changes',
        )

    def builds_get_retention_leases_for_build(
        self,
        *,
        project: str,
        build_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RetentionLease]]:
        "Builds_Get Retention Leases For Build. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/leases',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.RetentionLease],
            binary=False,
            service='build',
            operation='builds_get_retention_leases_for_build',
            route_template='/{project}/_apis/build/builds/{buildId}/leases',
        )

    def builds_get_build_logs(
        self,
        *,
        project: str,
        build_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildLog] | bytes]:
        "Builds_Get Build Logs. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/logs',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildLog] | bytes,
            binary=False,
            service='build',
            operation='builds_get_build_logs',
            route_template='/{project}/_apis/build/builds/{buildId}/logs',
        )

    def builds_get_build_log(
        self,
        *,
        project: str,
        build_id: int,
        log_id: int,
        start_line: int | None = None,
        end_line: int | None = None,
        accept: str = 'application/zip',
    ) -> ApiResponse[bytes]:
        "Builds_Get Build Log. Use accept='application/zip' for the default binary representation; pass another accepted media type for alternate representations."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/logs/{logId}',
            path_params={
                'project': project,
                'buildId': build_id,
                'logId': log_id,
            },
            query={
                'startLine': start_line,
                'endLine': end_line,
            },
            content_type=None,
            accept=accept,
            response_type=bytes,
            binary=True,
            service='build',
            operation='builds_get_build_log',
            route_template='/{project}/_apis/build/builds/{buildId}/logs/{logId}',
        )

    def properties_get_build_properties(
        self,
        *,
        project: str,
        build_id: int,
        filter: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PropertiesCollection]:
        "Properties_Get Build Properties. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/properties',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'filter': filter,
            },
            content_type=None,
            accept=accept,
            response_type=models.PropertiesCollection,
            binary=False,
            service='build',
            operation='properties_get_build_properties',
            route_template='/{project}/_apis/build/builds/{buildId}/properties',
        )

    def properties_update_build_properties(
        self,
        *,
        project: str,
        build_id: int,
        body: models.JsonPatchDocument,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PropertiesCollection]:
        "Properties_Update Build Properties. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/builds/{buildId}/properties',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            body=body,
            content_type='application/json-patch+json',
            accept=accept,
            response_type=models.PropertiesCollection,
            binary=False,
            service='build',
            operation='properties_update_build_properties',
            route_template='/{project}/_apis/build/builds/{buildId}/properties',
        )

    def report_get(
        self,
        *,
        project: str,
        build_id: int,
        type: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildReportMetadata]:
        "Report_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/report',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'type': type,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildReportMetadata,
            binary=False,
            service='build',
            operation='report_get',
            route_template='/{project}/_apis/build/builds/{buildId}/report',
        )

    def stages_update(
        self,
        *,
        build_id: int,
        stage_ref_name: str,
        project: str | None = None,
        body: models.UpdateStageParameters,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Stages_Update. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/builds/{buildId}/stages/{stageRefName}',
            path_params={
                'project': project,
                'buildId': build_id,
                'stageRefName': stage_ref_name,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='stages_update',
            route_template='/{project}/_apis/build/builds/{buildId}/stages/{stageRefName}',
        )

    def tags_add_build_tags(
        self,
        *,
        project: str,
        build_id: int,
        body: list[str],
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Add Build Tags. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/builds/{buildId}/tags',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_add_build_tags',
            route_template='/{project}/_apis/build/builds/{buildId}/tags',
        )

    def tags_get_build_tags(
        self,
        *,
        project: str,
        build_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Get Build Tags. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/tags',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_get_build_tags',
            route_template='/{project}/_apis/build/builds/{buildId}/tags',
        )

    def tags_update_build_tags(
        self,
        *,
        project: str,
        build_id: int,
        body: models.UpdateTagParameters,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Update Build Tags. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/builds/{buildId}/tags',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_update_build_tags',
            route_template='/{project}/_apis/build/builds/{buildId}/tags',
        )

    def tags_add_build_tag(
        self,
        *,
        project: str,
        build_id: int,
        tag: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Add Build Tag. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/build/builds/{buildId}/tags/{tag}',
            path_params={
                'project': project,
                'buildId': build_id,
                'tag': tag,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_add_build_tag',
            route_template='/{project}/_apis/build/builds/{buildId}/tags/{tag}',
        )

    def tags_delete_build_tag(
        self,
        *,
        project: str,
        build_id: int,
        tag: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Delete Build Tag. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/builds/{buildId}/tags/{tag}',
            path_params={
                'project': project,
                'buildId': build_id,
                'tag': tag,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_delete_build_tag',
            route_template='/{project}/_apis/build/builds/{buildId}/tags/{tag}',
        )

    def timeline_get(
        self,
        *,
        project: str,
        build_id: int,
        timeline_id: str | UUID | None = None,
        change_id: int | None = None,
        plan_id: str | UUID | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Timeline]:
        "Timeline_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/timeline/{timelineId}',
            path_params={
                'project': project,
                'buildId': build_id,
                'timelineId': timeline_id,
            },
            query={
                'changeId': change_id,
                'planId': plan_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.Timeline,
            binary=False,
            service='build',
            operation='timeline_get',
            route_template='/{project}/_apis/build/builds/{buildId}/timeline/{timelineId}',
        )

    def builds_get_build_work_items_refs(
        self,
        *,
        project: str,
        build_id: int,
        top: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.ResourceRef]]:
        "Builds_Get Build Work Items Refs. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/workitems',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                '$top': top,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.ResourceRef],
            binary=False,
            service='build',
            operation='builds_get_build_work_items_refs',
            route_template='/{project}/_apis/build/builds/{buildId}/workitems',
        )

    def builds_get_build_work_items_refs_from_commits(
        self,
        *,
        project: str,
        build_id: int,
        top: int | None = None,
        body: list[str],
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.ResourceRef]]:
        "Builds_Get Build Work Items Refs From Commits. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/builds/{buildId}/workitems',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                '$top': top,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[models.ResourceRef],
            binary=False,
            service='build',
            operation='builds_get_build_work_items_refs_from_commits',
            route_template='/{project}/_apis/build/builds/{buildId}/workitems',
        )

    def builds_get_changes_between_builds(
        self,
        *,
        project: str,
        from_build_id: int | None = None,
        to_build_id: int | None = None,
        top: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Change]]:
        "Builds_Get Changes Between Builds. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/changes',
            path_params={
                'project': project,
            },
            query={
                'fromBuildId': from_build_id,
                'toBuildId': to_build_id,
                '$top': top,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.Change],
            binary=False,
            service='build',
            operation='builds_get_changes_between_builds',
            route_template='/{project}/_apis/build/changes',
        )

    def definitions_create(
        self,
        *,
        project: str,
        definition_to_clone_id: int | None = None,
        definition_to_clone_revision: int | None = None,
        body: models.BuildDefinition,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinition]:
        "Definitions_Create. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/definitions',
            path_params={
                'project': project,
            },
            query={
                'definitionToCloneId': definition_to_clone_id,
                'definitionToCloneRevision': definition_to_clone_revision,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.BuildDefinition,
            binary=False,
            service='build',
            operation='definitions_create',
            route_template='/{project}/_apis/build/definitions',
        )

    def definitions_list(
        self,
        *,
        project: str,
        name: str | None = None,
        repository_id: str | None = None,
        repository_type: str | None = None,
        query_order: str | None = None,
        top: int | None = None,
        continuation_token: str | None = None,
        min_metrics_time: str | None = None,
        definition_ids: str | None = None,
        path: str | None = None,
        built_after: str | None = None,
        not_built_after: str | None = None,
        include_all_properties: bool | None = None,
        include_latest_builds: bool | None = None,
        task_id_filter: str | UUID | None = None,
        process_type: int | None = None,
        yaml_filename: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildDefinitionReference]]:
        "Definitions_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions',
            path_params={
                'project': project,
            },
            query={
                'name': name,
                'repositoryId': repository_id,
                'repositoryType': repository_type,
                'queryOrder': query_order,
                '$top': top,
                'continuationToken': continuation_token,
                'minMetricsTime': min_metrics_time,
                'definitionIds': definition_ids,
                'path': path,
                'builtAfter': built_after,
                'notBuiltAfter': not_built_after,
                'includeAllProperties': include_all_properties,
                'includeLatestBuilds': include_latest_builds,
                'taskIdFilter': task_id_filter,
                'processType': process_type,
                'yamlFilename': yaml_filename,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildDefinitionReference],
            binary=False,
            service='build',
            operation='definitions_list',
            route_template='/{project}/_apis/build/definitions',
        )

    def definitions_delete(
        self,
        *,
        project: str,
        definition_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Definitions_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/definitions/{definitionId}',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='definitions_delete',
            route_template='/{project}/_apis/build/definitions/{definitionId}',
        )

    def definitions_get(
        self,
        *,
        project: str,
        definition_id: int,
        revision: int | None = None,
        min_metrics_time: str | None = None,
        property_filters: str | None = None,
        include_latest_builds: bool | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinition]:
        "Definitions_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'revision': revision,
                'minMetricsTime': min_metrics_time,
                'propertyFilters': property_filters,
                'includeLatestBuilds': include_latest_builds,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildDefinition,
            binary=False,
            service='build',
            operation='definitions_get',
            route_template='/{project}/_apis/build/definitions/{definitionId}',
        )

    def definitions_restore_definition(
        self,
        *,
        project: str,
        definition_id: int,
        deleted: bool,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinition]:
        "Definitions_Restore Definition. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/definitions/{definitionId}',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'deleted': deleted,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildDefinition,
            binary=False,
            service='build',
            operation='definitions_restore_definition',
            route_template='/{project}/_apis/build/definitions/{definitionId}',
        )

    def definitions_update(
        self,
        *,
        project: str,
        definition_id: int,
        secrets_source_definition_id: int | None = None,
        secrets_source_definition_revision: int | None = None,
        body: models.BuildDefinition,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinition]:
        "Definitions_Update. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/build/definitions/{definitionId}',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'secretsSourceDefinitionId': secrets_source_definition_id,
                'secretsSourceDefinitionRevision': secrets_source_definition_revision,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.BuildDefinition,
            binary=False,
            service='build',
            operation='definitions_update',
            route_template='/{project}/_apis/build/definitions/{definitionId}',
        )

    def metrics_get_definition_metrics(
        self,
        *,
        project: str,
        definition_id: int,
        min_metrics_time: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildMetric]]:
        "Metrics_Get Definition Metrics. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}/metrics',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'minMetricsTime': min_metrics_time,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildMetric],
            binary=False,
            service='build',
            operation='metrics_get_definition_metrics',
            route_template='/{project}/_apis/build/definitions/{definitionId}/metrics',
        )

    def properties_get_definition_properties(
        self,
        *,
        project: str,
        definition_id: int,
        filter: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PropertiesCollection]:
        "Properties_Get Definition Properties. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}/properties',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'filter': filter,
            },
            content_type=None,
            accept=accept,
            response_type=models.PropertiesCollection,
            binary=False,
            service='build',
            operation='properties_get_definition_properties',
            route_template='/{project}/_apis/build/definitions/{definitionId}/properties',
        )

    def properties_update_definition_properties(
        self,
        *,
        project: str,
        definition_id: int,
        body: models.JsonPatchDocument,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PropertiesCollection]:
        "Properties_Update Definition Properties. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/definitions/{definitionId}/properties',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            body=body,
            content_type='application/json-patch+json',
            accept=accept,
            response_type=models.PropertiesCollection,
            binary=False,
            service='build',
            operation='properties_update_definition_properties',
            route_template='/{project}/_apis/build/definitions/{definitionId}/properties',
        )

    def resources_authorize_definition_resources(
        self,
        *,
        project: str,
        definition_id: int,
        body: list[models.DefinitionResourceReference],
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.DefinitionResourceReference]]:
        "Resources_Authorize Definition Resources. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/definitions/{definitionId}/resources',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[models.DefinitionResourceReference],
            binary=False,
            service='build',
            operation='resources_authorize_definition_resources',
            route_template='/{project}/_apis/build/definitions/{definitionId}/resources',
        )

    def resources_list(
        self,
        *,
        project: str,
        definition_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.DefinitionResourceReference]]:
        "Resources_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}/resources',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.DefinitionResourceReference],
            binary=False,
            service='build',
            operation='resources_list',
            route_template='/{project}/_apis/build/definitions/{definitionId}/resources',
        )

    def definitions_get_definition_revisions(
        self,
        *,
        project: str,
        definition_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildDefinitionRevision]]:
        "Definitions_Get Definition Revisions. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}/revisions',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildDefinitionRevision],
            binary=False,
            service='build',
            operation='definitions_get_definition_revisions',
            route_template='/{project}/_apis/build/definitions/{definitionId}/revisions',
        )

    def tags_add_definition_tags(
        self,
        *,
        project: str,
        definition_id: int,
        body: list[str],
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Add Definition Tags. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/definitions/{DefinitionId}/tags',
            path_params={
                'project': project,
                'DefinitionId': definition_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_add_definition_tags',
            route_template='/{project}/_apis/build/definitions/{DefinitionId}/tags',
        )

    def tags_get_definition_tags(
        self,
        *,
        project: str,
        definition_id: int,
        revision: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Get Definition Tags. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{DefinitionId}/tags',
            path_params={
                'project': project,
                'DefinitionId': definition_id,
            },
            query={
                'revision': revision,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_get_definition_tags',
            route_template='/{project}/_apis/build/definitions/{DefinitionId}/tags',
        )

    def tags_update_definition_tags(
        self,
        *,
        project: str,
        definition_id: int,
        body: models.UpdateTagParameters,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Update Definition Tags. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/definitions/{DefinitionId}/tags',
            path_params={
                'project': project,
                'DefinitionId': definition_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_update_definition_tags',
            route_template='/{project}/_apis/build/definitions/{DefinitionId}/tags',
        )

    def tags_add_definition_tag(
        self,
        *,
        project: str,
        definition_id: int,
        tag: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Add Definition Tag. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/build/definitions/{DefinitionId}/tags/{tag}',
            path_params={
                'project': project,
                'DefinitionId': definition_id,
                'tag': tag,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_add_definition_tag',
            route_template='/{project}/_apis/build/definitions/{DefinitionId}/tags/{tag}',
        )

    def tags_delete_definition_tag(
        self,
        *,
        project: str,
        definition_id: int,
        tag: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Delete Definition Tag. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/definitions/{DefinitionId}/tags/{tag}',
            path_params={
                'project': project,
                'DefinitionId': definition_id,
                'tag': tag,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_delete_definition_tag',
            route_template='/{project}/_apis/build/definitions/{DefinitionId}/tags/{tag}',
        )

    def yaml_get(
        self,
        *,
        project: str,
        definition_id: int,
        revision: int | None = None,
        min_metrics_time: str | None = None,
        property_filters: str | None = None,
        include_latest_builds: bool | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.YamlBuild]:
        "Yaml_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/{definitionId}/yaml',
            path_params={
                'project': project,
                'definitionId': definition_id,
            },
            query={
                'revision': revision,
                'minMetricsTime': min_metrics_time,
                'propertyFilters': property_filters,
                'includeLatestBuilds': include_latest_builds,
            },
            content_type=None,
            accept=accept,
            response_type=models.YamlBuild,
            binary=False,
            service='build',
            operation='yaml_get',
            route_template='/{project}/_apis/build/definitions/{definitionId}/yaml',
        )

    def templates_list(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildDefinitionTemplate]]:
        "Templates_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/templates',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildDefinitionTemplate],
            binary=False,
            service='build',
            operation='templates_list',
            route_template='/{project}/_apis/build/definitions/templates',
        )

    def templates_delete(
        self,
        *,
        project: str,
        template_id: str,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Templates_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/definitions/templates/{templateId}',
            path_params={
                'project': project,
                'templateId': template_id,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='templates_delete',
            route_template='/{project}/_apis/build/definitions/templates/{templateId}',
        )

    def templates_get(
        self,
        *,
        project: str,
        template_id: str,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinitionTemplate]:
        "Templates_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/definitions/templates/{templateId}',
            path_params={
                'project': project,
                'templateId': template_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildDefinitionTemplate,
            binary=False,
            service='build',
            operation='templates_get',
            route_template='/{project}/_apis/build/definitions/templates/{templateId}',
        )

    def templates_save_template(
        self,
        *,
        project: str,
        template_id: str,
        body: models.BuildDefinitionTemplate,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildDefinitionTemplate]:
        "Templates_Save Template. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/build/definitions/templates/{templateId}',
            path_params={
                'project': project,
                'templateId': template_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.BuildDefinitionTemplate,
            binary=False,
            service='build',
            operation='templates_save_template',
            route_template='/{project}/_apis/build/definitions/templates/{templateId}',
        )

    def folders_create(
        self,
        *,
        project: str,
        path: str,
        body: models.Folder,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Folder]:
        "Folders_Create. Use accept='application/json'."
        return self._transport.request(
            'PUT',
            '/{project}/_apis/build/folders',
            path_params={
                'project': project,
            },
            query={
                'path': path,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.Folder,
            binary=False,
            service='build',
            operation='folders_create',
            route_template='/{project}/_apis/build/folders',
        )

    def folders_delete(
        self,
        *,
        project: str,
        path: str,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Folders_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/folders',
            path_params={
                'project': project,
            },
            query={
                'path': path,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='folders_delete',
            route_template='/{project}/_apis/build/folders',
        )

    def folders_update(
        self,
        *,
        project: str,
        path: str,
        body: models.Folder,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Folder]:
        "Folders_Update. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/folders',
            path_params={
                'project': project,
            },
            query={
                'path': path,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.Folder,
            binary=False,
            service='build',
            operation='folders_update',
            route_template='/{project}/_apis/build/folders',
        )

    def folders_list(
        self,
        *,
        project: str,
        path: str | None = None,
        query_order: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.Folder]]:
        "Folders_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/folders/{path}',
            path_params={
                'project': project,
                'path': path,
            },
            query={
                'queryOrder': query_order,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.Folder],
            binary=False,
            service='build',
            operation='folders_list',
            route_template='/{project}/_apis/build/folders/{path}',
        )

    def general_settings_get(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PipelineGeneralSettings]:
        "General Settings_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/generalsettings',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=models.PipelineGeneralSettings,
            binary=False,
            service='build',
            operation='general_settings_get',
            route_template='/{project}/_apis/build/generalsettings',
        )

    def general_settings_update(
        self,
        *,
        project: str,
        body: models.PipelineGeneralSettings,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PipelineGeneralSettings]:
        "General Settings_Update. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/generalsettings',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.PipelineGeneralSettings,
            binary=False,
            service='build',
            operation='general_settings_update',
            route_template='/{project}/_apis/build/generalsettings',
        )

    def latest_get(
        self,
        *,
        project: str,
        definition: str,
        branch_name: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.Build]:
        "Latest_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/latest/{definition}',
            path_params={
                'project': project,
                'definition': definition,
            },
            query={
                'branchName': branch_name,
            },
            content_type=None,
            accept=accept,
            response_type=models.Build,
            binary=False,
            service='build',
            operation='latest_get',
            route_template='/{project}/_apis/build/latest/{definition}',
        )

    def metrics_get_project_metrics(
        self,
        *,
        project: str,
        metric_aggregation_type: str | None = None,
        min_metrics_time: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildMetric]]:
        "Metrics_Get Project Metrics. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/metrics/{metricAggregationType}',
            path_params={
                'project': project,
                'metricAggregationType': metric_aggregation_type,
            },
            query={
                'minMetricsTime': min_metrics_time,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildMetric],
            binary=False,
            service='build',
            operation='metrics_get_project_metrics',
            route_template='/{project}/_apis/build/metrics/{metricAggregationType}',
        )

    def options_list(
        self,
        *,
        project: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.BuildOptionDefinition]]:
        "Options_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/options',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.BuildOptionDefinition],
            binary=False,
            service='build',
            operation='options_list',
            route_template='/{project}/_apis/build/options',
        )

    def badge_get_build_badge_data(
        self,
        *,
        project: str,
        repo_type: str,
        repo_id: str | None = None,
        branch_name: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[str]:
        "Badge_Get Build Badge Data. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/repos/{repoType}/badge',
            path_params={
                'project': project,
                'repoType': repo_type,
            },
            query={
                'repoId': repo_id,
                'branchName': branch_name,
            },
            content_type=None,
            accept=accept,
            response_type=str,
            binary=False,
            service='build',
            operation='badge_get_build_badge_data',
            route_template='/{project}/_apis/build/repos/{repoType}/badge',
        )

    def retention_get(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[models.ProjectRetentionSetting]:
        "Retention_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/retention',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=models.ProjectRetentionSetting,
            binary=False,
            service='build',
            operation='retention_get',
            route_template='/{project}/_apis/build/retention',
        )

    def retention_update(
        self,
        *,
        project: str,
        body: models.UpdateProjectRetentionSettingModel,
        accept: str = 'application/json',
    ) -> ApiResponse[models.ProjectRetentionSetting]:
        "Retention_Update. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/retention',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.ProjectRetentionSetting,
            binary=False,
            service='build',
            operation='retention_update',
            route_template='/{project}/_apis/build/retention',
        )

    def leases_add(
        self,
        *,
        project: str,
        body: list[models.NewRetentionLease],
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RetentionLease]]:
        "Leases_Add. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/build/retention/leases',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=list[models.RetentionLease],
            binary=False,
            service='build',
            operation='leases_add',
            route_template='/{project}/_apis/build/retention/leases',
        )

    def leases_delete(
        self,
        *,
        project: str,
        ids: str,
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Leases_Delete. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/retention/leases',
            path_params={
                'project': project,
            },
            query={
                'ids': ids,
            },
            content_type=None,
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='leases_delete',
            route_template='/{project}/_apis/build/retention/leases',
        )

    def leases_get_retention_leases_by_minimal_retention_leases(
        self,
        *,
        project: str,
        leases_to_fetch: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RetentionLease]]:
        "Leases_Get Retention Leases By Minimal Retention Leases. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/retention/leases',
            path_params={
                'project': project,
            },
            query={
                'leasesToFetch': leases_to_fetch,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.RetentionLease],
            binary=False,
            service='build',
            operation='leases_get_retention_leases_by_minimal_retention_leases',
            route_template='/{project}/_apis/build/retention/leases',
        )

    def leases_get(
        self,
        *,
        project: str,
        lease_id: int,
        accept: str = 'application/json',
    ) -> ApiResponse[models.RetentionLease]:
        "Leases_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/retention/leases/{leaseId}',
            path_params={
                'project': project,
                'leaseId': lease_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.RetentionLease,
            binary=False,
            service='build',
            operation='leases_get',
            route_template='/{project}/_apis/build/retention/leases/{leaseId}',
        )

    def leases_update(
        self,
        *,
        project: str,
        lease_id: int,
        body: models.RetentionLeaseUpdate,
        accept: str = 'application/json',
    ) -> ApiResponse[models.RetentionLease]:
        "Leases_Update. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/retention/leases/{leaseId}',
            path_params={
                'project': project,
                'leaseId': lease_id,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.RetentionLease,
            binary=False,
            service='build',
            operation='leases_update',
            route_template='/{project}/_apis/build/retention/leases/{leaseId}',
        )

    def settings_get(
        self,
        *,
        project: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildSettings]:
        "Settings_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/settings',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildSettings,
            binary=False,
            service='build',
            operation='settings_get',
            route_template='/{project}/_apis/build/settings',
        )

    def settings_update(
        self,
        *,
        project: str | None = None,
        body: models.BuildSettings,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildSettings]:
        "Settings_Update. Use accept='application/json'."
        return self._transport.request(
            'PATCH',
            '/{project}/_apis/build/settings',
            path_params={
                'project': project,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=models.BuildSettings,
            binary=False,
            service='build',
            operation='settings_update',
            route_template='/{project}/_apis/build/settings',
        )

    def status_get(
        self,
        *,
        project: str,
        definition: str,
        branch_name: str | None = None,
        stage_name: str | None = None,
        job_name: str | None = None,
        configuration: str | None = None,
        label: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[str]:
        "Status_Get. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/status/{definition}',
            path_params={
                'project': project,
                'definition': definition,
            },
            query={
                'branchName': branch_name,
                'stageName': stage_name,
                'jobName': job_name,
                'configuration': configuration,
                'label': label,
            },
            content_type=None,
            accept=accept,
            response_type=str,
            binary=False,
            service='build',
            operation='status_get',
            route_template='/{project}/_apis/build/status/{definition}',
        )

    def tags_get_tags(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Get Tags. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/tags',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_get_tags',
            route_template='/{project}/_apis/build/tags',
        )

    def tags_delete_tag(
        self,
        *,
        project: str,
        tag: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Tags_Delete Tag. Use accept='application/json'."
        return self._transport.request(
            'DELETE',
            '/{project}/_apis/build/tags/{tag}',
            path_params={
                'project': project,
                'tag': tag,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='tags_delete_tag',
            route_template='/{project}/_apis/build/tags/{tag}',
        )

    def builds_get_work_items_between_builds(
        self,
        *,
        project: str,
        from_build_id: int,
        to_build_id: int,
        top: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.ResourceRef]]:
        "Builds_Get Work Items Between Builds. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/workitems',
            path_params={
                'project': project,
            },
            query={
                'fromBuildId': from_build_id,
                'toBuildId': to_build_id,
                '$top': top,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.ResourceRef],
            binary=False,
            service='build',
            operation='builds_get_work_items_between_builds',
            route_template='/{project}/_apis/build/workitems',
        )

    def source_providers_list(
        self,
        *,
        project: str,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.SourceProviderAttributes]]:
        "Source Providers_List. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceproviders',
            path_params={
                'project': project,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.SourceProviderAttributes],
            binary=False,
            service='build',
            operation='source_providers_list',
            route_template='/{project}/_apis/sourceproviders',
        )

    def source_providers_list_branches(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        branch_name: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[str]]:
        "Source Providers_List Branches. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/branches',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
                'branchName': branch_name,
            },
            content_type=None,
            accept=accept,
            response_type=list[str],
            binary=False,
            service='build',
            operation='source_providers_list_branches',
            route_template='/{project}/_apis/sourceProviders/{providerName}/branches',
        )

    def source_providers_get_file_contents(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        commit_or_branch: str | None = None,
        path: str | None = None,
        accept: str = 'text/plain',
    ) -> ApiResponse[bytes]:
        "Source Providers_Get File Contents. Use accept='text/plain' for the default binary representation; pass another accepted media type for alternate representations."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/filecontents',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
                'commitOrBranch': commit_or_branch,
                'path': path,
            },
            content_type=None,
            accept=accept,
            response_type=bytes,
            binary=True,
            service='build',
            operation='source_providers_get_file_contents',
            route_template='/{project}/_apis/sourceProviders/{providerName}/filecontents',
        )

    def source_providers_get_path_contents(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        commit_or_branch: str | None = None,
        path: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.SourceRepositoryItem]]:
        "Source Providers_Get Path Contents. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/pathcontents',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
                'commitOrBranch': commit_or_branch,
                'path': path,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.SourceRepositoryItem],
            binary=False,
            service='build',
            operation='source_providers_get_path_contents',
            route_template='/{project}/_apis/sourceProviders/{providerName}/pathcontents',
        )

    def source_providers_get_pull_request(
        self,
        *,
        project: str,
        provider_name: str,
        pull_request_id: str,
        repository_id: str | None = None,
        service_endpoint_id: str | UUID | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.PullRequest]:
        "Source Providers_Get Pull Request. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/pullrequests/{pullRequestId}',
            path_params={
                'project': project,
                'providerName': provider_name,
                'pullRequestId': pull_request_id,
            },
            query={
                'repositoryId': repository_id,
                'serviceEndpointId': service_endpoint_id,
            },
            content_type=None,
            accept=accept,
            response_type=models.PullRequest,
            binary=False,
            service='build',
            operation='source_providers_get_pull_request',
            route_template='/{project}/_apis/sourceProviders/{providerName}/pullrequests/{pullRequestId}',
        )

    def source_providers_list_repositories(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        result_set: str | None = None,
        page_results: bool | None = None,
        continuation_token: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[models.SourceRepositories]:
        "Source Providers_List Repositories. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/repositories',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
                'resultSet': result_set,
                'pageResults': page_results,
                'continuationToken': continuation_token,
            },
            content_type=None,
            accept=accept,
            response_type=models.SourceRepositories,
            binary=False,
            service='build',
            operation='source_providers_list_repositories',
            route_template='/{project}/_apis/sourceProviders/{providerName}/repositories',
        )

    def source_providers_restore_webhooks(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        body: list[str],
        accept: str = 'application/json',
    ) -> ApiResponse[Any]:
        "Source Providers_Restore Webhooks. Use accept='application/json'."
        return self._transport.request(
            'POST',
            '/{project}/_apis/sourceProviders/{providerName}/webhooks',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
            },
            body=body,
            content_type='application/json',
            accept=accept,
            response_type=Any,
            binary=False,
            service='build',
            operation='source_providers_restore_webhooks',
            route_template='/{project}/_apis/sourceProviders/{providerName}/webhooks',
        )

    def source_providers_list_webhooks(
        self,
        *,
        project: str,
        provider_name: str,
        service_endpoint_id: str | UUID | None = None,
        repository: str | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RepositoryWebhook]]:
        "Source Providers_List Webhooks. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/sourceProviders/{providerName}/webhooks',
            path_params={
                'project': project,
                'providerName': provider_name,
            },
            query={
                'serviceEndpointId': service_endpoint_id,
                'repository': repository,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.RepositoryWebhook],
            binary=False,
            service='build',
            operation='source_providers_list_webhooks',
            route_template='/{project}/_apis/sourceProviders/{providerName}/webhooks',
        )

    def artifacts_get_artifact(
        self,
        *,
        project: str,
        build_id: int,
        artifact_name: str,
        accept: str = 'application/json',
    ) -> ApiResponse[models.BuildArtifact | bytes]:
        "Artifacts_Get Artifact. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/artifacts',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'artifactName': artifact_name,
            },
            content_type=None,
            accept=accept,
            response_type=models.BuildArtifact | bytes,
            binary=False,
            service='build',
            operation='artifacts_get_artifact',
            route_template='/{project}/_apis/build/builds/{buildId}/artifacts',
        )

    def artifacts_get_file(
        self,
        *,
        project: str,
        build_id: int,
        artifact_name: str,
        file_id: str,
        file_name: str,
        accept: str = 'application/octet-stream',
    ) -> ApiResponse[bytes]:
        "Artifacts_Get File. Use accept='application/octet-stream' for the default binary representation; pass another accepted media type for alternate representations."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/builds/{buildId}/artifacts',
            path_params={
                'project': project,
                'buildId': build_id,
            },
            query={
                'artifactName': artifact_name,
                'fileId': file_id,
                'fileName': file_name,
            },
            content_type=None,
            accept=accept,
            response_type=bytes,
            binary=True,
            service='build',
            operation='artifacts_get_file',
            route_template='/{project}/_apis/build/builds/{buildId}/artifacts',
        )

    def leases_get_retention_leases_by_user_id(
        self,
        *,
        project: str,
        user_owner_id: str | UUID,
        definition_id: int | None = None,
        run_id: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RetentionLease]]:
        "Leases_Get Retention Leases By User Id. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/retention/leases',
            path_params={
                'project': project,
            },
            query={
                'userOwnerId': user_owner_id,
                'definitionId': definition_id,
                'runId': run_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.RetentionLease],
            binary=False,
            service='build',
            operation='leases_get_retention_leases_by_user_id',
            route_template='/{project}/_apis/build/retention/leases',
        )

    def leases_get_retention_leases_by_owner_id(
        self,
        *,
        project: str,
        owner_id: str | None = None,
        definition_id: int | None = None,
        run_id: int | None = None,
        accept: str = 'application/json',
    ) -> ApiResponse[list[models.RetentionLease]]:
        "Leases_Get Retention Leases By Owner Id. Use accept='application/json'."
        return self._transport.request(
            'GET',
            '/{project}/_apis/build/retention/leases',
            path_params={
                'project': project,
            },
            query={
                'ownerId': owner_id,
                'definitionId': definition_id,
                'runId': run_id,
            },
            content_type=None,
            accept=accept,
            response_type=list[models.RetentionLease],
            binary=False,
            service='build',
            operation='leases_get_retention_leases_by_owner_id',
            route_template='/{project}/_apis/build/retention/leases',
        )
