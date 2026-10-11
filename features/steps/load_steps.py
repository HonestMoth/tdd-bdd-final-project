"""Behave step that loads the Background product table into the API."""

import os
from http import HTTPStatus

import requests
from behave import given


BASE_URL = os.getenv("PRODUCTS_BASE_URL", "http://localhost:8080").rstrip("/")
PRODUCTS_URL = f"{BASE_URL}/products"


@given("the following products")
def step_load_products(context):
    """Clear existing products, then create each product in the feature table."""
    response = requests.get(PRODUCTS_URL, timeout=10)
    assert response.status_code == HTTPStatus.OK, response.text

    for product in response.json():
        deleted = requests.delete(
            f"{PRODUCTS_URL}/{product['id']}", timeout=10
        )
        assert deleted.status_code in (
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), deleted.text

    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"].strip().lower() in ("true", "1", "yes"),
            "category": row["category"].strip().upper(),
        }
        created = requests.post(PRODUCTS_URL, json=payload, timeout=10)
        assert created.status_code == HTTPStatus.CREATED, (
            f"Could not create {payload['name']}: "
            f"HTTP {created.status_code}: {created.text}"
        )
