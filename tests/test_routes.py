"""
REST API route tests.
"""

import unittest

from service import app
from service.models import db, Product, Category
from tests.factories import ProductFactory


class TestProductRoutes(unittest.TestCase):
    """Test the Product REST API."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def setUp(self):
        db.create_all()
        Product.query.delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        Product.query.delete()
        db.session.commit()

    def _create_product(self, **kwargs):
        """Create a product directly in the database."""
        product = ProductFactory(**kwargs)
        product.id = None
        product.create()
        return product

    def test_home_page(self):
        """GET / serves the administration UI."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Catalog Administration", response.data)

    def test_create_product(self):
        """POST creates a product and returns its serialized representation."""
        response = self.client.post(
            "/products",
            json={
                "name": "Hat",
                "description": "A red fedora",
                "price": "59.95",
                "available": True,
                "category": "CLOTHS",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Hat")
        self.assertIsNotNone(response.get_json()["id"])

    def test_create_product_requires_json(self):
        """POST rejects a request without JSON content type."""
        response = self.client.post("/products", data="not json")
        self.assertEqual(response.status_code, 415)

    def test_create_product_rejects_non_object_json(self):
        """POST rejects JSON values that are not objects."""
        response = self.client.post("/products", json=["not", "an", "object"])
        self.assertEqual(response.status_code, 400)

    def test_create_product_rejects_invalid_category(self):
        """POST reports invalid product data as HTTP 400."""
        response = self.client.post(
            "/products",
            json={
                "name": "Hat",
                "description": "A red fedora",
                "price": "59.95",
                "available": True,
                "category": "NOT_A_CATEGORY",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_read_product(self):
        """GET /products/<id> returns a product."""
        product = self._create_product(name="Hat")

        response = self.client.get(f"/products/{product.id}")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Hat")

    def test_read_product_not_found(self):
        """GET returns 404 when a product does not exist."""
        response = self.client.get("/products/999999")

        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        """PUT updates a product."""
        product = self._create_product(name="Hat")

        response = self.client.put(
            f"/products/{product.id}",
            json={
                "name": "Fedora",
                "description": "A black fedora",
                "price": 59.95,
                "available": True,
                "category": "CLOTHS",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Fedora")

    def test_update_product_requires_json(self):
        """PUT rejects a request without JSON content type."""
        product = self._create_product(name="Hat")
        response = self.client.put(f"/products/{product.id}", data="not json")
        self.assertEqual(response.status_code, 415)

    def test_update_product_rejects_non_object_json(self):
        """PUT rejects JSON values that are not objects."""
        product = self._create_product(name="Hat")
        response = self.client.put(f"/products/{product.id}", json=["bad"])
        self.assertEqual(response.status_code, 400)

    def test_update_product_not_found(self):
        """PUT returns 404 for an unknown product."""
        response = self.client.put(
            "/products/999999",
            json={"name": "Fedora"},
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_product(self):
        """DELETE removes a product."""
        product = self._create_product(name="Hat")

        response = self.client.delete(f"/products/{product.id}")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Product.find(product.id))

    def test_unsupported_method_returns_405(self):
        """Unsupported HTTP methods return a structured 405 response."""
        response = self.client.patch("/products")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.get_json()["error"], "Method not Allowed")

    def test_internal_server_error_handler(self):
        """The internal error handler returns a structured 500 response."""
        from service.common.error_handlers import internal_server_error

        response, code = internal_server_error(RuntimeError("test error"))
        self.assertEqual(code, 500)
        self.assertEqual(response.get_json()["error"], "Internal Server Error")

    def test_list_products(self):
        """GET /products returns all products."""
        self._create_product(name="Hat")
        self._create_product(name="Shoes")
        self._create_product(name="Big Mac")

        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.get_json()]
        self.assertCountEqual(names, ["Hat", "Shoes", "Big Mac"])

    def test_delete_product_not_found(self):
        """DELETE returns 404 when the product does not exist."""
        response = self.client.delete("/products/999999")
        self.assertEqual(response.status_code, 404)

    def test_list_products_by_description(self):
        """GET /products?description=... filters by description."""
        self._create_product(name="Hat", description="A red fedora")
        self._create_product(name="Shoes", description="Running shoes")
        response = self.client.get("/products?description=A%20red%20fedora")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["name"] for item in response.get_json()], ["Hat"])

    def test_list_products_by_name(self):
        """GET /products?name=Hat filters by name."""
        self._create_product(name="Hat")
        self._create_product(name="Shoes")

        response = self.client.get("/products?name=Hat")

        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.get_json()]
        self.assertEqual(names, ["Hat"])

    def test_list_products_by_category(self):
        """GET /products?category=FOOD filters by category."""
        self._create_product(name="Big Mac", category=Category.FOOD)
        self._create_product(name="Hat", category=Category.CLOTHS)

        response = self.client.get("/products?category=FOOD")

        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.get_json()]
        self.assertEqual(names, ["Big Mac"])

    def test_list_products_rejects_invalid_category(self):
        """Invalid category filters return HTTP 400."""
        response = self.client.get("/products?category=NOPE")
        self.assertEqual(response.status_code, 400)

    def test_list_products_rejects_invalid_availability(self):
        """Invalid availability filters return HTTP 400."""
        response = self.client.get("/products?available=sometimes")
        self.assertEqual(response.status_code, 400)

    def test_list_products_by_unavailability(self):
        """GET /products?available=false returns unavailable products."""
        self._create_product(name="Hat", available=True)
        self._create_product(name="Shoes", available=False)
        response = self.client.get("/products?available=false")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["name"] for item in response.get_json()], ["Shoes"])

    def test_list_products_by_availability(self):
        """GET /products?available=true filters by availability."""
        self._create_product(name="Hat", available=True)
        self._create_product(name="Shoes", available=False)

        response = self.client.get("/products?available=true")

        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.get_json()]
        self.assertEqual(names, ["Hat"])


if __name__ == "__main__":
    unittest.main()
