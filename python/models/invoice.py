from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class InvoiceStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


@dataclass
class Invoice:
    invoice_number: str
    sales_orders_id: int
    total_amount: Decimal
    due_date: date
    status: InvoiceStatus = InvoiceStatus.PENDING
    invoice_date: date | None = None
    id: int | None = None
