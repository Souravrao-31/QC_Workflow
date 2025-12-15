import uuid

from app.core.database import SessionLocal
from app.models.user import User
from app.models.drawing import Drawing
from app.models.enums import UserRole, DrawingStatus
from app.core.security import hash_password


def seed_users(db):
    users = [
        User(
            id=uuid.uuid4(),
            name="Admin User",
            role=UserRole.ADMIN.value,
            password_hash=hash_password("admin123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Drafter One",
            role=UserRole.DRAFTER.value,
            password_hash=hash_password("drafter123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Drafter Two",
            role=UserRole.DRAFTER.value,
            password_hash=hash_password("drafter123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Shift Lead One",
            role=UserRole.SHIFT_LEAD.value,
            password_hash=hash_password("shiftlead123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Shift Lead Two",
            role=UserRole.SHIFT_LEAD.value,
            password_hash=hash_password("shiftlead123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Final QC One",
            role=UserRole.FINAL_QC.value,
            password_hash=hash_password("finalqc123"),
        ),
        User(
            id=uuid.uuid4(),
            name="Final QC Two",
            role=UserRole.FINAL_QC.value,
            password_hash=hash_password("finalqc123"),
        ),
    ]

    db.add_all(users)
    db.commit()
    print("Users seeded")


def seed_drawings(db):
    drawings = [
        Drawing(
            title=f"Drawing {i}",
            status=DrawingStatus.UNASSIGNED.value,
        )
        for i in range(1, 6)
    ]

    db.add_all(drawings)
    db.commit()
    print("✅ Drawings seeded")


def main():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_drawings(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
