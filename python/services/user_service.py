import re

from exceptions import NotFoundError, PermissionDeniedError, ValidationError
from models.user import Role, User
from repository import user_repository
from services.auth_service import hash_password

EMAIL_PATTERN = re.compile(r"^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_BYTES = 72


def _require_admin(actor: User) -> None:
    if not actor.is_admin:
        raise PermissionDeniedError("Only an administrator can do this.")


def _validate_fields(
    first_name: str, last_name: str, email: str, phone_number: str
) -> tuple[str, str, str, str]:
    first_name, last_name, email, phone_number = (
        value.strip() for value in (first_name, last_name, email, phone_number)
    )

    if not (first_name and last_name and email and phone_number):
        raise ValidationError("All fields are required.")

    email = email.lower()
    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Email format is invalid.")

    return first_name, last_name, email, phone_number


def _validate_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
        )

    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValidationError("Password is too long.")


def list_users(actor: User) -> list[User]:
    _require_admin(actor)
    return user_repository.get_all()


def get_user(actor: User, user_id: int) -> User:
    _require_admin(actor)
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise NotFoundError(f"User {user_id} not found.")

    return user


def create_user(
    actor: User,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    password: str,
) -> User:
    _require_admin(actor)
    first_name, last_name, email, phone_number = _validate_fields(
        first_name, last_name, email, phone_number
    )
    _validate_password(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password_hash=hash_password(password),
        role=Role.USER,
    )
    return user_repository.create(user)


def update_user(
    actor: User,
    user_id: int,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    password: str | None = None,
) -> User:
    user = get_user(actor, user_id)

    user.first_name, user.last_name, user.email, user.phone_number = _validate_fields(
        first_name, last_name, email, phone_number
    )

    if password:
        _validate_password(password)
        user.password_hash = hash_password(password)

    updated = user_repository.update(user)

    if updated is None:
        raise NotFoundError(f"User {user_id} not found.")

    return updated


def delete_user(actor: User, user_id: int) -> None:
    target = get_user(actor, user_id)

    if target.is_admin:
        raise PermissionDeniedError("Administrator accounts cannot be deleted.")

    user_repository.delete(user_id)
