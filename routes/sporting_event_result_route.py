from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.sporting_event_result import SportingEventResult

router = APIRouter()


@router.post("/", response_description="Create a new SportingEventResult",
             status_code=status.HTTP_201_CREATED,
             response_model=SportingEventResult)
def create_sporting_event_result(request: Request, sporting_events_result: SportingEventResult = Body(...)):
    sporting_events_result = jsonable_encoder(sporting_events_result)
    new_sporting_event_result = request.app.database["sporting_events_result"].insert_one(sporting_events_result)
    created_sporting_event_result = request.app.database["sporting_events_result"].find_one(
        {"_id": new_sporting_event_result.inserted_id}
    )

    return created_sporting_event_result


@router.get("/", response_description="List all sporting_events_results", response_model=List[SportingEventResult])
def list_sporting_event_results(request: Request):
    sporting_events_results = list(request.app.database["sporting_events_result"].find(limit=100))
    return sporting_events_results


@router.put("/{id}", response_description="Update a sporting_events_result by id", response_model=SportingEventResult)
def update_sporting_event_result(_id: str, request: Request, sporting_events_result: SportingEventResult = Body(...)):
    sporting_events_result = {k: v for k, v in sporting_events_result.dict().items() if v is not None}
    if len(sporting_events_result) >= 1:
        update_result = request.app.database["sporting_events_result"].update_one({"_id": _id}, {"$set": sporting_events_result})
        if update_result.modified_count == 1:
            if (
                updated_sporting_event_result := request.app.database["sporting_events_result"].find_one({"_id": _id})
            ) is not None:
                return updated_sporting_event_result
    if (
        existing_sporting_event_result := request.app.database["sporting_events_result"].find_one({"_id": _id})
    ) is not None:
        return existing_sporting_event_result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SportingEventResult with ID {_id} not found")


@router.delete("/{id}", response_description="Delete a sporting_events_result")
def delete_sporting_event_result(_id: str, request: Request, response: Response):
    delete_result = request.app.database["sporting_events_result"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SportingEventResult with ID {_id} not found")
