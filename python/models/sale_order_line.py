from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SaleOrderLine:
    sales_orders_id: int
    products_id: int
    quantity: int
    unit_price: Decimal
    id: int | None = None

    @property
    def subtotal(self) -> Decimal:
        return self.quantity * self.unit_price
