from models.supplier import Supplier
from repository import supplier_repository


def list_suppliers() -> list[Supplier]:
    return supplier_repository.get_all()
