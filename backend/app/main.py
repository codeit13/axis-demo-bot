"""FastAPI main application."""
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .api import projects, agents, suggestions, approvals, issues, business_rules, change_impact, orchestration, dashboard

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize database
init_db()

app = FastAPI(
    title="AI Development Workflow Agents",
    description="Demo application for AI-powered development workflow agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(agents.router)
app.include_router(suggestions.router)
app.include_router(approvals.router)
app.include_router(issues.router)
app.include_router(business_rules.router)
app.include_router(change_impact.router)
app.include_router(orchestration.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "AI Development Workflow Agents API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
