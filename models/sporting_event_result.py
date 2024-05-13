from typing import Optional

from pydantic import BaseModel, Field


class SportingEventResult(BaseModel):
    sporting_event: str = Field(default_factory=str, alias="sporting_event")
    goals_local_team: int = Field(default_factory=int, alias="goals_local_team")
    goals_visiting_team: int = Field(default_factory=int, alias="goals_visiting_team")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "sporting_event": "ObjectId (referencia a la colección de encuentros deportivos)",
                "goals_local_team": 0,
                "goals_visiting_team": 0
            },
        }


class SportingEventResultUpdate(BaseModel):
    sporting_event: Optional[str]
    goals_local_team: Optional[int]
    goals_visiting_team: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "sporting_event": "ObjectId (referencia a la colección de encuentros deportivos)",
                "goals_local_team": 0,
                "goals_visiting_team": 0
            }
        }
