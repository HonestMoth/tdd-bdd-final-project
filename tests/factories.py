"""
Product factory for unit tests.
"""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products for testing."""

    class Meta:
        """Maps the factory to the Product model."""

        model = Product

    id = factory.Sequence(lambda n: n + 1)

    name = FuzzyChoice(
        [
            "Hat",
            "Pants",
            "Shirt",
            "Apple",
            "Banana",
            "Pots",
            "Towels",
            "Ford",
            "Chevy",
            "Hammer",
            "Wrench",
            "Shoes",
            "Big Mac",
            "Sheets",
        ]
    )

    description = factory.Faker("sentence")

    price = FuzzyDecimal(0.50, 2000.00, precision=2)

    available = FuzzyChoice([True, False])

    category = FuzzyChoice(
        [
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
