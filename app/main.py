from fastapi import FastAPI , Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.api.v1 import auth
from app.db.database import get_db
from sqladmin import Admin, ModelView
from app.db.models.user import User
from app.db.database import engine  
from app.admin.auth import AdminAuth 

app = FastAPI()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

admin = Admin(app, engine, authentication_backend=AdminAuth()) 

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.is_superuser]

admin.add_view(UserAdmin)