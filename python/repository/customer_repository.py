from db.db import Database
from models.customer import Customer

_COLUMNS = (
    "id_customers, first_name, last_name, email, phone_number, "
    "address, city, postal_code, created_at"
)


def _to_customer(row: tuple) -> Customer:
    (
        id_customers,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        city,
        postal_code,
        created_at,
    ) = row

    return Customer(
        id=id_customers,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        address=address,
        city=city,
        postal_code=postal_code,
        created_at=created_at,
    )


def get_all() -> list[Customer]:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM customers ORDER BY id_customers")
        return [_to_customer(row) for row in cursor.fetchall()]
