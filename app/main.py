from fastapi import FastAPI , Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.api.v1 import auth
from app.db.database import Base
from app.db.database import engine
from app.db.database import SessionLocal
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends[get_db]]