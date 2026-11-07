from db.db import Database
from models.product import Product

_COLUMNS = "id_products, name, reference, purchase_price, sale_price, stock_quantity"


def _to_product(row: tuple) -> Product:
    id_products, name, reference, purchase_price, sale_price, stock_quantity = row

    return Product(
        id=id_products,
        name=name,
        reference=reference,
        purchase_price=purchase_price,
        sale_price=sale_price,
        stock_quantity=stock_quantity,
    )


def get_all() -> list[Product]:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM products ORDER BY id_products")
        return [_to_product(row) for row in cursor.fetchall()]


def get_by_id(product_id: int, for_update: bool = False) -> Product | None:
    query = f"SELECT {_COLUMNS} FROM products WHERE id_products = %s"
    if for_update:
        query += " FOR UPDATE"

    with Database().connection.cursor() as cursor:
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
    return _to_product(row) if row else None


def decrease_stock(product_id: int, quantity: int) -> None:
    with Database().connection.cursor() as cursor:
        cursor.execute(
            "UPDATE products SET stock_quantity = stock_quantity - %s "
            "WHERE id_products = %s",
            (quantity, product_id),
        )
