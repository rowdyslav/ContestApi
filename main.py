from fastapi import FastAPI

from database.loader import db_lifespan
from routers import router as routers

app = FastAPI(lifespan=db_lifespan)

app.include_router(routers)
