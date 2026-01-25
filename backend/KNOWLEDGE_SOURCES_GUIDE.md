# Knowledge Sources Configuration Guide for Prompt Amplifier Agent

This guide explains how and where to define knowledge sources/contexts that the Prompt Amplifier Agent uses.

## Current Implementation

Currently, knowledge sources are **hardcoded** in `backend/app/agents/prompt_amplifier_agent.py` in the `rule_mapping` dictionary (lines ~152-178).

## Recommended Approaches

### Option 1: Database Table (Recommended for Production)

Create a `knowledge_sources` table to store and manage knowledge sources dynamically.

#### Step 1: Create Database Table

Create `backend/app/tables/knowledge_sources.py`:

```python
"""Knowledge Sources table for Prompt Amplifier Agent."""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum


class SourceType(str, enum.Enum):
    """Knowledge source types."""
    CODEBASE = "codebase"
    USER_CONTEXT = "user_context"
    SECURITY_POLICIES = "security_policies"
    ARCHITECTURE_STANDARDS = "architecture_standards"
    BEST_PRACTICES = "best_practices"
    DESIGN_PATTERNS = "design_patterns"
    AI_KNOWLEDGE = "ai_knowledge"
    CUSTOM = "custom"


class KnowledgeSource(Base):
    """Knowledge source model."""
    __tablename__ = "knowledge_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    type = Column(SQLEnum(SourceType), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Actual knowledge content or reference
    source_url = Column(String(500), nullable=True)  # URL to external source
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=0)  # Higher priority = used first
    metadata = Column(Text, nullable=True)  # JSON metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "source": self.name,
            "type": self.type.value,
            "description": self.description,
            "source_url": self.source_url,
            "priority": self.priority
        }


class KnowledgeSourceRepository:
    """Repository for knowledge source operations."""
    
    def __init__(self, db):
        self.db = db
    
    def get_all_active(self):
        """Get all active knowledge sources."""
        return self.db.query(KnowledgeSource).filter(
            KnowledgeSource.is_active == True
        ).order_by(KnowledgeSource.priority.desc()).all()
    
    def get_by_type(self, source_type: SourceType):
        """Get knowledge sources by type."""
        return self.db.query(KnowledgeSource).filter(
            KnowledgeSource.type == source_type,
            KnowledgeSource.is_active == True
        ).order_by(KnowledgeSource.priority.desc()).all()
    
    def get_by_name(self, name: str):
        """Get knowledge source by name."""
        return self.db.query(KnowledgeSource).filter(
            KnowledgeSource.name == name,
            KnowledgeSource.is_active == True
        ).first()
    
    def create(self, name: str, type: SourceType, description: str = None, 
               content: str = None, source_url: str = None, priority: int = 0):
        """Create a new knowledge source."""
        source = KnowledgeSource(
            name=name,
            type=type,
            description=description,
            content=content,
            source_url=source_url,
            priority=priority
        )
        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)
        return source
    
    def update(self, source_id: int, **kwargs):
        """Update a knowledge source."""
        source = self.db.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()
        if source:
            for key, value in kwargs.items():
                setattr(source, key, value)
            self.db.commit()
            self.db.refresh(source)
        return source
```

#### Step 2: Create Alembic Migration

```bash
cd backend
alembic revision -m "add_knowledge_sources_table"
```

Edit the migration file:

```python
"""add_knowledge_sources_table

Revision ID: xxxxx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.create_table(
        'knowledge_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.Enum('codebase', 'user_context', 'security_policies', 
                  'architecture_standards', 'best_practices', 'design_patterns', 
                  'ai_knowledge', 'custom', name='sourcetype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('priority', sa.Integer(), default=0),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_knowledge_sources_id'), 'knowledge_sources', ['id'], unique=False)
    op.create_index(op.f('ix_knowledge_sources_name'), 'knowledge_sources', ['name'], unique=True)
    op.create_index(op.f('ix_knowledge_sources_type'), 'knowledge_sources', ['type'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_knowledge_sources_type'), table_name='knowledge_sources')
    op.drop_index(op.f('ix_knowledge_sources_name'), table_name='knowledge_sources')
    op.drop_index(op.f('ix_knowledge_sources_id'), table_name='knowledge_sources')
    op.drop_table('knowledge_sources')
```

