from db.db import Database
from models.sale_order_line import SaleOrderLine

_COLUMNS = "id_sale_order_lines, sales_orders_id, products_id, quantity, unit_price"


def _to_sale_order_line(row: tuple) -> SaleOrderLine:
    id_sale_order_lines, sales_orders_id, products_id, quantity, unit_price = row

    return SaleOrderLine(
        id=id_sale_order_lines,
        sales_orders_id=sales_orders_id,
        products_id=products_id,
        quantity=quantity,
        unit_price=unit_price,
    )


def create(line: SaleOrderLine) -> SaleOrderLine:
    with Database().connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO sale_order_lines
                (sales_orders_id, products_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            RETURNING {_COLUMNS}
            """,
            (line.sales_orders_id, line.products_id, line.quantity, line.unit_price),
        )
        row = cursor.fetchone()
    return _to_sale_order_line(row)
