from database.loader import db_lifespan
from fastapi import FastAPI
from routers import router as routers

api = FastAPI(lifespan=db_lifespan)

api.include_router(routers)
