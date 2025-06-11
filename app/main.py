from fastapi import FastAPI , Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.api.v1 import auth
from app.db.database import get_db
app = FastAPI()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
