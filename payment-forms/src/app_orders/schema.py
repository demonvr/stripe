from pydantic import BaseModel


class ProductData(BaseModel):
    name: str
    description: str


class PriceData(BaseModel):
    currency: str
    product_data: ProductData
    unit_amount: int


class LineItems(BaseModel):
    price_data: PriceData
    quantity: int = 1
