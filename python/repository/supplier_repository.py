from db.db import Database
from models.supplier import Supplier

_COLUMNS = "id_suppliers, name, email, phone_number, city, created_at"


def _to_supplier(row: tuple) -> Supplier:
    id_suppliers, name, email, phone_number, city, created_at = row

    return Supplier(
        id=id_suppliers,
        name=name,
        email=email,
        phone_number=phone_number,
        city=city,
        created_at=created_at,
    )


def get_all() -> list[Supplier]:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM suppliers ORDER BY id_suppliers")
        return [_to_supplier(row) for row in cursor.fetchall()]
