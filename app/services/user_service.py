from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from jose import JWTError

async def get_admin_user(identifier: str, session: AsyncSession):
    result = await session.execute(
        select(User).where(
            (User.username == identifier) | (User.email == identifier)
        )
    )
    user = result.scalars().first()

    if user:
        print(f"User found: username={user.username}, email={user.email}, role={user.role}, is_superuser={user.is_superuser}")
    else:
        print(f"No user found with identifier '{identifier}'")

    if user and (user.is_superuser or user.role == "admin"):
        return user
    return None


async def verify_admin_token(token: str, session: AsyncSession):
    from app.core.security import decode_token  # Local import to avoid circularity
    
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            return False
            
        user = await get_admin_user(username, session)
        return user is not None
    except JWTError:
        return False