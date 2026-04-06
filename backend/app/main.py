from fastapi import FastAPI
from app.api.router import router
from app.models.schemas import SQLModel 
from app.models.database import engine, seed_data
from contextlib import asynccontextmanager




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_data(engine)  # If empty, seed the database with initial data
    yield
    pass

 

app = FastAPI(lifespan=lifespan)
app.include_router(router)