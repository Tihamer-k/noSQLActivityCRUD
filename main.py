from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

import create_mongo_db
from routes import (player_route, team_route, referee_route,
                    trainer_route, position_table_route, sporting_event_route, sporting_event_result_route)

config = dotenv_values(".env")
app = FastAPI()
app.mongodb_client = None


@app.on_event("startup")
def startup_bd_client():
    name, user, password = create_mongo_db.get_db_data()
    app.mongodb_client = MongoClient("mongodb://{}:{}@localhost:27017/{}".format(user, password, name))
    app.database = app.mongodb_client[name]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Shutting down the MongoDB database...")


app.include_router(player_route.router, tags=["players"], prefix="/player")
app.include_router(position_table_route.router, tags=["position_table"], prefix="/position_table")
app.include_router(team_route.router, tags=["teams"], prefix="/team")
app.include_router(referee_route.router, tags=["referees"], prefix="/referee")
app.include_router(trainer_route.router, tags=["trainers"], prefix="/trainer")
app.include_router(sporting_event_route.router, tags=["sporting_events"], prefix="/sporting_event")
app.include_router(sporting_event_result_route.router, tags=["sporting_event_results"], prefix="/sporting_event_result")
