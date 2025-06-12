# create_superuser.py
from app.db.database import async_session
from app.db.models.user import User, UserRole
from app.core.security import hash_password
from sqlalchemy.future import select  

async def create_superuser():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.role == UserRole.superuser))
        existing = result.scalar_one_or_none()

        if not existing:
            superuser = User(
                email="admin@supermail.com",
                hashed_password=hash_password("ToXic1234"),
                role=UserRole.superuser,
                is_active=True,
                is_verified=True,
                is_superuser=True
            )
            session.add(superuser)
            await session.commit()
            print("Superuser created.")
