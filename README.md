# TDD / BDD Final Project — Product Catalog

A Flask-based REST API and browser UI for managing a product catalog. The application supports creating, retrieving, updating, deleting, and filtering products using SQLAlchemy and SQLite by default, with optional PostgreSQL support.

The project follows **Test-Driven Development (TDD)** with `pytest` and **Behavior-Driven Development (BDD)** with Behave and Selenium.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Version 2 Fixes and Improvements](#version-2-fixes-and-improvements)

## Overview

The Product Catalog application provides endpoints and a browser-based interface for managing product records. It includes input validation, database integration, automated tests, and browser-driven scenarios to verify application behavior.

## Features

- Create, retrieve, update, and delete products.
- List and filter products by name, description, category, and availability.
- Validate product data, including required fields, categories, prices, and availability.
- Persist data using SQLite by default, with optional PostgreSQL configuration.
- Test application behavior using unit tests, route tests, and browser-driven BDD scenarios.
- Run the application locally on Windows, Linux, or macOS.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Application runtime |
| Flask | REST API and web application |
| SQLAlchemy | Database access and ORM |
| SQLite | Default local database |
| PostgreSQL | Optional alternative database |
| pytest | Unit and route testing |
| pytest-cov | Test coverage reporting |
| Behave | BDD scenarios |
| Selenium | Browser automation |
| Google Chrome | Browser used for BDD tests |
| Gunicorn | Production-style WSGI server |

## Project Structure

```text
tdd-bdd-final-project/
├── .devcontainer/       # Development container configuration
├── .vscode/             # VS Code settings
├── bin/                 # Supporting scripts
├── features/            # Behave feature files and step definitions
├── service/             # Flask application, models, and routes
├── tests/               # Automated tests
├── .env.example         # Example environment configuration
├── .flaskenv            # Flask configuration
├── .gitignore           # Git exclusions
├── Dockerfile           # Container build configuration
├── FIXES.md             # Fix documentation
├── LICENSE              # Project license
├── Makefile             # Common development commands
├── Procfile             # Process configuration
├── README.md             # Project documentation
├── requirements.txt     # Python dependencies
├── run.py               # Application entry point
├── setup.cfg            # Tool configuration
└── V2_CHANGES.md        # Version 2 change log
```

## Requirements

- Python 3.11
- Git
- Google Chrome for Selenium BDD tests
- PostgreSQL only if using PostgreSQL instead of the default SQLite database

## Getting Started

### 1. Clone the repository

```powershell
git clone https://github.com/HonestMoth/tdd-bdd-final-project.git
cd tdd-bdd-final-project
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```powershell
python run.py
```

Open the application in your browser:

**http://localhost:8080**

The application uses SQLite by default, so a separate database server is not required.

### Optional: Configure PostgreSQL

If PostgreSQL is installed and configured, set the database connection string before starting the application:

```powershell
$env:DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
python run.py
```

Replace the example credentials and database name with your own configuration.

On Linux or macOS, `honcho start` can run the processes defined in the supplied `Procfile`, which uses Gunicorn.

## Testing

### Run unit and route tests

```powershell
python -m pytest -v
```

### Generate a coverage report

```powershell
python -m pytest --cov=service --cov-report=term-missing
```

The course coverage goal is **at least 95%**. The report identifies uncovered lines that may require additional tests.

### Run BDD scenarios

Start the application in one terminal:

```powershell
python run.py
```

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m behave
```

Behave uses `PRODUCTS_BASE_URL`, which defaults to `http://localhost:8080`. To override the URL:

```powershell
$env:PRODUCTS_BASE_URL = "http://localhost:8080"
python -m behave
```

Google Chrome must be installed and compatible with Selenium. The Selenium driver is managed by the driver manager included with the pinned Selenium version.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Opens the administration UI |
| `POST` | `/products` | Creates a product |
| `GET` | `/products` | Lists products, with optional filters |
| `GET` | `/products/<id>` | Retrieves a product by ID |
| `PUT` | `/products/<id>` | Updates a product |
| `DELETE` | `/products/<id>` | Deletes a product |

### Product Filtering

The product listing endpoint supports filtering by:

- Name
- Description
- Category
- Availability

Use the filtering parameters implemented by the application when constructing requests.

## Version 2 Fixes and Improvements

### Database and Model

- Corrected the route/model database import to use the SQLAlchemy object defined in `service.models`.
- Made SQLite the default local database while retaining optional PostgreSQL support through `DATABASE_URI`.
- Replaced deprecated SQLAlchemy `Query.get()` usage with `db.session.get()`.
- Normalized serialized Decimal prices to avoid unnecessary trailing zeros in API responses.

### API and Validation

- Added the missing root administration UI and product-creation endpoints.
- Added input validation for missing fields, invalid categories, prices, and availability values.
- Improved handling of non-object JSON payloads and error responses.
- Added filtering for unavailable products.

### Testing and Compatibility

- Corrected the model test to use `len(Product.all())`, because `Product.all()` returns a list.
- Added tests for model-validation edge cases and the 405 and 500 error handlers.
- Replaced unsupported Nose/spec configuration with pytest and pytest-cov for Python 3.11 compatibility.
- Aligned Selenium selectors and the BDD base URL with the supplied HTML and `.env` port.

