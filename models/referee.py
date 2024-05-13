from typing import Optional

from pydantic import BaseModel, Field


class Referee(BaseModel):
    name: str = Field(default_factory=str, alias="name")
    country: str = Field(default_factory=str, alias="country")
    experience: str = Field(default_factory=str, alias="experience")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Michael Oliver",
                "country": "Inglaterra",
                "experience": "20 años de experiencia"
            }
        }


class RefereeUpdate(BaseModel):
    name: Optional[str]
    country: Optional[str]
    experience: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Michael Oliver",
                "country": "Inglaterra",
                "experience": "20 años de experiencia"
            }
        }
