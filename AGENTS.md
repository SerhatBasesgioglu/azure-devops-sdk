# Repository instructions

## Scope and working style

- Treat suggestions and review findings as requests for analysis only. Make code or documentation changes only when the user explicitly authorizes a bounded change; a documentation request is not blanket coding autonomy.
- Keep changes within the requested scope. Do not restructure the repository or lock in future structure without a specific request.
- Never read `.env`, print credentials, log PATs, or make live Azure DevOps mutation requests without explicit permission. Prefer offline tests with HTTPX `MockTransport`.

## Project facts

- This installable project is the `azure-devops-sdk` distribution, imported as `azure_devops_sdk`; it requires Python >=3.11 and uses synchronous HTTPX with Pydantic v2.
- The six service packages are `git`, `pipelines`, `core`, `build`, `policy`, and `task_agent`. They expose 111, 10, 18, 91, 12, and 56 operations respectively (298 total), sourced from the local Azure DevOps 7.0 REST specs checkout. `task_agent` represents the selected `taskAgent.json` spec, not all Distributed Task APIs.
- `client.py` and `_transport.py` are shared handwritten infrastructure. Per-service `client.py`, `models.py`, and `__init__.py` files, plus `_spec_manifest.json`, are generator-owned; do not hand-edit generated output. Change `scripts/generate_models.py` or its schema overlays, then regenerate.
- The default specification root is the sibling `../vsts-rest-api-specs/specification`; override it with `--spec-root PATH`. Run `uv run python scripts/generate_models.py` to regenerate.
- `backup/prototype/` is a historical snapshot, excluded from installed runtime and tests. Do not revive it as current implementation.
- The SDK accepts the HTTPS collection root from its caller; it does not load environment files, provide a demo console script, or make requests on import.
- Request logging uses `azure_devops_sdk.transport` at DEBUG with bounded structured metadata only. Preserve omission of URLs, path values, query/body/header contents, credentials, and exception text; only generated wrappers supply trusted route templates. The package's `NullHandler` must not configure application logging.
- Keep this repository a generic SDK, not a home for CLI/MCP/exporter or job-specific business logic; those are planned for a separate tooling repository, which has not yet been created. No consumers or cleanup jobs from that plan are implemented. Automatic pagination is not present; headers/continuation metadata are preserved. SDK-wide live on-prem compatibility is unverified. Tracing and metrics are paused and not a current priority.

## Change and validation guidance

- Preserve generated public aliases and unknown/extra fields. Distinguish absent fields from explicitly supplied `null`; retain correct JSON Patch array semantics and `application/json-patch+json`, raw byte request/response behavior, and response headers/pagination data.
- Use source-fixture tests to check actual spec examples and wire behavior; do not rely on operation counts alone. Fixture tests use `MockTransport` and run offline. Some require the sibling `vsts-rest-api-specs` checkout; without it, those tests skip or generation cannot run.
- Relevant checks: `uv run pytest`, `uv build`, and deterministic regeneration with `uv run python scripts/generate_models.py` (using `--spec-root PATH` when needed). Verify regeneration does not introduce unexpected diffs.
- Logging instrumentation belongs in handwritten `src/azure_devops_sdk/_transport.py` and `scripts/generate_models.py`; regenerate wrappers rather than editing generated clients. Keep request behavior independent of logging handler failures.
- For future tooling, start with a thin read-only inventory CLI and establish its pagination needs; do not implement it in this SDK repo. Any eventual stale-branch cleanup must start with discovery/reporting and dry-run, protect branches, and recheck before deletion. These roadmap notes are not authorization to implement or make live mutations.
