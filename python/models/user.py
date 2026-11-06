from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password_hash: str = field(repr=False)
    role: Role = Role.USER
    id: int | None = None
    created_at: datetime | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self) -> bool:
        return self.role is Role.ADMIN
