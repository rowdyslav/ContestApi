# type: ignore
from contextlib import asynccontextmanager

import dns.resolver
from beanie import init_beanie
from environs import Env
from fastapi import FastAPI
from icecream import ic
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from models import Contest, Project, User

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
env = Env()
env.read_env()

client = AsyncIOMotorClient(env.str("MONGO_URL"))
db = client["ContestApi"]
fs = AsyncIOMotorGridFSBucket(db)


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    ping_response = await db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        ic("Connected to database cluster.")
    await init_beanie(database=db, document_models=[User, Project, Contest])
    yield
    client.close()
