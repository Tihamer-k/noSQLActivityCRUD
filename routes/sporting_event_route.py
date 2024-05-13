from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.sporting_event import SportingEvent

router = APIRouter()


@router.post("/", response_description="Create a new SportingEvent",
             status_code=status.HTTP_201_CREATED,
             response_model=SportingEvent)
def create_sporting_event(request: Request, sporting_events: SportingEvent = Body(...)):
    sporting_events = jsonable_encoder(sporting_events)
    new_sporting_event = request.app.database["sporting_events"].insert_one(sporting_events)
    created_sporting_event = request.app.database["sporting_events"].find_one(
        {"_id": new_sporting_event.inserted_id}
    )

    return created_sporting_event


@router.get("/", response_description="List all sporting_eventss", response_model=List[SportingEvent])
def list_sporting_events(request: Request):
    sporting_eventss = list(request.app.database["sporting_events"].find(limit=100))
    return sporting_eventss


@router.put("/{id}", response_description="Update a sporting_events by id", response_model=SportingEvent)
def update_sporting_event(_id: str, request: Request, sporting_events: SportingEvent = Body(...)):
    sporting_events = {k: v for k, v in sporting_events.dict().items() if v is not None}
    if len(sporting_events) >= 1:
        update = request.app.database["sporting_events"].update_one({"_id": _id}, {"$set": sporting_events})
        if update.modified_count == 1:
            if (
                updated_sporting_event := request.app.database["sporting_events"].find_one({"_id": _id})
            ) is not None:
                return updated_sporting_event
    if (
        existing_sporting_event := request.app.database["sporting_events"].find_one({"_id": _id})
    ) is not None:
        return existing_sporting_event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SportingEvent with ID {_id} not found")


@router.delete("/{id}", response_description="Delete a sporting_events")
def delete_sporting_event(_id: str, request: Request, response: Response):
    delete = request.app.database["sporting_events"].delete_one({"_id": _id})

    if delete.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SportingEvent with ID {_id} not found")
