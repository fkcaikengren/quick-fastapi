from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.core.exceptions import NotFoundException
from api.src.orders.models import OrderInfo, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> OrderInfo:
        query: Select[tuple[OrderInfo]] = (
            select(OrderInfo)
            .where(OrderInfo.id == order_id)
            .options(selectinload(OrderInfo.items))
        )
        result = await self.session.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            raise NotFoundException("Order not found")

        return order

    async def list_by_user(self, user_id: int) -> list[OrderInfo]:
        query: Select[tuple[OrderInfo]] = (
            select(OrderInfo)
            .where(OrderInfo.user_id == user_id)
            .options(selectinload(OrderInfo.items))
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_items_by_order(self, order_id: int) -> list[OrderItem]:
        query: Select[tuple[OrderItem]] = select(OrderItem).where(
            OrderItem.order_id == order_id
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

