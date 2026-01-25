# MySQL Database Setup

The backend has been migrated from SQLite to MySQL. Each table is now organized in its own file under `app/tables/` with schema, types, and repository methods.

## Environment Variables

Add the following to your `backend/.env` file:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=ai_agents
```

## Database Setup

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE ai_agents CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Tables:**
   The tables will be automatically created when you run the application for the first time, or you can run:
   ```python
   from app.database import init_db
   init_db()
   ```

## Table Structure

Each table is defined in `app/tables/` with:
- **Schema**: SQLAlchemy model definition
- **Types**: Enums and type definitions
- **Repository**: CRUD methods for the table

### Tables:
- `projects.py` - Project definitions
- `code_files.py` - Code file storage
- `issues.py` - Issue/Bug tracking
- `suggestions.py` - AI agent suggestions
- `approvals.py` - Human approval records
- `agent_runs.py` - Agent execution history
- `business_rules.py` - Business logic rules
- `rule_versions.py` - Rule version history
- `change_impacts.py` - Change impact analysis
- `agent_dependencies.py` - Agent dependency tracking
- `release_checklists.py` - Release readiness checklists

## Usage Example

```python
from app.database import get_db
from app.tables import ProjectRepository

# In a route handler
def my_route(db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    project = repo.create(name="My Project", description="Description")
    all_projects = repo.get_all()
    project = repo.get_by_id(1)
```
