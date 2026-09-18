"""Custom exceptions for the Car Showroom System."""


class InvalidPriceError(Exception):
    """Raised when a car price is zero or negative."""

    pass


class CarNotFoundError(Exception):
    """Raised when a car id is not found in inventory."""

    pass


class InsufficientBudgetError(Exception):
    """Raised when a customer's budget is too low to buy a car."""

    pass
