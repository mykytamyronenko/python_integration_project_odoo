from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class SaleOrder:
    customers_id: int
    users_id: int
    total_amount: Decimal = Decimal("0")
    order_date: date | None = None
    id: int | None = None
