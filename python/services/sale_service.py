from decimal import Decimal

from db.db import Database
from exceptions import NotFoundError, ValidationError
from models.sale_order import SaleOrder
from models.sale_order_line import SaleOrderLine
from models.stock_movement import MovementType, StockMovement
from models.user import User
from repository import (
    customer_repository,
    product_repository,
    sale_order_line_repository,
    sale_order_repository,
    stock_movement_repository,
)


def _merge_items(items: list[tuple[int, int]]) -> dict[int, int]:
    if not items:
        raise ValidationError("A sale order needs at least one line.")

    quantities: dict[int, int] = {}
    for products_id, quantity in items:
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        quantities[products_id] = quantities.get(products_id, 0) + quantity

    return quantities


def create_sale_order(
    actor: User, customers_id: int, items: list[tuple[int, int]]
) -> tuple[SaleOrder, list[SaleOrderLine]]:
    quantities = _merge_items(items)

    if customer_repository.get_by_id(customers_id) is None:
        raise NotFoundError(f"Customer {customers_id} not found.")

    with Database().transaction():
        reserved = []
        total = Decimal("0")

        for products_id in sorted(quantities):
            quantity = quantities[products_id]
            product = product_repository.get_by_id(products_id, for_update=True)

            if product is None:
                raise NotFoundError(f"Product {products_id} not found.")

            if product.stock_quantity < quantity:
                raise ValidationError(
                    f"Not enough stock for {product.name}: "
                    f"{product.stock_quantity} available, {quantity} requested."
                )

            reserved.append((product, quantity))
            total += product.sale_price * quantity

        order = sale_order_repository.create(
            SaleOrder(customers_id=customers_id, users_id=actor.id, total_amount=total)
        )

        lines = []
        for product, quantity in reserved:
            line = sale_order_line_repository.create(
                SaleOrderLine(
                    sales_orders_id=order.id,
                    products_id=product.id,
                    quantity=quantity,
                    unit_price=product.sale_price,
                )
            )
            product_repository.decrease_stock(product.id, quantity)
            stock_movement_repository.create(
                StockMovement(
                    products_id=product.id,
                    users_id=actor.id,
                    quantity=quantity,
                    movement_type=MovementType.OUT,
                )
            )
            lines.append(line)

    return order, lines
