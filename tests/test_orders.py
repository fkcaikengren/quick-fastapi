import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from api.core.exceptions import NotFoundException
from api.src.orders.service import OrderService
from api.src.orders.schemas import OrderCreate, OrderItemCreate
from api.src.orders.models import OrderInfo
from api.src.goods.models import Goods

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def order_service(mock_session):
    service = OrderService(mock_session)
    service.goods_repo = AsyncMock()
    service.order_repo = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_create_order_success(order_service):
    user_id = 1
    order_data = OrderCreate(
        delivery_addr_id=101,
        items=[OrderItemCreate(goods_id=1, count=2)]
    )
    
    # Mock Goods
    mock_good = MagicMock(spec=Goods)
    mock_good.id = 1
    mock_good.name = "Test Good"
    mock_good.price = 10.0
    mock_good.stock = 100
    
    order_service.goods_repo.get_by_id.return_value = mock_good
    
    # Mock Order Return
    mock_created_order = MagicMock(spec=OrderInfo)
    mock_created_order.id = 1
    mock_created_order.user_id = user_id
    mock_created_order.delivery_addr_id = 101
    mock_created_order.total_amount = 20.0
    mock_created_order.status = 0
    mock_created_order.items = []
    
    order_service.order_repo.create.return_value = mock_created_order

    result = await order_service.create_order(user_id, order_data)

    assert result == mock_created_order
    order_service.goods_repo.get_by_id.assert_called_with(1)
    
    # Check if create was called with correct total amount
    args, _ = order_service.order_repo.create.call_args
    created_order_arg = args[0]
    assert created_order_arg.total_amount == 20.0
    assert len(created_order_arg.items) == 1
    assert created_order_arg.items[0].item_amount == 20.0

@pytest.mark.asyncio
async def test_create_order_insufficient_stock(order_service):
    user_id = 1
    order_data = OrderCreate(
        delivery_addr_id=101,
        items=[OrderItemCreate(goods_id=1, count=10)]
    )
    
    mock_good = MagicMock(spec=Goods)
    mock_good.id = 1
    mock_good.name = "Test Good"
    mock_good.price = 10.0
    mock_good.stock = 5
    
    order_service.goods_repo.get_by_id.return_value = mock_good

    with pytest.raises(HTTPException) as exc:
        await order_service.create_order(user_id, order_data)
    
    assert exc.value.status_code == 400
    assert "Insufficient stock" in exc.value.detail

@pytest.mark.asyncio
async def test_get_user_orders(order_service):
    user_id = 1
    mock_orders = [MagicMock(spec=OrderInfo)]
    order_service.order_repo.list_by_user.return_value = mock_orders

    result = await order_service.get_user_orders(user_id)
    assert result == mock_orders
    order_service.order_repo.list_by_user.assert_called_with(user_id)

@pytest.mark.asyncio
async def test_get_order_details_success(order_service):
    user_id = 1
    order_id = 100
    mock_order = MagicMock(spec=OrderInfo)
    mock_order.user_id = user_id
    mock_order.id = order_id
    
    order_service.order_repo.get_by_id.return_value = mock_order

    result = await order_service.get_order_details(user_id, order_id)
    assert result == mock_order
    order_service.order_repo.get_by_id.assert_called_with(order_id)

@pytest.mark.asyncio
async def test_get_order_details_not_found(order_service):
    user_id = 1
    order_id = 100
    
    # Mock repository raising NotFoundException
    order_service.order_repo.get_by_id.side_effect = NotFoundException("Order not found")

    with pytest.raises(NotFoundException):
        await order_service.get_order_details(user_id, order_id)

@pytest.mark.asyncio
async def test_get_order_details_forbidden(order_service):
    user_id = 1
    order_id = 100
    mock_order = MagicMock(spec=OrderInfo)
    mock_order.user_id = 2  # Different user
    mock_order.id = order_id
    
    order_service.order_repo.get_by_id.return_value = mock_order

    # Should raise NotFoundException to hide existence
    with pytest.raises(NotFoundException):
        await order_service.get_order_details(user_id, order_id)

@pytest.mark.asyncio
async def test_create_order_goods_not_found(order_service):
    user_id = 1
    order_data = OrderCreate(
        delivery_addr_id=101,
        items=[OrderItemCreate(goods_id=999, count=1)]
    )
    
    order_service.goods_repo.get_by_id.side_effect = NotFoundException("Goods not found")

    with pytest.raises(HTTPException) as exc:
        await order_service.create_order(user_id, order_data)
    
    assert exc.value.status_code == 400
    assert "Goods with id 999 not found" in exc.value.detail
