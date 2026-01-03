
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from api.core.exceptions import AlreadyExistsException, NotFoundException
from api.src.goods.models import Goods
from api.src.goods.schemas import GoodsCreate



class GoodsRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    
    # 定义模型的增删改查
    async def create(self, goods_data: GoodsCreate) -> Goods:
        """Create a new good.

        Args:
            goods_data: Good creation data

        Returns:
            Goods: Created good data
        """
        good = Goods(**goods_data.model_dump())
        try:
            self.session.add(good)
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistsException("Good already exists")
        return good


    async def get_by_id(self, goods_id: int) -> Goods:
        """Get good by ID.

        Args:
            goods_id: Good ID

        Returns:
            Good: Good data
        """
        good = await self.session.get(Goods, goods_id)
        if not good:
            raise NotFoundException("Good not found")
        return good


    async def get_all(self) -> list[Goods]:
        """Get all goods.

        Returns:
            List[Goods]: List of all goods
        """
        query = select(Goods)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, goods_id: int, goods_data: GoodsCreate) -> Goods:
        """Update good by ID.

        Args:
            goods_id: Goods ID
            goods_data: Goods update data

        Returns:
            Hero: Updated hero

        Raises:
            NotFoundException: If hero not found
        """
        update_data = goods_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields to update")

        query = update(Goods).where(Goods.id == goods_id).values(**update_data)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Goods with id {goods_id} not found")

        await self.session.commit()
        return await self.get_by_id(goods_id)

    async def delete(self, goods_id: int) -> None:
        """Delete good by ID.

        Args:
            goods_id: Goods ID

        Raises:
            NotFoundException: If hero not found
        """
        query = delete(Goods).where(Goods.id == goods_id)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Goods with id {goods_id} not found")

        await self.session.commit()
