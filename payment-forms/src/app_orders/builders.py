from app_orders.models import Item
from app_orders.schema import ProductData, PriceData, LineItems


def build_product_data(item: Item) -> ProductData:
    return ProductData(
        name=item.name,
        description=item.description
    )


def build_price_data(item: Item, product_data: ProductData) -> PriceData:
    return PriceData(
        currency=item.currency,
        unit_amount=int(item.price * 100),
        product_data=product_data
    )


def build_line_items(price_data: PriceData) -> LineItems:
    return LineItems(
        price_data=price_data,
        quantity=1
    )