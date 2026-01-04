from sqlalchemy.ext.asyncio import AsyncSession

from api.core.logging import get_logger
from api.src.goods.models import Goods
from api.src.goods.repository import GoodsRepository
from api.src.goods.schemas import GoodsCreate


logger = get_logger(__name__)


class GoodsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = GoodsRepository(session)

    async def create_good(self, goods_data: GoodsCreate) -> Goods:
        logger.debug(f"Creating goods: {goods_data.name}")
        return await self.repository.create(goods_data)

