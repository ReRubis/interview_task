"""This module contains the sql models for the subscriptions module."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.zypl_interview.database import Base
from src.zypl_interview.music.models import Band
from src.zypl_interview.users.models import User


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(ForeignKey(User.email), nullable=False)
    band_id: Mapped[int] = mapped_column(ForeignKey(Band.id), nullable=False)
