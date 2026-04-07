from fastapi import FastAPI
from app.api.router import router
from app.models.schemas import SQLModel 
from app.models.database import engine
from app.services.db_service import seed_database_if_empty
from contextlib import asynccontextmanager


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_database_if_empty()
    yield
    pass

 

app = FastAPI(lifespan=lifespan)
app.include_router(router)