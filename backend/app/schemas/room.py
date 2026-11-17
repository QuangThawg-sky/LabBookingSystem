
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RoomBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=255)
    capacity: int = Field(gt=0, le=500)
    description: Optional[str] = None
    is_active: bool = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    location: Optional[str] = Field(default=None, min_length=2, max_length=255)
    capacity: Optional[int] = Field(default=None, gt=0, le=500)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoomResponse(RoomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
