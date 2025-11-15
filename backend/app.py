# backend/app.py

from fastapi import FastAPI
from routers import health, projects, items

app = FastAPI(
    title="Media Monitoring Backend",
    version="1.0.0",
    description="AI-powered media monitoring system"
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(items.router)
