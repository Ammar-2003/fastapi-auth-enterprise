from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_async_db  # assuming async
from app.db.models.user import User
from .dependencies import require_role
from app.db.models.user import UserRole
from typing import Annotated

router = APIRouter()
db_dependency = Annotated[AsyncSession, Depends(get_async_db)]


@router.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: db_dependency,
    current_user=Depends(require_role(UserRole.staff))  # staff and above
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_superuser or user.is_admin:  # Ensure staff can't delete higher roles
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    await db.delete(user)
    await db.commit()
    return


@router.delete("/delete-admin/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(
    admin_id: int,
    db: db_dependency,
    current_user=Depends(require_role(UserRole.superuser))  # only superuser
):
    result = await db.execute(select(User).where(User.id == admin_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Admin user not found")

    if not user.is_admin:  # Make sure target is actually admin
        raise HTTPException(status_code=400, detail="Target user is not an admin")

    await db.delete(user)
    await db.commit()
    return
