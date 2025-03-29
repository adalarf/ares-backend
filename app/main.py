from fastapi import FastAPI
from auth.routers import auth
from app.tasks import setup_periodic_tasks


app = FastAPI(title="ARES Backend")

app.include_router(auth.router, prefix="/auth", tags=["auth"])

setup_periodic_tasks(app)
