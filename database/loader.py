# type: ignore
from contextlib import asynccontextmanager
from logging import info

import dns.resolver
from environs import Env
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
env = Env()
env.read_env()

client = AsyncIOMotorClient(env.str("MONGO_URL"))
db = client["ContestApi"]


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongodb_client = client
    app.database = db
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    yield

    app.mongodb_client.close()
