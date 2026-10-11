# TDD / BDD Final Project — Product Catalog (V2)

Flask REST API and browser UI for creating, reading, updating, deleting, and filtering products. The project uses SQLAlchemy, pytest for unit/route tests, and Behave + Selenium for browser-driven BDD scenarios.

## Requirements

- Python 3.11 (recommended for this dependency set)
- Google Chrome for Selenium BDD tests
- PostgreSQL only if you choose to use PostgreSQL instead of the default local SQLite database

## Windows PowerShell setup

```powershell
cd "D:\IBM Projects\tdd-bdd-final-project"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The default database is SQLite and does not require a separate database server. To use PostgreSQL, set `DATABASE_URI` before starting the application, for example:

```powershell
$env:DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
```

## Run the service

Start the service on Windows using:

```powershell
python run.py
```

Then open `http://localhost:8080` in your browser. On Linux/macOS, `honcho start` can run the supplied Procfile (which uses Gunicorn).

## Run tests

```powershell
python -m pytest -v
python -m pytest --cov=service --cov-report=term-missing
```

Coverage goal for the course is at least 95%; the report identifies uncovered lines that may need additional tests.

## Run BDD scenarios

Start the service in one terminal, then in a second terminal run:

```powershell
python -m behave
```

BDD uses `PRODUCTS_BASE_URL` with a default of `http://localhost:8080`. Override it if the service runs elsewhere:

```powershell
$env:PRODUCTS_BASE_URL = "http://localhost:8080"
python -m behave
```

Chrome must be installed and compatible with Selenium. The Selenium driver is managed by Selenium's driver manager in the pinned Selenium version.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Administration UI |
| POST | `/products` | Create a product |
| GET | `/products` | List products, optionally filtered by name, description, category, or availability |
| GET | `/products/<id>` | Retrieve one product |
| PUT | `/products/<id>` | Update a product |
| DELETE | `/products/<id>` | Delete a product |

## V2.1 fixes

- Fixed the model test to use `len(Product.all())`, because `Product.all()` returns a list.
- Normalized serialized Decimal prices so SQLite numeric scale does not produce values such as `59.9500000000`.
- Replaced the deprecated SQLAlchemy `Query.get()` lookup with `db.session.get()`.
- Added tests for model validation edge cases, the 405/500 error handlers, non-object JSON payloads, and unavailable-product filtering.

## V2 notes

- Fixed the route/model database import to use the SQLAlchemy object defined in `service.models`.
- Added the missing root UI and product-create endpoints.
- Made SQLite the local default while retaining PostgreSQL through `DATABASE_URI`.
- Added input validation for missing fields, invalid categories, prices, and availability values.
- Replaced unsupported Nose/spec configuration with pytest and pytest-cov for Python 3.11 compatibility.
- Aligned Selenium selectors and the BDD URL with the supplied HTML and `.env` port.
