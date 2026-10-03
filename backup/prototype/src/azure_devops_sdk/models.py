from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from .generated.git import GitRepository as Repository
from .generated.pipelines import Pipeline

T = TypeVar("T")


class AdoList(BaseModel, Generic[T]):
    count: int
    value: list[T]
    

class Project(BaseModel):
    id: UUID
    name: str
