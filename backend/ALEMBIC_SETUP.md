# Alembic Migrations Setup

Alembic has been configured for database migrations. Follow these steps to set up and use migrations.

## Environment Variables

Add the following MySQL credentials to your `backend/.env` file:

```env
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DATABASE=ai_agents
```

**Important:** Replace `your_mysql_password_here` with your actual MySQL root password.

## Database Setup

1. **Create the MySQL database** (if it doesn't exist):
   ```sql
   CREATE DATABASE ai_agents CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Verify your MySQL credentials** are correct in the `.env` file.

## Using Alembic

### Create a new migration:
```bash
cd backend
source ../.venv/bin/activate  # or activate your venv
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback to previous version:
```bash
alembic downgrade -1
```

### View migration history:
```bash
alembic history
```

### View current database version:
```bash
alembic current
```

## Initial Migration

Once your `.env` file is configured with correct MySQL credentials, create the initial migration:

```bash
cd backend
source ../.venv/bin/activate
alembic revision --autogenerate -m "Initial migration"
```

This will generate a migration file in `alembic/versions/` that creates all the tables.

Then apply it:
```bash
alembic upgrade head
```

## Notes

- The `alembic/env.py` file is configured to read database credentials from environment variables
- Migrations are stored in `alembic/versions/`
- The migration files are version-controlled, so commit them to your repository