#### Step 3: Update Prompt Amplifier Agent

Modify `backend/app/agents/prompt_amplifier_agent.py`:

```python
from ..tables.knowledge_sources import KnowledgeSourceRepository, SourceType

# In the analyze method, replace the hardcoded rule_mapping with:
knowledge_source_repo = KnowledgeSourceRepository(self.db)

# Get knowledge sources based on enabled rules
for rule in enabled_rules:
    rule_text = rule.get('text', '')
    
    # Map rule text to source type
    rule_to_type = {
        "Always add security requirements": SourceType.SECURITY_POLICIES,
        "Include Axis Bank naming conventions": SourceType.ARCHITECTURE_STANDARDS,
        "Suggest performance optimization": SourceType.BEST_PRACTICES,
        "Add testing requirements (>80% coverage)": SourceType.BEST_PRACTICES,
        "Reference internal design patterns": SourceType.DESIGN_PATTERNS
    }
    
    source_type = rule_to_type.get(rule_text)
    if source_type:
        sources = knowledge_source_repo.get_by_type(source_type)
        for source in sources:
            if not any(ks["source"] == source.name for ks in knowledge_sources_used):
                knowledge_sources_used.append(source.to_dict())
```

#### Step 4: Create API Endpoints

Create `backend/app/api/knowledge_sources.py`:

```python
"""Knowledge Sources API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..database import get_db
from ..tables.knowledge_sources import KnowledgeSourceRepository, SourceType

router = APIRouter(prefix="/api/knowledge-sources", tags=["knowledge-sources"])


class KnowledgeSourceCreate(BaseModel):
    name: str
    type: str
    description: str = None
    content: str = None
    source_url: str = None
    priority: int = 0


class KnowledgeSourceResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str = None
    source_url: str = None
    is_active: bool
    priority: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[KnowledgeSourceResponse])
def list_knowledge_sources(db: Session = Depends(get_db)):
    """List all active knowledge sources."""
    repo = KnowledgeSourceRepository(db)
    sources = repo.get_all_active()
    return sources


@router.post("/", response_model=KnowledgeSourceResponse)
def create_knowledge_source(source: KnowledgeSourceCreate, db: Session = Depends(get_db)):
    """Create a new knowledge source."""
    repo = KnowledgeSourceRepository(db)
    try:
        source_type = SourceType(source.type)
        new_source = repo.create(
            name=source.name,
            type=source_type,
            description=source.description,
            content=source.content,
            source_url=source.source_url,
            priority=source.priority
        )
        return new_source
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid source type: {source.type}")
```

#### Step 5: Seed Initial Data

Create `backend/seed_knowledge_sources.py`:

```python
"""Seed initial knowledge sources."""
from app.database import SessionLocal
from app.tables.knowledge_sources import KnowledgeSourceRepository, SourceType

def seed_knowledge_sources():
    """Seed initial knowledge sources."""
    db = SessionLocal()
    repo = KnowledgeSourceRepository(db)
    
    sources = [
        {
            "name": "Security & Compliance Policies",
            "type": SourceType.SECURITY_POLICIES,
            "description": "Security best practices and compliance requirements",
            "priority": 10
        },
        {
            "name": "Axis Bank Architecture Standards",
            "type": SourceType.ARCHITECTURE_STANDARDS,
            "description": "Internal naming conventions and architecture guidelines",
            "priority": 10
        },
        {
            "name": "Best Practices Repository",
            "type": SourceType.BEST_PRACTICES,
            "description": "Performance optimization patterns and strategies",
            "priority": 8
        },
        {
            "name": "Internal Microservice Templates",
            "type": SourceType.DESIGN_PATTERNS,
            "description": "Internal design patterns and microservice templates",
            "priority": 9
        },
        {
            "name": "AI Best Practices",
            "type": SourceType.AI_KNOWLEDGE,
            "description": "General AI coding best practices and patterns",
            "priority": 5
        }
    ]
    
    for source_data in sources:
        existing = repo.get_by_name(source_data["name"])
        if not existing:
            repo.create(**source_data)
            print(f"Created knowledge source: {source_data['name']}")
        else:
            print(f"Knowledge source already exists: {source_data['name']}")
    
    db.close()

if __name__ == "__main__":
    seed_knowledge_sources()
```

