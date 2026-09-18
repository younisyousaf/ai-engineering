"""Customer who can buy a car from the showroom."""


class Customer:
    """A customer with a name and a buying budget."""

    def __init__(self, name, budget):
        self.name = name
        self.budget = budget

    def can_afford(self, car):
        return self.budget >= car.price

    def __str__(self):
        return f"Customer: {self.name} | Budget: ${self.budget:,.2f}"
