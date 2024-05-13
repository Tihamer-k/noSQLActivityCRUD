from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.team import Team, TeamUpdate

router = APIRouter()


@router.post("/", response_description="Create a new Team",
             status_code=status.HTTP_201_CREATED,
             response_model=Team)
def create_team(request: Request, team: Team = Body(...)):
    team = jsonable_encoder(team)
    new_team = request.app.database["teams"].insert_one(team)
    created_team = request.app.database["teams"].find_one(
        {"_id": new_team.inserted_id}
    )

    return created_team


@router.get("/{team_id}", response_description="Get a single Team",
            response_model=Team)
def get_team(request: Request, team_id: str):
    team = request.app.database["teams"].find_one({"_id": team_id})
    if team:
        return team
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")


@router.get("/", response_description="Get all Teams",
            response_model=List[Team])
def get_all_teams(request: Request):
    teams = request.app.database["teams"].find()
    return list(teams)


@router.put("/{team_id}", response_description="Update a Team",
            response_model=Team)
def update_team(request: Request, team_id: str, team: TeamUpdate = Body(...)):
    team = jsonable_encoder(team)
    updated_team = request.app.database["teams"].update_one(
        {"_id": team_id},
        {"$set": team}
    )
    if updated_team.modified_count:
        updated_team = request.app.database["teams"].find_one({"_id": team_id})
        return updated_team
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")


@router.delete("/{team_id}", response_description="Delete a Team")
def delete_team(request: Request, team_id: str):
    deleted_team = request.app.database["teams"].delete_one({"_id": team_id})
    if deleted_team.deleted_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
