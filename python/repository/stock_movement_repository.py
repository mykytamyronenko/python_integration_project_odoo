from db.db import Database
from models.stock_movement import MovementType, StockMovement, StockMovementDetail


def _to_detail(row: tuple) -> StockMovementDetail:
    (
        id_stock_movements,
        product_reference,
        product_name,
        user_name,
        movement_type,
        quantity,
        movement_date,
    ) = row

    return StockMovementDetail(
        id=id_stock_movements,
        product_reference=product_reference,
        product_name=product_name,
        user_name=user_name,
        movement_type=MovementType(movement_type),
        quantity=quantity,
        movement_date=movement_date,
    )


def get_all_details() -> list[StockMovementDetail]:
    with Database().connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT sm.id_stock_movements,
                   p.reference,
                   p.name,
                   u.first_name || ' ' || u.last_name,
                   sm.movement_type,
                   sm.quantity,
                   sm.movement_date
            FROM stock_movements sm
            JOIN products p ON p.id_products = sm.products_id
            JOIN users u ON u.id_users = sm.users_id
            ORDER BY sm.movement_date DESC, sm.id_stock_movements DESC
            """
        )
        return [_to_detail(row) for row in cursor.fetchall()]


def create(movement: StockMovement) -> StockMovement:
    with Database().connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO stock_movements (products_id, users_id, quantity, movement_type)
            VALUES (%s, %s, %s, %s)
            RETURNING id_stock_movements, movement_date
            """,
            (
                movement.products_id,
                movement.users_id,
                movement.quantity,
                movement.movement_type.value,
            ),
        )
        id_stock_movements, movement_date = cursor.fetchone()

    return StockMovement(
        id=id_stock_movements,
        products_id=movement.products_id,
        users_id=movement.users_id,
        quantity=movement.quantity,
        movement_type=movement.movement_type,
        movement_date=movement_date,
    )
