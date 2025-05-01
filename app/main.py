from fastapi import FastAPI
from app.auth.routers import auth, stats
from app.training.routers import training
from app.nutrition.routers import nutrition
from app.blitz_poll.routers import blitz_poll
from .tasks import setup_periodic_tasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ARES Backend")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(training.router, prefix="/training", tags=["training"])
app.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
app.include_router(blitz_poll.router, prefix="/blitz", tags=["blitz_poll"])

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
