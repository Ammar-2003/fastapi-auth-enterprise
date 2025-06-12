from fastapi import Depends, HTTPException, status
from app.db.models.user import User, UserRole
from app.utils.auth import get_current_user  # You should already have this

def require_role(min_role: UserRole):
    def checker(current_user: User = Depends(get_current_user)):
        hierarchy = {
            UserRole.superuser: 4,
            UserRole.admin: 3,
            UserRole.staff: 2,
            UserRole.user: 1,
        }
        if hierarchy[current_user.role] < hierarchy[min_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action.",
            )
        return current_user
    return checker
