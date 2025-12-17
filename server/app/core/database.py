from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from app.core.config import settings
import os


DATABASE_URL = os.getenv("DATABASE_URL") or settings.DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)



def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


# python - <<EOF
# from app.core.database import engine
# engine.connect()
# print("Database connected successfully")
# EOF

# python - <<EOF
# from app.models.user import User
# from app.models.drawing import Drawing
# print(User.__tablename__)
# print(Drawing.__tablename__)
# EOF
