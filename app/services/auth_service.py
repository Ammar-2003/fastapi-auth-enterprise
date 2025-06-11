from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

async def register_user(user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if user:
        raise ValueError("User with this email already exists")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
