from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OrderItemCreate(BaseModel):
    goods_id: int
    count: int


class OrderCreate(BaseModel):
    delivery_addr_id: int
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    goods_id: int
    goods_name: str
    goods_price: float
    count: int
    item_amount: float

    model_config = ConfigDict(from_attributes=True)


class OrderInfoResponse(BaseModel):
    id: int
    user_id: int
    delivery_addr_id: int
    total_amount: float
    status: int
    create_time: datetime
    order_type: int
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
