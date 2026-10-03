# azure-devops-sdk

An installable, synchronous Azure DevOps REST SDK with spec-generated clients
for Git, Pipelines, Core, Build, Policy, and a Task Agent subset of
Distributed Task. Together these clients expose 298 operations from the Azure
DevOps 7.0 REST specifications. Task Agent represents the selected
`taskAgent.json` spec (56 operations), not the entire Distributed Task API.

## Usage

```python
from azure_devops_sdk import AdoClient

with AdoClient("https://dev.azure.com/organization", "your-pat") as ado:
    response = ado.git.repositories_get_repository(repository_id="...")
    repository = response.data

    # Other services share the same transport and API-version configuration.
    project = ado.core.projects_get(project_id="...")
```

The shared transport enforces HTTPS by default. `AdoClient` accepts optional
`transport`, `timeout`, and `allow_insecure_http` keyword arguments for test
injection and deliberate configuration. It does not load environment files,
run a demo, or perform network calls on import. Service API classes and models
are available under `azure_devops_sdk.{git,pipelines,core,build,policy,task_agent}`
and each service's `.models` module. The former `generated.*` paths,
`azure_devops_sdk.runtime`, and the old handwritten `list_projects` /
`list_repositories` facade are breaking internal API changes.

## Regeneration

Install development dependencies with `uv sync --dev`, then run
`uv run python scripts/generate_models.py`. By default, the generator reads the
sibling `../vsts-rest-api-specs/specification` checkout; use `--spec-root PATH`
to select another specification root. It writes generated service modules and
the source/operation manifest at `src/azure_devops_sdk/_spec_manifest.json`.

The generator preserves complete source `operationId`-based snake-case method
names (for example, `Preview_Preview` becomes `preview_preview`). Methods are
keyword-only and return `ApiResponse[T]`; arrays are typed as `list[T]`,
binary-only responses as `bytes`, and schema-less responses as `Any`. Each
method has an `accept` argument when response media types can vary. Mixed
JSON/binary responses default to JSON and are annotated as a union of the
schema model and `bytes`; binary-only endpoints default to their binary media
type. The transport owns the organization and API version.

## Logging

The SDK emits one completion event per transport request on the
`azure_devops_sdk.transport` logger. Successful calls are logged at `DEBUG`
with `event="request.completed"`; failed calls use `event="request.failed"`
at the same level. The record provides `sdk_service`, `sdk_operation`,
`http_method`, `route_template`, `status_code`, `duration_ms`, `outcome`, and
`error_type` attributes. Direct transport calls may have no service, operation,
or route template. Error categories are bounded (`http_error`, `timeout`,
`connection_error`, `transport_error`, `invalid_json`, `validation_error`,
`request_error`, `unexpected_error`); HTTP and parsing failures remain the
application's responsibility. The package installs a `NullHandler` only; it
does not configure logging output or alter root logger settings. Configure
formatting/handlers in the consuming application, for example:

```python
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("azure_devops_sdk").setLevel(logging.DEBUG)
```

Events intentionally omit URLs, path values, query parameters, request/response
bodies and headers, credentials, and exception text/tracebacks. The route
template is emitted only by generated wrappers; manually invoked transport
requests leave it unset unless the caller explicitly supplies safe metadata.
Other HTTP libraries may log full URLs independently; configure their loggers
separately rather than enabling global DEBUG output.
The SDK supplies ordinary `LogRecord` attributes rather than prescribing a
JSON formatter or telemetry exporter.

Explicit schema overlays address known malformed source shapes:
`JsonPatchDocument` is an array of `JsonPatchOperation`; its `value` accepts
arbitrary JSON; `PolicyConfiguration.settings` is a JSON object with arbitrary
properties; and `Change.item` references `GitItem` rather than an opaque `T`
string. Generated models preserve unknown fields and wire-name aliases.

`backup/prototype/` is a historical, non-installed snapshot of the handwritten
prototype and its two model tests. It is not a runnable SDK and is not used by
the generator or package.

## Current status and direction

This repository remains the generic, typed Azure DevOps SDK: six generated
services and 298 operations. The latest reported offline test baseline is 378
tests; pagination is not automatic, although response headers (including
continuation information) are preserved. SDK-wide compatibility with a live
on-premises Azure DevOps Server deployment has not been validated. Logging is
implemented as privacy-conscious structured DEBUG events; tracing and metrics
are not implemented and are paused, not a current priority.

Planned consumers include a CLI, MCP server, analysis/Prometheus exporter, and
operational jobs such as stale-branch cleanup and nonstandard-pipeline support.
The chosen direction is to keep this SDK focused on generic API calls and
transport, and put those tools and their shared business logic in a separate
tooling repository. That repository does not exist yet, and none of those
consumers/jobs has been implemented here. For the first tooling increment,
prefer a thin read-only inventory CLI and establish which workflows need
pagination before adding it. Validate reads against the target deployment
before making broader compatibility claims. Cleanup automation, when pursued,
should discover and report candidates first, support dry-run, protect branches,
and recheck immediately before deletion; it is not authorized or implemented by
this roadmap.
