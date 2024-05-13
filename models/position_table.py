from typing import Optional

from pydantic import BaseModel, Field


class PositionTable(BaseModel):
    team: str = Field(default_factory=str, alias="team")
    score: int = Field(default_factory=int, alias="score")
    matches_played: int = Field(default_factory=int, alias="matches_played")
    matches_won: int = Field(default_factory=int, alias="matches_won")
    drawn_matches: int = Field(default_factory=int, alias="drawn_matches")
    matches_lost: int = Field(default_factory=int, alias="matches_lost")
    goals_scored: int = Field(default_factory=int, alias="goals_scored")
    goals_against: int = Field(default_factory=int, alias="goals_against")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "team": "Liverpool",
                "score": 9,
                "matches_played": 5,
                "matches_won": 3,
                "drawn_matches": 1,
                "matches_lost": 1,
                "goals_scored": 6,
                "goals_against": 2
            }
        }


class PositionTableUpdate(BaseModel):
    team: Optional[str]
    score: Optional[int]
    matches_played: Optional[int]
    matches_won: Optional[int]
    drawn_matches: Optional[int]
    matches_lost: Optional[int]
    goals_scored: Optional[int]
    goals_against: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "team": "Liverpool",
                "score": 9,
                "matches_played": 5,
                "matches_won": 3,
                "drawn_matches": 1,
                "matches_lost": 1,
                "goals_scored": 6,
                "goals_against": 2
            }
        }