Run it:
```bash
cd backend
python seed_knowledge_sources.py
```

---

### Option 2: Configuration File (Simple Approach)

Create `backend/app/config/knowledge_sources.json`:

```json
{
  "knowledge_sources": [
    {
      "name": "Security & Compliance Policies",
      "type": "security_policies",
      "description": "Security best practices and compliance requirements",
      "priority": 10
    },
    {
      "name": "Axis Bank Architecture Standards",
      "type": "architecture_standards",
      "description": "Internal naming conventions and architecture guidelines",
      "priority": 10
    },
    {
      "name": "Best Practices Repository",
      "type": "best_practices",
      "description": "Performance optimization patterns and strategies",
      "priority": 8
    }
  ],
  "rule_mapping": {
    "Always add security requirements": "security_policies",
    "Include Axis Bank naming conventions": "architecture_standards",
    "Suggest performance optimization": "best_practices",
    "Add testing requirements (>80% coverage)": "best_practices",
    "Reference internal design patterns": "design_patterns"
  }
}
```

Then in the agent:

```python
import json
from pathlib import Path

# Load config
config_path = Path(__file__).parent.parent / "config" / "knowledge_sources.json"
with open(config_path) as f:
    config = json.load(f)

# Use in agent
knowledge_sources = config["knowledge_sources"]
rule_mapping = config["rule_mapping"]
```

---

### Option 3: Environment Variables + External Sources

For external knowledge sources (Confluence, SharePoint, etc.), use environment variables:

`.env`:
```env
KNOWLEDGE_SOURCE_CONFLUENCE_URL=https://confluence.company.com
KNOWLEDGE_SOURCE_SHAREPOINT_URL=https://sharepoint.company.com
KNOWLEDGE_SOURCE_WIKI_URL=https://wiki.company.com
```

Then create a service:

```python
# backend/app/services/knowledge_source_service.py
import os
import requests

class KnowledgeSourceService:
    """Service for fetching knowledge from external sources."""
    
    def __init__(self):
        self.confluence_url = os.getenv("KNOWLEDGE_SOURCE_CONFLUENCE_URL")
        self.sharepoint_url = os.getenv("KNOWLEDGE_SOURCE_SHAREPOINT_URL")
    
    def get_security_policies(self):
        """Fetch security policies from Confluence."""
        # Implementation to fetch from Confluence API
        pass
    
    def get_architecture_standards(self):
        """Fetch architecture standards from SharePoint."""
        # Implementation to fetch from SharePoint API
        pass
```

---

## Summary

**For Production/Demo:**
- ✅ **Use Option 1 (Database Table)** - Most flexible, can be managed via UI
- ✅ Create API endpoints to manage sources
- ✅ Seed initial data with `seed_knowledge_sources.py`

**For Quick Setup:**
- ✅ **Use Option 2 (Config File)** - Simple, no database changes needed

**For External Sources:**
- ✅ **Use Option 3** - Integrate with Confluence, SharePoint, etc.

## Next Steps

1. Choose an approach based on your needs
2. Implement the chosen approach
3. Update the Prompt Amplifier Agent to use the new system
4. Create UI in frontend to manage knowledge sources (if using database approach)
