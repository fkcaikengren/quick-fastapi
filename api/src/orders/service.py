from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.exceptions import NotFoundException
from api.src.goods.repository import GoodsRepository
from api.src.orders.models import OrderInfo, OrderItem
from api.src.orders.repository import OrderRepository
from api.src.orders.schemas import OrderCreate


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.goods_repo = GoodsRepository(session)

    async def create_order(self, user_id: int, order_data: OrderCreate) -> OrderInfo:
        total_amount = 0
        order_items = []

        if not order_data.items:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item"
            )

        for item_data in order_data.items:
            try:
                goods = await self.goods_repo.get_by_id(item_data.goods_id)
            except NotFoundException:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Goods with id {item_data.goods_id} not found"
                )

            if goods.stock < item_data.count:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for goods '{goods.name}'"
                )

            item_amount = float(goods.price) * item_data.count
            total_amount += item_amount

            order_item = OrderItem(
                goods_id=goods.id,
                goods_name=goods.name,
                goods_price=goods.price,
                count=item_data.count,
                item_amount=item_amount
            )
            order_items.append(order_item)

        order = OrderInfo(
            user_id=user_id,
            delivery_addr_id=order_data.delivery_addr_id,
            total_amount=total_amount,
            items=order_items,
            status=0,  # 0: Pending/Created
            order_type=0
        )

        return await self.order_repo.create(order)

    async def get_user_orders(self, user_id: int) -> list[OrderInfo]:
        return await self.order_repo.list_by_user(user_id)

    async def get_order_details(self, user_id: int, order_id: int) -> OrderInfo:
        try:
            order = await self.order_repo.get_by_id(order_id)
        except NotFoundException:
             raise NotFoundException("Order not found")

        if order.user_id != user_id:
            raise NotFoundException("Order not found")  # Hide existence for security

        return order
