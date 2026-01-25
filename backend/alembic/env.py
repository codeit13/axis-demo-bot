from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the backend directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import Base and all models
from app.database import Base
from app.tables import (
    Project, CodeFile, Issue, Suggestion, Approval,
    AgentRun, BusinessRule, RuleVersion, ChangeImpact,
    AgentDependency, ReleaseChecklist
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url from environment variables
# Check if URL is placeholder or not set
db_url = config.get_main_option("sqlalchemy.url")
if not db_url or db_url == "driver://user:pass@localhost/dbname":
    from urllib.parse import quote_plus
    
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = os.getenv("MYSQL_PORT", "3306")
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_database = os.getenv("MYSQL_DATABASE", "ai_agents")
    
    # URL encode user and password to handle special characters
    mysql_user_encoded = quote_plus(mysql_user)
    mysql_password_encoded = quote_plus(mysql_password) if mysql_password else ""
    
    # Construct database URL
    if mysql_password_encoded:
        database_url = f"mysql+pymysql://{mysql_user_encoded}:{mysql_password_encoded}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4"
    else:
        database_url = f"mysql+pymysql://{mysql_user_encoded}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4"
    
    # Escape % characters for ConfigParser (it interprets % as interpolation syntax)
    # We need to double the % signs so ConfigParser doesn't interpret them
    database_url_escaped = database_url.replace("%", "%%")
    
    config.set_main_option("sqlalchemy.url", database_url_escaped)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the config section and unescape % characters
    config_section = config.get_section(config.config_ini_section, {})
    if "sqlalchemy.url" in config_section:
        config_section["sqlalchemy.url"] = config_section["sqlalchemy.url"].replace("%%", "%")
    
    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
