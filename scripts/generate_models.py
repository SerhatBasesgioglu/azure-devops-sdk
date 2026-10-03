"""Generate complete Git/Pipelines Pydantic models and typed API wrappers."""

from __future__ import annotations

import argparse
import hashlib
import json
import keyword
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = REPOSITORY_ROOT / "src" / "azure_devops_sdk"
@dataclass(frozen=True)
class ServiceSpec:
    source: str
    class_name: str


SPECS = {
    "git": ServiceSpec("git/7.0/git.json", "GitApi"),
    "pipelines": ServiceSpec("pipelines/7.0/pipelines.json", "PipelinesApi"),
    "core": ServiceSpec("core/7.0/core.json", "CoreApi"),
    "build": ServiceSpec("build/7.0/build.json", "BuildApi"),
    "policy": ServiceSpec("policy/7.0/policy.json", "PolicyApi"),
    "task_agent": ServiceSpec("distributedTask/7.0/taskAgent.json", "TaskAgentApi"),
}
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def _refs(value: Any):
    if isinstance(value, dict):
        ref = value.get("$ref")
        if isinstance(ref, str):
            yield ref
        for nested in value.values():
            yield from _refs(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _refs(nested)


def _resolve(spec: dict[str, Any], value: Any) -> Any:
    while isinstance(value, dict) and "$ref" in value:
        ref = value["$ref"]
        prefix = "#/parameters/"
        name = ref.removeprefix(prefix)
        if not ref.startswith(prefix) or not name or "/" in name or name not in spec.get("parameters", {}):
            raise ValueError(f"Unsupported or unresolved parameter reference: {ref}")
        value = spec["parameters"][name]
    return value


def _snake(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    if not value:
        raise ValueError(f"Cannot create Python identifier from {value!r}")
    if value[0].isdigit() or keyword.iskeyword(value):
        value += "_"
    return value


def _schema_type(schema: dict[str, Any] | None, module: str) -> str:
    if not schema:
        return "Any"
    ref = schema.get("$ref")
    if ref:
        if not ref.startswith("#/definitions/"):
            raise ValueError(f"Unsupported schema reference: {ref}")
        return f"models.{ref.removeprefix('#/definitions/')}"
    if "allOf" in schema:
        refs = [part.get("$ref") for part in schema["allOf"] if isinstance(part, dict)]
        if len(refs) == 1 and refs[0] and refs[0].startswith("#/definitions/"):
            return f"models.{refs[0].removeprefix('#/definitions/')}"
        raise ValueError(f"Unsupported inline allOf response/body schema in {module}: {schema}")
    typ = schema.get("type")
    if typ == "array":
        return f"list[{_schema_type(schema.get('items'), module)}]"
    return {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "object": "dict[str, Any]"}.get(typ, "Any")


def _operations(spec: dict[str, Any]):
    found = []
    for group in ("paths", "x-ms-paths"):
        for route, path_item in spec.get(group, {}).items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() in HTTP_METHODS and isinstance(operation, dict):
                    found.append((group, route, method.lower(), path_item, operation))
    return found


def _response_type(operation: dict[str, Any], module: str) -> tuple[str, bool, str]:
    successes = [(code, response) for code, response in operation.get("responses", {}).items() if code == "default" or (code.isdigit() and 200 <= int(code) < 300)]
    if not successes:
        raise ValueError(f"Operation {operation.get('operationId')} has no success response")
    candidates = [(code, response) for code, response in successes if response.get("schema")]
    all_produces = [mime for _, response in successes for mime in response.get("produces", operation.get("produces", ["application/json"]))]
    all_binary = {mime for mime in all_produces if mime in {"application/octet-stream", "application/zip"}}
    all_json = [mime for mime in all_produces if "json" in mime.lower() or "+json" in mime.lower()]
    if not candidates:
        if all_binary and not all_json:
            return "bytes", True, sorted(all_binary)[0]
        return "Any", False, "application/json"
    code, response = candidates[0]
    schema = response["schema"]
    produces = list(response.get("produces", operation.get("produces", ["application/json"])))
    binary_mimes = {"application/octet-stream", "application/zip"}
    binary_types = {mime for mime in produces if mime in binary_mimes}
    json_types = [mime for mime in produces if "json" in mime.lower() or "+json" in mime.lower()]
    schema_is_binary = schema.get("type") == "file" or schema.get("format") in {"binary", "byte", "Stream"}
    if schema_is_binary or (binary_types and not json_types):
        return "bytes", True, next(iter(produces), "application/octet-stream")
    response_type = _schema_type(schema, module)
    if binary_types:
        response_type = f"{response_type} | bytes"
    # For a representation with JSON and binary alternatives, prefer its typed
    # schema by default. The transport still returns bytes for a binary media
    # type selected explicitly or returned by the server.
    accept = "application/json" if json_types else next(iter(produces), "application/json")
    return response_type, False, accept


def _make_api(module: str, spec: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    methods = []
    manifest_ops = []
    used_names: set[str] = set()
    for group, route, verb, path_item, operation in _operations(spec):
        operation_id = operation.get("operationId")
        if not operation_id:
            raise ValueError(f"Operation without operationId: {verb.upper()} {route}")
        name = _snake(operation_id)
        if name in used_names:
            raise ValueError(f"API method name collision in {module}: {name} ({operation_id})")
        used_names.add(name)
        params_by_key: dict[tuple[str, str], dict[str, Any]] = {}
        for raw in path_item.get("parameters", []) + operation.get("parameters", []):
            param = _resolve(spec, raw)
            key = (param.get("in", ""), param.get("name", ""))
            params_by_key[key] = param
        params = [p for p in params_by_key.values() if p.get("in") != "body" and p.get("name") not in {"organization", "api-version", "apiVersion"}]
        parameters = []
        signature = []
        path_names = [name for name in re.findall(r"\{([^}]+)\}", route.split("?", 1)[0]) if name != "organization"]
        path_wire_to_arg = {}
        for p in params:
            wire = p["name"]
            arg = _snake(wire)
            if arg in {x[0] for x in parameters}:
                raise ValueError(f"Parameter name collision in {operation_id}: {wire}")
            schema = p.get("schema", p)
            typ = _schema_type(schema, module)
            if schema.get("format") == "uuid":
                typ = "str | UUID"
            # Azure specs use x-ms-required for optional path segments. Honor it
            # for every path parameter, rather than special-casing project.
            required = p.get("required", p.get("in") == "path")
            if p.get("in") == "path" and (p.get("x-ms-required") is False or p.get("required") is False):
                required = False
            annotation = typ if required else f"{typ} | None"
            parameters.append((arg, wire, p.get("in"), required, annotation))
            signature.append(f"{arg}: {annotation}" + ("" if required else " = None"))
            if p.get("in") == "path":
                path_wire_to_arg[wire] = arg
        body = None
        for p in params_by_key.values():
            if p.get("in") == "body":
                if body is not None:
                    raise ValueError(f"Multiple bodies in {operation_id}")
                body = p
        if body:
            body_schema = body.get("schema") or {}
            body_type = "bytes" if body_schema.get("format") in {"Stream", "binary", "byte"} else _schema_type(body_schema, module)
            if body.get("required"):
                signature.append(f"body: {body_type}")
            else:
                signature.append(f"body: {body_type} | None = None")
        successes = [(code, response) for code, response in operation.get("responses", {}).items() if code == "default" or (code.isdigit() and 200 <= int(code) < 300)]
        declared_path_params = set(path_wire_to_arg)
        missing_path_params = {name for name in path_names if name.casefold() not in {key.casefold() for key in declared_path_params}}
        if missing_path_params:
            raise ValueError(f"Undeclared path parameter(s) in {operation_id}: {sorted(missing_path_params)}")
        route_query_names = set(re.findall(r"[?&]([^=&{}]+)=?\{?([^}&]*)\}?", route.split("?", 1)[1] if "?" in route else ""))
        declared_query = {p.get("name") for p in params_by_key.values() if p.get("in") == "query"}
        missing_query = {name for name, _ in route_query_names} - declared_query
        if missing_query:
            raise ValueError(f"Undeclared x-ms-paths query parameter(s) in {operation_id}: {sorted(missing_query)}")
        response_type, binary, accept = _response_type(operation, module)
        if binary and len([1 for _, r in operation.get("responses", {}).items() if r.get("schema")]) > 1:
            # Alternate success representations are selectable through accept.
            accept_default = accept
        else:
            accept_default = accept
        route_path = route.split("?", 1)[0].removeprefix("/{organization}")
        if not route_path.startswith("/"):
            raise ValueError(f"Malformed route {route}")
        path_expr = repr(route_path)
        route_path_args = {
            placeholder: next(arg for wire, arg in path_wire_to_arg.items() if wire.casefold() == placeholder.casefold())
            for placeholder in path_names
        }
        call_args = [f"path_params={{{', '.join(repr(k) + ': ' + v for k, v in route_path_args.items())}}}" ] if route_path_args else []
        query_params = [(arg, wire) for arg, wire, loc, _, _ in parameters if loc == "query"]
        if query_params:
            call_args.append(f"query={{{', '.join(repr(wire) + ': ' + arg for arg, wire in query_params)}}}")
            formats = {}
            for raw in path_item.get("parameters", []) + operation.get("parameters", []):
                p = _resolve(spec, raw)
                if p.get("in") == "query" and p.get("name") in {wire for _, wire in query_params} and p.get("type") == "array":
                    formats[p["name"]] = p.get("collectionFormat", "csv")
            if formats:
                call_args.append(f"query_formats={formats!r}")
        if body:
            call_args.append("body=body")
        consumes = operation.get("consumes", spec.get("consumes", []))
        content_type = consumes[0] if body and consumes else "application/json" if body else None
        call_args += [f"content_type={content_type!r}", f"accept=accept", f"response_type={response_type}", f"binary={binary!r}"]
        doc = f"{operation_id}. Use accept={accept_default!r}" + (" for the default binary representation; pass another accepted media type for alternate representations." if binary else ".")
        lines = [f"    def {name}(self, *, {', '.join(signature)}{', ' if signature else ''}accept: str = {accept_default!r}) -> ApiResponse[{response_type}]:", f"        {json.dumps(doc)}", f"        return self._transport.request({verb.upper()!r}, {path_expr}, {', '.join(call_args)})"]
        methods.extend(lines)
        manifest_ops.append({
            "operationId": operation_id, "source_id": operation.get("x-ms-vss-method", operation_id), "method": verb.upper(), "path": route_path,
            "source_path": route, "path_group": group, "python_method": name,
            "parameters": [{"name": wire, "python_name": arg, "in": loc, "required": required, "type": annotation} for arg, wire, loc, required, annotation in parameters],
            "body": ({"required": bool(body.get("required")), "type": body_type, "content_type": content_type} if body else None),
            "success_codes": [code for code, _ in successes], "response_type": response_type,
            "binary": binary, "accept": accept_default,
            "produces": sorted({m for _, r in successes for m in r.get("produces", operation.get("produces", []))}),
        })
    source = "\n".join([
        '"""Spec-generated Git/Pipelines REST methods."""', "from __future__ import annotations", "from typing import Any", "from uuid import UUID", "from azure_devops_sdk._transport import ApiResponse, AdoTransport", "from . import models", "",
        "class " + SPECS[module].class_name + ":", "    def __init__(self, transport: AdoTransport) -> None:", "        self._transport = transport", "", *methods, "",
    ])
    return source, {"operation_count": len(manifest_ops), "operations": manifest_ops}


def generate(spec_root: Path) -> None:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {"generator": "scripts/generate_models.py", "modules": {}}
    with tempfile.TemporaryDirectory(prefix="ado-models-") as temp_dir:
        staging = Path(temp_dir)
        for module, service in SPECS.items():
            relative_path = service.source
            spec_file = spec_root / relative_path
            raw = spec_file.read_bytes()
            spec = json.loads(raw.decode("utf-8-sig"))
            defs = spec.get("definitions", {})
            for ref in _refs(defs):
                if not ref.startswith("#/definitions/") or ref.removeprefix("#/definitions/") not in defs:
                    raise ValueError(f"Unresolved/unsupported model reference in {module}: {ref}")
            definitions = dict(defs)
            if module in {"git", "core", "build"}:
                # Wire examples use JSON Patch as an array. The source describes it
                # as an object with an array allOf, which generates an invalid body.
                assert "JsonPatchDocument" in defs and "JsonPatchOperation" in defs
                definitions["JsonPatchDocument"] = {"type": "array", "items": {"$ref": "#/definitions/JsonPatchOperation"}}
                # The value is a JToken/primitive: `{}` means arbitrary JSON,
                # including explicit null, strings, numbers, arrays and objects.
                patch_operation = definitions["JsonPatchOperation"]
                assert "value" in patch_operation.get("properties", {})
                patch_operation["properties"]["value"] = {
                    "description": "The value for the operation. This is either a primitive or a JToken.",
                }
            if module == "core":
                # Project-property examples contain scalar values (e.g. Agile),
                # not only JSON objects as the source schema claims.
                assert "ProjectProperty" in defs and "value" in defs["ProjectProperty"].get("properties", {})
                definitions["ProjectProperty"]["properties"]["value"] = {
                    "description": "The arbitrary JSON property value returned by the project properties APIs."
                }
            if module == "task_agent":
                # Deployment target examples contain string demands alongside
                # structured Demand records; keep the record alternative intact.
                assert "TaskAgentJobRequest" in defs
                demands = definitions["TaskAgentJobRequest"]["properties"]["demands"]
                assert demands.get("items", {}).get("$ref") == "#/definitions/Demand"
                demands["items"] = {"anyOf": [{"$ref": "#/definitions/Demand"}, {"type": "string"}]}
                # Public-key wire examples are base64 strings. Do not interpret
                # them as UTF-8 byte arrays: consumers need the exact RSA values.
                assert "TaskAgentPublicKey" in defs
                for member in ("exponent", "modulus"):
                    declared = definitions["TaskAgentPublicKey"]["properties"][member]
                    assert declared.get("type") == "array" and declared.get("items", {}).get("format") == "byte"
                    definitions["TaskAgentPublicKey"]["properties"][member] = {"type": "string"}
            if module == "policy":
                # JObject's CLR item/type description is metadata, not wire
                # properties. Settings and evaluation context are JSON objects.
                assert "JObject" in defs and "settings" in defs["PolicyConfiguration"]["properties"]
                definitions["JObject"] = {"type": "object", "additionalProperties": True}
                definitions["PolicyConfiguration"]["properties"]["settings"] = {
                    "type": "object", "additionalProperties": True,
                    "description": "The policy configuration settings."
                }
                assert "context" in defs["PolicyEvaluationRecord"]["properties"]
                definitions["PolicyEvaluationRecord"]["properties"]["context"] = {
                    "type": "object", "additionalProperties": True,
                    "description": "Internal context data of this policy evaluation."
                }
            if module == "git":
                # Keep the existing service-local settings correction.
                policy = definitions.get("PolicyConfiguration")
                if policy and isinstance(policy.get("properties", {}).get("settings"), dict):
                    policy["properties"]["settings"] = {"type": "object", "additionalProperties": True}
                # Change.item is a T-format GitItem value; constrain the shape to the reviewed GitItem model.
                change = definitions.get("Change")
                if change and isinstance(change.get("properties", {}).get("item"), dict):
                    change["properties"]["item"] = {"$ref": "#/definitions/GitItem"}
            bundle = {"$schema": "http://json-schema.org/draft-07/schema#", "definitions": definitions}
            input_file = staging / f"{module}.schema.json"
            output_file = staging / f"{module}.py"
            input_file.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            subprocess.run([
                sys.executable, "-m", "datamodel_code_generator", "--input", str(input_file),
                "--input-file-type", "jsonschema", "--output", str(output_file),
                "--output-model-type", "pydantic_v2.BaseModel", "--target-python-version", "3.11",
                "--snake-case-field", "--use-union-operator", "--disable-timestamp", "--strict-refs",
                "--extra-fields", "allow", "--allow-population-by-field-name",
                # date-time wire values may legitimately omit an offset; plain
                # datetime accepts those while retaining offsets when supplied.
                "--output-datetime-class", "datetime",
            ], check=True, cwd=REPOSITORY_ROOT)
            generated = output_file.read_text(encoding="utf-8")
            # Omit absent `from` on JSON Patch operations without omitting an
            # explicitly supplied null `value`. Apply consistently in all
            # service schemas that define the patch type.
            generated = generated.replace(
                "    from_: str | None = Field(\n        None,\n        alias='from',",
                "    from_: str | None = Field(\n        None,\n        alias='from',\n        exclude_if=lambda value: value is None,",
            )
            output_file.write_text(generated, encoding="utf-8")
            api_source, api_manifest = _make_api(module, spec)
            service_dir = PACKAGE_DIR / module
            service_dir.mkdir(parents=True, exist_ok=True)
            (service_dir / "models.py").write_bytes(output_file.read_bytes())
            api_name = "client.py"
            (service_dir / api_name).write_text(api_source, encoding="utf-8")
            class_name = service.class_name
            (service_dir / "__init__.py").write_text(
                f'"""Generated {module.title()} service API."""\n\nfrom .client import {class_name}\n\n__all__ = [{class_name!r}]\n',
                encoding="utf-8",
            )
            manifest["modules"][module] = {
                "source": relative_path, "source_sha256": hashlib.sha256(raw).hexdigest(),
                "definition_count": len(defs), "api_module": api_name, **api_manifest,
            }
        (PACKAGE_DIR / "_spec_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-root", type=Path, default=REPOSITORY_ROOT.parent / "vsts-rest-api-specs" / "specification", help="Root directory containing the Azure DevOps REST specification folders.")
    args = parser.parse_args()
    generate(args.spec_root.resolve())


if __name__ == "__main__":
    main()
