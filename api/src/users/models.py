from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    orders: Mapped[list["OrderInfo"]] = relationship("OrderInfo", back_populates="user") # noqa: F821
