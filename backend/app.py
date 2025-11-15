# backend/app.py

from fastapi import FastAPI
from routers import health, projects, items, test_db, clients,projects,scrape


app = FastAPI(
    title="Media Monitoring Backend",
    version="1.0.0",
    description="AI-powered media monitoring system"
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(items.router)
app.include_router(test_db.router)
app.include_router(clients.router)
app.include_router(scrape.router)

