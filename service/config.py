"""
Global Configuration for Application
"""
import os
import logging

# Get configuration from environment
# SQLite keeps the project runnable on a developer machine without a separate
# PostgreSQL server. Set DATABASE_URI to a PostgreSQL URL for deployed use.
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///product_catalog.sqlite")

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_POOL_SIZE = 2

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")
LOGGING_LEVEL = logging.INFO
