"""
Product model unit tests.
"""

import unittest
from decimal import Decimal

from service import app
from service.models import db, Product, Category
from tests.factories import ProductFactory


class TestProduct(unittest.TestCase):
    """Test cases for the Product model."""

    @classmethod
    def setUpClass(cls):
        """Configure the application for testing."""
        app.config["TESTING"] = True
        cls.app = app.test_client()

    def setUp(self):
        """Create a clean database state for each test."""
        db.create_all()
        Product.query.delete()
        db.session.commit()

    def tearDown(self):
        """Remove test data."""
        db.session.remove()
        Product.query.delete()
        db.session.commit()

    def test_read_a_product(self):
        """It should read a product by its ID."""
        product = ProductFactory()
        product.id = None
        product.create()

        found = Product.find(product.id)

        self.assertIsNotNone(found)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)

    def test_update_a_product(self):
        """It should update an existing product."""
        product = ProductFactory()
        product.id = None
        product.create()

        product.name = "Updated Hat"
        product.description = "An updated product"
        product.update()

        found = Product.find(product.id)

        self.assertEqual(found.name, "Updated Hat")
        self.assertEqual(found.description, "An updated product")

    def test_delete_a_product(self):
        """It should delete a product."""
        product = ProductFactory()
        product.id = None
        product.create()

        product_id = product.id
        product.delete()

        self.assertIsNone(Product.find(product_id))

    def test_list_all_products(self):
        """It should return all products."""
        for product in ProductFactory.create_batch(3):
            product.id = None
            product.create()

        products = Product.all()

        self.assertEqual(len(products), 3)

    def test_find_by_name(self):
        """It should find products by name."""
        product = ProductFactory(name="Hat")
        product.create()

        results = Product.find_by_name("Hat")

        self.assertGreaterEqual(results.count(), 1)
        self.assertEqual(results.first().name, "Hat")

    def test_find_by_category(self):
        """It should find products by category."""
        product = ProductFactory(category=Category.FOOD)
        product.create()

        results = Product.find_by_category(Category.FOOD)

        self.assertGreaterEqual(results.count(), 1)
        self.assertEqual(results.first().category, Category.FOOD)

    def test_serialize_product(self):
        """It should serialize enum and Decimal fields for the REST API."""
        product = ProductFactory(name="Hat", category=Category.CLOTHS, price=Decimal("59.95"))
        product.id = None
        product.create()
        data = product.serialize()
        self.assertEqual(data["name"], "Hat")
        self.assertEqual(data["category"], "CLOTHS")
        self.assertEqual(data["price"], "59.95")

    def test_find_by_price(self):
        """It should find products by a decimal price."""
        product = ProductFactory(price=Decimal("12.50"))
        product.id = None
        product.create()
        results = Product.find_by_price("12.50")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, product.name)

    def test_deserialize_missing_field(self):
        """It should reject product data with missing required fields."""
        from service.models import DataValidationError

        product = Product()
        with self.assertRaises(DataValidationError):
            product.deserialize({"name": "Hat"})

    def test_deserialize_invalid_price(self):
        """It should reject invalid product prices."""
        from service.models import DataValidationError

        product = Product()
        payload = {
            "name": "Hat",
            "description": "A red fedora",
            "price": "not-a-price",
            "available": True,
            "category": "CLOTHS",
        }
        with self.assertRaises(DataValidationError):
            product.deserialize(payload)

    def test_repr_product(self):
        """It should provide a useful string representation."""
        product = ProductFactory(name="Hat")
        product.id = 7
        self.assertEqual(repr(product), "<Product Hat id=[7]>")

    def test_update_requires_id(self):
        """It should reject updating a product without an ID."""
        from service.models import DataValidationError

        product = ProductFactory()
        product.id = None
        with self.assertRaises(DataValidationError):
            product.update()

    def test_deserialize_rejects_non_dictionary(self):
        """It should reject payloads that are not dictionaries."""
        from service.models import DataValidationError

        with self.assertRaises(DataValidationError):
            Product().deserialize(["not", "a", "dict"])

    def test_deserialize_rejects_empty_name(self):
        """It should reject an empty product name."""
        from service.models import DataValidationError

        payload = {"name": " ", "description": "Desc", "price": "1.00",
                   "available": True, "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            Product().deserialize(payload)

    def test_deserialize_rejects_empty_description(self):
        """It should reject an empty description."""
        from service.models import DataValidationError

        payload = {"name": "Item", "description": " ", "price": "1.00",
                   "available": True, "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            Product().deserialize(payload)

    def test_deserialize_rejects_negative_price(self):
        """It should reject a negative product price."""
        from service.models import DataValidationError

        payload = {"name": "Item", "description": "Desc", "price": "-1.00",
                   "available": True, "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            Product().deserialize(payload)

    def test_deserialize_rejects_non_boolean_availability(self):
        """It should require a Boolean availability value."""
        from service.models import DataValidationError

        payload = {"name": "Item", "description": "Desc", "price": "1.00",
                   "available": "true", "category": "FOOD"}
        with self.assertRaises(DataValidationError):
            Product().deserialize(payload)

    def test_deserialize_rejects_unknown_category(self):
        """It should reject unknown categories."""
        from service.models import DataValidationError

        payload = {"name": "Item", "description": "Desc", "price": "1.00",
                   "available": True, "category": "NOT_A_CATEGORY"}
        with self.assertRaises(DataValidationError):
            Product().deserialize(payload)

    def test_find_by_price_decimal(self):
        """It should accept a Decimal price query without string conversion."""
        product = ProductFactory(price=Decimal("17.25"))
        product.id = None
        product.create()
        results = Product.find_by_price(Decimal("17.25"))
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().id, product.id)

    def test_find_by_availability(self):
        """It should find products by availability."""
        product = ProductFactory(available=True)
        product.create()

        results = Product.find_by_availability(True)

        self.assertGreaterEqual(results.count(), 1)
        self.assertTrue(results.first().available)


if __name__ == "__main__":
    unittest.main()
