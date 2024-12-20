from fastapi import FastAPI

from database import db_lifespan
from routers import contests_router, projects_router, users_router

app = FastAPI(lifespan=db_lifespan)

for router in users_router, projects_router, contests_router:
    app.include_router(router)
