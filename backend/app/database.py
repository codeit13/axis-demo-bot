"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# MySQL connection settings from environment variables
from urllib.parse import quote_plus

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ai_agents")

# URL encode user and password to handle special characters
MYSQL_USER_ENCODED = quote_plus(MYSQL_USER)
MYSQL_PASSWORD_ENCODED = quote_plus(MYSQL_PASSWORD) if MYSQL_PASSWORD else ""

# Construct MySQL connection URL
if MYSQL_PASSWORD_ENCODED:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER_ENCODED}:{MYSQL_PASSWORD_ENCODED}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
else:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER_ENCODED}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# Create engine with MySQL-specific settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    # Import all table models to ensure they're registered with SQLAlchemy
    from .tables import (
        Project, CodeFile, Issue, Suggestion, Approval,
        AgentRun, BusinessRule, RuleVersion, ChangeImpact,
        AgentDependency, ReleaseChecklist
    )
    Base.metadata.create_all(bind=engine)
