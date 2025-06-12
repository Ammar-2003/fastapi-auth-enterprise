# api/v1/admin.py
from app.core.config import SECRET_KEY
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError
from app.db.models.user import User, UserRole 
from sqlalchemy.future import select
from app.db.database import async_session
from starlette.responses import RedirectResponse

ALGORITHM = "HS256"

class AdminAuth(AuthenticationBackend):
    async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("access_token")
        if not token:
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except JWTError:
            return False

        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if user and user.role in [UserRole.superuser, UserRole.admin]:
                return True
            return False

    async def login(self, request: Request) -> bool:
        # This is the login logic for the /admin login form
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if user and user.verify_password(password) and user.role in [UserRole.superuser, UserRole.admin]:
                token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie("access_token", token, httponly=True)
                request._cookies["access_token"] = token  # Optional for in-memory
                return response

        return False

    async def logout(self, request: Request) -> bool:
        response = RedirectResponse(url="/admin/login", status_code=302)
        response.delete_cookie("access_token")
        return response
