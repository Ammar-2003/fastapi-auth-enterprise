from fastapi import FastAPI
from sqladmin import Admin
from app.db.database import engine, Base
from app.db.admin import setup_admin
from app.core.config import settings
import asyncio

app = FastAPI()

# Create tables (async)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()
    setup_admin(app)

# Include your routers
from app.api.v1 import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])