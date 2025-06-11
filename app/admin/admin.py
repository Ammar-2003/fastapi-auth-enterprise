# app/admin/auth.py
from app.config import SECRET_KEY
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError

ALGORITHM = "HS256"

from app.db.database import async_session
from app.db.models.user import User
from sqlalchemy.future import select

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
            if user and user.is_superuser:
                return True
            return False

    async def login(self, request: Request) -> bool:
        return True

    async def logout(self, request: Request) -> bool:
        return True
