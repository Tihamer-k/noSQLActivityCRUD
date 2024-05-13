from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Player(BaseModel):
    name: str = Field(default_factory=str, alias="name")
    age: int = Field(default_factory=int, alias="age")
    position: str = Field(default_factory=str, alias="position")
    team: str = Field(default_factory=str, alias="team")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Harry Kane",
                "age": 31,
                "position": "Delantero",
                "team": "Bayern de Múnich"
            }
        }


class PlayerUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    position: Optional[str] = None
    team: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Harry Kane",
                "age": 31,
                "position": "Delantero",
                "team": "Bayern de Múnich"
            }
        }