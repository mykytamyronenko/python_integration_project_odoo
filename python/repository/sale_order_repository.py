from db.db import Database
from models.sale_order import SaleOrder

_COLUMNS = "id_sale_orders, customers_id, users_id, total_amount, order_date"


def _to_sale_order(row: tuple) -> SaleOrder:
    id_sale_orders, customers_id, users_id, total_amount, order_date = row

    return SaleOrder(
        id=id_sale_orders,
        customers_id=customers_id,
        users_id=users_id,
        total_amount=total_amount,
        order_date=order_date,
    )


def create(order: SaleOrder) -> SaleOrder:
    with Database().connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO sale_orders (customers_id, users_id, total_amount)
            VALUES (%s, %s, %s)
            RETURNING {_COLUMNS}
            """,
            (order.customers_id, order.users_id, order.total_amount),
        )
        row = cursor.fetchone()
    return _to_sale_order(row)
