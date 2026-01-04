from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.logging import get_logger
from api.src.goods.schemas import GoodsCreate, GoodsResponse
from api.src.goods.service import GoodsService


logger = get_logger(__name__)

router = APIRouter(prefix="/goods", tags=["goods"])


@router.post("/", response_model=GoodsResponse, status_code=status.HTTP_201_CREATED)
async def create_goods(
    goods_data: GoodsCreate, session: AsyncSession = Depends(get_session)
) -> GoodsResponse:
    logger.debug(f"Creating goods: {goods_data.name}")
    return await GoodsService(session).create_good(goods_data)

