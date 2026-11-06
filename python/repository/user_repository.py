from psycopg import errors
from db.db import Database
from exceptions import ConflictError
from models.user import Role, User


_COLUMNS = (
    "id_users, first_name, last_name, email, phone_number, "
    "password_hash, role, created_at"
)

_DUPLICATE_MESSAGES = {
    "uq_users_email": "This email is already used by another user.",
    "uq_users_phone_number": "This phone number is already used by another user.",
}


def _to_user(row: tuple) -> User:
    (
        id_users,
        first_name,
        last_name,
        email,
        phone_number,
        password_hash,
        role,
        created_at,
    ) = row

    return User(
        id=id_users,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password_hash=password_hash,
        role=Role(role),
        created_at=created_at,
    )


def _duplicate_error(error: errors.UniqueViolation) -> ConflictError:
    message = _DUPLICATE_MESSAGES.get(
        error.diag.constraint_name, "A user with the same data already exists."
    )
    return ConflictError(message)


def get_all() -> list[User]:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM users ORDER BY id_users")
        return [_to_user(row) for row in cursor.fetchall()]


def get_by_id(user_id: int) -> User | None:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM users WHERE id_users = %s", (user_id,))
        row = cursor.fetchone()
    return _to_user(row) if row else None


def get_by_email(email: str) -> User | None:
    with Database().connection.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNS} FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
    return _to_user(row) if row else None


def create(user: User) -> User:
    try:
        with Database().connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO users
                    (first_name, last_name, email, phone_number, password_hash, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING {_COLUMNS}
                """,
                (
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.phone_number,
                    user.password_hash,
                    user.role.value,
                ),
            )
            row = cursor.fetchone()
    except errors.UniqueViolation as error:
        raise _duplicate_error(error) from error
    return _to_user(row)


def update(user: User) -> User | None:
    try:
        with Database().connection.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE users
                SET first_name = %s, last_name = %s, email = %s,
                    phone_number = %s, password_hash = %s
                WHERE id_users = %s
                RETURNING {_COLUMNS}
                """,
                (
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.phone_number,
                    user.password_hash,
                    user.id,
                ),
            )
            row = cursor.fetchone()
    except errors.UniqueViolation as error:
        raise _duplicate_error(error) from error
    return _to_user(row) if row else None


def delete(user_id: int) -> bool:
    try:
        with Database().connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id_users = %s", (user_id,))
            return cursor.rowcount > 0
    except errors.ForeignKeyViolation as error:
        raise ConflictError(
            "This user cannot be deleted because it is linked to existing orders "
            "or stock movements."
        ) from error
