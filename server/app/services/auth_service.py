from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token


class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )
        return token
