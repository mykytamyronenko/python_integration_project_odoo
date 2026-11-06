from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    id: int | None = None
    created_at: datetime | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
