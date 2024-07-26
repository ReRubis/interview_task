from sqlalchemy.orm import Mapped, mapped_column

from src.zypl_interview.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str | None] = mapped_column(default=None, unique=True)
    """Hashed password"""
