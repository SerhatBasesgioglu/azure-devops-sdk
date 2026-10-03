"""Spec-generated Git/Pipelines REST methods."""
from __future__ import annotations
from typing import Any
from uuid import UUID
from azure_devops_sdk._transport import ApiResponse, AdoTransport
from . import models

class TaskAgentApi:
    def __init__(self, transport: AdoTransport) -> None:
        self._transport = transport

    def agentclouds_add(self, *, body: models.TaskAgentCloud, accept: str = 'application/json') -> ApiResponse[models.TaskAgentCloud]:
        "Agentclouds_Add. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/distributedtask/agentclouds', body=body, content_type='application/json', accept=accept, response_type=models.TaskAgentCloud, binary=False)
    def agentclouds_list(self, *, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentCloud]]:
        "Agentclouds_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/agentclouds', content_type=None, accept=accept, response_type=list[models.TaskAgentCloud], binary=False)
    def agentclouds_delete(self, *, agent_cloud_id: int, accept: str = 'application/json') -> ApiResponse[models.TaskAgentCloud]:
        "Agentclouds_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/distributedtask/agentclouds/{agentCloudId}', path_params={'agentCloudId': agent_cloud_id}, content_type=None, accept=accept, response_type=models.TaskAgentCloud, binary=False)
    def agentclouds_get(self, *, agent_cloud_id: int, accept: str = 'application/json') -> ApiResponse[models.TaskAgentCloud]:
        "Agentclouds_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/agentclouds/{agentCloudId}', path_params={'agentCloudId': agent_cloud_id}, content_type=None, accept=accept, response_type=models.TaskAgentCloud, binary=False)
    def agentclouds_update(self, *, agent_cloud_id: int, body: models.TaskAgentCloud, accept: str = 'application/json') -> ApiResponse[models.TaskAgentCloud]:
        "Agentclouds_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/distributedtask/agentclouds/{agentCloudId}', path_params={'agentCloudId': agent_cloud_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgentCloud, binary=False)
    def requests_list(self, *, agent_cloud_id: int, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentCloudRequest]]:
        "Requests_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/agentclouds/{agentCloudId}/requests', path_params={'agentCloudId': agent_cloud_id}, content_type=None, accept=accept, response_type=list[models.TaskAgentCloudRequest], binary=False)
    def agentcloudtypes_list(self, *, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentCloudType]]:
        "Agentcloudtypes_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/agentcloudtypes', content_type=None, accept=accept, response_type=list[models.TaskAgentCloudType], binary=False)
    def pools_add(self, *, body: models.TaskAgentPool, accept: str = 'application/json') -> ApiResponse[models.TaskAgentPool]:
        "Pools_Add. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/distributedtask/pools', body=body, content_type='application/json', accept=accept, response_type=models.TaskAgentPool, binary=False)
    def pools_get_agent_pools_by_ids(self, *, pool_ids: str, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentPool]]:
        "Pools_Get Agent Pools By Ids. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/pools', query={'poolIds': pool_ids, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentPool], binary=False)
    def pools_delete(self, *, pool_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Pools_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/distributedtask/pools/{poolId}', path_params={'poolId': pool_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def pools_get(self, *, pool_id: int, properties: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[models.TaskAgentPool]:
        "Pools_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/pools/{poolId}', path_params={'poolId': pool_id}, query={'properties': properties, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=models.TaskAgentPool, binary=False)
    def pools_update(self, *, pool_id: int, body: models.TaskAgentPool, accept: str = 'application/json') -> ApiResponse[models.TaskAgentPool]:
        "Pools_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/distributedtask/pools/{poolId}', path_params={'poolId': pool_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgentPool, binary=False)
    def agents_add(self, *, pool_id: int, body: models.TaskAgent, accept: str = 'application/json') -> ApiResponse[models.TaskAgent]:
        "Agents_Add. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/distributedtask/pools/{poolId}/agents', path_params={'poolId': pool_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgent, binary=False)
    def agents_list(self, *, pool_id: int, agent_name: str | None = None, include_capabilities: bool | None = None, include_assigned_request: bool | None = None, include_last_completed_request: bool | None = None, property_filters: str | None = None, demands: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgent]]:
        "Agents_List. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/pools/{poolId}/agents', path_params={'poolId': pool_id}, query={'agentName': agent_name, 'includeCapabilities': include_capabilities, 'includeAssignedRequest': include_assigned_request, 'includeLastCompletedRequest': include_last_completed_request, 'propertyFilters': property_filters, 'demands': demands}, content_type=None, accept=accept, response_type=list[models.TaskAgent], binary=False)
    def agents_delete(self, *, pool_id: int, agent_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Agents_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/distributedtask/pools/{poolId}/agents/{agentId}', path_params={'poolId': pool_id, 'agentId': agent_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def agents_get(self, *, pool_id: int, agent_id: int, include_capabilities: bool | None = None, include_assigned_request: bool | None = None, include_last_completed_request: bool | None = None, property_filters: str | None = None, accept: str = 'application/json') -> ApiResponse[models.TaskAgent]:
        "Agents_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/pools/{poolId}/agents/{agentId}', path_params={'poolId': pool_id, 'agentId': agent_id}, query={'includeCapabilities': include_capabilities, 'includeAssignedRequest': include_assigned_request, 'includeLastCompletedRequest': include_last_completed_request, 'propertyFilters': property_filters}, content_type=None, accept=accept, response_type=models.TaskAgent, binary=False)
    def agents_replace_agent(self, *, pool_id: int, agent_id: int, body: models.TaskAgent, accept: str = 'application/json') -> ApiResponse[models.TaskAgent]:
        "Agents_Replace Agent. Use accept='application/json'."
        return self._transport.request('PUT', '/_apis/distributedtask/pools/{poolId}/agents/{agentId}', path_params={'poolId': pool_id, 'agentId': agent_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgent, binary=False)
    def agents_update(self, *, pool_id: int, agent_id: int, body: models.TaskAgent, accept: str = 'application/json') -> ApiResponse[models.TaskAgent]:
        "Agents_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/distributedtask/pools/{poolId}/agents/{agentId}', path_params={'poolId': pool_id, 'agentId': agent_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgent, binary=False)
    def variablegroups_add(self, *, body: models.VariableGroupParameters, accept: str = 'application/json') -> ApiResponse[models.VariableGroup]:
        "Variablegroups_Add. Use accept='application/json'."
        return self._transport.request('POST', '/_apis/distributedtask/variablegroups', body=body, content_type='application/json', accept=accept, response_type=models.VariableGroup, binary=False)
    def variablegroups_share_variable_group(self, *, variable_group_id: int, body: list[models.VariableGroupProjectReference], accept: str = 'application/json') -> ApiResponse[Any]:
        "Variablegroups_Share Variable Group. Use accept='application/json'."
        return self._transport.request('PATCH', '/_apis/distributedtask/variablegroups', query={'variableGroupId': variable_group_id}, body=body, content_type='application/json', accept=accept, response_type=Any, binary=False)
    def variablegroups_delete(self, *, group_id: int, project_ids: str, accept: str = 'application/json') -> ApiResponse[Any]:
        "Variablegroups_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/_apis/distributedtask/variablegroups/{groupId}', path_params={'groupId': group_id}, query={'projectIds': project_ids}, content_type=None, accept=accept, response_type=Any, binary=False)
    def variablegroups_update(self, *, group_id: int, body: models.VariableGroupParameters, accept: str = 'application/json') -> ApiResponse[models.VariableGroup]:
        "Variablegroups_Update. Use accept='application/json'."
        return self._transport.request('PUT', '/_apis/distributedtask/variablegroups/{groupId}', path_params={'groupId': group_id}, body=body, content_type='application/json', accept=accept, response_type=models.VariableGroup, binary=False)
    def yamlschema_get(self, *, validate_task_names: bool | None = None, accept: str = 'application/json') -> ApiResponse[dict[str, Any]]:
        "Yamlschema_Get. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/yamlschema', query={'validateTaskNames': validate_task_names}, content_type=None, accept=accept, response_type=dict[str, Any], binary=False)
    def deploymentgroups_add(self, *, project: str, body: models.DeploymentGroupCreateParameter, accept: str = 'application/json') -> ApiResponse[models.DeploymentGroup]:
        "Deploymentgroups_Add. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/distributedtask/deploymentgroups', path_params={'project': project}, body=body, content_type='application/json', accept=accept, response_type=models.DeploymentGroup, binary=False)
    def deploymentgroups_list(self, *, project: str, name: str | None = None, action_filter: str | None = None, expand: str | None = None, continuation_token: str | None = None, top: int | None = None, ids: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.DeploymentGroup]]:
        "Deploymentgroups_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/deploymentgroups', path_params={'project': project}, query={'name': name, 'actionFilter': action_filter, '$expand': expand, 'continuationToken': continuation_token, '$top': top, 'ids': ids}, content_type=None, accept=accept, response_type=list[models.DeploymentGroup], binary=False)
    def deploymentgroups_delete(self, *, project: str, deployment_group_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Deploymentgroups_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}', path_params={'project': project, 'deploymentGroupId': deployment_group_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def deploymentgroups_get(self, *, project: str, deployment_group_id: int, action_filter: str | None = None, expand: str | None = None, accept: str = 'application/json') -> ApiResponse[models.DeploymentGroup]:
        "Deploymentgroups_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}', path_params={'project': project, 'deploymentGroupId': deployment_group_id}, query={'actionFilter': action_filter, '$expand': expand}, content_type=None, accept=accept, response_type=models.DeploymentGroup, binary=False)
    def deploymentgroups_update(self, *, project: str, deployment_group_id: int, body: models.DeploymentGroupUpdateParameter, accept: str = 'application/json') -> ApiResponse[models.DeploymentGroup]:
        "Deploymentgroups_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}', path_params={'project': project, 'deploymentGroupId': deployment_group_id}, body=body, content_type='application/json', accept=accept, response_type=models.DeploymentGroup, binary=False)
    def targets_list(self, *, project: str, deployment_group_id: int, tags: str | None = None, name: str | None = None, partial_name_match: bool | None = None, expand: str | None = None, agent_status: str | None = None, agent_job_result: str | None = None, continuation_token: str | None = None, top: int | None = None, enabled: bool | None = None, property_filters: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.DeploymentMachine]]:
        "Targets_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}/targets', path_params={'project': project, 'deploymentGroupId': deployment_group_id}, query={'tags': tags, 'name': name, 'partialNameMatch': partial_name_match, '$expand': expand, 'agentStatus': agent_status, 'agentJobResult': agent_job_result, 'continuationToken': continuation_token, '$top': top, 'enabled': enabled, 'propertyFilters': property_filters}, content_type=None, accept=accept, response_type=list[models.DeploymentMachine], binary=False)
    def targets_update(self, *, project: str, deployment_group_id: int, body: list[models.DeploymentTargetUpdateParameter], accept: str = 'application/json') -> ApiResponse[list[models.DeploymentMachine]]:
        "Targets_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}/targets', path_params={'project': project, 'deploymentGroupId': deployment_group_id}, body=body, content_type='application/json', accept=accept, response_type=list[models.DeploymentMachine], binary=False)
    def targets_delete(self, *, project: str, deployment_group_id: int, target_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Targets_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}/targets/{targetId}', path_params={'project': project, 'deploymentGroupId': deployment_group_id, 'targetId': target_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def targets_get(self, *, project: str, deployment_group_id: int, target_id: int, expand: str | None = None, accept: str = 'application/json') -> ApiResponse[models.DeploymentMachine]:
        "Targets_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/deploymentgroups/{deploymentGroupId}/targets/{targetId}', path_params={'project': project, 'deploymentGroupId': deployment_group_id, 'targetId': target_id}, query={'$expand': expand}, content_type=None, accept=accept, response_type=models.DeploymentMachine, binary=False)
    def environments_add(self, *, project: str, body: models.EnvironmentCreateParameter, accept: str = 'application/json') -> ApiResponse[models.EnvironmentInstance]:
        "Environments_Add. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/distributedtask/environments', path_params={'project': project}, body=body, content_type='application/json', accept=accept, response_type=models.EnvironmentInstance, binary=False)
    def environments_list(self, *, project: str, name: str | None = None, continuation_token: str | None = None, top: int | None = None, accept: str = 'application/json') -> ApiResponse[list[models.EnvironmentInstance]]:
        "Environments_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/environments', path_params={'project': project}, query={'name': name, 'continuationToken': continuation_token, '$top': top}, content_type=None, accept=accept, response_type=list[models.EnvironmentInstance], binary=False)
    def environments_delete(self, *, project: str, environment_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Environments_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/environments/{environmentId}', path_params={'project': project, 'environmentId': environment_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def environments_get(self, *, project: str, environment_id: int, expands: str | None = None, accept: str = 'application/json') -> ApiResponse[models.EnvironmentInstance]:
        "Environments_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/environments/{environmentId}', path_params={'project': project, 'environmentId': environment_id}, query={'expands': expands}, content_type=None, accept=accept, response_type=models.EnvironmentInstance, binary=False)
    def environments_update(self, *, project: str, environment_id: int, body: models.EnvironmentUpdateParameter, accept: str = 'application/json') -> ApiResponse[models.EnvironmentInstance]:
        "Environments_Update. Use accept='application/json'."
        return self._transport.request('PATCH', '/{project}/_apis/distributedtask/environments/{environmentId}', path_params={'project': project, 'environmentId': environment_id}, body=body, content_type='application/json', accept=accept, response_type=models.EnvironmentInstance, binary=False)
    def environmentdeployment_records_list(self, *, project: str, environment_id: int, continuation_token: str | None = None, top: int | None = None, accept: str = 'application/json') -> ApiResponse[list[models.EnvironmentDeploymentExecutionRecord]]:
        "Environmentdeployment Records_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/environments/{environmentId}/environmentdeploymentrecords', path_params={'project': project, 'environmentId': environment_id}, query={'continuationToken': continuation_token, 'top': top}, content_type=None, accept=accept, response_type=list[models.EnvironmentDeploymentExecutionRecord], binary=False)
    def kubernetes_add(self, *, project: str, environment_id: int, body: models.KubernetesResourceCreateParameters, accept: str = 'application/json') -> ApiResponse[models.KubernetesResource]:
        "Kubernetes_Add. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/distributedtask/environments/{environmentId}/providers/kubernetes', path_params={'project': project, 'environmentId': environment_id}, body=body, content_type='application/json', accept=accept, response_type=models.KubernetesResource, binary=False)
    def kubernetes_delete(self, *, project: str, environment_id: int, resource_id: int, accept: str = 'application/json') -> ApiResponse[Any]:
        "Kubernetes_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/environments/{environmentId}/providers/kubernetes/{resourceId}', path_params={'project': project, 'environmentId': environment_id, 'resourceId': resource_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def kubernetes_get(self, *, project: str, environment_id: int, resource_id: int, accept: str = 'application/json') -> ApiResponse[models.KubernetesResource]:
        "Kubernetes_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/environments/{environmentId}/providers/kubernetes/{resourceId}', path_params={'project': project, 'environmentId': environment_id, 'resourceId': resource_id}, content_type=None, accept=accept, response_type=models.KubernetesResource, binary=False)
    def queues_add(self, *, project: str | None = None, authorize_pipelines: bool | None = None, body: models.TaskAgentQueue, accept: str = 'application/json') -> ApiResponse[models.TaskAgentQueue]:
        "Queues_Add. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/distributedtask/queues', path_params={'project': project}, query={'authorizePipelines': authorize_pipelines}, body=body, content_type='application/json', accept=accept, response_type=models.TaskAgentQueue, binary=False)
    def queues_get_agent_queues_for_pools(self, *, pool_ids: str, project: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentQueue]]:
        "Queues_Get Agent Queues For Pools. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/queues', path_params={'project': project}, query={'poolIds': pool_ids, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentQueue], binary=False)
    def queues_delete(self, *, queue_id: int, project: str | None = None, accept: str = 'application/json') -> ApiResponse[Any]:
        "Queues_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/queues/{queueId}', path_params={'project': project, 'queueId': queue_id}, content_type=None, accept=accept, response_type=Any, binary=False)
    def queues_get(self, *, queue_id: int, project: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[models.TaskAgentQueue]:
        "Queues_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/queues/{queueId}', path_params={'project': project, 'queueId': queue_id}, query={'actionFilter': action_filter}, content_type=None, accept=accept, response_type=models.TaskAgentQueue, binary=False)
    def taskgroups_add(self, *, project: str, body: models.TaskGroupCreateParameter, accept: str = 'application/json') -> ApiResponse[models.TaskGroup]:
        "Taskgroups_Add. Use accept='application/json'."
        return self._transport.request('POST', '/{project}/_apis/distributedtask/taskgroups', path_params={'project': project}, body=body, content_type='application/json', accept=accept, response_type=models.TaskGroup, binary=False)
    def taskgroups_delete(self, *, project: str, task_group_id: str | UUID, comment: str | None = None, accept: str = 'application/json') -> ApiResponse[Any]:
        "Taskgroups_Delete. Use accept='application/json'."
        return self._transport.request('DELETE', '/{project}/_apis/distributedtask/taskgroups/{taskGroupId}', path_params={'project': project, 'taskGroupId': task_group_id}, query={'comment': comment}, content_type=None, accept=accept, response_type=Any, binary=False)
    def taskgroups_list(self, *, project: str, task_group_id: str | UUID | None = None, expanded: bool | None = None, task_id_filter: str | UUID | None = None, deleted: bool | None = None, top: int | None = None, continuation_token: str | None = None, query_order: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskGroup]]:
        "Taskgroups_List. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/taskgroups/{taskGroupId}', path_params={'project': project, 'taskGroupId': task_group_id}, query={'expanded': expanded, 'taskIdFilter': task_id_filter, 'deleted': deleted, '$top': top, 'continuationToken': continuation_token, 'queryOrder': query_order}, content_type=None, accept=accept, response_type=list[models.TaskGroup], binary=False)
    def taskgroups_update(self, *, project: str, task_group_id: str | UUID | None = None, body: models.TaskGroupUpdateParameter, accept: str = 'application/json') -> ApiResponse[models.TaskGroup]:
        "Taskgroups_Update. Use accept='application/json'."
        return self._transport.request('PUT', '/{project}/_apis/distributedtask/taskgroups/{taskGroupId}', path_params={'project': project, 'taskGroupId': task_group_id}, body=body, content_type='application/json', accept=accept, response_type=models.TaskGroup, binary=False)
    def variablegroups_get_variable_groups_by_id(self, *, project: str, group_ids: str, accept: str = 'application/json') -> ApiResponse[list[models.VariableGroup]]:
        "Variablegroups_Get Variable Groups By Id. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/variablegroups', path_params={'project': project}, query={'groupIds': group_ids}, content_type=None, accept=accept, response_type=list[models.VariableGroup], binary=False)
    def variablegroups_get(self, *, project: str, group_id: int, accept: str = 'application/json') -> ApiResponse[models.VariableGroup]:
        "Variablegroups_Get. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/variablegroups/{groupId}', path_params={'project': project, 'groupId': group_id}, content_type=None, accept=accept, response_type=models.VariableGroup, binary=False)
    def pools_get_agent_pools(self, *, pool_name: str | None = None, properties: str | None = None, pool_type: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentPool]]:
        "Pools_Get Agent Pools. Use accept='application/json'."
        return self._transport.request('GET', '/_apis/distributedtask/pools', query={'poolName': pool_name, 'properties': properties, 'poolType': pool_type, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentPool], binary=False)
    def queues_get_agent_queues_by_names(self, *, queue_names: str, project: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentQueue]]:
        "Queues_Get Agent Queues By Names. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/queues', path_params={'project': project}, query={'queueNames': queue_names, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentQueue], binary=False)
    def queues_get_agent_queues_by_ids(self, *, queue_ids: str, project: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentQueue]]:
        "Queues_Get Agent Queues By Ids. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/queues', path_params={'project': project}, query={'queueIds': queue_ids, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentQueue], binary=False)
    def queues_get_agent_queues(self, *, project: str | None = None, queue_name: str | None = None, action_filter: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.TaskAgentQueue]]:
        "Queues_Get Agent Queues. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/queues', path_params={'project': project}, query={'queueName': queue_name, 'actionFilter': action_filter}, content_type=None, accept=accept, response_type=list[models.TaskAgentQueue], binary=False)
    def variablegroups_get_variable_groups(self, *, project: str, group_name: str | None = None, action_filter: str | None = None, top: int | None = None, continuation_token: int | None = None, query_order: str | None = None, accept: str = 'application/json') -> ApiResponse[list[models.VariableGroup]]:
        "Variablegroups_Get Variable Groups. Use accept='application/json'."
        return self._transport.request('GET', '/{project}/_apis/distributedtask/variablegroups', path_params={'project': project}, query={'groupName': group_name, 'actionFilter': action_filter, '$top': top, 'continuationToken': continuation_token, 'queryOrder': query_order}, content_type=None, accept=accept, response_type=list[models.VariableGroup], binary=False)
