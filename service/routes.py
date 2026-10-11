"""REST API routes for the Product Catalog service."""

from flask import abort, jsonify, request, send_from_directory

from service import app
from service.common import status
from service.models import Product, Category


def _get_category(value):
    """Convert a category name to a Category enum or return HTTP 400."""
    try:
        return Category[str(value).strip().upper()]
    except (KeyError, AttributeError):
        abort(status.HTTP_400_BAD_REQUEST, description="Invalid category")


def _get_boolean(value):
    """Parse a query-string Boolean strictly."""
    normalized = str(value).strip().lower()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    abort(
        status.HTTP_400_BAD_REQUEST,
        description="available must be true or false",
    )


@app.route("/", methods=["GET"])
def index():
    """Serve the Product Catalog administration page."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/products", methods=["POST"])
def create_product():
    """Create a product from a JSON request body."""
    if not request.is_json:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            description="Content-Type must be application/json",
        )
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(status.HTTP_400_BAD_REQUEST, description="JSON body must be an object")

    product = Product()
    product.deserialize(data)
    product.create()
    app.logger.info("Created product with ID %s", product.id)
    return jsonify(product.serialize()), status.HTTP_201_CREATED


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieve a product by its ID."""
    product = Product.find(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND, description="Product not found")
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a product from a JSON request body."""
    if not request.is_json:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            description="Content-Type must be application/json",
        )
    product = Product.find(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND, description="Product not found")

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(status.HTTP_400_BAD_REQUEST, description="JSON body must be an object")
    product.deserialize(data)
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product by its ID."""
    product = Product.find(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND, description="Product not found")
    product.delete()
    return "", status.HTTP_204_NO_CONTENT


@app.route("/products", methods=["GET"])
def list_products():
    """List products, applying the first supplied supported filter.

    The browser form submits multiple default-valued fields. Prioritizing name,
    then description, category, and availability preserves the lab's expected
    single-filter behavior while allowing combined query strings from the UI.
    """
    name = request.args.get("name")
    description = request.args.get("description")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif description:
        products = Product.query.filter(Product.description == description)
    elif category:
        products = Product.find_by_category(_get_category(category))
    elif available is not None and available != "":
        products = Product.find_by_availability(_get_boolean(available))
    else:
        products = Product.all()

    return jsonify([product.serialize() for product in products]), status.HTTP_200_OK
