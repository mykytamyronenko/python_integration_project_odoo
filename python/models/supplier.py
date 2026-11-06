from dataclasses import dataclass
from datetime import datetime


@dataclass
class Supplier:
    name: str
    email: str
    phone_number: str
    city: str | None = None
    id: int | None = None
    created_at: datetime | None = None
