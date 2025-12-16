from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.services.exceptions import PermissionDenied


class UserService:

    @staticmethod
    def create_user(
        db: Session,
        *,
        name: str,
        password: str,
        role: str,
        current_user_role: str,
    ) -> User:
        # RBAC: only ADMIN can create users
        if current_user_role != "ADMIN":
            raise PermissionDenied("Only admin can create users")

        # Prevent duplicate usernames
        existing = db.query(User).filter(User.name == name).first()
        if existing:
            raise ValueError("User with this name already exists")

        user = User(
            name=name,
            role=role,
            password_hash=hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
