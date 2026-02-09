"""FastAPI main application."""
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from .database import init_db
from .api import projects, agents, suggestions, approvals, issues, business_rules, change_impact, orchestration, dashboard, chat

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

# CORS middleware - allow all origins in production, specific in dev
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (all already have /api prefix)
app.include_router(projects.router)
app.include_router(agents.router)
app.include_router(suggestions.router)
app.include_router(approvals.router)
app.include_router(issues.router)
app.include_router(business_rules.router)
app.include_router(change_impact.router)
app.include_router(orchestration.router)
app.include_router(dashboard.router)
app.include_router(chat.router)

# Path to frontend dist folder
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"
FRONTEND_INDEX = FRONTEND_DIST / "index.html"

# Mount static assets (JS, CSS, images, etc.)
# Vite outputs assets to /assets/ directory
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api")
def api_info():
    """API info endpoint."""
    return {
        "message": "AI Development Workflow Agents API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


# Catch-all route for SPA - must be last
@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    """
    Serve the Vue.js SPA for all non-API routes.
    This handles client-side routing and 404s.
    """
    # Don't serve SPA for API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Don't serve SPA for static assets (already handled by mounts)
    if full_path.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Static file not found")
    
    # Try to serve static files from dist root (favicon.ico, robots.txt, etc.)
    static_file = FRONTEND_DIST / full_path
    if static_file.exists() and static_file.is_file():
        return FileResponse(str(static_file))
    
    # Serve index.html for all other routes (SPA routing)
    # This handles Vue Router client-side routes and 404s
    if FRONTEND_INDEX.exists():
        return FileResponse(str(FRONTEND_INDEX))
    else:
        return HTMLResponse(
            content="""
            <html>
                <head><title>Frontend Not Built</title></head>
                <body>
                    <h1>Frontend Not Built</h1>
                    <p>Please build the frontend first by running: <code>cd frontend && npm run build</code></p>
                </body>
            </html>
            """,
            status_code=503
        )
