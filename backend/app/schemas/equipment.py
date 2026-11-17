
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EquipmentStatus = Literal[
    "available",
    "in_use",
    "maintenance",
    "damaged"
]


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    asset_code: str = Field(min_length=2, max_length=50)
    description: str | None = None
    status: EquipmentStatus = "available"


class EquipmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    asset_code: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = None
    status: EquipmentStatus | None = None


class EquipmentResponse(BaseModel):
    id: int
    name: str
    asset_code: str
    description: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
