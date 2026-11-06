from models.stock_movement import StockMovement
from repository import stock_movement_repository


def list_stock_movements() -> list[StockMovement]:
    return stock_movement_repository.get_all_details()
