from typing import Optional

from pydantic import BaseModel, Field


class SportingEvent(BaseModel):
    local_team: str = Field(default_factory=str, alias="local_team")
    visiting_team: str = Field(default_factory=str, alias="visiting_team")
    date: str = Field(default_factory=str, alias="date")
    referee: str = Field(default_factory=str, alias="referee")
    result: str = Field(default_factory=str, alias="result")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "local_team": "Liverpool",
                "visiting_team": "Arsenal",
                "date": "2024-05-16",
                "referee": "Michael Oliver",
                "result": "3-2"
            },
        }


class SportingEventUpdate(BaseModel):
    local_team: Optional[str]
    visiting_team: Optional[str]
    date: Optional[str]
    referee: Optional[str]
    result: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "local_team": "Liverpool",
                "visiting_team": "Arsenal",
                "date": "2024-05-16",
                "referee": "Michael Oliver",
                "result": "3-2"
            }
        }
