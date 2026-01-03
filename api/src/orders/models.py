from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from api.core.database import Base


class OrderInfo(Base):
    __tablename__ = "order_info"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    delivery_addr_id: Mapped[int] = mapped_column(Integer, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    create_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    order_type: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship("User", back_populates="orders") # noqa: F821
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order_info", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("order_info.id", ondelete="CASCADE"), nullable=False
    )
    goods_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("goods.id", ondelete="RESTRICT"), nullable=False
    )
    goods_name: Mapped[str] = mapped_column(String(100), nullable=False)
    goods_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    item_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order_info: Mapped["OrderInfo"] = relationship(back_populates="items")
    goods: Mapped["Goods"] = relationship("Goods", back_populates="order_items") # noqa: F821

