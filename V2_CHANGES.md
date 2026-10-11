# V2 change log

## Environment and startup

- Updated dependency pins for a supported Python 3.11 development environment.
- Replaced Nose/spec with pytest and pytest-cov because Nose 1.3.7 is incompatible with modern Python versions.
- Updated VS Code test discovery and Makefile test targets to use pytest.
- Changed local database default to SQLite; PostgreSQL remains configurable through `DATABASE_URI`.
- Added `run.py` for a Windows-friendly development server.
- Updated `bin/setup.sh` so it does not replace/remove the system-wide `python3` alternative and no longer starts an unnecessary PostgreSQL container for the SQLite default.

## Application

- Fixed the database import path: SQLAlchemy's `db` object is defined in `service.models`, not `service`.
- Added the root route to serve the existing administration page.
- Added `POST /products` to create products.
- Kept CRUD endpoints and added/retained filtering for name, description, category, and availability.
- Improved request validation and converted invalid product payloads into HTTP 400 responses.
- Corrected the browser's unavailable-product search behavior and the results table's Price header.
- Added an explicit update success message for the BDD scenario.

## Tests and BDD

- Fixed tests to import `db` from `service.models`.
- Fixed the list-all model test to persist its generated products.
- Added tests for create, invalid input, root UI, description filtering, serialization, price lookup, and validation failures.
- Aligned Selenium selectors with the real IDs in `service/static/index.html`.
- Set the default BDD URL to port 8080 and made it configurable with `PRODUCTS_BASE_URL`.
- Updated availability assertions to reflect the actual UI's dropdown control.

## Verification

- Python syntax compilation (`compileall`) passed during preparation.
- Full pytest and Selenium BDD execution could not be run in this build environment because package installation requires network access, which was unavailable. Run the verification commands in `README.md` after installing dependencies locally.


## V2.1 follow-up fixes from local test output

- Fixed `test_list_all_products`: `Product.all()` returns a Python list, so the assertion now uses `len(products)` instead of the query-only `count()` API.
- Normalized `Decimal` values in `Product.serialize()` to avoid trailing database scale zeros (for example, `59.9500000000`).
- Replaced deprecated `Product.query.get()` with `db.session.get()`.
- Added model validation and route/error-handler coverage tests to help reach the course coverage target.
