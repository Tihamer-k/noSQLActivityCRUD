from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.referee import Referee, RefereeUpdate

router = APIRouter()


@router.post("/", response_description="Create a new Referee",
             status_code=status.HTTP_201_CREATED,
             response_model=Referee)
def create_referee(request: Request, referee: Referee = Body(...)):
    referee = jsonable_encoder(referee)
    new_referee = request.app.database["referees"].insert_one(referee)
    created_referee = request.app.database["referees"].find_one(
        {"_id": new_referee.inserted_id}
    )

    return created_referee


@router.get("/{referee_id}", response_description="Get a single Referee",
            response_model=Referee)
def get_referee(request: Request, referee_id: str):
    referee = request.app.database["referees"].find_one({"_id": referee_id})
    if referee:
        return referee
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Referee {referee_id} not found")


@router.get("/", response_description="Get all Referees",
            response_model=List[Referee])
def get_all_referees(request: Request):
    referees = request.app.database["referees"].find()
    return list(referees)


@router.put("/{referee_id}", response_description="Update a Referee",
            response_model=Referee)
def update_referee(request: Request, referee_id: str, referee: RefereeUpdate = Body(...)):
    referee = jsonable_encoder(referee)
    updated_referee = request.app.database["referees"].update_one(
        {"_id": referee_id},
        {"$set": referee}
    )
    if updated_referee.modified_count:
        updated_referee = request.app.database["referees"].find_one({"_id": referee_id})
        return updated_referee
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Referee {referee_id} not found")


@router.delete("/{referee_id}", response_description="Delete a Referee")
def delete_referee(request: Request, referee_id: str):
    deleted_referee = request.app.database["referees"].delete_one({"_id": referee_id})
    if deleted_referee.deleted_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Referee {referee_id} not found")
