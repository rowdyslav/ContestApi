from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db_lifespan
from routers import contests_router, projects_router, users_router

app = FastAPI(lifespan=db_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in users_router, projects_router, contests_router:
    app.include_router(router)
