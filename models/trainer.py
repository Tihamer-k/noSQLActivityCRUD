from typing import Optional

from pydantic import BaseModel, Field


class Trainer(BaseModel):
    name: str = Field(default_factory=str, alias="name")
    age: int = Field(default_factory=str, alias="age")
    experience: str = Field(default_factory=str, alias="experience")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Pep Guardiola",
                "age": 51,
                "experience": "20 años de experiencia"
            }
        }


class TrainerUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    experience: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Pep Guardiola",
                "age": 51,
                "experience": "20 años de experiencia"
            }
        }
