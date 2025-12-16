from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from app.core.config import settings
import os

engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
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
