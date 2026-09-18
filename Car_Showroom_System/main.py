"""
Car Showroom System — interactive console menu.

Run from this folder:
    python main.py
"""

from models import Customer, ElectricCar, PetrolCar, Showroom
from utils.exceptions import (
    CarNotFoundError,
    InsufficientBudgetError,
    InvalidPriceError,
)
from utils.file_handler import load_inventory, save_inventory
from utils.helpers import filter_by_brand, filter_by_max_price, unique_brands


def seed_showroom(showroom):
    """Add a few sample cars so the app is usable right away."""
    showroom.add_car(ElectricCar("Tesla", "Model 3", 2024, 42000, "White", 60))
    showroom.add_car(PetrolCar("Toyota", "Corolla", 2023, 22000, "Silver", "petrol"))
    showroom.add_car(ElectricCar("BYD", "Atto 3", 2024, 31000, "Blue", 60))
    showroom.add_car(PetrolCar("Honda", "Civic", 2022, 25000, "Black", "petrol"))


def print_menu():
    print("\n" + "=" * 50)
    print("       CAR SHOWROOM SYSTEM")
    print("=" * 50)
    print("1. Add car")
    print("2. View all cars")
    print("3. Search / filter cars")
    print("4. Sell car")
    print("5. Sales report")
    print("6. Save inventory")
    print("7. Load inventory")
    print("8. Merge demo (__add__)")
    print("9. Exit")
    print("=" * 50)


def get_int(prompt):
    """Read input and cast to int (type_conversion practice)."""
    return int(input(prompt))


def get_float(prompt):
    """Read input and cast to float."""
    return float(input(prompt))


def add_car(showroom):
    print("\n--- Add Car ---")
    print("a) Electric")
    print("b) Petrol")
    kind = input("Choose type (a/b): ").strip().lower()

    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    color = input("Color: ").strip()

    try:
        year = get_int("Year: ")
        price = get_float("Price: ")

        if kind == "a":
            battery = get_float("Battery kWh: ")
            car = ElectricCar(brand, model, year, price, color, battery)
        elif kind == "b":
            fuel = input("Fuel type (petrol/diesel) [petrol]: ").strip() or "petrol"
            car = PetrolCar(brand, model, year, price, color, fuel)
        else:
            print("Invalid type. Choose 'a' or 'b'.")
            return

        showroom.add_car(car)
        print(f"Added: {car}")
    except InvalidPriceError as error:
        print(f"Error: {error}")
    except ValueError:
        print("Error: year, price, and battery must be numbers.")


def view_cars(showroom):
    print(f"\n--- Inventory ({showroom}) ---")
    if not showroom.cars:
        print("No cars in inventory.")
        return

    # Polymorphism: same loop works for ElectricCar and PetrolCar
    for car in showroom.cars:
        print(car)

    brands = unique_brands(showroom.cars)
    print(f"\nUnique brands ({len(brands)}): {', '.join(sorted(brands))}")


def search_cars(showroom):
    print("\n--- Search / Filter ---")
    print("a) By brand")
    print("b) By max price")
    choice = input("Choose (a/b): ").strip().lower()

    cars = showroom.available_cars()
    if not cars:
        print("No available cars to search.")
        return

    try:
        if choice == "a":
            brand = input("Brand name: ").strip()
            results = filter_by_brand(cars, brand)
        elif choice == "b":
            max_price = get_float("Max price: ")
            results = filter_by_max_price(cars, max_price)
        else:
            print("Invalid choice.")
            return
    except ValueError:
        print("Error: price must be a number.")
        return

    if not results:
        print("No matching cars.")
        return

    print(f"Found {len(results)} car(s):")
    for car in results:
        print(car)


def sell_car(showroom):
    print("\n--- Sell Car ---")
    available = showroom.available_cars()
    if not available:
        print("No available cars to sell.")
        return

    print("Available cars:")
    for car in available:
        print(car)

    try:
        car_id = get_int("Enter car id to sell: ")
        name = input("Customer name: ").strip()
        budget = get_float("Customer budget: ")
        customer = Customer(name, budget)
        sold = showroom.sell_car(car_id, customer)
        print(f"Sold to {customer.name}: {sold}")
    except (CarNotFoundError, InsufficientBudgetError) as error:
        print(f"Error: {error}")
    except ValueError:
        print("Error: id and budget must be numbers.")


def sales_report(showroom):
    print("\n--- Sales Report ---")
    report = showroom.sales_report()
    print(f"Cars sold: {report['sold_count']}")
    print(f"Total revenue: ${report['total_revenue']:,.2f}")
    brands = report["brands_sold"]
    if brands:
        print(f"Brands sold: {', '.join(sorted(brands))}")
    else:
        print("Brands sold: (none yet)")

    if report["details"]:
        print("\nDetails:")
        for sale in report["details"]:
            print(
                f"  - {sale['customer']} bought {sale['brand']} {sale['model']} "
                f"for ${sale['price']:,.2f}"
            )


def save_data(showroom):
    print("\n--- Save Inventory ---")
    try:
        path = save_inventory(showroom)
    except OSError as error:
        print(f"Error: {error}")
    else:
        print(f"Inventory saved to: {path}")


def load_data(showroom):
    print("\n--- Load Inventory ---")
    try:
        path = load_inventory(showroom)
    except FileNotFoundError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Error: {error}")
    else:
        print(f"Inventory loaded from: {path}")
        print(showroom)


def merge_demo(showroom):
    """Demonstrate __add__ by merging a tiny second showroom."""
    print("\n--- Merge Demo (__add__) ---")
    branch = Showroom("City Branch")
    branch.add_car(PetrolCar("Suzuki", "Swift", 2021, 15000, "Red", "petrol"))

    merged = showroom + branch
    print(f"Original: {showroom}")
    print(f"Branch:   {branch}")
    print(f"Merged:   {merged}")
    print(f"Merged length (__len__): {len(merged)}")
    print("\nCars in merged showroom:")
    for car in merged.cars:
        print(f"  {car}")


def main():
    showroom = Showroom("Younis Auto House")
    seed_showroom(showroom)
    print(f"Welcome! Seeded {len(showroom)} sample cars.")
    print(showroom)

    running = True
    while running:
        print_menu()
        try:
            choice = input("Enter choice (1-9): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice == "1":
            add_car(showroom)
        elif choice == "2":
            view_cars(showroom)
        elif choice == "3":
            search_cars(showroom)
        elif choice == "4":
            sell_car(showroom)
        elif choice == "5":
            sales_report(showroom)
        elif choice == "6":
            save_data(showroom)
        elif choice == "7":
            load_data(showroom)
        elif choice == "8":
            merge_demo(showroom)
        elif choice == "9":
            print("Thank you for using Car Showroom System. Goodbye!")
            running = False
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
