from urllib import request

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.trainer import Trainer, TrainerUpdate

router = APIRouter()


@router.post("/", response_description="Create a new Trainer",
             status_code=status.HTTP_201_CREATED,
             response_model=Trainer)
def create_trainer(request: Request, trainer: Trainer = Body(...)):
    trainer = jsonable_encoder(trainer)
    new_trainer = request.app.database["trainers"].insert_one(trainer)
    created_trainer = request.app.database["trainers"].find_one(
        {"_id": new_trainer.inserted_id}
    )

    return created_trainer


@router.get("/{trainer_id}", response_description="Get a single Trainer",
            response_model=Trainer)
def get_trainer(request: Request, trainer_id: str):
    trainer = request.app.database["trainers"].find_one({"_id": trainer_id})
    if trainer:
        return trainer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trainer {trainer_id} not found")


@router.get("/", response_description="Get all Trainers",
            response_model=List[Trainer])
def get_all_trainers(request: Request):
    trainers = request.app.database["trainers"].find()
    return list(trainers)


@router.put("/{trainer_id}", response_description="Update a Trainer",
            response_model=Trainer)
def update_trainer(request: Request, trainer_id: str, trainer: TrainerUpdate = Body(...)):
    trainer = jsonable_encoder(trainer)
    updated_trainer = request.app.database["trainers"].update_one(
        {"_id": trainer_id},
        {"$set": trainer}
    )
    if updated_trainer.modified_count:
        updated_trainer = request.app.database["trainers"].find_one({"_id": trainer_id})
        return updated_trainer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trainer {trainer_id} not found")


@router.delete("/{trainer_id}", response_description="Delete a Trainer")
def delete_trainer(request: Request, trainer_id: str):
    deleted_trainer = request.app.database["trainers"].delete_one({"_id": trainer_id})
    if deleted_trainer.deleted_count:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trainer {trainer_id} not found")
