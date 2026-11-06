from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class PurchaseOrderStatus(str, Enum):
    ORDERED = "ORDERED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


@dataclass
class PurchaseOrder:
    users_id: int
    suppliers_id: int
    status: PurchaseOrderStatus = PurchaseOrderStatus.ORDERED
    total_amount: Decimal = Decimal("0")
    order_date: date | None = None
    id: int | None = None
