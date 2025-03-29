from fastapi import FastAPI
from auth.routers import auth


app = FastAPI(title="ARES Backend")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
