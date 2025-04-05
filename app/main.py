from fastapi import FastAPI
from app.auth.routers import auth, stats
from .tasks import setup_periodic_tasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(title="ARES Backend")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

setup_periodic_tasks(app)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
