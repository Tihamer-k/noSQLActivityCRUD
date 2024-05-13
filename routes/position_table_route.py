from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.position_table import PositionTable

router = APIRouter()


@router.post("/", response_description="Create a new PositionTable",
             status_code=status.HTTP_201_CREATED,
             response_model=PositionTable)
def create_position_table(request: Request, position_table: PositionTable = Body(...)):
    position_table = jsonable_encoder(position_table)
    new_position_table = request.app.database["position_table"].insert_one(position_table)
    created_position_table = request.app.database["position_table"].find_one(
        {"_id": new_position_table.inserted_id}
    )

    return created_position_table


@router.get("/", response_description="List all position_tables", response_model=List[PositionTable])
def list_position_tables(request: Request):
    position_tables = list(request.app.database["position_table"].find(limit=100))
    return position_tables


@router.put("/{id}", response_description="Update a position_table by id", response_model=PositionTable)
def update_position_table(_id: str, request: Request, position_table: PositionTable = Body(...)):
    position_table = {k: v for k, v in position_table.dict().items() if v is not None}
    if len(position_table) >= 1:
        update_result = request.app.database["position_table"].update_one({"_id": _id}, {"$set": position_table})
        if update_result.modified_count == 1:
            if (
                updated_position_table := request.app.database["position_table"].find_one({"_id": _id})
            ) is not None:
                return updated_position_table
    if (
        existing_position_table := request.app.database["position_table"].find_one({"_id": _id})
    ) is not None:
        return existing_position_table
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PositionTable with ID {_id} not found")


@router.delete("/{id}", response_description="Delete a position_table")
def delete_position_table(_id: str, request: Request, response: Response):
    delete_result = request.app.database["position_table"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PositionTable with ID {_id} not found")
