
from sqlalchemy import BigInteger,Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.core.database import Base


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=True)
    img: Mapped[str] = mapped_column(String(255), nullable=True)
    detail: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    order_items: Mapped[list["OrderItem"]] = relationship( 
        "OrderItem", back_populates="goods"
    )
