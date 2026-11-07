import getpass
import logging

from psycopg import Error as DatabaseError

from db.db import Database
from exceptions import AppError, ValidationError
from services import (
    auth_service,
    customer_service,
    product_service,
    sale_service,
    stock_movement_service,
    supplier_service,
    user_service,
)

logger = logging.getLogger(__name__)


def ask(label, default=""):
    suffix = f" [{default}]" if default else ""
    return input(f"{label}{suffix}: ").strip() or default


def ask_int(label):
    try:
        return int(input(f"{label}: ").strip())
    except ValueError:
        raise ValidationError("Please enter a valid number.") from None


def print_users(users):
    print(f"{'ID':<5}{'Name':<28}{'Email':<36}{'Phone':<20}{'Role':<6}")
    print("-" * 95)
    for u in users:
        print(
            f"{u.id:<5}{u.full_name:<28}{u.email:<36}"
            f"{u.phone_number:<20}{u.role.value:<6}"
        )


def print_customers(customers):
    print(f"{'ID':<5}{'Name':<26}{'Email':<36}{'Phone':<20}{'City':<14}")
    print("-" * 101)
    for c in customers:
        city = c.city or "-"
        print(
            f"{c.id:<5}{c.full_name:<26}{c.email:<36}"
            f"{c.phone_number:<20}{city:<14}"
        )


def print_suppliers(suppliers):
    print(f"{'ID':<5}{'Name':<22}{'Email':<32}{'Phone':<20}{'City':<12}")
    print("-" * 91)
    for s in suppliers:
        city = s.city or "-"
        print(f"{s.id:<5}{s.name:<22}{s.email:<32}{s.phone_number:<20}{city:<12}")


def print_products(products):
    print(
        f"{'ID':<5}{'Reference':<14}{'Name':<32}"
        f"{'Purchase':>10}{'Sale':>10}{'Stock':>8}"
    )
    print("-" * 79)
    for p in products:
        print(
            f"{p.id:<5}{p.reference:<14}{p.name:<32}"
            f"{p.purchase_price:>10.2f}{p.sale_price:>10.2f}{p.stock_quantity:>8}"
        )


def print_stock_movements(movements):
    print(
        f"{'ID':<5}{'Date':<12}{'Type':<6}{'Qty':>5}  "
        f"{'Reference':<14}{'Product':<32}{'User':<20}"
    )
    print("-" * 96)
    for m in movements:
        date_text = str(m.movement_date)
        print(
            f"{m.id:<5}{date_text:<12}{m.movement_type.value:<6}{m.quantity:>5}  "
            f"{m.product_reference:<14}{m.product_name:<32}{m.user_name:<20}"
        )


def ask_sale_items(products):
    products_by_id = {p.id: p for p in products}
    items = []

    while True:
        products_id = ask_int("Product ID")
        if products_id not in products_by_id:
            print("Unknown product ID.")
            continue

        quantity = ask_int("Quantity")
        items.append((products_id, quantity))

        if input("Add another line? (y/N): ").strip().lower() != "y":
            return items


def print_sale_order(order, lines, products):
    products_by_id = {p.id: p for p in products}

    print(f"\nSale order {order.id} created ({order.order_date}).")
    for line in lines:
        product = products_by_id[line.products_id]
        print(
            f"  {product.reference:<14}{product.name:<32}"
            f"{line.quantity:>4} x {line.unit_price:>8.2f} = {line.subtotal:>9.2f}"
        )
    print(f"Total: {order.total_amount:.2f}")


if __name__ == "__main__":
    current_user = None
    continue_app = True

    try:
        while continue_app:
            try:
                if current_user is None:
                    print("\nMenu")
                    print("Log in - 1")
                    print("Quit - 0")

                    match input("Your choice: ").strip():
                        case "1":
                            email = input("Email: ")
                            password = getpass.getpass("Password: ")
                            current_user = auth_service.login(email, password)
                            print(
                                f"Welcome, {current_user.full_name} "
                                f"({current_user.role.value})."
                            )
                        case "0":
                            continue_app = False
                        case _:
                            print("Invalid choice.")

                else:
                    print("\nMenu")
                    print("My profile - 1")
                    print("List customers - 2")
                    print("List products - 3")
                    print("List suppliers - 4")
                    print("List stock movements - 5")
                    print("Create a sale order - 6")
                    if current_user.is_admin:
                        print("List users - 7")
                        print("Create a user - 8")
                        print("Update a user - 9")
                        print("Delete a user - 10")
                    print("Log out - 0")

                    match input("Your choice: ").strip():
                        case "1":
                            print(f"ID:    {current_user.id}")
                            print(f"Name:  {current_user.full_name}")
                            print(f"Email: {current_user.email}")
                            print(f"Phone: {current_user.phone_number}")
                            print(f"Role:  {current_user.role.value}")

                        case "2":
                            print_customers(customer_service.list_customers())

                        case "3":
                            print_products(product_service.list_products())

                        case "4":
                            print_suppliers(supplier_service.list_suppliers())

                        case "5":
                            print_stock_movements(
                                stock_movement_service.list_stock_movements()
                            )

                        case "6":
                            print_customers(customer_service.list_customers())
                            customers_id = ask_int("Customer ID")

                            products = product_service.list_products()
                            print_products(products)
                            items = ask_sale_items(products)

                            order, lines = sale_service.create_sale_order(
                                current_user, customers_id, items
                            )
                            print_sale_order(order, lines, products)

                        case "7" if current_user.is_admin:
                            print_users(user_service.list_users(current_user))

                        case "8" if current_user.is_admin:
                            first_name = input("First name: ")
                            last_name = input("Last name: ")
                            email = input("Email: ")
                            phone_number = input("Phone number: ")
                            password = getpass.getpass("Password: ")
                            created = user_service.create_user(
                                current_user,
                                first_name,
                                last_name,
                                email,
                                phone_number,
                                password,
                            )
                            print(f"User created with id {created.id}.")

                        case "9" if current_user.is_admin:
                            print_users(user_service.list_users(current_user))
                            user_id = ask_int("ID of the user to update")
                            user = user_service.get_user(current_user, user_id)

                            print("Leave a field empty to keep its current value.")
                            first_name = ask("First name", user.first_name)
                            last_name = ask("Last name", user.last_name)
                            email = ask("Email", user.email)
                            phone_number = ask("Phone number", user.phone_number)
                            password = getpass.getpass(
                                "New password (empty to keep the current one): "
                            )

                            updated = user_service.update_user(
                                current_user,
                                user_id,
                                first_name,
                                last_name,
                                email,
                                phone_number,
                                password or None,
                            )
                            if updated.id == current_user.id:
                                current_user = updated
                            print(f"User {updated.id} updated.")

                        case "10" if current_user.is_admin:
                            print_users(user_service.list_users(current_user))
                            user_id = ask_int("ID of the user to delete")
                            user = user_service.get_user(current_user, user_id)

                            answer = input(
                                f"Delete {user.full_name} ({user.email})? (y/N): "
                            )
                            if answer.strip().lower() == "y":
                                user_service.delete_user(current_user, user_id)
                                print("User deleted.")
                            else:
                                print("Cancelled.")

                        case "0":
                            current_user = None
                            print("Logged out.")

                        case _:
                            print("Invalid choice.")

            except AppError as error:
                print(f"Error: {error}")
            except DatabaseError:
                logger.exception("Database error")
                print("Error: a database problem occurred.")

    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
    finally:
        Database().close()
