from motor.motor_asyncio import AsyncIOMotorCollection

from database import db

users_collection: AsyncIOMotorCollection = db.get_collection("users")
projects_collection: AsyncIOMotorCollection = db.get_collection("projects")
contests_collection: AsyncIOMotorCollection = db.get_collection("contests")

from .contests import router as contests_router
from .projects import router as projects_router
from .users import router as users_router
