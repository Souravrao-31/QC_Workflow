from app.services.exceptions import InvalidCredentials
from app.core.security import verify_password, create_access_token
from app.models.user import User


class AuthService:

    @staticmethod
    def login(db, name: str, password: str) -> str:
        user = db.query(User).filter(User.name == name).first()

        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentials()

        return create_access_token(
            {"sub": str(user.id), "role": user.role}
        )
