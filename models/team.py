from typing import Optional

from pydantic import BaseModel, Field


class Team(BaseModel):
    name: str = Field(default_factory=str, alias="name")
    city: str = Field(default_factory=str, alias="city")
    trainer: str = Field(default_factory=str, alias="trainer")
    players: list = Field(default_factory=str, alias="players")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Manchester City",
                "city": "Manchester",
                "trainer": "ObjectId_del_entrenador",
                "players": ["ObjectId_del_deportista_1", "ObjectId_del_deportista_2"]
            },
        }


class TeamUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    trainer: Optional[str]
    players: Optional[list]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Manchester City",
                "city": "Manchester",
                "trainer": "ObjectId_del_entrenador",
                "players": ["ObjectId_del_deportista_1", "ObjectId_del_deportista_2"]
            }
        }
