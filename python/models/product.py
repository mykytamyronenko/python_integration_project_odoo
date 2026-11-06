from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    reference: str
    purchase_price: float
    sale_price: float
    stock_quantity: int
    id: int | None = None
