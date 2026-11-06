from models.product import Product
from repository import product_repository


def list_products() -> list[Product]:
    return product_repository.get_all()
