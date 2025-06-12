from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, HTTPException, status
from app.db.models.user import User
from app.db.database import engine, async_session
from app.core.config import settings
from app.core.security import create_access_token, hash_password , verify_password
from app.services.user_service import get_admin_user, verify_admin_token
from datetime import timedelta

from fastapi import Request, HTTPException, status
import logging

logger = logging.getLogger(__name__)

class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        identifier = form.get("username")  # username or email
        password = form.get("password")
        
        async with async_session() as session:
            user = await get_admin_user(identifier, session)
            
            if not user:
                logger.warning(f"Login failed: No user found with identifier '{identifier}'")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or not authorized",
                )

            if not verify_password(password, user.hashed_password):
                logger.warning(f"Login failed: Incorrect password for user '{identifier}'")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                )

            access_token = create_access_token(
                data={"sub": user.username},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            request.session.update({"token": access_token})
            logger.info(f"Login success: User '{identifier}' logged in successfully.")
            return True

    async def logout(self, request: Request) -> bool:
        logger.info("Admin user logged out.")
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            logger.warning("Authentication failed: No access token in session.")
            return False
        
        async with async_session() as session:
            valid = await verify_admin_token(token, session)
            if not valid:
                logger.warning("Authentication failed: Invalid or expired access token.")
            return valid


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active, User.role]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.created_at]
    form_columns = [User.username, User.email, "password", User.is_active, User.role]
    
    can_create = True
    can_edit = True
    can_delete = True
    name = "User"
    name_plural = "Users"

    async def on_model_change(self, data, model, is_created):
        if "password" in data:
            model.hashed_password = hash_password(data["password"])

def setup_admin(app):
    authentication_backend = AdminAuthBackend(secret_key=settings.SECRET_KEY)
    
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        base_url="/admin",
        title=f"{settings.PROJECT_NAME} Admin",
        templates_dir="templates/admin",
    )
    
    admin.add_view(UserAdmin)