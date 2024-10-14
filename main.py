from fastapi import FastAPI

from database.loader import db_lifespan
from routers import contests_router, students_router, projects_router

app = FastAPI(lifespan=db_lifespan)

for router in contests_router, projects_router ,students_router:
    app.include_router(router)
