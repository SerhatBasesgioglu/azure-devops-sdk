"""Spec-generated Git/Pipelines REST methods."""
from __future__ import annotations
from typing import Any
from uuid import UUID
from azure_devops_sdk._transport import ApiResponse, AdoTransport
from . import models

class CoreApi:
    def __init__(self, transport: AdoTransport) -> None:
        self._transport = transport

    def processes_list(self, *, accept: str = 'application/json') -> ApiResponse[list[models.Process]]:
        "Processes_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/process/processes', content_type=None, accept=accept, response_type=list[models.Process], binary=False, service='core', operation='processes_list', route_template='/_apis/process/processes')
    def processes_get(self, *, process_id: str | UUID, accept: str = 'application/json') -> ApiResponse[models.Process]:
        "Processes_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/process/processes/{processId}', path_params={'processId': process_id}, content_type=None, accept=accept, response_type=models.Process, binary=False, service='core', operation='processes_get', route_template='/_apis/process/processes/{processId}')
    def projects_list(self, *, state_filter: str | None = None, top: int | None = None, skip: int | None = None, continuation_token: str | None = None, get_default_team_image_url: bool | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TeamProjectReference]]:
        "Projects_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects', query={'stateFilter': state_filter, '$top': top, '$skip': skip, 'continuationToken': continuation_token, 'getDefaultTeamImageUrl': get_default_team_image_url}, content_type=None, accept=accept, response_type=list[models.TeamProjectReference], binary=False, service='core', operation='projects_list', route_template='/_apis/projects')
    def projects_create(self, *, body: models.TeamProject, accept: str = 'application/json') -> ApiResponse[models.OperationReference]:
        "Projects_Create. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/projects', body=body, content_type='application/json', accept=accept, response_type=models.OperationReference, binary=False, service='core', operation='projects_create', route_template='/_apis/projects')
    def projects_get(self, *, project_id: str, include_capabilities: bool | None = None, include_history: bool | None = None, accept: str = 'application/json') -> ApiResponse[models.TeamProject]:
        "Projects_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects/{projectId}', path_params={'projectId': project_id}, query={'includeCapabilities': include_capabilities, 'includeHistory': include_history}, content_type=None, accept=accept, response_type=models.TeamProject, binary=False, service='core', operation='projects_get', route_template='/_apis/projects/{projectId}')
    def projects_delete(self, *, project_id: str | UUID, accept: str = 'application/json') -> ApiResponse[models.OperationReference]:
        "Projects_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/projects/{projectId}', path_params={'projectId': project_id}, content_type=None, accept=accept, response_type=models.OperationReference, binary=False, service='core', operation='projects_delete', route_template='/_apis/projects/{projectId}')
    def projects_update(self, *, project_id: str | UUID, body: models.TeamProject, accept: str = 'application/json') -> ApiResponse[models.OperationReference]:
        "Projects_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/projects/{projectId}', path_params={'projectId': project_id}, body=body, content_type='application/json', accept=accept, response_type=models.OperationReference, binary=False, service='core', operation='projects_update', route_template='/_apis/projects/{projectId}')
    def avatar_remove_project_avatar(self, *, project_id: str, accept: str = 'application/json') -> ApiResponse[Any]:
        "Avatar_Remove Project Avatar. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/projects/{projectId}/avatar', path_params={'projectId': project_id}, content_type=None, accept=accept, response_type=Any, binary=False, service='core', operation='avatar_remove_project_avatar', route_template='/_apis/projects/{projectId}/avatar')
    def avatar_set_project_avatar(self, *, project_id: str, body: models.ProjectAvatar, accept: str = 'application/json') -> ApiResponse[Any]:
        "Avatar_Set Project Avatar. Use accept='application/json'."
        return self._transport.request('PUT', '/_apis/projects/{projectId}/avatar', path_params={'projectId': project_id}, body=body, content_type='application/json', accept=accept, response_type=Any, binary=False, service='core', operation='avatar_set_project_avatar', route_template='/_apis/projects/{projectId}/avatar')
    def projects_get_project_properties(self, *, project_id: str | UUID, keys: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.ProjectProperty]]:
        "Projects_Get Project Properties. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects/{projectId}/properties', path_params={'projectId': project_id}, query={'keys': keys}, content_type=None, accept=accept, response_type=list[models.ProjectProperty], binary=False, service='core', operation='projects_get_project_properties', route_template='/_apis/projects/{projectId}/properties')
    def projects_set_project_properties(self, *, project_id: str | UUID, body: models.JsonPatchDocument, accept: str = 'application/json') -> ApiResponse[Any]:
        "Projects_Set Project Properties. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/projects/{projectId}/properties', path_params={'projectId': project_id}, body=body, content_type='application/json-patch+json', accept=accept, response_type=Any, binary=False, service='core', operation='projects_set_project_properties', route_template='/_apis/projects/{projectId}/properties')
    def teams_create(self, *, project_id: str, body: models.WebApiTeam, accept: str = 'application/json') -> ApiResponse[models.WebApiTeam]:
        "Teams_Create. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/projects/{projectId}/teams', path_params={'projectId': project_id}, body=body, content_type='application/json', accept=accept, response_type=models.WebApiTeam, binary=False, service='core', operation='teams_create', route_template='/_apis/projects/{projectId}/teams')
    def teams_get_teams(self, *, project_id: str, mine: bool | None = None, top: int | None = None, skip: int | None = None, expand_identity: bool | None = None, accept: str = 'application/json') -> ApiResponse[list[models.WebApiTeam]]:
        "Teams_Get Teams. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects/{projectId}/teams', path_params={'projectId': project_id}, query={'$mine': mine, '$top': top, '$skip': skip, '$expandIdentity': expand_identity}, content_type=None, accept=accept, response_type=list[models.WebApiTeam], binary=False, service='core', operation='teams_get_teams', route_template='/_apis/projects/{projectId}/teams')
    def teams_delete(self, *, project_id: str, team_id: str, accept: str = 'application/json') -> ApiResponse[Any]:
        "Teams_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/projects/{projectId}/teams/{teamId}', path_params={'projectId': project_id, 'teamId': team_id}, content_type=None, accept=accept, response_type=Any, binary=False, service='core', operation='teams_delete', route_template='/_apis/projects/{projectId}/teams/{teamId}')
    def teams_get(self, *, project_id: str, team_id: str, expand_identity: bool | None = None, accept: str = 'application/json') -> ApiResponse[models.WebApiTeam]:
        "Teams_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects/{projectId}/teams/{teamId}', path_params={'projectId': project_id, 'teamId': team_id}, query={'$expandIdentity': expand_identity}, content_type=None, accept=accept, response_type=models.WebApiTeam, binary=False, service='core', operation='teams_get', route_template='/_apis/projects/{projectId}/teams/{teamId}')
    def teams_update(self, *, project_id: str, team_id: str, body: models.WebApiTeam, accept: str = 'application/json') -> ApiResponse[models.WebApiTeam]:
        "Teams_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/projects/{projectId}/teams/{teamId}', path_params={'projectId': project_id, 'teamId': team_id}, body=body, content_type='application/json', accept=accept, response_type=models.WebApiTeam, binary=False, service='core', operation='teams_update', route_template='/_apis/projects/{projectId}/teams/{teamId}')
    def teams_get_team_members_with_extended_properties(self, *, project_id: str, team_id: str, top: int | None = None, skip: int | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TeamMember]]:
        "Teams_Get Team Members With Extended Properties. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/projects/{projectId}/teams/{teamId}/members', path_params={'projectId': project_id, 'teamId': team_id}, query={'$top': top, '$skip': skip}, content_type=None, accept=accept, response_type=list[models.TeamMember], binary=False, service='core', operation='teams_get_team_members_with_extended_properties', route_template='/_apis/projects/{projectId}/teams/{teamId}/members')
    def teams_get_all_teams(self, *, mine: bool | None = None, top: int | None = None, skip: int | None = None, expand_identity: bool | None = None, accept: str = 'application/json') -> ApiResponse[list[models.WebApiTeam]]:
        "Teams_Get All Teams. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/teams', query={'$mine': mine, '$top': top, '$skip': skip, '$expandIdentity': expand_identity}, content_type=None, accept=accept, response_type=list[models.WebApiTeam], binary=False, service='core', operation='teams_get_all_teams', route_template='/_apis/teams')
