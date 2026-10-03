from uuid import UUID

import pytest
from pydantic import ValidationError

from azure_devops_sdk.models import AdoList, Project


def test_projects_response_parses() -> None:
    project_id = "11111111-1111-1111-1111-111111111111"

    projects = AdoList[Project].model_validate(
        {
            "count": 1,
            "value": [{"id": project_id, "name": "Example project"}],
        }
    )

    assert projects.count == len(projects.value)
    assert projects.value[0].name == "Example project"
    assert projects.value[0].id == UUID(project_id)


def test_project_requires_id() -> None:
    with pytest.raises(ValidationError) as exc_info:
        AdoList[Project].model_validate(
            {"count": 1, "value": [{"name": "Example project"}]}
        )

    error = exc_info.value.errors()[0]
    assert error["loc"] == ("value", 0, "id")
    assert error["type"] == "missing"
