import bcrypt

from exceptions import AuthenticationError
from models.user import User
from repository import user_repository


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def login(email: str, password: str) -> User:
    user = user_repository.get_by_email(email.strip().lower())

    if user is None or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid email or password.")

    return user
