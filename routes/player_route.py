from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.player import Player

router = APIRouter()


@router.post("/", response_description="Create a new Player",
             status_code=status.HTTP_201_CREATED,
             response_model=Player)
def create_player(request: Request, player: Player = Body(...)):
    player = jsonable_encoder(player)
    new_player = request.app.database["players"].insert_one(player)
    created_player = request.app.database["players"].find_one(
        {"_id": new_player.inserted_id}
    )

    return created_player


@router.get("/", response_description="List all players", response_model=List[Player])
def list_players(request: Request):
    players = list(request.app.database["players"].find(limit=100))
    return players


# @router.get("/{id}", response_description="Get a single player by id", response_model=Player)
# def find_player(_id: str, request: Request):
#     if (player := request.app.database["players"].find_one({"_id": _id})) is not None:
#         return player
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player with ID {_id} not found")


@router.put("/{id}", response_description="Update a player by id", response_model=Player)
def update_player(_id: str, request: Request, player: Player = Body(...)):
    player = {k: v for k, v in player.dict().items() if v is not None}
    if len(player) >= 1:
        update_result = request.app.database["players"].update_one({"_id": _id}, {"$set": player})
        if update_result.modified_count == 1:
            if (
                updated_player := request.app.database["players"].find_one({"_id": _id})
            ) is not None:
                return updated_player
    if (
        existing_player := request.app.database["players"].find_one({"_id": _id})
    ) is not None:
        return existing_player
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player with ID {_id} not found")


@router.delete("/{id}", response_description="Delete a player")
def delete_player(_id: str, request: Request, response: Response):
    delete_result = request.app.database["players"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player with ID {_id} not found")
