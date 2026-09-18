"""Car hierarchy: base Car plus ElectricCar and PetrolCar subclasses."""

from utils.exceptions import InvalidPriceError


class Car:
    """Base class for all cars in the showroom."""

    # Class attribute: shared counter used to assign unique ids
    _next_id = 1

    def __init__(self, brand, model, year, price, color):
        self.id = Car._next_id
        Car._next_id += 1

        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.status = "available"  # or "sold"
        self._price = None
        self.price = price  # goes through the property setter

        # Immutable snapshot of core specs (tuple practice from data_structures)
        self.specs = (brand, model, year, color)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise InvalidPriceError("Price must be greater than zero.")
        self._price = value

    def display_info(self):
        """Polymorphic display — subclasses override to add extra details."""
        return (
            f"[#{self.id}] {self.brand} {self.model} ({self.year}) | "
            f"{self.color} | ${self.price:,.2f} | {self.status}"
        )

    def to_dict(self):
        """Convert to a dict so we can save to JSON."""
        return {
            "type": "car",
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "color": self.color,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Car (or subclass) from a dict loaded from JSON."""
        car_type = data.get("type", "car")

        if car_type == "electric":
            car = ElectricCar(
                data["brand"],
                data["model"],
                data["year"],
                data["price"],
                data["color"],
                data["battery_kwh"],
            )
        elif car_type == "petrol":
            car = PetrolCar(
                data["brand"],
                data["model"],
                data["year"],
                data["price"],
                data["color"],
                data.get("fuel_type", "petrol"),
            )
        else:
            car = cls(
                data["brand"],
                data["model"],
                data["year"],
                data["price"],
                data["color"],
            )

        # Restore saved id and status (override auto-assigned values)
        car.id = data["id"]
        car.status = data.get("status", "available")
        if car.id >= Car._next_id:
            Car._next_id = car.id + 1
        return car

    def __str__(self):
        return self.display_info()


class ElectricCar(Car):
    """Electric car with a battery capacity in kWh."""

    def __init__(self, brand, model, year, price, color, battery_kwh):
        super().__init__(brand, model, year, price, color)
        self.battery_kwh = battery_kwh

    def display_info(self):
        base = super().display_info()
        return f"{base} | Battery: {self.battery_kwh} kWh (Electric)"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "electric"
        data["battery_kwh"] = self.battery_kwh
        return data


class PetrolCar(Car):
    """Petrol/diesel car with a fuel type."""

    def __init__(self, brand, model, year, price, color, fuel_type="petrol"):
        super().__init__(brand, model, year, price, color)
        self.fuel_type = fuel_type

    def display_info(self):
        base = super().display_info()
        return f"{base} | Fuel: {self.fuel_type} (Petrol/ICE)"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "petrol"
        data["fuel_type"] = self.fuel_type
        return data
