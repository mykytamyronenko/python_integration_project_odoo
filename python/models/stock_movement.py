from dataclasses import dataclass
from datetime import date
from enum import Enum


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"


@dataclass
class StockMovement:
    products_id: int
    users_id: int
    quantity: int
    movement_type: MovementType
    movement_date: date | None = None
    id: int | None = None
