from fastapi import FastAPI , Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.api.v1 import auth
from app.db.database import get_db
from sqladmin import Admin, ModelView
from app.db.models.user import User
from app.db.database import engine  # your SQLAlchemy engine

app = FastAPI()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# ✅ Setup sqladmin
admin = Admin(app, engine)

# ✅ Register a model view
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name]

admin.add_view(UserAdmin)