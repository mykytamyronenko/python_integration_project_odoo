import getpass
import logging

from psycopg import Error as DatabaseError

from db.db import Database
from exceptions import AppError, ValidationError
from services import auth_service, user_service, customer_service, product_service, stock_movement_service, supplier_service

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


if __name__ == "__main__":
    current_user = None
    continue_app = True

    try:
        while continue_app:
            try:
                if current_user is None:
                    print("====================")
                    print()
                    print("Menu : ")
                    print("Log in - 1")
                    print("Quit - 0")
                    print("====================")

                    match input("Your choice: ").strip():
                        case "1":
                            print()
                            email = input("Email: ")
                            password = getpass.getpass("Password: ")
                            current_user = auth_service.login(email, password)
                            print()
                            print(
                                f"Welcome, {current_user.full_name} "
                                f"({current_user.role.value})."
                            )
                        case "0":
                            print()
                            continue_app = False
                        case _:
                            print()
                            print("Invalid choice.")

                else:
                    print("====================")
                    print()
                    print("Menu : ")
                    print("My profile - 1")
                    if current_user.is_admin:
                        print("List users - 2")
                        print("Create a user - 3")
                        print("Update a user - 4")
                        print("Delete a user - 5")
                    print("Log out - 0")
                    print("====================")

                    match input("Your choice: ").strip():
                        case "1":
                            print()
                            print(f"ID:    {current_user.id}")
                            print(f"Name:  {current_user.full_name}")
                            print(f"Email: {current_user.email}")
                            print(f"Phone: {current_user.phone_number}")
                            print(f"Role:  {current_user.role.value}")

                        case "2" if current_user.is_admin:
                            print()
                            print_users(user_service.list_users(current_user))

                        case "3" if current_user.is_admin:
                            print()
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

                        case "4" if current_user.is_admin:
                            print()
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

                        case "5" if current_user.is_admin:
                            print()
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
                            print()
                            current_user = None
                            print("Logged out.")

                        case _:
                            print()
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
