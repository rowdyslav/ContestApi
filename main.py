from fastapi import FastAPI

from routers import router as routers

app = FastAPI()
app.include_router(routers)
