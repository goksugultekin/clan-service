from fastapi import FastAPI
from app.api.routers import clans
from app.models.base import Base
from app.core.db import engine

app = FastAPI(title="Clan API (Local Version)", version="1.0.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(clans.router)

@app.get("/")
def root():
    return {"message": "clan API is running"}
