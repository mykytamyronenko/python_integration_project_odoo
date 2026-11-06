from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    name: str
    reference: str
    purchase_price: Decimal
    sale_price: Decimal
    stock_quantity: int = 0
    id: int | None = None
