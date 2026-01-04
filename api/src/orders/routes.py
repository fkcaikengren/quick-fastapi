from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.logging import get_logger
from api.core.security import get_current_user
from api.src.users.models import User
from api.src.orders.schemas import OrderCreate, OrderInfoResponse
from api.src.orders.service import OrderService

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderInfoResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> OrderInfoResponse:
    """Create a new order."""
    logger.debug(f"Creating order for user: {current_user.id}")
    service = OrderService(session)
    return await service.create_order(current_user.id, order_data)


@router.get("/", response_model=list[OrderInfoResponse])
async def list_orders(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[OrderInfoResponse]:
    """List current user's orders."""
    service = OrderService(session)
    return await service.get_user_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderInfoResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> OrderInfoResponse:
    """Get specific order details."""
    service = OrderService(session)
    return await service.get_order_details(current_user.id, order_id)
