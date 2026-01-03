from pydantic import BaseModel, ConfigDict, Field


class GoodsCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Good name")
    title: str = Field(None, description="Good title")
    img: str = Field(None, description="Good image URL")
    detail: str = Field(None, description="Good detail")
    price: float = Field(..., description="Good price")
    stock: int = Field(0, description="Good stock")
