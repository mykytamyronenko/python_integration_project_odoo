from models.customer import Customer
from repository import customer_repository


def list_customers() -> list[Customer]:
    return customer_repository.get_all()
