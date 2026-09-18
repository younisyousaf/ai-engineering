"""Showroom that holds cars and records sales."""

from utils.exceptions import CarNotFoundError, InsufficientBudgetError
from utils.helpers import total_price, unique_brands


class Showroom:
    """Manages a list of cars and a sales history dict."""

    def __init__(self, name):
        self.name = name
        self.cars = []  # list of Car objects
        self.sales = {}  # dict: car_id -> sale record

    def add_car(self, car):
        self.cars.append(car)
        return car

    def get_car_by_id(self, car_id):
        for car in self.cars:
            if car.id == car_id:
                return car
        raise CarNotFoundError(f"No car found with id #{car_id}.")

    def available_cars(self):
        return [car for car in self.cars if car.status == "available"]

    def sell_car(self, car_id, customer):
        """Sell an available car to a customer; record the sale in self.sales."""
        car = self.get_car_by_id(car_id)

        if car.status == "sold":
            raise CarNotFoundError(f"Car #{car_id} is already sold.")

        if not customer.can_afford(car):
            raise InsufficientBudgetError(
                f"{customer.name}'s budget (${customer.budget:,.2f}) "
                f"is less than the car price (${car.price:,.2f})."
            )

        car.status = "sold"
        self.sales[car.id] = {
            "car": str(car),
            "brand": car.brand,
            "model": car.model,
            "price": car.price,
            "customer": customer.name,
        }
        return car

    def sales_report(self):
        """Build a summary using dict, set, and total_price (map/sum)."""
        sold_cars = [car for car in self.cars if car.status == "sold"]
        return {
            "sold_count": len(sold_cars),
            "total_revenue": total_price(sold_cars),
            "brands_sold": unique_brands(sold_cars),
            "details": list(self.sales.values()),
        }

    def __len__(self):
        """Number of cars currently in the showroom inventory."""
        return len(self.cars)

    def __str__(self):
        available = len(self.available_cars())
        return (
            f"{self.name} | Total cars: {len(self)} | "
            f"Available: {available} | Sold: {len(self.sales)}"
        )

    def __add__(self, other):
        """Merge two showrooms into a new one (special method practice)."""
        if not isinstance(other, Showroom):
            return NotImplemented

        merged = Showroom(f"{self.name} + {other.name}")
        # Copy car references into the new showroom list
        merged.cars = self.cars + other.cars
        merged.sales = {**self.sales, **other.sales}
        return merged
