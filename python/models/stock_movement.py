from dataclasses import dataclass
from datetime import date
from enum import Enum


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

# represents the row as it is stored in the table
@dataclass
class StockMovement:
    products_id: int
    users_id: int
    quantity: int
    movement_type: MovementType
    movement_date: date | None = None
    id: int | None = None


# used for display: contains the product name and the user's name
@dataclass
class StockMovementDetail:
    id: int
    product_reference: str
    product_name: str
    user_name: str
    movement_type: MovementType
    quantity: int
    movement_date: date