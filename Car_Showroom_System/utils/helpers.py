"""Search and summary helpers using lambda, map, and filter."""


def filter_by_brand(cars, brand):
    """Return cars whose brand matches (case-insensitive)."""
    brand_lower = brand.strip().lower()
    return list(filter(lambda car: car.brand.lower() == brand_lower, cars))


def filter_by_max_price(cars, max_price):
    """Return cars with price less than or equal to max_price."""
    return list(filter(lambda car: car.price <= max_price, cars))


def filter_available(cars):
    """Return only cars that are still available (not sold)."""
    return list(filter(lambda car: car.status == "available", cars))


def total_price(cars):
    """Sum all car prices using map (same idea as map + lambda in functions.ipynb)."""
    prices = list(map(lambda car: car.price, cars))
    return sum(prices)


def unique_brands(cars):
    """Collect unique brand names using a set."""
    return {car.brand for car in cars}
