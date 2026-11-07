from models.stock_movement import StockMovementDetail
from repository import stock_movement_repository


def list_stock_movements() -> list[StockMovementDetail]:
    return stock_movement_repository.get_all_details()
