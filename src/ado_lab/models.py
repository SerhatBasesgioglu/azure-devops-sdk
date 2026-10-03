from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class AdoList(BaseModel, Generic[T]):
    count: int
    value: list[T]
    

class Project(BaseModel):
    id: UUID
    name: str

class Repository(BaseModel):
    id: str
    name: str

